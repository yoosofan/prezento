# prezento – Modern RST → HTML slide generator
# Uses b6plus instead of impress.js
# Outputs: .html, .step4pdf.html, .presentation.html
# [ADDED] Optional: --outdir builds a standalone, self-contained folder
#         (index.html + <name>.concise4pdf.html + copied resources +
#         list_of_resources.rst manifest) -- see build_standalone_folder().

import os
import argparse
import textwrap
import copy
import re
import shutil     # [ADDED] used by build_standalone_folder() to copy resource files
import datetime   # [ADDED] used by build_standalone_folder() to timestamp the manifest
import graphviz
from docutils import nodes
from docutils.parsers.rst import Directive, directives
from docutils.core import publish_doctree, publish_from_doctree
from docutils.writers.html5_polyglot import Writer as HTML5WriterBase, HTMLTranslator
from docutils.frontend import OptionParser
from docutils.utils import Reporter

# ── Custom nodes ─────────────────────────────────────────────────────────────
class slido_block(nodes.container):
    pass
class graphviz_block(nodes.General, nodes.Element):
    pass
# [ADDED] New custom node for the komento block
class komento_block(nodes.container):
    pass

# ── Directives ───────────────────────────────────────────────────────────────
class PrezentoDirective(Directive):
    has_content = True
    optional_arguments = 10
    final_argument_whitespace = True
    option_spec = {
        'css': directives.unchanged,
        'js':  directives.unchanged,
        'width': directives.unchanged,
        'height': directives.unchanged,
    }

    def run(self):
        config = self.options.copy()
        if self.arguments:
            config['title'] = ' '.join(self.arguments)
        self.state.document.presentation_config = config
        return []


class SlidoDirective(Directive):
    optional_arguments = 10
    final_argument_whitespace = True
    has_content = True
    option_spec = {
        'class': directives.class_option,
        'id':    directives.unchanged,
        'step':  directives.flag,
    }

    def run(self):
        node = slido_block()
        if self.arguments:
            node['title'] = ' '.join(self.arguments)
        if 'class' in self.options:
            node['classes'] = self.options['class']
        if 'id' in self.options:
            node['ids'] = [self.options['id']]
        if 'step' in self.options:
            node['classes'] = node.get('classes', []) + ['step']

        # Dedent content
        text = '\n'.join(self.content)
        dedented = textwrap.dedent(text)
        content = self.content.__class__(
            dedented.splitlines(), source=self.state.document['source']
        )
        self.state.nested_parse(content, self.content_offset, node)
        return [node]


class GraphvizDirective(Directive):
    has_content = True
    option_spec = {
        'align': directives.unchanged,
        'class': directives.class_option,
        'width': directives.unchanged,
        'height': directives.unchanged,
        'scale': directives.unchanged,
        'alt': directives.unchanged,
        'name': directives.unchanged,
        'target': directives.unchanged
    }

    def run(self):
        node = graphviz_block()

        if 'class' in self.options:
            node['classes'] = self.options['class']
        if 'align' in self.options:
            node['align'] = self.options['align']
        if 'width' in self.options:
            node['width'] = self.options['width']
        if 'height' in self.options:
            node['height'] = self.options['height']
        if 'scale' in self.options:
            node['scale'] = self.options['scale']

        dot_code = '\n'.join(self.content)
        try:
            svg = graphviz.Source(dot_code).pipe(format='svg').decode('utf-8')
            if '<svg' in svg:
                svg = svg[svg.find('<svg'):]

                svg = re.sub(r'(class="[^"]*?\b)step(\b[^"]*")', r'\1incremental\2', svg)

                if 'width' in self.options or 'height' in self.options:
                    svg = re.sub(r'(<svg[^>]*?)\s+width="[^"]+"', r'\1', svg, count=1)
                    svg = re.sub(r'(<svg[^>]*?)\s+height="[^"]+"', r'\1', svg, count=1)

                    new_attrs = ""
                    if 'width' in self.options:
                        new_attrs += f' width="{self.options["width"]}"'
                    if 'height' in self.options:
                        new_attrs += f' height="{self.options["height"]}"'

                    svg = svg.replace('<svg', f'<svg{new_attrs}', 1)

            node['svg'] = svg
        except Exception:
            node['svg'] = ''
        return [node]

