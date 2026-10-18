#!/usr/bin/env python3
"""Validator for the TVKTĐGH/KHMT specification and its controlled glossary.

Commands
    check            validate the glossary, the generated dictionary block and
                     the QT rule references of the spec
    sync             regenerate only the marked dictionary block, then check
    lint FILE...     lint Markdown/text files against the glossary

Diagnostics are printed to stdout as ``path:line: severity code message``,
sorted by path, line, code and message. A one-line summary goes to stderr.
Exit status: 0 = no errors (warnings allowed), 1 = at least one error,
2 = command-line usage error.

Only the Python 3 standard library is used. Glossary text and linted text are
normalised to Unicode NFC before comparison so that composed and decomposed
Vietnamese diacritics match.
"""

from __future__ import annotations

import argparse
import csv
import io
import re
import sys
import unicodedata
from bisect import bisect_right
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_GLOSSARY = ROOT / "glossary" / "glossary.csv"
DEFAULT_SPEC = ROOT / "spec" / "TVKTDGH-KHMT.md"

BEGIN_MARKER = "<!-- BEGIN GENERATED GLOSSARY -->"
END_MARKER = "<!-- END GENERATED GLOSSARY -->"

COLUMNS = (
    "canonical",
    "english_equivalent",
    "language_policy",
    "part_of_speech",
    "approved_meaning",
    "scope",
    "first_use_form",
    "forbidden_alternatives",
    "approved_example",
    "non_approved_example",
    "note",
)
REQUIRED_COLUMNS = (
    "canonical",
    "language_policy",
    "part_of_speech",
    "approved_meaning",
    "scope",
    "approved_example",
)
POLICIES = ("A", "B", "C")
PARTS_OF_SPEECH = (
    "noun",
    "verb",
    "adjective",
    "adverb",
    "conjunction",
    "preposition",
    "abbreviation",
)
MAX_SCOPE_LENGTH = 40

TABLE_HEADERS = (
    "Dạng chuẩn",
    "Từ loại",
    "Nghĩa được duyệt",
    "Phạm vi",
    "Dạng lần đầu",
    "Không dùng",
    "Ví dụ đúng",
    "Ví dụ sai",
)
GROUP_TITLES = {
    "A": "Chính sách A — Giữ nguyên tiếng Anh",
    "B": "Chính sách B — Tiếng Anh kèm giải thích tiếng Việt ở lần đầu",
    "C": "Chính sách C — Dùng tiếng Việt",
}
GENERATED_NOTICE = (
    "<!-- Sinh tự động từ glossary CSV bằng `python3 tools/validate.py sync`. "
    "Không sửa tay. -->"
)
EMPTY_GROUP_TEXT = "Không có mục nào."

MAX_STEP_TOKENS = 20
MAX_SENTENCE_TOKENS = 25

ERROR = "error"
WARNING = "warning"

# Labels that mark the following/own blockquote as a non-approved example.
NON_APPROVED_LABELS = (
    "trước",
    "không dùng",
    "ví dụ sai",
    "ví dụ không được duyệt",
    "không được duyệt",
    "không đạt",
    "non-approved example",
    "non-approved",
    "bad example",
)

CODE_PLACEHOLDER = "\ue000"

FENCE_OPEN_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
HEADING_RE = re.compile(r"^ {0,3}#{1,6}(?:\s|$)")
QUOTE_RE = re.compile(r"^ {0,3}(?:>[ \t]?)+")
INLINE_CODE_RE = re.compile(r"(?<!`)(`+)(?!`)(.+?)(?<!`)\1(?!`)")
LINK_RE = re.compile(r"!?\[([^\]]*)\]\([^)]*\)")
LIST_RE = re.compile(r"^\s*([-*+]|\d{1,9}[.)])\s+(.*)$")
TABLE_RE = re.compile(r"^\s*\|")
COMMENT_RE = re.compile(r"^\s*<!--.*-->\s*$")
SENTENCE_BREAK_RE = re.compile(r"(?<=[.!?…])\s+")
FIRST_USE_RE = re.compile(r"^[^()]+ \([^()]+\)$")
QT_HEADING_RE = re.compile(r"^ {0,3}#{3,4}\s+QT\s+(\d+(?:\.\d+)+)")
QT_REF_RE = re.compile(r"\bQT\s+(\d+(?:\.\d+)+)")
_LABEL_RE = re.compile(
    r"^(?:" + "|".join(re.escape(label) for label in NON_APPROVED_LABELS) + r")"
    r"\s*(?:\([^)]*\))?\s*(?:[:：].*)?$"
)
_LIST_MARKER_RE = re.compile(r"^\s*(?:[-*+]|\d{1,9}[.)])\s+")


