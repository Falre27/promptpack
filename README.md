# promptpack CLI 📦⚡

[![PyPI version](https://img.shields.io/pypi/v/promptpack-cli.svg?color=blue)](https://pypi.org/project/promptpack-cli/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-brightgreen.svg)](https://python.org)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

> **Convert any codebase or local directory into a clean, perfectly formatted LLM prompt in one single command.**

---

## ⚡ The Problem vs. Solution

| ❌ The Old Way (Manual Copy-Paste) | ✅ The `promptpack` Way |
| :--- | :--- |
| Hand-picking 20+ code files one by one | **One command:** `promptpack . --clip` |
| Pasting messy `node_modules` or `.git` files by accident | **Automatic `.gitignore` & binary file filtering** |
| LLMs confusing file structure and imports | **Generates clean ASCII tree hierarchy at top of prompt** |
| Context window blowing up unexpectedly | **Built-in Token Estimator with warning thresholds** |

---

## 🚀 Quickstart

### 1. Installation

Install via PyPI:
```bash
pip install promptpack-cli
```

*(Optional) Install clipboard support directly:*
```bash
pip install promptpack-cli[clip]
```

### 2. Usage Examples

**Copy entire current directory directly to clipboard for Claude or ChatGPT:**
```bash
promptpack . --clip
```

**Save formatted prompt to a file:**
```bash
promptpack ./my-project --output prompt.md
```

**Ignore specific custom folders or large files:**
```bash
promptpack . --ignore docs tests --max-size-kb 200 -o prompt.md
```

---

## ✨ Features

- 🌲 **Tree-Structure Generator:** Embeds an ASCII directory tree at the top of your prompt so LLMs instantly understand your project architecture.
- 🙈 **`.gitignore` & Smart Filter Aware:** Automatically respects root and nested `.gitignore` files, ignoring `node_modules`, `.git`, `__pycache__`, `.venv`, and binary files.
- 🧮 **Token Estimator & Warning System:** Calculates approximate LLM token count (~4 chars/token) and alerts you if prompt length exceeds typical LLM context windows (>100k tokens).
- 📋 **Direct Clipboard Integration (`--clip`):** Instant `pyperclip` support to pack and paste code in 2 seconds without creating extra temporary files.
- 🎨 **Language Syntax Auto-Detection:** Maps extensions (`.py`, `.ts`, `.rs`, `.go`, `.json`, etc.) to clean Markdown codeblock syntax tags (` ```python `, ` ```typescript `).

---

## 🛠️ Command-Line Interface (CLI Reference)

```text
usage: promptpack [-h] [-o OUTPUT] [-c] [-i IGNORE [IGNORE ...]] 
                  [--max-size-kb MAX_SIZE_KB] [--no-tree] 
                  [--include-hidden] [-v] [path]

Convert any codebase directory into a clean, LLM-ready prompt.

positional arguments:
  path                  Path to target directory (default: '.')

options:
  -h, --help            show this help message and exit
  -o, --output OUTPUT   Output file path (e.g. prompt.md).
  -c, --clip            Copy output directly to clipboard.
  -i, --ignore IGNORE   Additional folders, files, or glob patterns to ignore.
  --max-size-kb MAX_SIZE Limit max individual file size in KB (default: 500).
  --no-tree             Skip generating project directory tree.
  --include-hidden      Include hidden files and dot-directories.
  -v, --version         Show program version.
```

---

## 📦 How to Publish to PyPI (Step-by-Step)

To publish your own version to PyPI (Python Package Index):

1. **Install build tools:**
   ```bash
   pip install --upgrade build twine
   ```

2. **Build source distribution and wheel:**
   ```bash
   python -m build
   ```

3. **Upload package to PyPI:**
   ```bash
   python -m twine upload dist/*
   ```

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for local setup and guidelines.

---

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.