# [ADDED] New directive class for presenter comments
class KomentoDirective(Directive):
    has_content = True
    optional_arguments = 10
    final_argument_whitespace = True
    option_spec = {
        'class': directives.class_option,
        'id':    directives.unchanged,
    }

    def run(self):
        node = komento_block()
        if 'class' in self.options:
            node['classes'] = self.options['class']
        if 'id' in self.options:
            node['ids'] = [self.options['id']]

        # Dedent content properly so internal nested elements format correctly
        text = '\n'.join(self.content)
        dedented = textwrap.dedent(text)
        content = self.content.__class__(
            dedented.splitlines(), source=self.state.document['source']
        )
        self.state.nested_parse(content, self.content_offset, node)
        return [node]

directives.register_directive('prezento', PrezentoDirective)
directives.register_directive('slido', SlidoDirective)
# [CHANGED] Renamed from 'yographviz' to 'grafo'
directives.register_directive('grafo', GraphvizDirective)
# [ADDED] Registered the new 'komento' directive
directives.register_directive('komento', KomentoDirective)

# ── Step Helpers ─────────────────────────────────────────────────────────────
_STEP_CONTAINER_TYPES = (
    slido_block,
    nodes.container,
    nodes.block_quote,
    nodes.bullet_list,
    nodes.enumerated_list,
    nodes.definition_list,
)

def _is_step_container(node):
    return (
        isinstance(node, _STEP_CONTAINER_TYPES)
        and isinstance(node, nodes.Element)
        and 'step' in node.get('classes', [])
    )

def _is_atomic_step(node):
    return (
        isinstance(node, nodes.Element)
        and 'step' in node.get('classes', [])
        and not _is_step_container(node)
    )

# ── Step PDF Expansion ──────────────────────────────────────────────────────
def _assign_reveal_indices(root):
    counter = [0]

    def walk(node):
        if _is_step_container(node):
            for child in node.children:
                if isinstance(child, nodes.Text):
                    continue
                counter[0] += 1
                child['_reveal_index'] = counter[0]
                walk(child)
        elif _is_atomic_step(node):
            counter[0] += 1
            node['_reveal_index'] = counter[0]
        else:
            for child in node.children:
                if not isinstance(child, nodes.Text):
                    walk(child)

    walk(root)
    return counter[0]


def _apply_step_visibility(root, step):
    for node in root.findall(nodes.Element):
        ri = node.get('_reveal_index', 0)
        if ri == 0:
            continue
        classes = [c for c in node.get('classes', []) if c not in ('step', 'step-hidden')]
        if ri > step:
            classes.append('step-hidden')
        node['classes'] = classes


def _deep_clone(node):
    orig_parent = node.parent
    node.parent = None
    try:
        return copy.deepcopy(node)
    finally:
        node.parent = orig_parent


def _expand_slide(slide, slide_number):
    template = _deep_clone(slide)
    total = _assign_reveal_indices(template)
    if total == 0:
        slide['_slide_number'] = slide_number
        return [slide]

    sections = []
    for step in range(1, total + 1):
        sec = copy.deepcopy(template)
        _apply_step_visibility(sec, step)
        sec['_slide_number'] = slide_number
        sections.append(sec)
    return sections

def _expand_document_for_step_pdf(document):
    new_children = []
    slide_num = 0
    for node in list(document.children):
        if isinstance(node, slido_block):
            slide_num += 1
            new_children.extend(_expand_slide(node, slide_num))
        else:
            new_children.append(node)
    document.children = new_children
    for child in document.children:
        child.parent = document


# ── b6plus Transformation ───────────────────────────────────────────────────
def _b6_transform(document):
    """Convert step semantics to b6plus `incremental` classes."""

    # Phase 1: Handle slido blocks with step
    for slide in document.findall(slido_block):
        classes = slide.get('classes', [])
        if 'step' not in classes:
            continue

        slide['classes'] = [c for c in classes if c != 'step']

        for child in slide.children:
            if not isinstance(child, nodes.Element):
                continue
            if isinstance(child, (nodes.title, nodes.colspec, nodes.thead)):
                continue
            child_classes = list(child.get('classes', []))
            if 'incremental' not in child_classes:
                child['classes'] = child_classes + ['incremental']

    # Phase 2: Other step containers and atomic elements
    for node in document.findall(nodes.Element):
        classes = node.get('classes', [])
        if 'step' not in classes:
            continue

        clean = [c for c in classes if c != 'step']

        if 'incremental' not in clean:
            clean.append('incremental')

        node['classes'] = clean