# --------------------------------------------------------------------------
# Diagnostics and file access
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class Diagnostic:
    path: str
    line: int
    severity: str
    code: str
    message: str

    def format(self) -> str:
        return f"{self.path}:{self.line}: {self.severity} {self.code} {self.message}"

    def sort_key(self) -> Tuple[str, int, str, str, str]:
        return (self.path, self.line, self.code, self.message, self.severity)


def has_errors(diagnostics: Iterable[Diagnostic]) -> bool:
    return any(d.severity == ERROR for d in diagnostics)


def show(path: Path) -> str:
    """Display form of a path: repo-relative when inside the repo, else as given."""
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except (ValueError, OSError):
        return path.as_posix()


def read_text(
    path: Path, encoding: str = "utf-8"
) -> Tuple[Optional[str], List[Diagnostic]]:
    shown = show(path)
    try:
        with open(path, encoding=encoding, newline="") as handle:
            return handle.read(), []
    except FileNotFoundError:
        return None, [Diagnostic(shown, 1, ERROR, "FILE_MISSING", "file not found")]
    except UnicodeDecodeError:
        return None, [
            Diagnostic(shown, 1, ERROR, "FILE_UNREADABLE", "file is not valid UTF-8")
        ]
    except OSError as exc:
        reason = exc.strerror or type(exc).__name__
        return None, [
            Diagnostic(shown, 1, ERROR, "FILE_UNREADABLE", f"cannot read file: {reason}")
        ]


# --------------------------------------------------------------------------
# Glossary
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class Entry:
    canonical: str
    english_equivalent: str
    language_policy: str
    part_of_speech: str
    approved_meaning: str
    scope: str
    first_use_form: str
    forbidden_alternatives: str
    approved_example: str
    non_approved_example: str
    note: str
    line: int

    @property
    def forbidden(self) -> Tuple[str, ...]:
        if not self.forbidden_alternatives:
            return ()
        return tuple(part.strip() for part in self.forbidden_alternatives.split("|"))


def _check_entry(entry: Entry, shown: str) -> List[Diagnostic]:
    diags: List[Diagnostic] = []

    def err(code: str, message: str) -> None:
        diags.append(Diagnostic(shown, entry.line, ERROR, code, message))

    for column in REQUIRED_COLUMNS:
        if not getattr(entry, column):
            err("GLOSSARY_REQUIRED", f"missing required value for '{column}'")

    if entry.language_policy and entry.language_policy not in POLICIES:
        err(
            "GLOSSARY_POLICY",
            f"language_policy '{entry.language_policy}' must be one of "
            + ", ".join(POLICIES),
        )
    if entry.part_of_speech and entry.part_of_speech not in PARTS_OF_SPEECH:
        err(
            "GLOSSARY_POS",
            f"part_of_speech '{entry.part_of_speech}' must be one of "
            + ", ".join(PARTS_OF_SPEECH),
        )
    if entry.scope:
        if entry.scope != entry.scope.lower() or len(entry.scope) > MAX_SCOPE_LENGTH:
            err(
                "GLOSSARY_SCOPE",
                f"scope '{entry.scope}' must be a short lowercase label "
                f"(at most {MAX_SCOPE_LENGTH} characters)",
            )
    if (
        entry.canonical
        and entry.language_policy in ("A", "B")
        and not entry.canonical.isascii()
    ):
        err(
            "GLOSSARY_CANONICAL",
            f"canonical '{entry.canonical}' must be an English (ASCII) form "
            f"for policy {entry.language_policy}",
        )
    if entry.language_policy == "B" and entry.canonical:
        form = entry.first_use_form
        if not form:
            err(
                "GLOSSARY_FIRST_USE",
                "policy B requires first_use_form written 'English (Vietnamese)'",
            )
        elif not FIRST_USE_RE.match(form):
            err(
                "GLOSSARY_FIRST_USE",
                f"first_use_form '{form}' must be written 'English (Vietnamese)'",
            )
        elif not form.lower().startswith(entry.canonical.lower() + " ("):
            err(
                "GLOSSARY_FIRST_USE",
                f"first_use_form '{form}' must start with canonical "
                f"'{entry.canonical}' followed by ' ('",
            )

    if entry.forbidden_alternatives:
        seen = set()
        for alt in entry.forbidden:
            if not alt:
                err("GLOSSARY_FORBIDDEN", "empty alternative in forbidden_alternatives")
                continue
            if alt.casefold() in seen:
                err("GLOSSARY_FORBIDDEN", f"duplicate forbidden alternative '{alt}'")
            seen.add(alt.casefold())
    return diags


