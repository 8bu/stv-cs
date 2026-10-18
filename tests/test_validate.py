"""Behavior tests for tools/validate.py. Standard library only."""

from __future__ import annotations

import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
import unicodedata
import unittest
from pathlib import Path

TESTS = Path(__file__).resolve().parent
ROOT = TESTS.parent
FIXTURES = TESTS / "fixtures"
GLOSSARIES = FIXTURES / "glossary"
SPECS = FIXTURES / "spec"
LINTS = FIXTURES / "lint"

_spec = importlib.util.spec_from_file_location("validate", ROOT / "tools" / "validate.py")
validate = importlib.util.module_from_spec(_spec)
sys.modules["validate"] = validate
_spec.loader.exec_module(validate)

GOOD_GLOSSARY = GLOSSARIES / "good.csv"
HEADER = ",".join(validate.COLUMNS)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def codes(diagnostics, severity=None):
    return [
        (d.line, d.code)
        for d in sorted(diagnostics, key=validate.Diagnostic.sort_key)
        if severity is None or d.severity == severity
    ]


def read_bytes_text(path: Path) -> str:
    with open(path, encoding="utf-8", newline="") as handle:
        return handle.read()


def write_text(path: Path, text: str) -> None:
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)


class TempDirCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = Path(self._tmp.name)

    def copy(self, source: Path, name: str = None) -> Path:
        target = self.tmp / (name or source.name)
        shutil.copyfile(source, target)
        return target

    def glossary_from_rows(self, *rows: str) -> Path:
        path = self.tmp / "glossary.csv"
        write_text(path, "\n".join([HEADER, *rows]) + "\n")
        return path


class GlossaryTests(TempDirCase):
    def test_good_glossary_loads_in_csv_order(self):
        entries, diags = validate.load_glossary(GOOD_GLOSSARY)
        self.assertEqual(diags, [])
        self.assertEqual(
            [(e.canonical, e.part_of_speech) for e in entries],
            [
                ("endpoint", "noun"),
                ("cache", "noun"),
                ("cache", "verb"),
                ("pipe", "noun"),
                ("machine learning", "noun"),
                ("tải lên", "verb"),
            ],
        )
        self.assertEqual(entries[0].forbidden, ("điểm cuối", "đầu cuối"))

    def test_bad_glossaries_report_exact_codes_and_lines(self):
        expected = {
            "bad_header.csv": [(1, "GLOSSARY_HEADER")],
            "bad_policy.csv": [(2, "GLOSSARY_POLICY")],
            "bad_pos.csv": [(2, "GLOSSARY_POS")],
            "bad_b_first_use.csv": [(2, "GLOSSARY_FIRST_USE"), (3, "GLOSSARY_FIRST_USE")],
            "bad_missing_required.csv": [(2, "GLOSSARY_REQUIRED")],
            "bad_columns.csv": [(2, "GLOSSARY_COLUMNS")],
            "bad_duplicate.csv": [(3, "GLOSSARY_DUPLICATE")],
            "bad_forbidden.csv": [(2, "GLOSSARY_FORBIDDEN"), (2, "GLOSSARY_FORBIDDEN")],
            "bad_canonical.csv": [(2, "GLOSSARY_CANONICAL")],
            "bad_scope.csv": [(2, "GLOSSARY_SCOPE")],
        }
        for name, want in expected.items():
            with self.subTest(fixture=name):
                _, diags = validate.load_glossary(GLOSSARIES / name)
                self.assertEqual(codes(diags), want)
                self.assertTrue(all(d.severity == "error" for d in diags))

    def test_missing_file_is_reported(self):
        entries, diags = validate.load_glossary(self.tmp / "absent.csv")
        self.assertEqual(entries, [])
        self.assertEqual(codes(diags), [(1, "FILE_MISSING")])

    def test_non_utf8_file_is_reported(self):
        path = self.tmp / "glossary.csv"
        path.write_bytes(b"\xff\xfe\x00bad")
        _, diags = validate.load_glossary(path)
        self.assertEqual(codes(diags), [(1, "FILE_UNREADABLE")])

    def test_empty_file_is_reported(self):
        path = self.tmp / "glossary.csv"
        path.write_text("", encoding="utf-8")
        _, diags = validate.load_glossary(path)
        self.assertEqual(codes(diags), [(1, "GLOSSARY_HEADER")])

    def test_multiline_cell_keeps_following_row_line_numbers(self):
        path = self.tmp / "glossary.csv"
        write_text(
            path,
            HEADER + "\n"
            'endpoint,endpoint,A,noun,"Dòng một\nDòng hai",api,,,Gọi endpoint.,,\n'
            "cache,cache,A,noun,Vùng nhớ đệm,hệ thống,,,Xóa cache.,,\n"
            "cache,cache,A,noun,vùng nhớ đệm,hệ thống,,,Xóa cache nữa.,,\n",
        )
        entries, diags = validate.load_glossary(path)
        self.assertEqual(entries[0].approved_meaning, "Dòng một\nDòng hai")
        self.assertEqual([e.line for e in entries], [2, 4, 5])
        self.assertEqual(codes(diags), [(5, "GLOSSARY_DUPLICATE")])

    def test_same_spelling_with_different_meaning_is_allowed(self):
        path = self.glossary_from_rows(
            "cache,cache,A,noun,Vùng nhớ đệm,hệ thống,,,Xóa cache.,,",
            "cache,cache,A,noun,Bộ đệm phần cứng,phần cứng,,,Đọc cache CPU.,,",
        )
        _, diags = validate.load_glossary(path)
        self.assertEqual(diags, [])


