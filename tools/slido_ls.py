#!/usr/bin/env python3
# Gemini AI, A specialized SLP server, $ chmod a+x slido_ls.py
# Kate --> Settings --> Configure Kate
# New Window --> Plugins(from left) --> LSP Client --> Tick (enable)
# --> Apply --> LSP Client will be shown in the left --> Click on it
# Click on the tab by the name "user server settings"
# Add the following code
#   {
#       "servers": {
#           "rst": {
#               "command": ["/home/absolute/path/to/here/prezento/tools/slido_ls.py"],
#               "rootIndicationFileNames": [],
#               "highlightingModeRegex": "^reStructuredText$"
#           }
#       }
#   }
#
import sys
import json
import re

def send_rpc(response):
    """Formats and forcefully flushes a standard JSON-RPC payload to Kate."""
    body = json.dumps(response)
    payload = f"Content-Length: {len(body)}\r\n\r\n{body}"
    sys.stdout.write(payload)
    sys.stdout.flush()

def extract_slido_symbols(lines):
    """Parses presentation mode: Returns sequentially numbered slides."""
    symbols = []
    slide_counter = 1

    for index, line in enumerate(lines):
        # Bracket notation handles the dot strings without syntax warnings
        match = re.match(r'^[.][.]\s+slido::\s*(.*)', line)
        if match:
            raw_name = match.group(1).strip()
            display_name = f"({slide_counter}) {raw_name}" if raw_name else f"({slide_counter}) [Untitled Slide]"
            slide_counter += 1

            item_range = {
                "start": {"line": index, "character": 0},
                "end": {"line": index, "character": len(line)}
            }
            symbols.append({
                "name": display_name,
                "detail": "slido directive",
                "kind": 5,  # 5 = Class representation kind
                "range": item_range,
                "selectionRange": item_range
            })
    return symbols

def extract_normal_rst_symbols(lines):
    """Parses normal document mode: Extracts rst headers as a deep hierarchical tree."""
    flat_headers = []
    total_lines = len(lines)
    levels_seen = []  # Tracks unique underline chars seen to establish weights dynamically

    # Map array to supply distinct graphical symbol icons for up to 6 nested document depths
    # 2=Module, 3=Namespace, 5=Class, 6=Method, 12=Function, 13=Variable
    kind_map = [2, 3, 5, 6, 12, 13]

    for index, line in enumerate(lines):
        # CRITICAL FIX: Section title text MUST start exactly at Column 1 (no indentation)
        if not line or line[0].isspace():
            continue

        if index + 1 < total_lines:
            next_line = lines[index + 1]

            # CRITICAL FIX: Underline text MUST also start exactly at Column 1
            if not next_line or next_line[0].isspace():
                continue

            next_line_stripped = next_line.strip()
            title_text_stripped = line.strip()

            # CRITICAL FIX 1: Underline must be solid, at least 3 chars, AND at least as long as title text
            if (len(next_line_stripped) >= 3 and
                len(next_line_stripped) >= len(title_text_stripped) and
                #next_line_stripped[0] in '=-~`^:"' and
                next_line_stripped[0] in '#*=-^`~' and
                len(set(next_line_stripped)) == 1):

                char_marker = next_line_stripped[0]

                if char_marker not in levels_seen:
                    levels_seen.append(char_marker)

                # Determine numerical nesting depth based on when the character was first introduced
                depth_level = levels_seen.index(char_marker)

                item_range = {
                    "start": {"line": index, "character": 0},
                    "end": {"line": index + 1, "character": len(lines[index + 1])}
                }

                # CRITICAL FIX 2: Dynamically map depths to distinct structural visual icons to allow 4+ layers
                kind_type = kind_map[depth_level] if depth_level < len(kind_map) else 13

                flat_headers.append({
                    "name": title_text_stripped,
                    "detail": f"Level {depth_level + 1} Section",
                    "kind": kind_type,
                    "range": item_range,
                    "selectionRange": item_range,
                    "children": [],
                    "_depth": depth_level  # Internal meta tracking property
                })

    # Reconstruct the flat parsed stream into a multi-tier recursive node tree
    root_symbols = []
    active_branch_stack = []  # Evaluates parenting depth contexts linearly

    for header in flat_headers:
        # Prune the tree branch back until we find a suitable parent tier
        while active_branch_stack and active_branch_stack[-1]["_depth"] >= header["_depth"]:
            active_branch_stack.pop()

        # Clean up internal metadata tag to avoid causing schema validation complaints in Kate
        clean_node = {k: v for k, v in header.items() if k != "_depth"}

        if not active_branch_stack:
            root_symbols.append(clean_node)
        else:
            # Append item directly inside its validated structural parent block array
            active_branch_stack[-1]["children"].append(clean_node)

        # Reference this element as the active node index target for the next loop items
        active_branch_stack.append(header)

    return root_symbols

def main():
    documents = {}

    while True:
        try:
            # Read header components safely out of binary stream layers
            header_line = b""
            while b"\r\n" not in header_line:
                char = sys.stdin.buffer.read(1)
                if not char:
                    return
                header_line += char

            if b"Content-Length:" in header_line:
                parts = header_line.split(b":")
                length = int(parts[1].strip())

                sys.stdin.buffer.read(2)  # Clear trailing separator line (\r\n)

                body_bytes = sys.stdin.buffer.read(length)
                request = json.loads(body_bytes.decode('utf-8'))

                method = request.get("method")
                req_id = request.get("id")
                params = request.get("params", {})

                if method == "initialize":
                    send_rpc({
                        "id": req_id,
                        "result": {
                            "capabilities": {
                                "textDocumentSync": 1,
                                "documentSymbolProvider": True
                            }
                        }
                    })

                elif method == "textDocument/didOpen":
                    doc = params.get("textDocument", {})
                    uri = doc.get("uri")
                    if uri:
                        documents[uri] = doc.get("text", "")

                elif method == "textDocument/didChange":
                    uri = params.get("textDocument", {}).get("uri")
                    changes = params.get("contentChanges", [])
                    if uri and changes:
                        documents[uri] = changes[0].get("text", "")

                elif method == "textDocument/documentSymbol":
                    uri = params.get("textDocument", {}).get("uri")
                    doc_text = documents.get(uri, "")
                    lines = doc_text.splitlines()

                    # Safe bracket sequence verification check
                    if any(re.match(r'^[.][.]\s+prezento::', l1) for l1 in lines):
                        symbols = extract_slido_symbols(lines)
                    else:
                        symbols = extract_normal_rst_symbols(lines)

                    send_rpc({
                        "id": req_id,
                        "result": symbols
                    })

                elif req_id is not None:
                    send_rpc({"id": req_id, "result": None})

        except Exception as e:
            sys.stderr.write(f"[Server Error] {str(e)}\n")
            sys.stderr.flush()
            continue

if __name__ == "__main__":
    main()
