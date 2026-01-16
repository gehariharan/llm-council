"""Simple access key validation for chat endpoints."""

import json
import os
from functools import lru_cache
from pathlib import Path
from typing import Optional

from fastapi import HTTPException, status


def _get_access_key_path() -> Path:
    """
    Resolve the path to the JSON file that stores the chat access key.
    Defaults to `access_key.json` in the project root, but can be overridden
    with the CHAT_ACCESS_KEY_PATH environment variable.
    """
    configured_path = os.getenv("CHAT_ACCESS_KEY_PATH")
    if configured_path:
        return Path(configured_path)
    return Path("access_key.json")


@lru_cache(maxsize=1)
def _load_access_key() -> str:
    """Load the access key from disk and cache it for reuse."""
    path = _get_access_key_path()
    if not path.exists():
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Access key file not found on the server.",
        )

    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Invalid access key JSON configuration.",
        ) from exc

    key = data.get("access_key")
    if not key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Access key missing in configuration.",
        )

    return key


def validate_access_key(provided_key: Optional[str]):
    """
    Ensure a request supplied the correct access key.

    Args:
        provided_key: Access key string supplied by the client.
    """
    if not provided_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Missing access key.",
        )

    expected_key = _load_access_key()
    if provided_key != expected_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid access key.",
        )
