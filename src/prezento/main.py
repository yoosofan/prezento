# prezento – Modern RST → HTML slide generator
# Uses b6plus instead of impress.js
# Outputs: .html, .substep.pdf.html, .presentation.html

import os
import argparse
import textwrap
import copy
import re
import graphviz
from docutils import nodes
from docutils.parsers.rst import Directive, directives
from docutils.core import publish_doctree, publish_from_doctree
from docutils.writers.html5_polyglot import Writer as HTML5WriterBase, HTMLTranslator
# [NEW] Imports for proper settings handling
from docutils.frontend import OptionParser
from docutils.utils import Reporter

# ── Custom nodes ─────────────────────────────────────────────────────────────
class slido_block(nodes.container):
    pass
class graphviz_block(nodes.General, nodes.Element):
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
    }

    def run(self):
        node = slido_block()
        if self.arguments:
            node['title'] = ' '.join(self.arguments)
        if 'class' in self.options:
            node['classes'] = self.options['class']
        if 'id' in self.options:
            node['ids'] = [self.options['id']]

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
        'height': directives.unchanged
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

        dot_code = '\n'.join(self.content)
        try:
            svg = graphviz.Source(dot_code).pipe(format='svg').decode('utf-8')
            if '<svg' in svg:
                svg = svg[svg.find('<svg'):]

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


directives.register_directive('prezento', PrezentoDirective)
directives.register_directive('slido', SlidoDirective)
directives.register_directive('yographviz', GraphvizDirective)

# ── Substep Helpers ──────────────────────────────────────────────────────────

_SUBSTEP_CONTAINER_TYPES = (
    slido_block,
    nodes.container,
    nodes.block_quote,
    nodes.bullet_list,
    nodes.enumerated_list,
    nodes.definition_list,
)


def _is_substep_container(node):
    return (
        isinstance(node, _SUBSTEP_CONTAINER_TYPES)
        and isinstance(node, nodes.Element)
        and 'substep' in node.get('classes', [])
    )


def _is_atomic_substep(node):
    return (
        isinstance(node, nodes.Element)
        and 'substep' in node.get('classes', [])
        and not _is_substep_container(node)
    )

# ── Substep PDF Expansion ───────────────────────────────────────────────────
def _assign_reveal_indices(root):
    counter = [0]

    def walk(node):
        if _is_substep_container(node):
            for child in node.children:
                if isinstance(child, nodes.Text):
                    continue
                counter[0] += 1
                child['_reveal_index'] = counter[0]
                walk(child)
        elif _is_atomic_substep(node):
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
        classes = [c for c in node.get('classes', []) if c not in ('substep', 'substep-hidden')]
        if ri > step:
            classes.append('substep-hidden')
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


def _expand_document_for_substep_pdf(document):
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
    """Convert substep semantics to b6plus `incremental` / `next` classes."""

    # Phase 1: Handle slido blocks with substep
    for slide in document.findall(slido_block):
        classes = slide.get('classes', [])
        if 'substep' not in classes:
            continue

        slide['classes'] = [c for c in classes if c != 'substep']

        for child in slide.children:
            if not isinstance(child, nodes.Element):
                continue
            if isinstance(child, (nodes.title, nodes.colspec, nodes.thead)):
                continue
            child_classes = list(child.get('classes', []))
            if 'next' not in child_classes:
                child['classes'] = child_classes + ['next']

    # Phase 2: Other substep containers and atomic elements
    for node in document.findall(nodes.Element):
        classes = node.get('classes', [])
        if 'substep' not in classes:
            continue

        clean = [c for c in classes if c != 'substep']

        if _is_substep_container(node):
            if 'incremental' not in clean:
                clean.append('incremental')
        else:
            if 'next' not in clean:
                clean.append('next')

        node['classes'] = clean


# ── CSS & Assets ─────────────────────────────────────────────────────────────
_CSS_FULLWIDTH = (
    '<style>body,footer,header{'
    'max-width:none!important;width:100%;padding:1px 2%;margin:0 auto;'
    '}</style>'
)

_CSS_SUBSTEP_HIDDEN = '<style>.substep-hidden{opacity:0;}</style>'

_CSS_B6PLUS = (
    '<style>'
    'body.full .next:not(.active):not(.visited),'
    'body.full .incremental>*:not(.active):not(.visited),'
    'body.full .overlay>*:not(.active):not(.visited){visibility:hidden}'
    'body.full .slide-number{display:none}'
    'body.full section.slide{padding-bottom:1rem;break-after:auto;background-color:#ffffff;}'
    '</style>'
)