def load_glossary(path: Path) -> Tuple[List[Entry], List[Diagnostic]]:
    """Parse and validate the glossary. Row order is preserved."""
    shown = show(path)
    text, diags = read_text(path, encoding="utf-8-sig")
    if text is None:
        return [], diags
    text = unicodedata.normalize("NFC", text)

    reader = csv.reader(io.StringIO(text, newline=""), strict=True)
    rows: List[Tuple[int, List[str]]] = []
    previous_line = 0
    try:
        for row in reader:
            start = previous_line + 1
            previous_line = reader.line_num
            if row:
                rows.append((start, row))
    except csv.Error as exc:
        return [], [
            Diagnostic(shown, max(reader.line_num, 1), ERROR, "GLOSSARY_CSV", f"invalid CSV: {exc}")
        ]

    if not rows:
        return [], [Diagnostic(shown, 1, ERROR, "GLOSSARY_HEADER", "glossary is empty")]
    header_line, header = rows[0]
    if tuple(cell.strip() for cell in header) != COLUMNS:
        return [], [
            Diagnostic(
                shown,
                header_line,
                ERROR,
                "GLOSSARY_HEADER",
                "header must be exactly: " + ",".join(COLUMNS),
            )
        ]

    entries: List[Entry] = []
    for line, row in rows[1:]:
        if len(row) != len(COLUMNS):
            diags.append(
                Diagnostic(
                    shown,
                    line,
                    ERROR,
                    "GLOSSARY_COLUMNS",
                    f"expected {len(COLUMNS)} columns, found {len(row)}",
                )
            )
            continue
        values = [cell.strip() for cell in row]
        entry = Entry(*values, line=line)
        diags.extend(_check_entry(entry, shown))
        entries.append(entry)

    first_seen: Dict[Tuple[str, str, str], int] = {}
    for entry in entries:
        key = (
            entry.canonical.casefold(),
            entry.part_of_speech,
            entry.approved_meaning.casefold(),
        )
        if key in first_seen:
            diags.append(
                Diagnostic(
                    shown,
                    entry.line,
                    ERROR,
                    "GLOSSARY_DUPLICATE",
                    f"duplicate of line {first_seen[key]} "
                    "(same canonical, part_of_speech and approved_meaning)",
                )
            )
        else:
            first_seen[key] = entry.line

    canonicals = {entry.canonical.casefold() for entry in entries if entry.canonical}
    for entry in entries:
        for alt in entry.forbidden:
            if alt and alt.casefold() in canonicals:
                diags.append(
                    Diagnostic(
                        shown,
                        entry.line,
                        ERROR,
                        "GLOSSARY_FORBIDDEN",
                        f"forbidden alternative '{alt}' is also an approved canonical form",
                    )
                )
    return entries, diags


# --------------------------------------------------------------------------
# Generated dictionary block
# --------------------------------------------------------------------------


def _cell(value: str) -> str:
    return re.sub(r"\r\n|\r|\n", "<br>", value).replace("|", r"\|")


def _row(cells: Sequence[str]) -> str:
    return "| " + " | ".join(cells) + " |"


