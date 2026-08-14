#!/usr/bin/env python3
"""Sync the course site from the LaTeX syllabus.

The syllabus is the authoritative document. This script pulls it, compiles it,
and regenerates the two things on the site that are derived from it:

  assets/syllabus.pdf   the compiled syllabus, linked from the site
  _data/schedule.yml    the schedule table, parsed from the Lecture Schedule
                        tabular in main.tex

Run it whenever the syllabus changes, then commit and push. The push is the
deploy: .github/workflows/pages.yml rebuilds the site on every push to main.

    bin/sync-syllabus.py                     # pull, build, regenerate
    bin/sync-syllabus.py --check             # report drift, write nothing
    bin/sync-syllabus.py --no-pull --no-pdf  # schedule only, from the local tex

LaTeX is compiled in a scratch directory so the Overleaf-backed clone never
picks up aux files, which would otherwise get pushed back to Overleaf.
"""

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEFAULT_SYLLABUS = REPO.parent / "syllabus"

MONTHS = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
    "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12,
}
YEAR = "26"

# Initials in the syllabus table, spelled out for the web.
LEADS = {
    "CH": "Heckman",
    "MZ": "Zhao",
    "Both": "Heckman &amp; Zhao",
}

WEEKDAYS = {"M": "Monday", "T": "Tuesday", "W": "Wednesday",
            "Th": "Thursday", "F": "Friday"}

HEADER = """\
# The course schedule. Each entry becomes one row of the table on /schedule/.
#
# GENERATED FILE. Do not edit by hand: bin/sync-syllabus.py regenerates it from
# the Lecture Schedule table in the syllabus (../syllabus/main.tex, Overleaf).
# To change the schedule, change the syllabus and re-run the script.
#
# Fields (all optional except `date` and `topic`):
#   date       - shown in the first column, e.g. "8/25/26"
#   topic      - lecture topic
#   lead       - who is leading the lecture
#   assignment - string; also accepts Markdown link syntax
"""


def read_tex(path):
    """Read main.tex. The document declares latin1, so fall back to it."""
    raw = path.read_bytes()
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("latin-1")


def find_schedule_table(tex):
    """Return the body rows of the Lecture Schedule tabular."""
    anchor = tex.find("Lecture Schedule")
    if anchor == -1:
        sys.exit("error: no 'Lecture Schedule' heading in the syllabus")
    body = re.search(
        r"\\begin\{tabular\}.*?\\midrule(?P<rows>.*?)\\bottomrule",
        tex[anchor:],
        re.DOTALL,
    )
    if not body:
        sys.exit("error: found the heading but not the tabular below it")
    return body.group("rows")


def detex(cell):
    """Turn one LaTeX table cell into the HTML the Jekyll template expects."""
    cell = cell.strip()
    cell = re.sub(r"\\(?:text|emph)(?:it|bf)?\{(.*?)\}", r"\1", cell)
    cell = cell.replace(r"\&", "&amp;")
    cell = cell.replace(r"\%", "%")
    cell = cell.replace("~", " ")
    cell = re.sub(r"\\\\$", "", cell)
    return cell.strip()


def parse_date(cell):
    """'Aug 20' -> ('8/20/26', None). 'Dec 9 (W)' -> ('12/9/26', 'Wednesday')."""
    weekday = None
    marker = re.search(r"\((\w+)\)\s*$", cell)
    if marker:
        weekday = WEEKDAYS.get(marker.group(1))
        cell = cell[: marker.start()].strip()
    m = re.match(r"([A-Z][a-z]{2})\s+(\d{1,2})$", cell)
    if not m:
        return None, None
    month, day = m.groups()
    if month not in MONTHS:
        return None, None
    return f"{MONTHS[month]}/{int(day)}/{YEAR}", weekday


def parse_entry(date_cell, topic_cell, lead_cell):
    """Build one schedule entry, or None if this half of the row is empty."""
    date_cell = date_cell.strip()
    if not date_cell:
        return None

    date, weekday = parse_date(detex(date_cell))
    if date is None:
        raise ValueError(f"unreadable date {date_cell.strip()!r}")

    # A non-class day (reading day, break) is italicised in the syllabus.
    no_class = bool(re.search(r"\\(?:textit|emph)\{", topic_cell))
    topic = detex(topic_cell)

    # "Model Evaluation (A2 out)" carries the assignment in the topic cell.
    assignment = None
    released = re.search(r"\s*\((A\d+ out)\)\s*$", topic)
    if released:
        assignment = released.group(1)
        topic = topic[: released.start()].strip()

    if weekday:
        topic = f"{topic} ({weekday})"
    if no_class:
        topic = f"{topic} &mdash; no class"

    lead = LEADS.get(detex(lead_cell).strip())

    entry = {"date": date, "topic": topic}
    if lead:
        entry["lead"] = lead
    if assignment:
        entry["assignment"] = assignment
    return entry


