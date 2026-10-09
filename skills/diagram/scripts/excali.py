"""Build Excalidraw diagrams from Python, and refuse the ones not worth looking at.

Copy this file beside a diagram spec (`<name>.py`) in the session's diagrams folder, the way clipkit sits beside
a clip. A spec builds a list of elements with the helpers below and calls `write(name, els)`, which checks the
diagram and writes `<name>.excalidraw` (open at excalidraw.com or in the VS Code extension) and `<name>.view.json`
(the Excalidraw MCP `create_view` format). `write` exits non-zero when `check` finds a problem.

Shapes are small named nodes. Words that explain go in `note()`s outside the shapes, tied to what they explain
by a leader line. Arrows carry the relationship, with a verb on them. `write` also emits `<name>.claims.md`, every
arrow and note as one line, so a fresh agent can check what the picture asserts without trusting how it looks.
"""
import json
import sys
from pathlib import Path

BLUE, GREEN, ORANGE, PURPLE, RED, YELLOW, TEAL, GREY = (
    "#a5d8ff", "#b2f2bb", "#ffd8a8", "#d0bfff", "#ffc9c9", "#fff3bf", "#c3fae8", "#e9ecef")
INK, MUTED, ALERT = "#1e1e1e", "#666666", "#c92a2a"
CHAR = 0.55          # average glyph width as a fraction of font size, Excalidraw's hand font
SIZE = 18
NODE_WORDS = 4       # a node label longer than this is a sentence: make it a note
NODE_LINES = 2
NODE_MAX = (300, 120)
NOTE_LINE = 36       # characters per note line before it must wrap
MIN_FONT = {800: 16, 1200: 18, 1600: 21, 2000: 24, 2400: 28}  # the view renders ~700 px wide

SIDES = {"r": (1, 0.5), "l": (0, 0.5), "t": (0.5, 0), "b": (0.5, 1),
         "tl": (0.2, 0), "tr": (0.8, 0), "bl": (0.2, 1), "br": (0.8, 1)}


def extent(t, size):
    lines = t.split("\n")
    return max(len(line) for line in lines) * size * CHAR, len(lines) * size * 1.25


def node(i, x, y, label, fill=BLUE, w=None, h=None, size=SIZE, stroke=INK, dashed=False, shape="rectangle"):
    """A thing in the system: a component, a state, a file, an actor. One to four words."""
    tw, th = extent(label, size)
    w = w or max(90, round(tw + 36))
    h = h or max(56, round(th + 26))
    e = {"type": shape, "id": i, "x": x, "y": y, "width": w, "height": h, "backgroundColor": fill,
         "fillStyle": "solid", "strokeColor": stroke, "label": {"text": label, "fontSize": size}, "_node": True}
    if shape == "rectangle":
        e["roundness"] = {"type": 3}
    if dashed:
        e["strokeStyle"] = "dashed"
    return e


def lane(i, x, y, w, h, title, fill=GREY):
    """A swimlane or zone: an actor's timeline, a process, a file. Title sits outside, top left."""
    return [{"type": "rectangle", "id": i, "x": x, "y": y, "width": w, "height": h, "backgroundColor": fill,
             "fillStyle": "solid", "strokeColor": MUTED, "strokeWidth": 1, "opacity": 30, "roundness": {"type": 3},
             "_zone": True},
            text(i + "_title", x, y - 28, title, 18, MUTED)]


def text(i, x, y, t, size=SIZE, color=INK):
    return {"type": "text", "id": i, "x": x, "y": y, "text": t, "fontSize": size, "strokeColor": color}


def wrap(t, width=NOTE_LINE):
    out = []
    for para in t.split("\n"):
        line = ""
        for word in para.split():
            if line and len(line) + 1 + len(word) > width:
                out.append(line)
                line = word
            else:
                line = f"{line} {word}".strip()
        out.append(line)
    return "\n".join(out)