class GenerationTests(TempDirCase):
    def fixture_block_body(self):
        lines = read_bytes_text(SPECS / "good_synced.md").split("\n")
        begin = lines.index(validate.BEGIN_MARKER)
        end = lines.index(validate.END_MARKER)
        return lines[begin + 1 : end]

    def test_generated_body_matches_reviewed_fixture(self):
        entries, _ = validate.load_glossary(GOOD_GLOSSARY)
        self.assertEqual(validate.generate_block_body(entries), self.fixture_block_body())

    def test_pipes_are_escaped_and_newlines_become_breaks(self):
        path = self.tmp / "glossary.csv"
        write_text(
            path,
            HEADER + "\n"
            'pipe,pipe,A,noun,"a | b\nc",shell,,,Dùng pipe.,,\n',
        )
        entries, diags = validate.load_glossary(path)
        self.assertEqual(diags, [])
        body = "\n".join(validate.generate_block_body(entries))
        self.assertIn(r"| pipe | noun | a \| b<br>c | shell |", body)

    def test_empty_groups_still_get_a_heading(self):
        path = self.glossary_from_rows("tải lên,upload,C,verb,Gửi tệp,mạng,,,Tải lên tệp.,,")
        entries, _ = validate.load_glossary(path)
        body = validate.generate_block_body(entries)
        self.assertEqual(body.count(validate.EMPTY_GROUP_TEXT), 2)
        for title in validate.GROUP_TITLES.values():
            self.assertIn(f"#### {title}", body)

    def test_rows_keep_csv_order_within_group(self):
        path = self.glossary_from_rows(
            "zeta,zeta,A,noun,Z,api,,,Dùng zeta.,,",
            "alpha,alpha,A,noun,A,api,,,Dùng alpha.,,",
        )
        entries, _ = validate.load_glossary(path)
        rows = [l for l in validate.generate_block_body(entries) if l.startswith("| zeta") or l.startswith("| alpha")]
        self.assertEqual([r.split(" | ")[0] for r in rows], ["| zeta", "| alpha"])