def parse_schedule(tex):
    """Walk the tabular in reading order: Tuesday column, then Thursday.

    A row this function cannot read is fatal. Skipping it would drop a lecture
    from the published schedule while the script still reported success, which
    is a worse failure than not building at all.
    """
    entries, problems = [], []
    for line in find_schedule_table(tex).split(r"\\"):
        line = line.strip()
        if not line or line.startswith("%"):
            continue
        # Split on column separators only: `\&` is a literal ampersand.
        cells = re.split(r"(?<!\\)&", line)
        if len(cells) != 6:
            problems.append(f"{len(cells)} columns, expected 6: {line[:70]}")
            continue
        for half in (cells[0:3], cells[3:6]):
            try:
                entry = parse_entry(*half)
            except ValueError as exc:
                problems.append(f"{exc}: {line[:70]}")
                continue
            if entry:
                entries.append(entry)

    if problems:
        sys.exit("error: the Lecture Schedule table did not parse\n"
                 + "\n".join(f"  - {p}" for p in problems)
                 + "\nnothing written; fix the syllabus table or the parser")
    return entries


def render(entries):
    out = [HEADER.rstrip("\n")]
    for entry in entries:
        out.append("")
        for key in ("date", "topic", "lead", "assignment"):
            if key in entry:
                prefix = "- " if key == "date" else "  "
                out.append(f'{prefix}{key}: "{entry[key]}"')
    return "\n".join(out) + "\n"


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args],
                          capture_output=True, text=True)


def build_pdf(syllabus, dest):
    """Compile main.tex in a scratch dir, so the Overleaf clone stays clean."""
    with tempfile.TemporaryDirectory() as scratch:
        result = subprocess.run(
            ["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error",
             f"-outdir={scratch}", "main.tex"],
            cwd=str(syllabus), capture_output=True, text=True,
        )
        built = Path(scratch) / "main.pdf"
        if result.returncode != 0 or not built.exists():
            sys.stderr.write(result.stdout[-2000:])
            sys.exit("error: latexmk failed to build the syllabus")
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(built, dest)
    return dest


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--syllabus-repo", type=Path, default=DEFAULT_SYLLABUS,
                    help="path to the Overleaf-backed syllabus clone")
    ap.add_argument("--no-pull", action="store_true", help="skip git pull")
    ap.add_argument("--no-pdf", action="store_true", help="skip the LaTeX build")
    ap.add_argument("--check", action="store_true",
                    help="report drift and exit nonzero; write nothing")
    args = ap.parse_args()

    syllabus = args.syllabus_repo.expanduser().resolve()
    tex_path = syllabus / "main.tex"
    if not tex_path.exists():
        sys.exit(f"error: no main.tex under {syllabus}")

    if not args.no_pull and not args.check:
        pull = git(syllabus, "pull", "--ff-only")
        if pull.returncode != 0:
            sys.exit(f"error: git pull failed\n{pull.stderr}")
        print(f"syllabus: {pull.stdout.strip().splitlines()[0]}")

    entries = parse_schedule(read_tex(tex_path))
    if not entries:
        sys.exit("error: parsed zero schedule entries; refusing to write")
    rendered = render(entries)

    schedule = REPO / "_data" / "schedule.yml"
    current = schedule.read_text() if schedule.exists() else ""

    if args.check:
        if current == rendered:
            print(f"schedule.yml: up to date ({len(entries)} entries)")
            return 0
        print(f"schedule.yml: DRIFT, {len(entries)} entries in the syllabus")
        return 1

    if current == rendered:
        print(f"schedule.yml: unchanged ({len(entries)} entries)")
    else:
        schedule.write_text(rendered)
        print(f"schedule.yml: rewrote {len(entries)} entries")

    if not args.no_pdf:
        pdf = build_pdf(syllabus, REPO / "assets" / "syllabus.pdf")
        print(f"syllabus.pdf: {pdf.stat().st_size // 1024} KB")

    return 0


if __name__ == "__main__":
    sys.exit(main())