def note(els, i, x, y, t, to=None, side="l", size=18, color=MUTED):
    """Narrative outside the shapes. With `to`, a thin leader line from the note to that element's `side`."""
    body = wrap(t)
    out = [text(i, x, y, body, size, color) | {"_note": True}]
    if to:
        by = {e["id"]: e for e in els if "id" in e}
        target = by[to]
        fx, fy = SIDES[side]
        tx, ty = target["x"] + target["width"] * fx, target["y"] + target["height"] * fy
        w, h = extent(body, size)
        sx = x + w if tx > x + w else x
        sy = min(max(ty, y), y + h)
        out.append({"type": "arrow", "id": i + "_lead", "x": sx, "y": sy, "width": abs(tx - sx), "height": abs(ty - sy),
                    "points": [[0, 0], [tx - sx, ty - sy]], "endArrowhead": None, "strokeColor": MUTED,
                    "strokeWidth": 1, "strokeStyle": "dotted", "endBinding": {"elementId": to, "fixedPoint": [fx, fy]},
                    "_leader": True})
    return out


def link(els, i, src, dst, s="r", d="l", verb=None, color=INK, dashed=False, size=18):
    """A relationship: data moving, control passing, time ordering, ownership. `verb` says which."""
    by = {e["id"]: e for e in els if "id" in e}
    a, b = by[src], by[dst]
    (fx, fy), (tx, ty) = SIDES[s], SIDES[d]
    x0, y0 = a["x"] + a["width"] * fx, a["y"] + a["height"] * fy
    x1, y1 = b["x"] + b["width"] * tx, b["y"] + b["height"] * ty
    e = {"type": "arrow", "id": i, "x": x0, "y": y0, "width": abs(x1 - x0), "height": abs(y1 - y0),
         "points": [[0, 0], [x1 - x0, y1 - y0]], "endArrowhead": "arrow", "strokeColor": color, "strokeWidth": 2,
         "startBinding": {"elementId": src, "fixedPoint": [fx, fy]},
         "endBinding": {"elementId": dst, "fixedPoint": [tx, ty]}}
    if verb:
        e["label"] = {"text": verb, "fontSize": size}
    if dashed:
        e["strokeStyle"] = "dashed"
    return e


def axis(i, x, y, length, label="time", vertical=False):
    """The time arrow for a timeline or sequence. Time runs left to right, or top to bottom, never both."""
    dx, dy = (0, length) if vertical else (length, 0)
    return [{"type": "arrow", "id": i, "x": x, "y": y, "width": abs(dx), "height": abs(dy), "points": [[0, 0], [dx, dy]],
             "endArrowhead": "arrow", "strokeColor": MUTED, "strokeWidth": 1, "_axis": True},
            text(i + "_label", x + dx + (8 if not vertical else -20), y + dy + (-10 if not vertical else 8), label, 18, MUTED)]


def key(i, x, y, entries, size=18):
    """The colour key: one swatch per meaning, `entries` as {fill: "what it means"}. Required once a diagram uses
    more than one fill or any colour on a stroke; the next reader never finds the colours obvious."""
    out = []
    for n, (fill, meaning) in enumerate(entries.items()):
        row = y + n * (size + 14)
        out.append({"type": "rectangle", "id": f"{i}_{n}", "x": x, "y": row, "width": 28, "height": size + 4,
                    "backgroundColor": fill, "fillStyle": "solid", "strokeColor": MUTED, "strokeWidth": 1,
                    "_key": True})
        out.append(text(f"{i}_{n}_t", x + 40, row, meaning, size, MUTED) | {"_key": True})
    return out


def claims(els):
    """Every arrow and note as a line a reader can check against the evidence, without looking at the picture."""
    by = {e["id"]: e for e in els if "id" in e}

    def name(i):
        return by[i]["label"]["text"].replace("\n", " ") if by[i].get("label") else i

    out = []
    for e in els:
        if e["type"] == "arrow" and not e.get("_leader") and not e.get("_axis"):
            verb = e.get("label", {}).get("text", "").replace("\n", " ")
            out.append(f"- {e['id']}: {name(e['startBinding']['elementId'])} -{verb}-> {name(e['endBinding']['elementId'])}")
    for e in els:
        if e.get("_note"):
            lead = by.get(e["id"] + "_lead")
            on = f" (on {name(lead['endBinding']['elementId'])})" if lead else ""
            out.append(f"- {e['id']}{on}: {' '.join(e['text'].split())}")
    return out


def _box(e):
    if e["type"] == "text":
        w, h = extent(e["text"], e["fontSize"])
        return e["x"], e["y"], w, h
    if e["type"] == "arrow":
        xs = [e["x"] + p[0] for p in e["points"]]
        ys = [e["y"] + p[1] for p in e["points"]]
        return min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys)
    return e["x"], e["y"], e["width"], e["height"]


