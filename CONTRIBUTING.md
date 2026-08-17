# Contributing to promptpack 🤝

Thank you for your interest in contributing to `promptpack`!

## 🚀 Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/username/promptpack.git
   cd promptpack
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies in editable mode:**
   ```bash
   pip install -e .
   pip install pathspec pyperclip pytest
   ```

4. **Run test suite:**
   ```bash
   python -m unittest discover tests
   ```

## 📝 Pull Request Guidelines

- Ensure unit tests pass before submitting.
- Keep standard code style (PEP 8).
- Update `README.md` if adding or changing CLI arguments.