# ── CSS & Assets ─────────────────────────────────────────────────────────────
_CSS_FULLWIDTH = (
    '<style>body,footer,header{'
    'max-width:none!important;width:100%;padding:1px 2%;margin:0 auto;'
    '}</style>'
)

_CSS_STEP_HIDDEN = '<style>.step-hidden{opacity:0;}</style>'


# ── Translators ──────────────────────────────────────────────────────────────
class SlidoTranslator(HTMLTranslator):
    def __init__(self, document, output_type='standard'):
        super().__init__(document)
        self.slide_count = 0
        self.config = getattr(document, 'presentation_config', {})
        self.output_type = output_type

    def visit_document(self, node):
        super().visit_document(node)

        self.head = [tag for tag in self.head if not tag.strip().startswith('<title')]

        self.head.append(_CSS_FULLWIDTH)
        if self.output_type == 'step':
            self.head.append(_CSS_STEP_HIDDEN)

        cfg = self.config
        if 'title' in cfg:
            self.head.append(f'<title>{cfg["title"]}</title>\n')
        if 'css' in cfg:
            for css in cfg['css'].split(','):
                self.head.append(f'<link rel="stylesheet" href="{css.strip()}" type="text/css" />\n')
        if 'js' in cfg:
            for js in cfg['js'].split(','):
                self.head.append(f'<script src="{js.strip()}"></script>\n')

    def depart_document(self, node):
        super().depart_document(node)
        self.body_prefix = [x.replace('<main>', '') for x in self.body_prefix]
        self.body_suffix = [x.replace('</main>\n', '').replace('</main>', '') for x in self.body_suffix]

    def visit_slido_block(self, node):
        if '_slide_number' in node:
            self.slide_count = node['_slide_number']
        else:
            self.slide_count += 1

        extra = [c for c in node.get('classes', []) if c not in ('step', 'step-hidden')]
        class_str = ' '.join(['slide'] + extra)
        id_attr = f' id="{node["ids"][0]}"' if node.get('ids') else ''
        self.body.append(f'<section class="{class_str}"{id_attr}>\n')
        if node.get('title'):
            self.body.append(f'<h2>{node["title"]}</h2>\n')

    def depart_slido_block(self, node):
        self.body.append(f'<div class="slide-number">{self.slide_count}</div></section>\n')

    # [ADDED] Handler functions to output the new komento_block as a `<section class="comment">`
    def visit_komento_block(self, node):
        extra = node.get('classes', [])
        # Merge our required 'comment' class with any user-supplied classes
        class_str = ' '.join(['comment'] + extra)
        id_attr = f' id="{node["ids"][0]}"' if node.get('ids') else ''
        self.body.append(f'<section class="{class_str}"{id_attr}>\n')

    # [ADDED] Close the section tag when departing the komento_block
    def depart_komento_block(self, node):
        self.body.append('</section>\n')

    def visit_graphviz_block(self, node):
        align = node.get('align', 'center')

        classes = ['graphviz-container'] + node.get('classes', [])

        styles = []
        if align == 'center':
            styles.append('margin: 0 auto;')
            styles.append('text-align: center;')
        elif align == 'left':
            styles.append('margin-right: auto;')
            styles.append('text-align: left;')
        elif align == 'right':
            styles.append('margin-left: auto;')
            styles.append('text-align: right;')

        if 'scale' in node:
            try:
                scale_val = float(node['scale']) / 100.0
                styles.append(f'transform: scale({scale_val});')
                if align == 'center':
                    styles.append('transform-origin: top center;')
                elif align == 'right':
                    styles.append('transform-origin: top right;')
                else:
                    styles.append('transform-origin: top left;')
            except ValueError:
                pass

        class_str = ' '.join(classes)
        style_str = ' '.join(styles)

        self.body.append(f'<div class="{class_str}" style="{style_str}">\n{node.get("svg", "")}\n</div>\n')
        raise nodes.SkipNode


