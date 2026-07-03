#!/usr/bin/env python3
"""Bundle index.html into a self-contained single file for sharing.

Inlines the GLB model and story image as base64 data URIs so the file
works with a plain double-click — no web server, no sibling files.
Fonts and the model-viewer library still load from CDN (needs internet).

Usage: python3 package.py <story_jpeg> <out.html>
"""
import base64, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
story_jpg, out_path = sys.argv[1], sys.argv[2]

with open(os.path.join(ROOT, "index.html")) as f:
    html = f.read()

with open(os.path.join(ROOT, "eggshell-box.glb"), "rb") as f:
    glb_uri = "data:model/gltf-binary;base64," + base64.b64encode(f.read()).decode()

with open(story_jpg, "rb") as f:
    jpg_uri = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()

replacements = [
    ('src="eggshell-box.glb"', f'src="{glb_uri}"'),
    # poster not needed once the model is inline; drop to keep the file lean
    ('poster="design/eggshell-box-3d.png"\n        ', ""),
    ('poster="design/eggshell-box-3d.png" ', ""),
    ('src="design/eggshell-box-3d.png"', f'src="{jpg_uri}"'),
]
for old, new in replacements:
    if old in html:
        html = html.replace(old, new)

assert "eggshell-box.glb" not in html, "GLB reference not fully inlined"
assert "design/" not in html, "local file references remain"

with open(out_path, "w") as f:
    f.write(html)
print(f"wrote {out_path} ({os.path.getsize(out_path)/1e6:.2f} MB, fully self-contained)")