def check(name, els):
    """Layout problems and the grammar problems that make a diagram not worth reading."""
    problems = []
    ids = [e["id"] for e in els if "id" in e]
    if len(ids) != len(set(ids)):
        problems.append("duplicate ids")
    nodes = [e for e in els if e.get("_node")]
    relations = [e for e in els if e["type"] == "arrow" and not e.get("_leader") and not e.get("_axis")]
    if not relations:
        problems.append("no arrows: a diagram with no relationships is a table or a list; write that instead")
    if len(nodes) > 14:
        problems.append(f"{len(nodes)} nodes: past about 12 the eye stops following; split it or cut it")
    for e in nodes:
        label = e["label"]["text"]
        if len(label.split()) > NODE_WORDS or label.count("\n") >= NODE_LINES:
            problems.append(f"{e['id']}: label '{label[:40]}' is a sentence; name the thing and put the rest in a note()")
        if e["width"] > NODE_MAX[0] or e["height"] > NODE_MAX[1]:
            problems.append(f"{e['id']}: {e['width']}x{e['height']} is a block, not a node")
        tw, th = extent(label, e["label"]["fontSize"])
        if tw > e["width"] - 12 or th > e["height"] - 6:
            problems.append(f"{e['id']}: label overflows its shape")
    for e in relations:
        for k in ("startBinding", "endBinding"):
            if e.get(k) and e[k]["elementId"] not in ids:
                problems.append(f"{e['id']}: {k} names a missing element")
    for e in els:
        if e.get("_note") and any(len(line) > NOTE_LINE + 12 for line in e["text"].split("\n")):
            problems.append(f"{e['id']}: note line too long; let note() wrap it")
    solid = [(e["id"], *_box(e)) for e in els if e["type"] != "arrow" and not e.get("_zone")]
    for e in relations:
        ends = {e[k]["elementId"] for k in ("startBinding", "endBinding") if e.get(k)}
        (x0, y0), (x1, y1) = e["points"][0], e["points"][-1]
        for i, x, y, w, h in solid:
            if i in ends or i.startswith(e["id"]):
                continue
            for t in range(1, 40):
                px, py = e["x"] + x0 + (x1 - x0) * t / 40, e["y"] + y0 + (y1 - y0) * t / 40
                if x + 2 < px < x + w - 2 and y + 2 < py < y + h - 2:
                    problems.append(f"arrow {e['id']} crosses {i}")
                    break
    for n, (i, x, y, w, h) in enumerate(solid):
        for j, x2, y2, w2, h2 in solid[n + 1:]:
            if x < x2 + w2 and x2 < x + w and y < y2 + h2 and y2 < y + h:
                problems.append(f"overlap {i} / {j}")
    fills = {e["backgroundColor"] for e in nodes}
    strokes = {e.get("strokeColor", INK) for e in nodes + relations} - {INK}
    if (len(fills) > 1 or strokes) and not any(e.get("_key") for e in els):
        problems.append(f"{len(fills)} fills and {len(strokes)} stroke colours with no key(); say what each colour means")
    cam = camera(els)
    floor = MIN_FONT[cam["width"]]
    sizes = [e["fontSize"] for e in els if e["type"] == "text"] + [e["label"]["fontSize"] for e in els if e.get("label")]
    if min(sizes) < floor:
        problems.append(f"camera is {cam['width']} wide, so text under {floor} px is unreadable inline; "
                        f"smallest is {min(sizes)}. Tighten the layout or raise the font")
    for p in problems:
        print(f"{name}: {p}")
    return not problems


def camera(els, pad=40):
    boxes = [_box(e) for e in els]
    x0, y0 = min(b[0] for b in boxes) - pad, min(b[1] for b in boxes) - pad
    w = max(b[0] + b[2] for b in boxes) + pad - x0
    h = max(b[1] + b[3] for b in boxes) + pad - y0
    for cw, ch in ((800, 600), (1200, 900), (1600, 1200), (2000, 1500), (2400, 1800)):
        if w <= cw and h <= ch:
            return {"type": "cameraUpdate", "width": cw, "height": ch, "x": x0, "y": y0}
    return {"type": "cameraUpdate", "width": 2400, "height": 1800, "x": x0, "y": y0}