class PresentationSlidoTranslator(SlidoTranslator):
    def __init__(self, document):
        super().__init__(document)
        self.slide_count = 0
        self.config = getattr(document, 'presentation_config', {})
        self._progress_emitted = False

    def visit_document(self, node):
        SlidoTranslator.visit_document(self, node)
        cfg = self.config

        _B6PLUS_JS_URL = 'assets/b6plus.js'

        _CSS_B6PLUS = (
            '<style>'
            'body.full .next:not(.active):not(.visited),'
            'body.full .incremental>*:not(.active):not(.visited),'
            'body.full .overlay>*:not(.active):not(.visited){visibility:hidden}'
            'body.full section.slide{padding-bottom:1rem;break-after:auto;background-color:#ffffff;}'
            '</style>\n'
        )

        if 'css' in cfg:
            for css in cfg['css'].split(','):
                self.head.append(
                    f'<link rel="stylesheet" href="{css.strip()}" type="text/css" />\n'
                )

        self.head.append(_CSS_FULLWIDTH)
        self.head.append(_CSS_B6PLUS)

        self.head.append(f'<script src="{_B6PLUS_JS_URL}"></script>\n')

        if 'js' in cfg:
            for js in cfg['js'].split(','):
                self.head.append(f'<script src="{js.strip()}"></script>\n')

        self.body.append(
            '<script>\n'
            'document.addEventListener("DOMContentLoaded", function() {\n'
            '    setTimeout(function() {\n'
            '        if (typeof b6plus !== "undefined" && typeof b6plus.init === "function") {\n'
            '            b6plus.init();\n'
            '        } else if (typeof b6plus !== "undefined") {\n'
            '            console.log("b6plus loaded - auto mode");\n'
            '        }\n'
            '    }, 10);\n'
            '});\n'
            '</script>\n'
        )

# ── Writers ──────────────────────────────────────────────────────────────────
class SlidoWriter(HTML5WriterBase):
    def __init__(self, output_type='standard'):
        super().__init__()
        self._output_type = output_type
        self.translator_class = lambda doc: SlidoTranslator(doc, output_type=output_type)

        self.settings = OptionParser(
            components=(self,),
            defaults={
                'file_insertion_enabled': True,
                'raw_enabled': True,
                'halt_level': Reporter.WARNING_LEVEL,
                'report_level': Reporter.WARNING_LEVEL,
                'output_encoding': 'utf-8',
            }
        ).get_default_values()

    def translate(self):
        if self._output_type == 'step':
            _expand_document_for_step_pdf(self.document)
        super().translate()


class PresentationSlidoWriter(HTML5WriterBase):
    def __init__(self):
        super().__init__()
        self.translator_class = PresentationSlidoTranslator

        self.settings = OptionParser(
            components=(self,),
            defaults={
                'file_insertion_enabled': True,
                'raw_enabled': True,
                'halt_level': Reporter.WARNING_LEVEL,
                'report_level': Reporter.WARNING_LEVEL,
                'output_encoding': 'utf-8',
            }
        ).get_default_values()

    def translate(self):
        _b6_transform(self.document)
        super().translate()


# ── Public API ───────────────────────────────────────────────────────────────
def publish_to_html(source_rst: str, output_type: str = 'standard') -> bytes:
    doctree = publish_doctree(source_rst)
    if output_type == 'presentation':
        writer = PresentationSlidoWriter()
    else:
        writer = SlidoWriter(output_type=output_type)
    return publish_from_doctree(doctree, writer=writer, settings=writer.settings)


# ════════════════════════════════════════════════════════════════════════════
# [ADDED] Standalone-folder ("--outdir") feature
# ════════════════════════════════════════════════════════════════════════════
# Everything in this section is new. It implements a self-contained output
# folder (similar to Hovercraft's / prezentprogramo's default behaviour)
# holding:
#   outdir/index.html                  -- same content as *.presentation.html
#   outdir/<name>.concise4pdf.html     -- same content as the default
#                                          *.concise4pdf.html output, kept
#                                          under its own filename
#   outdir/list_of_resources.rst       -- manifest tying every copied file
#                                          back to its original source file
#   outdir/<...>                       -- copies of every local image, css,
#                                          js, the b6plus.js library, and any
#                                          ".. include::" file the slides use,
#                                          each placed at the SAME relative
#                                          path it already has in the HTML
#                                          (so none of the existing <img>,
#                                          <link>, or <script> tags need to
#                                          be rewritten).
#
# No HTTP server and no source-file watcher are implemented here on purpose
# (per explicit request) -- this only builds the folder and writes the
# manifest so that a *future* "rebuild if a source changed" feature has the
# recorded modification times/sizes it would need to detect staleness.