class SyncCheckTests(TempDirCase):
    def test_check_passes_on_fresh_spec(self):
        self.assertEqual(validate.check(GOOD_GLOSSARY, SPECS / "good_synced.md"), [])

    def test_check_flags_stale_block(self):
        diags = validate.check(GOOD_GLOSSARY, SPECS / "stale.md")
        self.assertEqual(codes(diags), [(19, "SPEC_STALE")])

    def test_check_flags_missing_markers(self):
        diags = validate.check(GOOD_GLOSSARY, SPECS / "no_markers.md")
        self.assertEqual(codes(diags), [(1, "SPEC_MARKERS"), (1, "SPEC_MARKERS")])

    def test_check_flags_duplicate_and_reversed_markers(self):
        base = read_bytes_text(SPECS / "good_synced.md")
        duplicated = self.tmp / "dup.md"
        write_text(duplicated, base + validate.BEGIN_MARKER + "\n")
        self.assertEqual(codes(validate.check(GOOD_GLOSSARY, duplicated)), [(47 + 1, "SPEC_MARKERS")])
        reversed_ = self.tmp / "rev.md"
        write_text(reversed_, f"{validate.END_MARKER}\n{validate.BEGIN_MARKER}\n")
        self.assertEqual(codes(validate.check(GOOD_GLOSSARY, reversed_)), [(1, "SPEC_MARKERS")])

    def test_check_reports_invalid_glossary_instead_of_stale_block(self):
        diags = validate.check(GLOSSARIES / "bad_policy.csv", SPECS / "good_synced.md")
        self.assertEqual(codes(diags), [(2, "GLOSSARY_POLICY")])

    def test_check_reports_missing_spec(self):
        diags = validate.check(GOOD_GLOSSARY, self.tmp / "absent.md")
        self.assertEqual(codes(diags), [(1, "FILE_MISSING")])

    def test_sync_rewrites_stale_block_to_reviewed_output(self):
        spec = self.copy(SPECS / "stale.md")
        changed, diags = validate.sync(GOOD_GLOSSARY, spec)
        self.assertTrue(changed)
        self.assertEqual(diags, [])
        self.assertEqual(read_bytes_text(spec), read_bytes_text(SPECS / "good_synced.md"))

    def test_sync_is_idempotent(self):
        spec = self.copy(SPECS / "stale.md")
        validate.sync(GOOD_GLOSSARY, spec)
        first = read_bytes_text(spec)
        changed, diags = validate.sync(GOOD_GLOSSARY, spec)
        self.assertFalse(changed)
        self.assertEqual(diags, [])
        self.assertEqual(read_bytes_text(spec), first)

    def test_sync_changes_only_the_marked_block(self):
        prefix = "Dòng đầu  \n\n```\n" + validate.BEGIN_MARKER + "\nkhông đụng\n" + validate.END_MARKER + "\n```\n\n"
        suffix = "Đuôi không xuống dòng cuối\t"
        spec = self.tmp / "spec.md"
        write_text(
            spec,
            prefix + validate.BEGIN_MARKER + "\ncũ\n" + validate.END_MARKER + "\n" + suffix,
        )
        validate.sync(GOOD_GLOSSARY, spec)
        result = read_bytes_text(spec)
        self.assertTrue(result.startswith(prefix + validate.BEGIN_MARKER + "\n"))
        self.assertTrue(result.endswith("\n" + validate.END_MARKER + "\n" + suffix))
        self.assertNotIn("cũ", result)
        self.assertIn("| endpoint | noun |", result)

    def test_sync_preserves_crlf_line_endings(self):
        good = read_bytes_text(SPECS / "good_synced.md")
        stale = read_bytes_text(SPECS / "stale.md")
        spec = self.tmp / "spec.md"
        write_text(spec, stale.replace("\n", "\r\n"))
        validate.sync(GOOD_GLOSSARY, spec)
        self.assertEqual(read_bytes_text(spec), good.replace("\n", "\r\n"))
        self.assertEqual(validate.check(GOOD_GLOSSARY, spec), [])

    def test_sync_without_markers_fails_and_leaves_file_untouched(self):
        spec = self.copy(SPECS / "no_markers.md")
        before = read_bytes_text(spec)
        changed, diags = validate.sync(GOOD_GLOSSARY, spec)
        self.assertFalse(changed)
        self.assertEqual(codes(diags), [(1, "SPEC_MARKERS"), (1, "SPEC_MARKERS")])
        self.assertEqual(read_bytes_text(spec), before)

    def test_sync_with_invalid_glossary_leaves_file_untouched(self):
        spec = self.copy(SPECS / "stale.md")
        before = read_bytes_text(spec)
        changed, diags = validate.sync(GLOSSARIES / "bad_columns.csv", spec)
        self.assertFalse(changed)
        self.assertEqual(codes(diags), [(2, "GLOSSARY_COLUMNS")])
        self.assertEqual(read_bytes_text(spec), before)

    def test_sync_still_reports_reference_errors_after_updating(self):
        spec = self.copy(SPECS / "bad_refs.md")
        changed, diags = validate.sync(GOOD_GLOSSARY, spec)
        self.assertFalse(changed)
        self.assertEqual(
            [code for _, code in codes(diags)],
            ["REF_UNRESOLVED", "REF_DUPLICATE", "REF_UNRESOLVED"],
        )


