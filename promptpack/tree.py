"""
Tree visualization generator for promptpack.
"""

from pathlib import Path
from typing import List, Dict, Any


def build_tree_structure(paths: List[Path]) -> Dict[str, Any]:
    """
    Build a nested dict structure representing files and folders.
    """
    tree: Dict[str, Any] = {}
    for path in sorted(paths):
        parts = path.parts
        curr = tree
        for part in parts:
            if part not in curr:
                curr[part] = {}
            curr = curr[part]
    return tree


def render_tree(tree: Dict[str, Any], prefix: str = "") -> List[str]:
    """
    Render nested dict tree into tree visualization lines.
    """
    lines: List[str] = []
    items = sorted(tree.keys())
    count = len(items)

    for index, name in enumerate(items):
        is_last = (index == count - 1)
        connector = "└── " if is_last else "├── "
        child_prefix = "    " if is_last else "│   "

        lines.append(f"{prefix}{connector}{name}")

        subtree = tree[name]
        if subtree:
            lines.extend(render_tree(subtree, prefix + child_prefix))

    return lines


def generate_directory_tree(paths: List[Path], root_name: str = ".") -> str:
    """
    Generate ASCII directory tree string from list of relative paths.
    """
    if not paths:
        return f"{root_name}\n└── (empty or no matched files)"

    nested = build_tree_structure(paths)
    rendered_lines = render_tree(nested)
    return f"{root_name}/\n" + "\n".join(rendered_lines)
