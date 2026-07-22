"""Atomic canonical-record writes with a cross-process per-record lock."""

from __future__ import annotations

import json
import os
import time
import uuid
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator


class LockTimeoutError(TimeoutError):
    """Raised when another process retains the same record lock."""


def _safe_record_id(record_id: str) -> str:
    if not record_id or any(ch not in "abcdefghijklmnopqrstuvwxyz0123456789-" for ch in record_id):
        raise ValueError(f"unsafe record id: {record_id!r}")
    return record_id


@contextmanager
def record_lock(root: Path, record_id: str, timeout: float = 5.0) -> Iterator[Path]:
    """Acquire an exclusive lock file without relying on platform-specific APIs."""

    safe_id = _safe_record_id(record_id)
    lock_dir = root.resolve() / ".locks"
    lock_dir.mkdir(parents=True, exist_ok=True)
    lock_path = lock_dir / f"{safe_id}.lock"
    deadline = time.monotonic() + timeout

    while True:
        try:
            fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, f"pid={os.getpid()}\n".encode("ascii"))
            os.close(fd)
            break
        except FileExistsError:
            if time.monotonic() >= deadline:
                raise LockTimeoutError(f"timed out waiting for {lock_path}")
            time.sleep(0.02)

    try:
        yield lock_path
    finally:
        try:
            lock_path.unlink()
        except FileNotFoundError:
            pass


def atomic_write_json(root: Path, relative_path: Path, record: dict, timeout: float = 5.0) -> Path:
    """Write one JSON record atomically while locking by its canonical id."""

    root = root.resolve()
    target = (root / relative_path).resolve()
    if root not in target.parents:
        raise ValueError("target escapes repository root")

    record_id = _safe_record_id(str(record.get("id", "")))
    if target.stem != record_id:
        raise ValueError("filename must equal record id")

    target.parent.mkdir(parents=True, exist_ok=True)
    with record_lock(root, record_id, timeout=timeout):
        temp = target.with_name(f".{target.name}.{uuid.uuid4().hex}.tmp")
        try:
            payload = json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
            temp.write_text(payload, encoding="utf-8", newline="\n")
            os.replace(temp, target)
        finally:
            if temp.exists():
                temp.unlink()
    return target
