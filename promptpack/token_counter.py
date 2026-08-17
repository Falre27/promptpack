"""
Token estimation utilities for promptpack.
"""
from typing import Tuple


def estimate_tokens(text: str) -> int:
    """
    Estimate token count for LLM context.
    Standard heuristic: ~4 characters per token for standard English/code text.
    """
    if not text:
        return 0
    return max(1, len(text) // 4)


def get_token_warning(token_count: int, threshold: int = 100000) -> Tuple[bool, str]:
    """
    Returns a warning status and message if estimated tokens exceed recommended limits.
    """
    if token_count > threshold:
        return True, (
            f"⚠️ Warning: Estimated output is ~{token_count:,} tokens "
            f"(exceeds typical ~{threshold:,} prompt limit). "
            "Consider excluding large subfolders or files using --ignore."
        )
    return False, f"Estimated prompt length: ~{token_count:,} tokens ({len(text_bytes(token_count)):,} chars approx)."


def text_bytes(tokens: int) -> str:
    return "a" * (tokens * 4)