# ── Translators ──────────────────────────────────────────────────────────────
class SlidoTranslator(HTMLTranslator):
    def __init__(self, document, output_type='standard'):
        super().__init__(document)
        self.slide_count = 0
        self.config = getattr(document, 'presentation_config', {})
        self.output_type = output_type

    def visit_document(self, node):
        super().visit_document(node)
        self.head.append(_CSS_FULLWIDTH)
        if self.output_type == 'substep':
            self.head.append(_CSS_SUBSTEP_HIDDEN)

        cfg = self.config
        if 'title' in cfg:
            self.head.append(f'<title>{cfg["title"]}</title>')
        if 'css' in cfg:
            for css in cfg['css'].split(','):
                self.head.append(f'<link rel="stylesheet" href="{css.strip()}" type="text/css" />')
        if 'js' in cfg:
            for js in cfg['js'].split(','):
                self.head.append(f'<script src="{js.strip()}"></script>')

    def depart_document(self, node):
        super().depart_document(node)
        self.body_prefix = [x.replace('<main>', '') for x in self.body_prefix]
        self.body_suffix = [x.replace('</main>\n', '').replace('</main>', '') for x in self.body_suffix]

    def visit_slido_block(self, node):
        if '_slide_number' in node:
            self.slide_count = node['_slide_number']
        else:
            self.slide_count += 1

        extra = [c for c in node.get('classes', []) if c not in ('substep', 'substep-hidden')]
        class_str = ' '.join(['slide'] + extra)
        id_attr = f' id="{node["ids"][0]}"' if node.get('ids') else ''
        self.body.append(f'<section class="{class_str}"{id_attr}>\n')
        if node.get('title'):
            self.body.append(f'<h2>{node["title"]}</h2>\n')

    def depart_slido_block(self, node):
        self.body.append(f'<div class="slide-number">{self.slide_count}</div></section>\n')

    def visit_graphviz_block(self, node):
        # [CHANGED] Calculate container styles dynamically based on the options passed.
        align = node.get('align', 'center')

        # [ADDED] Merge the default container class with any user-supplied classes
        classes = ['graphviz-container'] + node.get('classes', [])

        # [ADDED] Build inline styling to handle the alignment
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

        class_str = ' '.join(classes)
        style_str = ' '.join(styles)

        # [CHANGED] Output the customized div with the dynamic styles and classes
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

        if 'title' in cfg:
            self.head.append(f'<title>{cfg["title"]}</title>')

        _B6PLUS_JS_URL = 'assets/b6plus.js'
        #_SIMPLE_CSS_URL = 'assets/style.css'

        # 1. b6plus framework CSS first
        #self.head.append(f'<link rel="stylesheet" href="{_SIMPLE_CSS_URL}" />')

        # 2. User CSS (can override b6plus)
        if 'css' in cfg:
            for css in cfg['css'].split(','):
                self.head.append(
                    f'<link rel="stylesheet" href="{css.strip()}" type="text/css" />'
                )

        self.head.append(_CSS_FULLWIDTH)
        self.head.append(_CSS_B6PLUS)

        # 3. b6plus script
        self.head.append(f'<script src="{_B6PLUS_JS_URL}"></script>')

        # 4. Additional user JS
        if 'js' in cfg:
            for js in cfg['js'].split(','):
                self.head.append(f'<script src="{js.strip()}"></script>')

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

        # [FIXED] Proper docutils settings to prevent exit on missing PIL
        # and allow :scale: / image attributes to work gracefully
        self.settings = OptionParser(
            components=(self,),
            defaults={
                'file_insertion_enabled': True,
                'raw_enabled': True,
                'halt_level': Reporter.ERROR_LEVEL,      # Only stop on real errors
                'report_level': Reporter.WARNING_LEVEL,
                'output_encoding': 'utf-8',
                'no_file_insertion': False,
            }
        ).get_default_values()

    def translate(self):
        if self._output_type == 'substep':
            _expand_document_for_substep_pdf(self.document)
        super().translate()


class PresentationSlidoWriter(HTML5WriterBase):
    def __init__(self):
        super().__init__()
        self.translator_class = PresentationSlidoTranslator

        # [FIXED] Same robust settings for presentation output
        self.settings = OptionParser(
            components=(self,),
            defaults={
                'file_insertion_enabled': True,
                'raw_enabled': True,
                'halt_level': Reporter.ERROR_LEVEL,
                'report_level': Reporter.WARNING_LEVEL,
                'output_encoding': 'utf-8',
                'no_file_insertion': False,
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


def main():
    parser = argparse.ArgumentParser(description='prezent v1')
    parser.add_argument('input_file')
    parser.add_argument('-o', '--output')
    parser.add_argument('-s', '--substep', action='store_true')
    parser.add_argument('-np', '--no-presentation', action='store_true')
    args = parser.parse_args()

    with open(args.input_file, 'r', encoding='utf-8') as f:
        source = f.read()

    base = os.path.splitext(args.input_file)[0]

    out = args.output or (base + '.concise4pdf.html')
    with open(out, 'w', encoding='utf-8') as f:
        f.write(publish_to_html(source).decode('utf-8'))
    print(f'Written: {out}')

    if args.substep:
        sub = base + '.substep4pdf.html'
        with open(sub, 'w', encoding='utf-8') as f:
            f.write(publish_to_html(source, 'substep').decode('utf-8'))
        print(f'Written: {sub}')

    if not args.no_presentation:
        pres = base + '.presentation.html'
        with open(pres, 'w', encoding='utf-8') as f:
            f.write(publish_to_html(source, 'presentation').decode('utf-8'))
        print(f'Written: {pres}')


if __name__ == '__main__':
    main()