def _collect_referenced_resources(source_rst: str, input_dir: str):
    """
    [ADDED] Discover every local file the generated HTML depends on.

    This parses `source_rst` into its own, independent doctree (a separate
    publish_doctree() call from the ones inside publish_to_html(), so that
    none of the existing three-output generation code path is touched) and
    collects:
        * every ".. image::" / ".. figure::" URI
        * the css/js files listed in the ".. prezento::" options
        * the b6plus.js presentation-library asset
        * every file pulled in via ".. include::" (docutils itself records
          these automatically into `settings.record_dependencies` whenever
          `file_insertion_enabled` is true, so we simply read that list back
          out instead of re-implementing docutils' own path resolution)

    Returns a list of dicts, each with:
        kind       -- 'image' | 'css' | 'js' | 'library' | 'include'
        rel_path   -- the path exactly as written in the RST/HTML (this is
                      reused unchanged as the copy's location inside outdir)
        abs_path   -- resolved absolute path on disk, or None if not found
        external   -- True for http(s)/data URIs, which are never copied

    NOTE on path resolution: relative paths are resolved against `input_dir`
    (the directory containing the main .rst file). This matches how a
    browser resolves the same relative URLs once the HTML sits next to its
    resources, and it matches how docutils' own ".. include::" directive
    resolves paths when publish_doctree() is called without an explicit
    source_path (it falls back to the current working directory, which in
    prezento's documented usage is the input file's own directory).
    """
    resources = []

    # A dedicated, silent parse: report_level/halt_level are raised so this
    # extra scanning pass does not print duplicate warnings on top of the
    # ones the real publish_to_html() calls already show the user.
    doctree = publish_doctree(
        source_rst,
        settings_overrides={
            'file_insertion_enabled': True,
            'report_level': Reporter.SEVERE_LEVEL,
            'halt_level': Reporter.SEVERE_LEVEL,
        },
    )

    # ---- images (".. image::" and ".. figure::", which contains an image) --
    for img in doctree.findall(nodes.image):
        uri = img.get('uri')
        if uri:
            resources.append({'kind': 'image', 'rel_path': uri})

    # ---- css / js declared on the ".. prezento::" directive ----------------
    cfg = getattr(doctree, 'presentation_config', {})
    if 'css' in cfg:
        for css in cfg['css'].split(','):
            css = css.strip()
            if css:
                resources.append({'kind': 'css', 'rel_path': css})
    if 'js' in cfg:
        for js in cfg['js'].split(','):
            js = js.strip()
            if js:
                resources.append({'kind': 'js', 'rel_path': js})

    # ---- the b6plus.js presentation library --------------------------------
    # Mirrors the '_B6PLUS_JS_URL' literal inside
    # PresentationSlidoTranslator.visit_document(); duplicated here (rather
    # than imported/shared) so that none of the existing translator code
    # needs to be touched for this feature.
    resources.append({'kind': 'library', 'rel_path': 'assets/b6plus.js'})

    # ---- ".. include::" file dependencies -----------------------------------
    record_deps = getattr(doctree.settings, 'record_dependencies', None)
    if record_deps is not None:
        for dep_path in record_deps.list:
            resources.append({'kind': 'include', 'rel_path': dep_path})

    # ---- de-duplicate --------------------------------------------------------
    # The same file may be referenced more than once (e.g. one image used on
    # two slides); keep only the first occurrence so it is copied/listed once.
    seen = set()
    deduped = []
    for res in resources:
        if res['rel_path'] in seen:
            continue
        seen.add(res['rel_path'])
        deduped.append(res)
    resources = deduped

    # ---- resolve absolute paths on disk (skip external URLs) ----------------
    external_prefixes = ('http://', 'https://', '//', 'data:')
    for res in resources:
        rel = res['rel_path']
        if rel.startswith(external_prefixes):
            res['abs_path'] = None
            res['external'] = True
        else:
            candidate = os.path.normpath(os.path.join(input_dir, rel))
            res['abs_path'] = candidate if os.path.isfile(candidate) else None
            res['external'] = False

    return resources


