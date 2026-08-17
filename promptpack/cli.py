"""
CLI entry point for promptpack.
"""

import sys
import argparse
from pathlib import Path
from typing import Optional

from promptpack import __version__
from promptpack.scanner import CodebaseScanner
from promptpack.formatter import format_prompt
from promptpack.token_counter import estimate_tokens, get_token_warning


def copy_to_clipboard(text: str) -> bool:
    """
    Attempt to copy text to system clipboard via pyperclip.
    """
    try:
        import pyperclip
        pyperclip.copy(text)
        return True
    except Exception as e:
        print(f"❌ Clipboard Error: Could not access clipboard ({e}).", file=sys.stderr)
        return False


def main(args_list: Optional[list] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="promptpack",
        description="Convert any codebase directory into a clean, LLM-ready prompt formatted for Claude & ChatGPT.",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to target directory (default: current directory '.')",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Output file path (e.g. prompt.md). If not specified, prints to stdout.",
    )
    parser.add_argument(
        "-c",
        "--clip",
        action="store_true",
        help="Copy output directly to clipboard via pyperclip.",
    )
    parser.add_argument(
        "-i",
        "--ignore",
        nargs="+",
        help="Additional folders, files, or glob patterns to ignore.",
    )
    parser.add_argument(
        "--max-size-kb",
        type=int,
        default=500,
        help="Maximum individual file size in KB to include (default: 500 KB).",
    )
    parser.add_argument(
        "--no-tree",
        action="store_true",
        help="Skip generating the project directory tree header.",
    )
    parser.add_argument(
        "--include-hidden",
        action="store_true",
        help="Include hidden files and dot-directories.",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    args = parser.parse_args(args_list)

    target_dir = Path(args.path).resolve()
    if not target_dir.exists():
        print(f"❌ Error: Target path '{args.path}' does not exist.", file=sys.stderr)
        return 1

    if not target_dir.is_dir():
        print(f"❌ Error: Target path '{args.path}' is not a directory.", file=sys.stderr)
        return 1

    print(f"📦 Scanning codebase at: {target_dir} ...", file=sys.stderr)

    scanner = CodebaseScanner(
        root_dir=str(target_dir),
        custom_ignores=args.ignore,
        max_file_size_kb=args.max_size_kb,
        include_hidden=args.include_hidden,
    )

    file_contents, included_paths = scanner.scan()

    if not file_contents:
        print("⚠️ Warning: No matching text files found in the specified directory.", file=sys.stderr)
        return 0

    formatted_text = format_prompt(
        file_contents=file_contents,
        included_paths=included_paths,
        root_name=target_dir.name,
        include_tree=not args.no_tree,
    )

    # Token estimation & stats
    tokens = estimate_tokens(formatted_text)
    is_warn, warn_msg = get_token_warning(tokens)

    print(f"✨ Packed {len(file_contents)} files successfully!", file=sys.stderr)
    print(f"📊 {warn_msg}", file=sys.stderr)

    # Handle output destination
    if args.clip:
        if copy_to_clipboard(formatted_text):
            print("📋 Output successfully copied to system clipboard!", file=sys.stderr)

    if args.output:
        output_file = Path(args.output).resolve()
        try:
            output_file.write_text(formatted_text, encoding="utf-8")
            print(f"💾 Output saved to: {output_file}", file=sys.stderr)
        except OSError as e:
            print(f"❌ Error saving to file: {e}", file=sys.stderr)
            return 1

    if not args.output and not args.clip:
        print(formatted_text)

    return 0


if __name__ == "__main__":
    sys.exit(main())