def generate_block_body(entries: Sequence[Entry]) -> List[str]:
    """Lines between the markers (exclusive), without line terminators."""
    lines = [GENERATED_NOTICE, ""]
    for policy in POLICIES:
        group = [entry for entry in entries if entry.language_policy == policy]
        lines.append(f"#### {GROUP_TITLES[policy]}")
        lines.append("")
        if not group:
            lines.append(EMPTY_GROUP_TEXT)
        else:
            lines.append(_row(TABLE_HEADERS))
            lines.append(_row(["---"] * len(TABLE_HEADERS)))
            for entry in group:
                lines.append(
                    _row(
                        _cell(value)
                        for value in (
                            entry.canonical,
                            entry.part_of_speech,
                            entry.approved_meaning,
                            entry.scope,
                            entry.first_use_form,
                            ", ".join(entry.forbidden),
                            entry.approved_example,
                            entry.non_approved_example,
                        )
                    )
                )
        lines.append("")
    return lines


def classify_lines(lines: Sequence[str]) -> List[str]:
    """Label each line: text, code (fenced), generated, begin, or end."""
    kinds: List[str] = []
    fence: Optional[Tuple[str, int]] = None
    in_generated = False
    for raw in lines:
        line = raw.rstrip("\r")
        if fence is None:
            if line == BEGIN_MARKER:
                kinds.append("begin")
                in_generated = True
                continue
            if line == END_MARKER:
                kinds.append("end")
                in_generated = False
                continue
            if in_generated:
                kinds.append("generated")
                continue
            match = FENCE_OPEN_RE.match(line)
            if match and not (match.group(1)[0] == "`" and "`" in line[match.end():]):
                fence = (match.group(1)[0], len(match.group(1)))
                kinds.append("code")
                continue
            kinds.append("text")
        else:
            kinds.append("code")
            stripped = line.strip()
            if stripped and set(stripped) == {fence[0]} and len(stripped) >= fence[1]:
                fence = None
    return kinds


def locate_block(
    lines: Sequence[str], shown: str
) -> Tuple[Optional[Tuple[int, int]], List[Diagnostic]]:
    """Zero-based indexes of the BEGIN and END marker lines."""
    kinds = classify_lines(lines)
    begins = [i for i, kind in enumerate(kinds) if kind == "begin"]
    ends = [i for i, kind in enumerate(kinds) if kind == "end"]
    diags: List[Diagnostic] = []
    for label, marker, found in (("BEGIN", BEGIN_MARKER, begins), ("END", END_MARKER, ends)):
        if not found:
            diags.append(
                Diagnostic(shown, 1, ERROR, "SPEC_MARKERS", f"missing marker line '{marker}'")
            )
        elif len(found) > 1:
            diags.append(
                Diagnostic(
                    shown,
                    found[1] + 1,
                    ERROR,
                    "SPEC_MARKERS",
                    f"duplicate {label} marker (first at line {found[0] + 1})",
                )
            )
    if not diags and ends[0] < begins[0]:
        diags.append(
            Diagnostic(
                shown, ends[0] + 1, ERROR, "SPEC_MARKERS", "END marker precedes BEGIN marker"
            )
        )
    if diags:
        return None, diags
    return (begins[0], ends[0]), []


def _strip_cr(line: str) -> str:
    return line[:-1] if line.endswith("\r") else line


def check_generated_block(
    spec_text: str, entries: Sequence[Entry], shown: str
) -> List[Diagnostic]:
    lines = spec_text.split("\n")
    located, diags = locate_block(lines, shown)
    if located is None:
        return diags
    begin, end = located
    current = [_strip_cr(line) for line in lines[begin + 1 : end]]
    if current != generate_block_body(entries):
        return [
            Diagnostic(
                shown,
                begin + 1,
                ERROR,
                "SPEC_STALE",
                "generated glossary block is out of date; run "
                "'python3 tools/validate.py sync'",
            )
        ]
    return []


# --------------------------------------------------------------------------
# Markdown scanning shared by reference checks and lint
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class Line:
    no: int
    text: str
    heading: bool
    quote: bool


def _is_non_approved_label(text: str) -> bool:
    text = _LIST_MARKER_RE.sub("", text.strip())
    text = text.replace("*", "").replace("_", "").strip().lower()
    return bool(text) and _LABEL_RE.match(text) is not None