class ReferenceTests(unittest.TestCase):
    def refs(self, text):
        return [(d.line, d.code, d.message) for d in validate.check_references(text, "x.md")]

    def test_fixture_reports_unresolved_and_duplicate_but_skips_ignored_content(self):
        diags = validate.check(GOOD_GLOSSARY, SPECS / "bad_refs.md")
        self.assertEqual(
            [(d.line, d.code, d.message) for d in sorted(diags, key=validate.Diagnostic.sort_key)],
            [
                (5, "REF_UNRESOLVED", "QT 9.9 has no matching '### QT 9.9' or '#### QT 9.9' heading"),
                (7, "REF_DUPLICATE", "duplicate heading for QT 1.1 (first defined at line 3)"),
                (9, "REF_UNRESOLVED", "QT 2.3 has no matching '### QT 2.3' or '#### QT 2.3' heading"),
            ],
        )

    def test_resolved_references_pass_for_levels_three_and_four(self):
        text = "### QT 1.1 — A\n\n#### QT 1.1.1 — B\n\nXem QT 1.1 và QT 1.1.1.\n"
        self.assertEqual(self.refs(text), [])

    def test_trailing_sentence_period_is_not_part_of_the_number(self):
        self.assertEqual(self.refs("### QT 2.1 — A\n\nXem QT 2.1.\n"), [])

    def test_other_heading_levels_do_not_define_rules(self):
        diags = self.refs("## QT 3.1 — A\n\n##### QT 3.2 — B\n\nXem QT 3.1 và QT 3.2.\n")
        self.assertEqual(
            [(line, code) for line, code, _ in diags],
            [(1, "REF_UNRESOLVED"), (3, "REF_UNRESOLVED"), (5, "REF_UNRESOLVED"), (5, "REF_UNRESOLVED")],
        )

    def test_reference_inside_heading_text_is_checked(self):
        diags = self.refs("### QT 1.1 — Theo QT 4.4\n")
        self.assertEqual([(line, code) for line, code, _ in diags], [(1, "REF_UNRESOLVED")])

    def test_references_in_generated_block_are_ignored(self):
        text = f"{validate.BEGIN_MARKER}\nXem QT 9.9\n{validate.END_MARKER}\n"
        self.assertEqual(self.refs(text), [])

    def test_labeled_non_approved_quote_is_ignored_but_other_quotes_are_not(self):
        ignored = "**Ví dụ sai:**\n\n> Xem QT 9.9.\n"
        self.assertEqual(self.refs(ignored), [])
        inline_label = "> **Ví dụ sai:** Xem QT 9.9.\n"
        self.assertEqual(self.refs(inline_label), [])
        standard_label = "**Không dùng:**\n\n> Xem QT 9.9.\n"
        self.assertEqual(self.refs(standard_label), [])
        kept = "Sau:\n\n> Xem QT 9.9.\n"
        self.assertEqual([(line, code) for line, code, _ in self.refs(kept)], [(3, "REF_UNRESOLVED")])