def _copy_resource(res: dict, outdir: str):
    """
    [ADDED] Copy a single resource (as discovered by
    _collect_referenced_resources) into `outdir`, preserving its relative
    path exactly so the already-generated HTML keeps working unmodified.

    Sets and returns extra bookkeeping keys on `res` used by the manifest:
        status  -- 'copied' | 'missing' | 'external (not copied)' |
                   'skipped (outside outdir)'
        size    -- size in bytes of the source file (set only when copied)
        mtime   -- modification time of the source file (set only when copied)
    """
    res['size'] = None
    res['mtime'] = None

    if res.get('external'):
        res['status'] = 'external (not copied)'
        return res

    res['status'] = 'missing'
    if not res.get('abs_path'):
        return res

    # Guard against a relative path (e.g. via '../..') that would copy a
    # file outside of `outdir`; such resources are skipped rather than
    # silently written somewhere unexpected on disk.
    dest = os.path.normpath(os.path.join(outdir, res['rel_path']))
    outdir_abs = os.path.abspath(outdir)
    if os.path.commonpath([outdir_abs, os.path.abspath(dest)]) != outdir_abs:
        res['status'] = 'skipped (outside outdir)'
        return res

    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.copy2(res['abs_path'], dest)   # copy2 preserves mtime for future diffing

    stat = os.stat(res['abs_path'])
    res['status'] = 'copied'
    res['size'] = stat.st_size
    res['mtime'] = stat.st_mtime
    return res