def scan_lines(text: str) -> List[Line]:
    """Return one Line per source line; ignored content becomes a blank line.

    Ignored: fenced code, the generated glossary block (markers included) and
    blockquotes labeled as non-approved examples. Inline code spans are replaced
    by a single placeholder character.
    """
    raw_lines = text.split("\n")
    kinds = classify_lines(raw_lines)
    out: List[Line] = []
    in_quote = False
    skip_quote = False
    previous = ""
    for number, (raw, kind) in enumerate(zip(raw_lines, kinds), start=1):
        line = raw.rstrip("\r")
        if kind != "text":
            out.append(Line(number, "", False, False))
            in_quote = skip_quote = False
            previous = ""
            continue
        match = QUOTE_RE.match(line)
        if match:
            body = line[match.end():]
            if not in_quote:
                in_quote = True
                skip_quote = _is_non_approved_label(body) or _is_non_approved_label(previous)
                previous = ""
            if skip_quote:
                out.append(Line(number, "", False, True))
                continue
            out.append(
                Line(
                    number,
                    INLINE_CODE_RE.sub(CODE_PLACEHOLDER, body),
                    bool(HEADING_RE.match(body)),
                    True,
                )
            )
            continue
        in_quote = skip_quote = False
        if line.strip():
            previous = line
        out.append(
            Line(
                number,
                INLINE_CODE_RE.sub(CODE_PLACEHOLDER, line),
                bool(HEADING_RE.match(line)),
                False,
            )
        )
    return out


def _clean_inline(text: str) -> str:
    return LINK_RE.sub(r"\1", text).replace("*", "").strip()


@dataclass
class Block:
    kind: str  # para, bullet, numbered, table
    quote: bool
    parts: List[Tuple[int, str]]

    def joined(self) -> Tuple[str, List[int]]:
        starts: List[int] = []
        position = 0
        for _, part in self.parts:
            starts.append(position)
            position += len(part) + 1
        return " ".join(part for _, part in self.parts), starts

    def line_at(self, starts: Sequence[int], offset: int) -> int:
        return self.parts[max(bisect_right(starts, offset) - 1, 0)][0]


def build_blocks(lines: Sequence[Line]) -> List[Block]:
    blocks: List[Block] = []
    current: Optional[Block] = None

    def flush() -> None:
        nonlocal current
        if current is not None and any(part for _, part in current.parts):
            current.parts = [(n, p) for n, p in current.parts if p]
            blocks.append(current)
        current = None

    for line in lines:
        text = line.text
        if line.heading or not text.strip() or COMMENT_RE.match(text):
            flush()
            continue
        if TABLE_RE.match(text):
            flush()
            current = Block("table", line.quote, [(line.no, _clean_inline(text))])
            flush()
            continue
        item = LIST_RE.match(text)
        if item:
            flush()
            kind = "numbered" if item.group(1)[0].isdigit() else "bullet"
            current = Block(kind, line.quote, [(line.no, _clean_inline(item.group(2)))])
            continue
        if current is not None and current.quote == line.quote:
            current.parts.append((line.no, _clean_inline(text)))
        else:
            flush()
            current = Block("para", line.quote, [(line.no, _clean_inline(text))])
    flush()
    return blocks


# --------------------------------------------------------------------------
# Rule-reference integrity
# --------------------------------------------------------------------------


def check_references(spec_text: str, shown: str) -> List[Diagnostic]:
    definitions: Dict[str, int] = {}
    references: List[Tuple[int, str]] = []
    diags: List[Diagnostic] = []
    for line in scan_lines(spec_text):
        text = line.text
        if line.heading:
            match = QT_HEADING_RE.match(text)
            if match:
                number = match.group(1)
                if number in definitions:
                    diags.append(
                        Diagnostic(
                            shown,
                            line.no,
                            ERROR,
                            "REF_DUPLICATE",
                            f"duplicate heading for QT {number} "
                            f"(first defined at line {definitions[number]})",
                        )
                    )
                else:
                    definitions[number] = line.no
                text = text[match.end():]
        for match in QT_REF_RE.finditer(text):
            references.append((line.no, match.group(1)))
    for number_line, number in references:
        if number not in definitions:
            diags.append(
                Diagnostic(
                    shown,
                    number_line,
                    ERROR,
                    "REF_UNRESOLVED",
                    f"QT {number} has no matching '### QT {number}' or "
                    f"'#### QT {number}' heading",
                )
            )
    return diags