class LintTests(TempDirCase):
    @classmethod
    def setUpClass(cls):
        cls.entries, diags = validate.load_glossary(GOOD_GLOSSARY)
        assert not diags

    def lint(self, text):
        return validate.lint_text(text, "x.md", self.entries)

    def lint_codes(self, text):
        return [(d.line, d.code) for d in sorted(self.lint(text), key=validate.Diagnostic.sort_key)]

    def test_good_fixture_has_no_diagnostics(self):
        self.assertEqual(validate.lint_files([LINTS / "good.md"], self.entries), [])

    def test_forbidden_fixture(self):
        diags = validate.lint_files([LINTS / "bad_forbidden.md"], self.entries)
        self.assertEqual(
            [d.format() for d in sorted(diags, key=validate.Diagnostic.sort_key)],
            [
                f"{rel(LINTS / 'bad_forbidden.md')}:3: error FORBIDDEN_TERM "
                "forbidden alternative 'điểm cuối'; use 'endpoint'",
                f"{rel(LINTS / 'bad_forbidden.md')}:5: error FORBIDDEN_TERM "
                "forbidden alternative 'upload'; use 'tải lên'",
            ],
        )

    def test_first_use_fixture_flags_only_the_first_occurrence(self):
        diags = validate.lint_files([LINTS / "bad_first_use.md"], self.entries)
        self.assertEqual(
            [d.format() for d in diags],
            [
                f"{rel(LINTS / 'bad_first_use.md')}:3: error FIRST_USE_B "
                "first use of 'machine learning' must be written 'machine learning (học máy)'"
            ],
        )

    def test_length_fixture_yields_warnings_only(self):
        diags = validate.lint_files([LINTS / "warnings.md"], self.entries)
        self.assertFalse(validate.has_errors(diags))
        self.assertEqual(
            [d.format() for d in sorted(diags, key=validate.Diagnostic.sort_key)],
            [
                f"{rel(LINTS / 'warnings.md')}:3: warning LONG_STEP "
                "numbered item has 21 tokens; limit is 20",
                f"{rel(LINTS / 'warnings.md')}:7: warning LONG_SENTENCE "
                "sentence has 26 tokens; limit is 25",
            ],
        )

    def test_forbidden_match_respects_word_boundaries_and_case(self):
        self.assertEqual(self.lint_codes("Đã uploaded tệp.\n"), [])
        self.assertEqual(self.lint_codes("Chạy UPLOAD ngay.\n"), [(1, "FORBIDDEN_TERM")])
        self.assertEqual(self.lint_codes("Xem điểm cuối cùng.\n"), [(1, "FORBIDDEN_TERM")])

    def test_forbidden_match_works_on_decomposed_unicode(self):
        text = unicodedata.normalize("NFD", "Gửi đến điểm cuối này.\n")
        self.assertEqual(self.lint_codes(text), [(1, "FORBIDDEN_TERM")])

    def test_forbidden_term_reported_once_per_line_and_alternative(self):
        text = "Điểm cuối và điểm cuối nữa.\n"
        self.assertEqual(self.lint_codes(text), [(1, "FORBIDDEN_TERM")])

    def test_ignored_regions_are_not_linted(self):
        text = (
            "# Tiêu đề điểm cuối\n\n"
            "Mã `điểm cuối` và `` điểm cuối ` `` bỏ qua.\n\n"
            "```\nđiểm cuối\n```\n\n"
            "~~~\nupload\n~~~\n\n"
            "Ví dụ sai:\n\n> Gọi điểm cuối.\n\n"
            "> **Không được duyệt:** gọi điểm cuối.\n\n"
            f"{validate.BEGIN_MARKER}\nđiểm cuối\n{validate.END_MARKER}\n"
        )
        self.assertEqual(self.lint_codes(text), [])

    def test_quote_after_unlabeled_line_is_linted(self):
        text = "Trước khi chạy, đọc kỹ.\n\n> Gọi điểm cuối.\n"
        self.assertEqual(self.lint_codes(text), [(3, "FORBIDDEN_TERM")])

    def test_first_use_accepts_exact_form_case_insensitively_and_with_emphasis(self):
        self.assertEqual(self.lint_codes("Machine learning (học máy) là gì.\n"), [])
        self.assertEqual(self.lint_codes("**machine learning** (học máy) là gì.\n"), [])

    def test_first_use_rejects_missing_translation_and_wrong_translation(self):
        self.assertEqual(self.lint_codes("Dùng machine learning.\n"), [(1, "FIRST_USE_B")])
        self.assertEqual(self.lint_codes("Dùng machine learning (máy học).\n"), [(1, "FIRST_USE_B")])

    def test_first_use_ignores_code_and_headings_when_locating_first_occurrence(self):
        text = "# Machine learning\n\nMã `machine learning`.\n\nDùng machine learning (học máy).\n"
        self.assertEqual(self.lint_codes(text), [])

    def test_first_use_is_not_required_when_term_is_absent(self):
        self.assertEqual(self.lint_codes("Không nhắc thuật ngữ nào.\n"), [])

    def test_first_use_is_checked_per_file(self):
        good = self.tmp / "a.md"
        bad = self.tmp / "b.md"
        write_text(good, "Dùng machine learning (học máy).\n")
        write_text(bad, "Dùng machine learning.\n")
        diags = validate.lint_files([good, bad], self.entries)
        self.assertEqual([(Path(d.path).name, d.code) for d in diags], [("b.md", "FIRST_USE_B")])

    def test_numbered_item_limit_is_twenty_tokens(self):
        twenty = " ".join(["từ"] * 20)
        self.assertEqual(self.lint_codes(f"1. {twenty}\n"), [])
        self.assertEqual(self.lint_codes(f"1. {twenty} từ\n"), [(1, "LONG_STEP")])

    def test_numbered_item_counts_continuation_lines(self):
        words = ["từ"] * 21
        text = "1. " + " ".join(words[:10]) + "\n   " + " ".join(words[10:]) + "\n"
        self.assertEqual(self.lint_codes(text), [(1, "LONG_STEP")])

    def test_numbered_item_with_parenthesis_marker_is_procedural(self):
        self.assertEqual(self.lint_codes("1) " + " ".join(["từ"] * 21) + "\n"), [(1, "LONG_STEP")])

    def test_sentence_limit_is_twenty_five_tokens(self):
        twenty_five = " ".join(["từ"] * 25)
        self.assertEqual(self.lint_codes(f"{twenty_five}.\n"), [])
        self.assertEqual(self.lint_codes(f"{twenty_five} từ.\n"), [(1, "LONG_SENTENCE")])

    def test_sentence_spanning_lines_is_reported_at_its_first_line(self):
        first = " ".join(["từ"] * 13)
        second = " ".join(["từ"] * 13)
        text = f"Câu ngắn.\n{first}\n{second}.\n"
        self.assertEqual(self.lint_codes(text), [(2, "LONG_SENTENCE")])

    def test_sentences_are_measured_separately(self):
        sentence = " ".join(["từ"] * 15)
        self.assertEqual(self.lint_codes(f"{sentence}. {sentence}.\n"), [])

    def test_bullets_and_approved_quotes_use_the_sentence_limit(self):
        long = " ".join(["từ"] * 26)
        self.assertEqual(self.lint_codes(f"- {long}\n"), [(1, "LONG_SENTENCE")])
        self.assertEqual(self.lint_codes(f"Sau:\n\n> {long}\n"), [(3, "LONG_SENTENCE")])

    def test_headings_tables_and_labeled_bad_examples_are_not_length_checked(self):
        long = " ".join(["từ"] * 40)
        self.assertEqual(self.lint_codes(f"# {long}\n"), [])
        self.assertEqual(self.lint_codes(f"| {long} | b |\n"), [])
        self.assertEqual(self.lint_codes(f"Trước:\n\n> {long}\n"), [])

    def test_inline_code_counts_as_one_token(self):
        exact = "Chạy " + " ".join(["từ"] * 23) + " `một lệnh rất dài với nhiều từ bên trong`.\n"
        self.assertEqual(self.lint_codes(exact), [])
        over = "Chạy " + " ".join(["từ"] * 24) + " `một lệnh`.\n"
        self.assertEqual(self.lint_codes(over), [(1, "LONG_SENTENCE")])

    def test_unreadable_lint_input_is_an_error(self):
        diags = validate.lint_files([self.tmp / "absent.md"], self.entries)
        self.assertEqual(codes(diags), [(1, "FILE_MISSING")])


