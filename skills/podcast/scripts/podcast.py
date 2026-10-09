#!/usr/bin/env python3
"""Check and inspect a two-host podcast script before it is rendered.

  podcast.py lint <script.md>      format, source tags, words the hosts may not use; exit 1 on a problem
  podcast.py claims <script.md>    every line with its source tag, numbered, for the verifier
  podcast.py speech <script.md>    the spoken text only, tags stripped (what the listener hears)
  podcast.py stats <script.md>     words, estimated minutes, lines per chapter

Script format: references/script-format.md.
"""
import json
import re
import sys

LINE = re.compile(r"^(A|B): (.+?)\s*\{src: ([^}]*)\}((?:\s*\{\w+\})*)\s*$")
# Pace markers after the source tag. render.py turns them into gap and speed; the even rhythm of one fixed gap
# after every line is what makes an episode sound relentless.
MARKS = {"beat", "think", "slow", "quick"}
RELENTLESS_WORDS = 225   # about ninety seconds at 150 a minute with nothing changing pace; radio says change every minute
THINKING = r"\b(hm+|hang on)\b"
CHAPTER = re.compile(r"^## (.+)$")
WORDS_PER_MINUTE = 150

# Words the audit of nine NotebookLM episodes found the hosts reaching for when the sources did not say it.
BANNED = [
    (r"\bcryptographic", "no hash in these systems is cryptographic unless a source says so"),
    (r"\bbulletproof|\bimmune\b|\bguarantee[sd]?\b", "state the residual instead"),
    (r"\byou (engineered|designed|chose|decided|built|ran)\b", "attribute with the source's owner words"),
    (r"\bthe (engineers|team)\b", "name the actor: the bot, the human, the reviewer"),
    (r"\bobviously\b|\bof course\b", "nothing is obvious to the listener"),
]
NUM = r"\b\d[\d,.]*\b|\b(hundred|thousand|million|billion|percent)\b|\b(twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety)(-\w+)?\b"
NUMBERS_PER_1000_WORDS = 5   # about one every two to three minutes: numbers are rationed, stories are not
SPOKEN = r"(zero|one|two|three|four|five|six|seven|eight|nine|ten|\w+teen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|\d+)"
# A replay preamble teaches a mental model; ids, versions and type names belong in the guide's text.
TRIVIA = [
    (rf"\bdecisions? {SPOKEN}\b", "decision ids belong in the guide and the debrief, not in audio"),
    (rf"\bsessions? {SPOKEN}\b", "session numbers are trivia to a listener"),
    (rf"\bversions? {SPOKEN}\b|\blayout {SPOKEN}\b", "version numbers are trivia to a listener"),
]
EAR = [
    (r"\b[A-Z][a-z]+[A-Z]\w*\b|\b[a-z]+_[a-z_]+\b", "type and function names are trivia; say what the thing does"),
    (r"\bv\d{1,3}\b", "say 'session 19', not 'v19'"),
    (r"\b[0-9a-f]{7,40}\b", "hex does not survive speech; name the commit by role or date"),
    (r"`", "backticks are read literally or dropped; write the spoken form"),
    (r"\w: [ui]\d+\b", "'name: type' is read as 'name dot type'"),
]


def parse(path):
    text = open(path).read()
    meta = {}
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                v = v.strip()
                meta[k.strip()] = json.loads(v) if v.startswith("{") else v
        text = text[m.end():]
    offset = m.group(0).count("\n") if m else 0
    chapters, problems = [], []
    for n, raw in enumerate(text.splitlines(), offset + 1):
        line = raw.rstrip()
        if not line or line.startswith("<!--"):
            continue
        c = CHAPTER.match(line)
        if c:
            chapters.append({"title": c.group(1), "lines": []})
            continue
        m = LINE.match(line)
        if not m:
            problems.append((n, "not 'A: text {src: ...}' or '## Chapter'"))
            continue
        if not chapters:
            problems.append((n, "line before the first chapter"))
            continue
        marks = re.findall(r"\{(\w+)\}", m.group(4))
        for mark in marks:
            if mark not in MARKS:
                problems.append((n, f"unknown marker {{{mark}}}; one of {', '.join(sorted(MARKS))}"))
        chapters[-1]["lines"].append({"n": n, "speaker": m.group(1), "text": m.group(2), "src": m.group(3).strip(),
                                      "marks": set(marks)})
    return meta, chapters, problems