# --------------------------------------------------------------------------
# check / sync
# --------------------------------------------------------------------------


def check(glossary_path: Path, spec_path: Path) -> List[Diagnostic]:
    entries, diags = load_glossary(glossary_path)
    spec_text, spec_diags = read_text(spec_path)
    diags = diags + spec_diags
    if spec_text is None:
        return diags
    shown = show(spec_path)
    spec_text = unicodedata.normalize("NFC", spec_text)
    if not has_errors(diags):
        diags += check_generated_block(spec_text, entries, shown)
    diags += check_references(spec_text, shown)
    return diags


def sync(glossary_path: Path, spec_path: Path) -> Tuple[bool, List[Diagnostic]]:
    """Rewrite only the marked block. Returns (changed, diagnostics)."""
    entries, diags = load_glossary(glossary_path)
    if has_errors(diags):
        return False, diags
    spec_text, diags = read_text(spec_path)
    if spec_text is None:
        return False, diags
    lines = spec_text.split("\n")
    located, diags = locate_block(lines, show(spec_path))
    if located is None:
        return False, diags
    begin, end = located
    terminator = "\r" if lines[begin].endswith("\r") else ""
    body = [line + terminator for line in generate_block_body(entries)]
    new_lines = lines[: begin + 1] + body + lines[end:]
    changed = new_lines != lines
    if changed:
        with open(spec_path, "w", encoding="utf-8", newline="") as handle:
            handle.write("\n".join(new_lines))
    return changed, check(glossary_path, spec_path)


# --------------------------------------------------------------------------
# lint
# --------------------------------------------------------------------------


def _term_regex(term: str) -> "re.Pattern[str]":
    return re.compile(r"(?<!\w)" + re.escape(term) + r"(?!\w)", re.IGNORECASE)


def _sentence_spans(text: str) -> List[Tuple[int, int]]:
    spans: List[Tuple[int, int]] = []
    start = 0
    for match in SENTENCE_BREAK_RE.finditer(text):
        spans.append((start, match.start()))
        start = match.end()
    spans.append((start, len(text)))
    return [(s, e) for s, e in spans if text[s:e].strip()]


def lint_text(text: str, shown: str, entries: Sequence[Entry]) -> List[Diagnostic]:
    text = unicodedata.normalize("NFC", text)
    blocks = build_blocks(scan_lines(text))
    diags: List[Diagnostic] = []

    forbidden: Dict[str, Tuple[str, List[str]]] = {}
    for entry in entries:
        for alt in entry.forbidden:
            if not alt:
                continue
            _, canonicals = forbidden.setdefault(alt.casefold(), (alt, []))
            if entry.canonical not in canonicals:
                canonicals.append(entry.canonical)
    forbidden_regexes = [
        (_term_regex(alt), alt, canonicals) for alt, canonicals in forbidden.values()
    ]

    first_use: Dict[str, Tuple[str, List[str]]] = {}
    for entry in entries:
        if entry.language_policy == "B" and entry.first_use_form:
            _, forms = first_use.setdefault(entry.canonical.casefold(), (entry.canonical, []))
            if entry.first_use_form not in forms:
                forms.append(entry.first_use_form)
    first_use_regexes = {
        key: (_term_regex(canonical), canonical, forms)
        for key, (canonical, forms) in first_use.items()
    }
    pending_first_use = set(first_use_regexes)

    reported = set()
    for block in blocks:
        joined, starts = block.joined()

        for regex, alt, canonicals in forbidden_regexes:
            for match in regex.finditer(joined):
                line = block.line_at(starts, match.start())
                if (line, alt.casefold()) in reported:
                    continue
                reported.add((line, alt.casefold()))
                preferred = " / ".join(f"'{c}'" for c in canonicals)
                diags.append(
                    Diagnostic(
                        shown,
                        line,
                        ERROR,
                        "FORBIDDEN_TERM",
                        f"forbidden alternative '{alt}'; use {preferred}",
                    )
                )

        for key in sorted(pending_first_use):
            regex, canonical, forms = first_use_regexes[key]
            match = regex.search(joined)
            if match is None:
                continue
            pending_first_use.discard(key)
            lowered = joined.lower()
            if not any(lowered.startswith(form.lower(), match.start()) for form in forms):
                diags.append(
                    Diagnostic(
                        shown,
                        block.line_at(starts, match.start()),
                        ERROR,
                        "FIRST_USE_B",
                        f"first use of '{canonical}' must be written '{forms[0]}'",
                    )
                )

        if block.kind == "numbered":
            count = len(joined.split())
            if count > MAX_STEP_TOKENS:
                diags.append(
                    Diagnostic(
                        shown,
                        block.parts[0][0],
                        WARNING,
                        "LONG_STEP",
                        f"numbered item has {count} tokens; limit is {MAX_STEP_TOKENS}",
                    )
                )
        elif block.kind in ("para", "bullet"):
            for start, end in _sentence_spans(joined):
                count = len(joined[start:end].split())
                if count > MAX_SENTENCE_TOKENS:
                    diags.append(
                        Diagnostic(
                            shown,
                            block.line_at(starts, start),
                            WARNING,
                            "LONG_SENTENCE",
                            f"sentence has {count} tokens; limit is {MAX_SENTENCE_TOKENS}",
                        )
                    )
    return diags