def _write_resource_manifest(outdir, input_file, generated_files, resources):
    """
    [ADDED] Write outdir/list_of_resources.rst: a plain-text, valid-RST
    manifest recording, for every generated HTML file and every copied
    resource, which original source file it came from and that file's size
    and modification time at the moment this folder was built. A future
    "rebuild if changed" feature can re-stat the original files and compare
    them against these recorded values to know whether the folder is stale.
    """
    lines = []
    lines.append('List of Resources')
    lines.append('==================')
    lines.append('')
    lines.append(
        'This file is generated automatically by prezento. It records every '
        'source file that the HTML in this folder depends on, so that a '
        'future version of prezento can detect when this folder needs to be '
        'rebuilt. Do not edit it by hand -- it is overwritten every time '
        'this standalone folder is regenerated.'
    )
    lines.append('')

    main_stat = os.stat(input_file)
    lines.append(f':generated_at: {datetime.datetime.now().isoformat()}')
    lines.append(f':main_source_file: {os.path.basename(input_file)}')
    lines.append(f':main_source_mtime: {main_stat.st_mtime}')
    lines.append(f':main_source_size: {main_stat.st_size}')
    lines.append('')

    lines.append('Generated files')
    lines.append('----------------')
    lines.append('')
    for filename, description in generated_files:
        file_path = os.path.join(outdir, filename)
        try:
            sz = os.path.getsize(file_path)
        except OSError:
            sz = 0
        lines.append(f'* **{filename}** -- {description} ({sz} bytes)')
    lines.append('')

    lines.append('Tracked resources')
    lines.append('------------------')
    lines.append('')
    if not resources:
        lines.append('(none found)')
    for res in resources:
        detail = res['status']
        if res['status'] == 'copied':
            detail += f", {res['size']} bytes, source mtime {res['mtime']}"
        lines.append(
            f"* **{res['kind']}** ``{res['rel_path']}`` -> "
            f"``{res['rel_path']}`` [{detail}]"
        )
    lines.append('')

    manifest_path = os.path.join(outdir, 'list_of_resources.rst')
    with open(manifest_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    return manifest_path


def build_standalone_folder(input_file: str, source: str, outdir: str):
    """
    [ADDED] Build the full standalone, self-contained output folder:
        outdir/index.html                  (== *.presentation.html)
        outdir/<name>.concise4pdf.html
        outdir/list_of_resources.rst       (dependency manifest)
        outdir/<...copied images, css, js, b6plus.js, include files...>

    This is the entry point for the new `--outdir` CLI option. It always
    (re)generates its own presentation/concise HTML internally, independent
    of the -s/--step and -np/--no-presentation flags, which only control the
    separate, plain same-directory outputs main() writes alongside the
    source file -- this keeps the standalone-folder feature self-contained
    and predictable regardless of those flags.

    Note: this does not delete any pre-existing content already present at
    `outdir` (no rebuild/staleness logic is implemented yet, by design --
    see the module-level comment above this section).
    """
    os.makedirs(outdir, exist_ok=True)

    input_dir = os.path.dirname(os.path.abspath(input_file))
    base_name = os.path.splitext(os.path.basename(input_file))[0]

    # 1. Generate the two HTML variants this folder is meant to hold.
    presentation_html = publish_to_html(source, 'presentation').decode('utf-8')
    concise_html = publish_to_html(source, 'standard').decode('utf-8')

    index_path = os.path.join(outdir, 'index.html')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(presentation_html)

    concise_name = f'{base_name}.concise4pdf.html'
    concise_path = os.path.join(outdir, concise_name)
    with open(concise_path, 'w', encoding='utf-8') as f:
        f.write(concise_html)

    # 2. Discover and copy every local resource the HTML depends on.
    resources = _collect_referenced_resources(source, input_dir)
    for res in resources:
        _copy_resource(res, outdir)

    # 3. Write the manifest tying it all together.
    generated_files = [
        ('index.html', f'same content as {base_name}.presentation.html'),
        (concise_name,
         'concise / print-friendly HTML (same content as the default '
         '*.concise4pdf.html output)'),
    ]
    manifest_path = _write_resource_manifest(
        outdir, input_file, generated_files, resources
    )

    # 4. Console summary.
    n_copied = sum(1 for r in resources if r['status'] == 'copied')
    n_missing = sum(1 for r in resources if r['status'] == 'missing')
    n_external = sum(1 for r in resources if r['status'] == 'external (not copied)')
    n_other = len(resources) - n_copied - n_missing - n_external

    print(f'Standalone folder written: {outdir}')
    print(f'  {index_path}')
    print(f'  {concise_path}')
    print(f'  {manifest_path}')
    summary = f'  Resources: {n_copied} copied, {n_missing} missing, {n_external} external'
    if n_other:
        summary += f', {n_other} skipped'
    print(summary)


def main():
    parser = argparse.ArgumentParser(description='prezent v1')
    parser.add_argument('input_file')
    parser.add_argument('-o', '--output')
    parser.add_argument('-s', '--step', action='store_true')
    parser.add_argument('-np', '--no-presentation', action='store_true')
    # [ADDED] --outdir: build a standalone, self-contained folder containing
    # index.html, <name>.concise4pdf.html, copies of every local resource
    # they use, and a list_of_resources.rst manifest. See
    # build_standalone_folder() for details.
    parser.add_argument('-d', '--outdir',
                         help='Build a standalone folder containing index.html, '
                              '<name>.concise4pdf.html, copies of every local '
                              'resource they use, and a list_of_resources.rst '
                              'manifest')
    args = parser.parse_args()

    with open(args.input_file, 'r', encoding='utf-8') as f:
        source = f.read()

    base = os.path.splitext(args.input_file)[0]

    out = args.output or (base + '.concise4pdf.html')
    with open(out, 'w', encoding='utf-8') as f:
        f.write(publish_to_html(source).decode('utf-8'))
    print(f'Written: {out}')

    if args.step:
        sub = base + '.step4pdf.html'
        with open(sub, 'w', encoding='utf-8') as f:
            f.write(publish_to_html(source, 'step').decode('utf-8'))
        print(f'Written: {sub}')

    if not args.no_presentation:
        pres = base + '.presentation.html'
        with open(pres, 'w', encoding='utf-8') as f:
            f.write(publish_to_html(source, 'presentation').decode('utf-8'))
        print(f'Written: {pres}')

    # [ADDED] Build the standalone, self-contained output folder if requested.
    if args.outdir:
        build_standalone_folder(args.input_file, source, args.outdir)


# ── CLI ──────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    main()
