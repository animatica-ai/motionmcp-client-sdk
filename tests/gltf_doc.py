"""Shared glTF document builder for tests.

Builds the minimal-but-complete glTF documents used to exercise
``parse_gltf`` / ``parse_gltf_samples``, in the same conventions the MMCP
server uses (embedded base64 buffers, per-sample animations, the
``MMCP_motion`` contacts extension). When the client moves to its own
repo, a copy of this file goes with it, so both test suites keep the same
builder.
"""

from __future__ import annotations

import base64
import math
import struct


def _accessor(doc, blob, component_type, type_str, count, fmt, values):
    """Append raw *values* to *blob*, register bufferView + accessor."""
    offset = len(blob)
    packed = b"".join(struct.pack(fmt, *v) if isinstance(v, (tuple, list))
                      else struct.pack(fmt, v) for v in values)
    blob += packed
    doc["bufferViews"].append(
        {"buffer": 0, "byteOffset": offset, "byteLength": len(packed)})
    doc["accessors"].append({
        "bufferView": len(doc["bufferViews"]) - 1, "byteOffset": 0,
        "componentType": component_type, "count": count, "type": type_str})
    return len(doc["accessors"]) - 1, blob


def build_gltf(num_samples=1, contacts=None, with_rotations=True):
    """A 3-joint, 2-frame document: Hips → Spine → Head.

    Frame 0 all-identity; frame 1 rotates Hips 90° about +Y. The root
    carries a translation track ([1,2,3] then [4,5,6]); rest offsets are
    Hips (0,1,0), Spine +0.5, Head +0.3 — accumulation must produce world
    rest heights 1.0 / 1.5 / 1.8.
    """
    doc = {
        "nodes": [
            {"name": "Hips", "translation": [0.0, 1.0, 0.0], "children": [1]},
            {"name": "Spine", "translation": [0.0, 0.5, 0.0], "children": [2]},
            {"name": "Head", "translation": [0.0, 0.3, 0.0]},
        ],
        "bufferViews": [], "accessors": [], "animations": [], "buffers": [],
    }
    blob = b""

    times = [0.0, 1.0 / 30.0]
    t_acc, blob = _accessor(doc, blob, 5126, "SCALAR", 2, "<f", times)

    half = math.sqrt(0.5)
    quats = {
        0: [(0.0, 0.0, 0.0, 1.0), (0.0, half, 0.0, half)],   # Hips: 90° yaw
        1: [(0.0, 0.0, 0.0, 1.0), (0.0, 0.0, 0.0, 1.0)],
        2: [(0.0, 0.0, 0.0, 1.0), (0.0, 0.0, 0.0, 1.0)],
    }
    rot_acc = {}
    for ni, values in quats.items():
        rot_acc[ni], blob = _accessor(doc, blob, 5126, "VEC4", 2, "<4f", values)
    trans_acc, blob = _accessor(doc, blob, 5126, "VEC3", 2, "<3f",
                                [(1.0, 2.0, 3.0), (4.0, 5.0, 6.0)])

    for _ in range(num_samples):
        channels, samplers = [], []
        if with_rotations:
            for ni in (0, 1, 2):
                samplers.append({"input": t_acc, "output": rot_acc[ni]})
                channels.append({"sampler": len(samplers) - 1,
                                 "target": {"node": ni, "path": "rotation"}})
        samplers.append({"input": t_acc, "output": trans_acc})
        channels.append({"sampler": len(samplers) - 1,
                         "target": {"node": 0, "path": "translation"}})
        doc["animations"].append({"channels": channels, "samplers": samplers})

    doc["buffers"] = [{
        "byteLength": len(blob),
        "uri": "data:application/octet-stream;base64,"
               + base64.b64encode(blob).decode("ascii"),
    }]
    if contacts is not None:
        doc["extensions"] = {"MMCP_motion": {"samples": contacts}}
    return doc