def lint_files(paths: Sequence[Path], entries: Sequence[Entry]) -> List[Diagnostic]:
    diags: List[Diagnostic] = []
    for path in paths:
        text, read_diags = read_text(path)
        if text is None:
            diags += read_diags
        else:
            diags += lint_text(text, show(path), entries)
    return diags


# --------------------------------------------------------------------------
# Command line
# --------------------------------------------------------------------------


def _emit(diagnostics: Iterable[Diagnostic]) -> List[Diagnostic]:
    ordered = sorted(set(diagnostics), key=Diagnostic.sort_key)
    for diagnostic in ordered:
        print(diagnostic.format())
    return ordered


def _summary(command: str, diagnostics: Sequence[Diagnostic]) -> int:
    errors = sum(1 for d in diagnostics if d.severity == ERROR)
    warnings = len(diagnostics) - errors
    if errors:
        print(f"{command}: {errors} error(s), {warnings} warning(s)", file=sys.stderr)
        return 1
    print(f"{command}: ok ({warnings} warning(s))", file=sys.stderr)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="validate.py",
        description="Validate the TVKTĐGH/KHMT glossary, spec and Markdown files.",
    )
    commands = parser.add_subparsers(dest="command", required=True, metavar="command")
    for name, summary in (
        ("check", "validate glossary, generated block freshness and QT references"),
        ("sync", "regenerate the generated glossary block, then run check"),
    ):
        sub = commands.add_parser(name, help=summary, description=summary)
        sub.add_argument("--glossary", type=Path, default=DEFAULT_GLOSSARY, help="glossary CSV path")
        sub.add_argument("--spec", type=Path, default=DEFAULT_SPEC, help="spec Markdown path")
    lint = commands.add_parser(
        "lint", help="lint Markdown/text files", description="Lint UTF-8 Markdown/text files."
    )
    lint.add_argument("--glossary", type=Path, default=DEFAULT_GLOSSARY, help="glossary CSV path")
    lint.add_argument("files", nargs="+", type=Path, metavar="FILE")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8")
    args = build_parser().parse_args(argv)

    if args.command == "check":
        diagnostics = _emit(check(args.glossary, args.spec))
    elif args.command == "sync":
        changed, found = sync(args.glossary, args.spec)
        diagnostics = _emit(found)
        if not has_errors(diagnostics):
            state = "updated" if changed else "already up to date"
            print(f"sync: {show(args.spec)} {state}", file=sys.stderr)
    else:
        entries, glossary_diags = load_glossary(args.glossary)
        if has_errors(glossary_diags):
            diagnostics = _emit(glossary_diags)
        else:
            diagnostics = _emit(lint_files(args.files, entries))
    return _summary(args.command, diagnostics)


if __name__ == "__main__":
    sys.exit(main())
