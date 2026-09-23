"""Validate real repository sources and isolated negative fixtures; no network."""
import contextlib
import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import check
from check_docs import load_json, validate_documents

ROOT = Path(__file__).resolve().parent.parent
HUB_SPEC = "docs/hub/AI-Tycoon-Hub-UI佈局與RWD行為規範.md"
HUB_GUIDE = "docs/hub/README.md"
HUB_HTML = "docs/hub/AI-Tycoon-Hub.html"


class DocumentChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repo"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns(
            ".git", "__pycache__", ".venv", "node_modules"))

    def append(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as stream:
            stream.write("\n" + text + "\n")

    def registry(self, mutate):
        path = self.root / "docs/index.json"
        data = load_json(path)
        mutate(data["documents"])
        path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    def errors(self):
        errors, _ = validate_documents(self.root, check.BANNED_TERMS, check.VAGUE_TERMS)
        return errors

    def assert_error(self, code):
        errors = self.errors()
        self.assertTrue(any(e.startswith(code + ":") for e in errors), errors)

    def run_full_check(self):
        output = io.StringIO()
        with mock.patch.multiple(check, ROOT=self.root, TOKENS=self.root / "tokens",
                                 SPEC=self.root / "SPEC.md", CHANGELOG=self.root / "CHANGELOG.md"):
            with contextlib.redirect_stdout(output):
                result = check.main()
        return result, output.getvalue()

    def test_repository_passes(self):
        self.assertEqual(self.errors(), [])
        self.assertEqual(self.run_full_check()[0], 0)

    def test_nested_broken_link(self):
        self.append(HUB_GUIDE, "[missing](missing.md)")
        self.assert_error("DOC005")

    def test_broken_heading_anchor(self):
        self.append(HUB_GUIDE, "[missing](README.md#not-a-heading)")
        self.assert_error("DOC005")

    def test_utf8_relative_link_and_anchor(self):
        self.append("README.md", "[來源](docs/hub/README.md#來源與角色)")
        self.assertEqual(self.errors(), [])

    def test_missing_registered_document(self):
        (self.root / HUB_SPEC).unlink()
        self.assert_error("DOC002")

    def test_new_document_requires_registration(self):
        self.append("docs/new/deep.md", "# New file")
        self.assert_error("DOC004")

    def test_duplicate_registry_path(self):
        self.registry(lambda docs: docs.append(dict(docs[0])))
        self.assert_error("DOC003")

    def test_duplicate_normative_scope(self):
        self.append("docs/hub/second.md", "# Second specification")
        self.registry(lambda docs: docs.append({"path": "docs/hub/second.md", "role": "normative", "scope": "hub"}))
        self.assert_error("DOC003")

    def test_unknown_role(self):
        self.registry(lambda docs: docs[0].update(role="approved-product"))
        self.assert_error("DOC003")

    def test_html_cannot_become_normative(self):
        self.registry(lambda docs: next(d for d in docs if d["path"] == HUB_HTML).update(role="normative"))
        self.assert_error("DOC003")

    def test_reference_source_must_be_normative(self):
        self.registry(lambda docs: next(d for d in docs if d["path"] == HUB_HTML).update(source="README.md"))
        self.assert_error("DOC006")

    def test_reference_source_must_share_scope(self):
        self.registry(lambda docs: next(d for d in docs if d["path"] == HUB_HTML).update(source="SPEC.md"))
        self.assert_error("DOC006")

    def test_changed_reference_hash(self):
        self.append(HUB_HTML, "<!-- Changed without a source record. -->")
        self.assert_error("DOC006")

    def test_recursive_wording(self):
        self.append(HUB_GUIDE, "屏幕")
        self.assert_error("DOC007")

    def test_page_normative_vague_terms(self):
        self.append(HUB_SPEC, "建議新增控制項。")
        self.assert_error("DOC007")

    def test_examples_are_not_rules(self):
        self.append(HUB_SPEC, "```md\n屏幕 建議 [missing](missing.md)\n```\n`屏幕` 是引用。")
        self.assertEqual(self.errors(), [])

    def test_reference_links(self):
        self.append(HUB_GUIDE, "[共用規範][base]\n\n[base]: ../../SPEC.md")
        self.assertEqual(self.errors(), [])

    def test_missing_reference_definition(self):
        self.append(HUB_GUIDE, "[Missing][not-defined]")
        self.assert_error("DOC005")

    def test_external_urls_are_not_fetched(self):
        self.append(HUB_GUIDE, "[External](https://example.invalid/unreachable)")
        self.assertEqual(self.errors(), [])

    def test_registry_path_cannot_escape(self):
        self.registry(lambda docs: docs[0].update(path="../README.md"))
        self.assert_error("DOC002")

    def test_relative_link_cannot_escape(self):
        self.append("README.md", "[outside](../outside.md)")
        self.assert_error("DOC005")

    def test_claude_import_must_resolve(self):
        (self.root / "CLAUDE.md").write_text("@MISSING.md\n", encoding="utf-8")
        self.assert_error("DOC008")

    def test_duplicate_json_keys_rejected(self):
        path = self.root / "docs/index.json"
        path.write_text('{"schemaVersion": 1, "schemaVersion": 2, "documents": []}')
        self.assert_error("DOC001")

    def test_duplicate_token_keys_rejected(self):
        path = self.root / "tokens/layer.json"
        path.write_text('{"id": "layer", "id": "other"}')
        with self.assertRaisesRegex(ValueError, "重複 JSON 鍵"):
            load_json(path)

    def test_contrast_regression_still_fails(self):
        path = self.root / "tokens/color.json"
        data = load_json(path)
        data["primitive"]["neutral"]["900"] = "#FFFFFF"
        path.write_text(json.dumps(data))
        result, output = self.run_full_check()
        self.assertEqual(result, 1)
        self.assertIn("對比不足", output)

    def test_cyclic_token_reference_still_fails(self):
        with self.assertRaisesRegex(ValueError, "循環引用"):
            check.resolve({"test": {"a": "{test.b}", "b": "{test.a}"}}, "{test.a}")

    def test_repeated_check_does_not_reuse_errors(self):
        check.errors.append("a previous failed run")
        self.assertEqual(self.run_full_check()[0], 0)
        self.assertEqual(self.run_full_check()[0], 0)

    def test_malformed_token_file_exits_cleanly(self):
        (self.root / "tokens/layout.json").write_text("{broken")
        result = subprocess.run([sys.executable, str(self.root / "scripts/check.py")],
                                capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 1)
        self.assertIn("無法完成檢查", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
