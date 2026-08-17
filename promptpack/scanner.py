"""
Directory scanner and file filter module for promptpack.
"""

import os
from pathlib import Path
from typing import List, Set, Optional, Tuple, Dict

try:
    import pathspec
    HAS_PATHSPEC = True
except ImportError:
    HAS_PATHSPEC = False

DEFAULT_IGNORED_DIRS: Set[str] = {
    ".git",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    "env",
    ".env",
    ".pytest_cache",
    ".mypy_cache",
    ".tox",
    ".idea",
    ".vscode",
    "build",
    "dist",
    "target",
    "bin",
    "obj",
    "coverage",
    ".next",
    ".nuxt",
    ".output",
}

DEFAULT_IGNORED_EXTENSIONS: Set[str] = {
    # Images & Media
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg", ".webp", ".bmp", ".tiff",
    ".mp3", ".mp4", ".wav", ".avi", ".mov", ".flv", ".webm", ".m4a",
    # Documents & Archives
    ".pdf", ".zip", ".tar", ".gz", ".7z", ".rar", ".bz2", ".xz", ".iso",
    # Binaries & Compiled
    ".exe", ".dll", ".so", ".dylib", ".bin", ".o", ".a", ".pyc", ".pyo", ".pyd",
    ".db", ".sqlite", ".sqlite3", ".class", ".jar",
    # Fonts
    ".woff", ".woff2", ".ttf", ".eot", ".otf",
}

DEFAULT_IGNORED_FILES: Set[str] = {
    ".DS_Store",
    "Thumbs.db",
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "poetry.lock",
    "Pipfile.lock",
    "Cargo.lock",
}


def is_binary_file(file_path: Path, sample_size: int = 1024) -> bool:
    """
    Check if a file is binary by inspecting sample bytes for null chars.
    """
    if file_path.suffix.lower() in DEFAULT_IGNORED_EXTENSIONS:
        return True
    try:
        with open(file_path, "rb") as f:
            chunk = f.read(sample_size)
            if b"\x00" in chunk:
                return True
    except OSError:
        return True
    return False


def load_gitignore_spec(root_dir: Path) -> Optional[object]:
    """
    Load .gitignore patterns using pathspec if installed.
    """
    if not HAS_PATHSPEC:
        return None

    patterns: List[str] = []
    gitignore_path = root_dir / ".gitignore"
    if gitignore_path.exists():
        try:
            with open(gitignore_path, "r", encoding="utf-8", errors="ignore") as f:
                patterns = f.readlines()
        except OSError:
            pass

    if patterns:
        return pathspec.PathSpec.from_lines("gitwildmatch", patterns)
    return None


class CodebaseScanner:
    """
    Scans project directory and collects list of text files respecting ignores.
    """

    def __init__(
        self,
        root_dir: str,
        custom_ignores: Optional[List[str]] = None,
        max_file_size_kb: int = 500,
        include_hidden: bool = False,
    ):
        self.root_dir = Path(root_dir).resolve()
        self.max_file_size_bytes = max_file_size_kb * 1024
        self.include_hidden = include_hidden
        self.custom_ignores = set(custom_ignores or [])
        self.gitignore_spec = load_gitignore_spec(self.root_dir)

    def is_ignored(self, path: Path) -> bool:
        """
        Check if path should be ignored based on defaults, .gitignore, and custom flags.
        """
        rel_path = path.relative_to(self.root_dir)
        rel_str = str(rel_path)

        # Check directory / filename parts
        for part in path.parts:
            if part in DEFAULT_IGNORED_DIRS and not self.include_hidden:
                return True
            if part in self.custom_ignores:
                return True
            if part.startswith(".") and not self.include_hidden and part not in {".", ".."}:
                if path.is_dir() and part in DEFAULT_IGNORED_DIRS:
                    return True

        if path.is_file():
            if path.name in DEFAULT_IGNORED_FILES:
                return True
            if path.name in self.custom_ignores:
                return True
            if path.suffix.lower() in DEFAULT_IGNORED_EXTENSIONS:
                return True

        # Check gitignore spec
        if self.gitignore_spec:
            # Check rel_str and rel_str + '/' for directories
            match_str = f"{rel_str}/" if path.is_dir() else rel_str
            if self.gitignore_spec.match_file(match_str):
                return True

        return False

    def scan(self) -> Tuple[Dict[Path, str], List[Path]]:
        """
        Scan directory recursively and return:
        - dictionary mapping relative Path -> file text content
        - list of all included paths (files and directories) for tree generation
        """
        file_contents: Dict[Path, str] = {}
        all_included_paths: List[Path] = []

        for root, dirs, files in os.walk(self.root_dir, topdown=True):
            current_root = Path(root)

            # Filter subdirectories in-place
            dirs[:] = [
                d for d in dirs
                if not self.is_ignored(current_root / d)
            ]

            rel_root = current_root.relative_to(self.root_dir)
            if rel_root != Path("."):
                all_included_paths.append(rel_root)

            for file in sorted(files):
                file_path = current_root / file
                if self.is_ignored(file_path):
                    continue

                rel_file = file_path.relative_to(self.root_dir)

                # Size check
                try:
                    if file_path.stat().st_size > self.max_file_size_bytes:
                        continue
                except OSError:
                    continue

                # Binary check
                if is_binary_file(file_path):
                    continue

                # Read text
                try:
                    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                        content = f.read()
                    file_contents[rel_file] = content
                    all_included_paths.append(rel_file)
                except Exception:
                    continue

        return file_contents, all_included_paths