def pace(chapters):
    """The rhythm problems: a long stretch with no change of pace, pauses stacked into drama, the analogy said once."""
    problems = []
    for ch in chapters:
        lines = ch["lines"]
        run = 0
        for ln in lines:
            run += len(ln["text"].split())
            if ln["marks"] & {"beat", "think", "slow"}:
                run = 0
            elif run > RELENTLESS_WORDS:
                problems.append((ln["n"], f"{run} words since the last beat, think or slow; something has to change "
                                          f"about once a minute or the listener drifts and cannot get back in"))
                run = 0
        for a, b in zip(lines, lines[1:]):
            if "beat" in a["marks"] and "beat" in b["marks"]:
                problems.append((b["n"], "two beats in a row is drama, not pace"))
        thinks = [ln for ln in lines if "think" in ln["marks"]]
        if len(thinks) > 1:
            problems.append((thinks[1]["n"], "one {think} question to the listener per chapter"))
        for ln in thinks:
            if ln["speaker"] != "B" or not ln["text"].rstrip().endswith("?"):
                problems.append((ln["n"], "{think} goes on B's question to the listener, and the line ends in '?'"))
        hangs = [ln for ln in lines if re.search(THINKING, ln["text"], re.I)]
        if len(hangs) > 1:
            problems.append((hangs[1]["n"], "one 'hm' or 'hang on' per chapter; more is a tic"))
    with_analogy = [i for i, ch in enumerate(chapters) if any("analogy" in ln["src"] for ln in ch["lines"])]
    if chapters and (len(with_analogy) < 3 or with_analogy[-1] != len(chapters) - 1):
        problems.append((0, "the picture is said three times: built, restated mid-story with what it has gained, "
                            "and closed in the last chapter. Tag each pass 'analogy'"))
    return problems


def lint(path):
    meta, chapters, problems = parse(path)
    for key in ("title", "commit", "sources"):
        if key not in meta:
            problems.append((0, f"front matter has no {key}"))
    for ch in chapters:
        for ln in ch["lines"]:
            if not ln["src"]:
                problems.append((ln["n"], "empty src; use 'src: -' only for a line with no claim"))
            rules = [(p, w, re.I) for p, w in BANNED + TRIVIA] + [(p, w, 0) for p, w in EAR]
            for pat, why, flags in rules:
                hit = re.search(pat, ln["text"], flags)
                if hit:
                    problems.append((ln["n"], f"{why}: {hit.group(0)!r}"))
    problems += pace(chapters)
    words = sum(len(ln["text"].split()) for ch in chapters for ln in ch["lines"])
    numbers = sum(len(re.findall(NUM, ln["text"], re.I)) for ch in chapters for ln in ch["lines"])
    if words and numbers * 1000 / words > NUMBERS_PER_1000_WORDS:
        problems.append((0, f"{numbers} numbers in {words} words; keep the ones that change intuition "
                            f"(budget {NUMBERS_PER_1000_WORDS} per 1000 words)"))
    for n, p in problems:
        print(f"{path}:{n}: {p}")
    print(f"{sum(len(c['lines']) for c in chapters)} lines, {len(chapters)} chapters, {len(problems)} problems")
    return 1 if problems else 0


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    cmd, path = argv
    if cmd == "lint":
        return lint(path)
    meta, chapters, _ = parse(path)
    if cmd == "claims":
        for ch in chapters:
            print(f"## {ch['title']}")
            for ln in ch["lines"]:
                print(f"L{ln['n']} {ln['speaker']}: {ln['text']}  [src: {ln['src']}]")
    elif cmd == "speech":
        for ch in chapters:
            print(f"\n## {ch['title']}")
            for ln in ch["lines"]:
                print(f"{ln['speaker']}: {ln['text']}")
    elif cmd == "stats":
        total = 0
        for ch in chapters:
            words = sum(len(ln["text"].split()) for ln in ch["lines"])
            total += words
            print(f"{words / WORDS_PER_MINUTE:5.1f} min  {len(ch['lines']):3d} lines  {ch['title']}")
        print(f"{total} words, about {total / WORDS_PER_MINUTE:.0f} min")
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