def native(elements, name):
    """An Excalidraw scene: each `label` becomes a text element bound to its container; arrows bind their ends."""
    out, bound = [], {}
    for e in elements:
        if e["type"] == "arrow":
            for k in ("startBinding", "endBinding"):
                if e.get(k):
                    bound.setdefault(e[k]["elementId"], []).append({"type": "arrow", "id": e["id"]})
    for n, e in enumerate(elements):
        e = {k: v for k, v in e.items() if not k.startswith("_")}
        e = dict(e, seed=1000 + n, version=1, versionNonce=n, isDeleted=False, angle=0, groupIds=[], frameId=None,
                 roughness=1, opacity=e.get("opacity", 100), strokeWidth=e.get("strokeWidth", 2),
                 strokeStyle=e.get("strokeStyle", "solid"), fillStyle=e.get("fillStyle", "solid"),
                 backgroundColor=e.get("backgroundColor", "transparent"), strokeColor=e.get("strokeColor", INK),
                 locked=False, link=None, updated=1, boundElements=list(bound.get(e["id"], [])),
                 roundness=e.get("roundness"))
        label = e.pop("label", None)
        if e["type"] == "text":
            w, h = extent(e["text"], e["fontSize"])
            e.update(fontFamily=1, textAlign="left", verticalAlign="top", containerId=None, originalText=e["text"],
                     lineHeight=1.25, autoResize=True, width=w, height=h)
        if e["type"] == "arrow":
            for k in ("startBinding", "endBinding"):
                if e.get(k):
                    e[k] = dict(e[k], focus=0, gap=4)
            e.update(startArrowhead=None, lastCommittedPoint=None, elbowed=False)
            e.setdefault("startBinding", None)
            e.setdefault("endBinding", None)
            e.setdefault("endArrowhead", "arrow")
        out.append(e)
        if label:
            tid = e["id"] + "_t"
            size = label.get("fontSize", SIZE)
            tw, th = extent(label["text"], size)
            cx, cy = e["x"] + e["width"] / 2, e["y"] + e["height"] / 2
            if e["type"] == "arrow":
                (x0, y0), (x1, y1) = e["points"][0], e["points"][-1]
                cx, cy = e["x"] + (x0 + x1) / 2, e["y"] + (y0 + y1) / 2
            e["boundElements"].append({"type": "text", "id": tid})
            out.append({"type": "text", "id": tid, "x": cx - tw / 2, "y": cy - th / 2, "width": tw, "height": th,
                        "text": label["text"], "originalText": label["text"], "fontSize": size, "fontFamily": 1,
                        "textAlign": "center", "verticalAlign": "middle", "containerId": e["id"], "lineHeight": 1.25,
                        "autoResize": True, "strokeColor": INK, "backgroundColor": "transparent",
                        "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid", "roughness": 1, "opacity": 100,
                        "angle": 0, "groupIds": [], "frameId": None, "roundness": None, "seed": 5000 + n,
                        "version": 1, "versionNonce": 5000 + n, "isDeleted": False, "boundElements": [],
                        "updated": 1, "link": None, "locked": False})
    return {"type": "excalidraw", "version": 2, "source": name, "elements": out,
            "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None}, "files": {}}


def write(name, els, here=None):
    """Check, then write <name>.excalidraw, <name>.view.json and <name>.claims.md (every arrow and note as a line, for
    the verifier) beside the calling spec. Exit 1 on a problem."""
    here = Path(here or sys.argv[0]).resolve().parent
    ok = check(name, els)
    view = [camera(els)] + [{k: v for k, v in e.items() if not k.startswith("_")} for e in els]
    (here / f"{name}.excalidraw").write_text(json.dumps(native(els, name), indent=1))
    (here / f"{name}.view.json").write_text(json.dumps(view, separators=(",", ":")))
    spec = sys.modules["__main__"].__doc__ or ""
    (here / f"{name}.claims.md").write_text(f"# {name}\n\n{spec.strip()}\n\n" + "\n".join(claims(els)) + "\n")
    print(f"{name}: {sum(1 for e in els if e.get('_node'))} nodes, "
          f"{sum(1 for e in els if e['type'] == 'arrow' and not e.get('_leader') and not e.get('_axis'))} relations, "
          f"{'ok' if ok else 'PROBLEMS'}")
    if not ok:
        sys.exit(1)
