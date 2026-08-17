"""
Unit test suite for promptpack CLI, scanner, tree generator, and token estimator.
"""

import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from promptpack.scanner import CodebaseScanner
from promptpack.tree import generate_directory_tree
from promptpack.token_counter import estimate_tokens, get_token_warning
from promptpack.formatter import format_prompt, get_language_for_file
from promptpack.cli import main


class TestPromptPack(unittest.TestCase):

    def test_token_counter(self):
        sample_text = "a" * 400
        tokens = estimate_tokens(sample_text)
        self.assertEqual(tokens, 100)
        is_warn, msg = get_token_warning(150000, threshold=100000)
        self.assertTrue(is_warn)
        self.assertIn("Warning", msg)

    def test_language_detection(self):
        self.assertEqual(get_language_for_file(Path("main.py")), "python")
        self.assertEqual(get_language_for_file(Path("index.ts")), "typescript")
        self.assertEqual(get_language_for_file(Path("Dockerfile")), "dockerfile")

    def test_tree_generation(self):
        paths = [
            Path("src/index.js"),
            Path("src/utils.js"),
            Path("README.md"),
        ]
        tree_str = generate_directory_tree(paths, root_name="my_project")
        self.assertIn("my_project/", tree_str)
        self.assertIn("README.md", tree_str)
        self.assertIn("src", tree_str)

    def test_scanner_and_cli_output(self):
        with TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            
            # Create sample folder structure
            (tmp_path / "src").mkdir()
            (tmp_path / "node_modules").mkdir()
            (tmp_path / ".git").mkdir()

            (tmp_path / "src" / "main.py").write_text("print('hello world')", encoding="utf-8")
            (tmp_path / "README.md").write_text("# Test Repo", encoding="utf-8")
            (tmp_path / "node_modules" / "junk.js").write_text("console.log('junk')", encoding="utf-8")
            (tmp_path / "image.png").write_bytes(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR")

            scanner = CodebaseScanner(root_dir=str(tmp_path))
            file_contents, included_paths = scanner.scan()

            # Verify ignored directories and binary files
            self.assertIn(Path("src/main.py"), file_contents)
            self.assertIn(Path("README.md"), file_contents)
            self.assertNotIn(Path("node_modules/junk.js"), file_contents)
            self.assertNotIn(Path("image.png"), file_contents)

            # Test CLI output file creation
            out_file = tmp_path / "prompt_out.md"
            exit_code = main([str(tmp_path), "--output", str(out_file)])
            self.assertEqual(exit_code, 0)
            self.assertTrue(out_file.exists())

            content = out_file.read_text(encoding="utf-8")
            self.assertIn("## Project Directory Tree", content)
            self.assertIn("print('hello world')", content)


if __name__ == "__main__":
    unittest.main()
