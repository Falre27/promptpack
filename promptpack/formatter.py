"""
Markdown prompt formatter for promptpack.
"""

from pathlib import Path
from typing import Dict, List
from promptpack.tree import generate_directory_tree
from promptpack.token_counter import estimate_tokens

EXTENSION_TO_LANG: Dict[str, str] = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "jsx",
    ".ts": "typescript",
    ".tsx": "tsx",
    ".json": "json",
    ".html": "html",
    ".css": "css",
    ".scss": "scss",
    ".sass": "sass",
    ".less": "less",
    ".md": "markdown",
    ".pyi": "python",
    ".c": "c",
    ".cpp": "cpp",
    ".h": "cpp",
    ".hpp": "cpp",
    ".cs": "csharp",
    ".java": "java",
    ".kt": "kotlin",
    ".rs": "rust",
    ".go": "go",
    ".rb": "ruby",
    ".php": "php",
    ".sh": "bash",
    ".bash": "bash",
    ".zsh": "bash",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".toml": "toml",
    ".xml": "xml",
    ".sql": "sql",
    ".dockerfile": "dockerfile",
    ".swift": "swift",
    ".r": "r",
    ".vue": "vue",
    ".svelte": "svelte",
}


def get_language_for_file(path: Path) -> str:
    """
    Determine Markdown code block language identifier from filename or extension.
    """
    name_lower = path.name.lower()
    if name_lower == "dockerfile":
        return "dockerfile"
    if name_lower == "makefile":
        return "makefile"

    ext = path.suffix.lower()
    return EXTENSION_TO_LANG.get(ext, "")


def format_prompt(
    file_contents: Dict[Path, str],
    included_paths: List[Path],
    root_name: str = ".",
    include_tree: bool = True,
) -> str:
    """
    Format project tree and files into a clean LLM context prompt string.
    """
    output_parts: List[str] = []

    # Header / Context notice
    output_parts.append("# Codebase Prompt Pack")
    output_parts.append("This document contains the project structure and context for the codebase.\n")

    # Directory Tree
    if include_tree:
        output_parts.append("## Project Directory Tree")
        output_parts.append("```")
        output_parts.append(generate_directory_tree(included_paths, root_name=root_name))
        output_parts.append("```\n")

    # File Contents
    output_parts.append("## File Contents\n")

    sorted_files = sorted(file_contents.keys())
    for rel_path in sorted_files:
        content = file_contents[rel_path]
        lang = get_language_for_file(rel_path)

        output_parts.append(f"### `{rel_path}`")
        output_parts.append(f"```{lang}")
        output_parts.append(content)
        output_parts.append("```\n")

    return "\n".join(output_parts)