class CliTests(TempDirCase):
    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(ROOT / "tools" / "validate.py"), *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )

    def paths(self, spec: Path, glossary: Path = GOOD_GLOSSARY):
        return ["--glossary", str(glossary), "--spec", str(spec)]

    def test_check_succeeds_silently_on_valid_inputs(self):
        result = self.run_cli("check", *self.paths(SPECS / "good_synced.md"))
        self.assertEqual((result.returncode, result.stdout), (0, ""))
        self.assertIn("check: ok", result.stderr)

    def test_check_fails_with_stable_diagnostic_on_stale_block(self):
        result = self.run_cli("check", *self.paths(SPECS / "stale.md"))
        self.assertEqual(result.returncode, 1)
        self.assertEqual(
            result.stdout.splitlines(),
            [
                f"{rel(SPECS / 'stale.md')}:19: error SPEC_STALE generated glossary block "
                "is out of date; run 'python3 tools/validate.py sync'"
            ],
        )

    def test_check_reports_every_reference_error_in_sorted_order(self):
        result = self.run_cli("check", *self.paths(SPECS / "bad_refs.md"))
        self.assertEqual(result.returncode, 1)
        self.assertEqual(
            [line.split(" ")[0:3] for line in result.stdout.splitlines()],
            [
                [f"{rel(SPECS / 'bad_refs.md')}:5:", "error", "REF_UNRESOLVED"],
                [f"{rel(SPECS / 'bad_refs.md')}:7:", "error", "REF_DUPLICATE"],
                [f"{rel(SPECS / 'bad_refs.md')}:9:", "error", "REF_UNRESOLVED"],
            ],
        )

    def test_check_reports_missing_file_with_exit_one(self):
        result = self.run_cli("check", *self.paths(self.tmp / "absent.md"))
        self.assertEqual(result.returncode, 1)
        self.assertIn("error FILE_MISSING file not found", result.stdout)

    def test_sync_then_check_round_trip(self):
        spec = self.copy(SPECS / "stale.md")
        synced = self.run_cli("sync", *self.paths(spec))
        self.assertEqual((synced.returncode, synced.stdout), (0, ""))
        self.assertIn("updated", synced.stderr)
        self.assertEqual(read_bytes_text(spec), read_bytes_text(SPECS / "good_synced.md"))
        again = self.run_cli("sync", *self.paths(spec))
        self.assertEqual(again.returncode, 0)
        self.assertIn("already up to date", again.stderr)
        self.assertEqual(self.run_cli("check", *self.paths(spec)).returncode, 0)

    def test_sync_with_invalid_glossary_fails_without_writing(self):
        spec = self.copy(SPECS / "stale.md")
        before = read_bytes_text(spec)
        result = self.run_cli("sync", *self.paths(spec, GLOSSARIES / "bad_policy.csv"))
        self.assertEqual(result.returncode, 1)
        self.assertIn(":2: error GLOSSARY_POLICY", result.stdout)
        self.assertEqual(read_bytes_text(spec), before)

    def test_lint_exits_nonzero_on_errors(self):
        result = self.run_cli(
            "lint", "--glossary", str(GOOD_GLOSSARY), str(LINTS / "bad_forbidden.md")
        )
        self.assertEqual(result.returncode, 1)
        self.assertEqual(
            result.stdout.splitlines()[0],
            f"{rel(LINTS / 'bad_forbidden.md')}:3: error FORBIDDEN_TERM "
            "forbidden alternative 'điểm cuối'; use 'endpoint'",
        )

    def test_lint_warnings_do_not_fail(self):
        result = self.run_cli(
            "lint", "--glossary", str(GOOD_GLOSSARY), str(LINTS / "warnings.md")
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(len(result.stdout.splitlines()), 2)
        self.assertIn("warning LONG_STEP", result.stdout)

    def test_lint_accepts_several_files_and_sorts_by_path(self):
        result = self.run_cli(
            "lint",
            "--glossary",
            str(GOOD_GLOSSARY),
            str(LINTS / "bad_first_use.md"),
            str(LINTS / "bad_forbidden.md"),
            str(LINTS / "good.md"),
        )
        self.assertEqual(result.returncode, 1)
        paths = [line.split(":")[0] for line in result.stdout.splitlines()]
        self.assertEqual(paths, sorted(paths))
        self.assertEqual(len(paths), 3)

    def test_lint_with_invalid_glossary_reports_glossary_errors_only(self):
        result = self.run_cli(
            "lint", "--glossary", str(GLOSSARIES / "bad_pos.csv"), str(LINTS / "bad_forbidden.md")
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("GLOSSARY_POS", result.stdout)
        self.assertNotIn("FORBIDDEN_TERM", result.stdout)

    def test_usage_errors_exit_two(self):
        self.assertEqual(self.run_cli().returncode, 2)
        self.assertEqual(self.run_cli("lint").returncode, 2)
        self.assertEqual(self.run_cli("unknown").returncode, 2)


if __name__ == "__main__":
    unittest.main()
