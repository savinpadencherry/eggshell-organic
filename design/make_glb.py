#!/usr/bin/env python3
"""Build eggshell-box.glb: an exact cuboid with the panel artwork as PBR textures.

Usage: python3 make_glb.py <texture_dir> <out.glb>
Expects panel-{front,back,top,bottom,side}.png in <texture_dir>.
"""
import json, struct, sys, os

TEX_DIR, OUT = sys.argv[1], sys.argv[2]

# box dimensions (metres) — front 2400x1000, top 2400x760 artwork ratios
W, H, D = 2.4, 1.0, 0.76
x, y, z = W / 2, H / 2, D / 2

# corners listed BL, BR, TR, TL as seen from outside; UVs map artwork upright
FACES = [
    # name         corners                                                      normal
    ("front",  [(-x,-y, z), ( x,-y, z), ( x, y, z), (-x, y, z)], ( 0, 0, 1)),
    ("back",   [( x,-y,-z), (-x,-y,-z), (-x, y,-z), ( x, y,-z)], ( 0, 0,-1)),
    ("top",    [(-x, y, z), ( x, y, z), ( x, y,-z), (-x, y,-z)], ( 0, 1, 0)),
    ("bottom", [(-x,-y,-z), ( x,-y,-z), ( x,-y, z), (-x,-y, z)], ( 0,-1, 0)),
    ("side",   [( x,-y, z), ( x,-y,-z), ( x, y,-z), ( x, y, z)], ( 1, 0, 0)),  # right
    ("side",   [(-x,-y,-z), (-x,-y, z), (-x, y, z), (-x, y,-z)], (-1, 0, 0)),  # left
]
TEXTURES = ["front", "back", "top", "bottom", "side"]  # material per texture

def pad4(b, fill=b"\x00"):
    return b + fill * (-len(b) % 4)

bin_parts, buffer_views, accessors, primitives = [], [], [], []
offset = 0

def add_view(data, target=None):
    global offset
    data = pad4(data)
    view = {"buffer": 0, "byteOffset": offset, "byteLength": len(data)}
    if target:
        view["target"] = target
    buffer_views.append(view)
    bin_parts.append(data)
    offset += len(data)
    return len(buffer_views) - 1

for name, corners, normal in FACES:
    pos = b"".join(struct.pack("<3f", *c) for c in corners)
    nrm = struct.pack("<3f", *normal) * 4
    uv = struct.pack("<8f", 0, 1, 1, 1, 1, 0, 0, 0)
    idx = struct.pack("<6H", 0, 1, 2, 0, 2, 3)

    mins = [min(c[i] for c in corners) for i in range(3)]
    maxs = [max(c[i] for c in corners) for i in range(3)]

    a0 = len(accessors)
    accessors += [
        {"bufferView": add_view(pos, 34962), "componentType": 5126, "count": 4,
         "type": "VEC3", "min": mins, "max": maxs},
        {"bufferView": add_view(nrm, 34962), "componentType": 5126, "count": 4, "type": "VEC3"},
        {"bufferView": add_view(uv, 34962), "componentType": 5126, "count": 4, "type": "VEC2"},
        {"bufferView": add_view(idx, 34963), "componentType": 5123, "count": 6, "type": "SCALAR"},
    ]
    primitives.append({
        "attributes": {"POSITION": a0, "NORMAL": a0 + 1, "TEXCOORD_0": a0 + 2},
        "indices": a0 + 3,
        "material": TEXTURES.index(name),
    })

images = []
for t in TEXTURES:
    with open(os.path.join(TEX_DIR, f"panel-{t}.png"), "rb") as f:
        images.append({"bufferView": add_view(f.read()), "mimeType": "image/png",
                       "name": f"panel-{t}"})

gltf = {
    "asset": {"version": "2.0", "generator": "eggshell-design-pipeline"},
    "scene": 0,
    "scenes": [{"nodes": [0]}],
    "nodes": [{"mesh": 0, "name": "EggShellBox"}],
    "meshes": [{"primitives": primitives, "name": "carton"}],
    "accessors": accessors,
    "bufferViews": buffer_views,
    "buffers": [{"byteLength": offset}],
    "images": images,
    "samplers": [{"magFilter": 9729, "minFilter": 9987, "wrapS": 33071, "wrapT": 33071}],
    "textures": [{"sampler": 0, "source": i} for i in range(len(TEXTURES))],
    "materials": [{
        "name": t,
        "pbrMetallicRoughness": {
            "baseColorTexture": {"index": i},
            "metallicFactor": 0.0,
            "roughnessFactor": 0.85,
        },
    } for i, t in enumerate(TEXTURES)],
}

json_chunk = pad4(json.dumps(gltf, separators=(",", ":")).encode(), b" ")
bin_chunk = b"".join(bin_parts)
total = 12 + 8 + len(json_chunk) + 8 + len(bin_chunk)

with open(OUT, "wb") as f:
    f.write(struct.pack("<4sII", b"glTF", 2, total))
    f.write(struct.pack("<I4s", len(json_chunk), b"JSON") + json_chunk)
    f.write(struct.pack("<I4s", len(bin_chunk), b"BIN\x00") + bin_chunk)

print(f"wrote {OUT} ({total/1e6:.2f} MB, {len(primitives)} faces, {len(TEXTURES)} textures)")
