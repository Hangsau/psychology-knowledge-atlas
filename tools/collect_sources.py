"""Retrieve selected public source-pack items into the private research cache."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import BinaryIO


ROOT = Path(__file__).resolve().parents[1]
SAFE_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ALLOWED_ACCESS = {
    "open_fulltext",
    "public_domain_fulltext",
    "repository_manuscript",
    "preprint",
    "publicly_readable_license_unclear",
}
EXTENSIONS = {
    "application/pdf": ".pdf",
    "application/epub+zip": ".epub",
    "text/html": ".html",
    "text/plain": ".txt",
    "application/xml": ".xml",
    "text/xml": ".xml",
}


def safe_http_url(url: str) -> str:
    """Percent-encode Unicode path/query content while preserving URL structure."""
    parts = urllib.parse.urlsplit(url)
    if parts.scheme not in {"http", "https"} or not parts.netloc:
        raise ValueError("download_url must use HTTP(S)")
    path = urllib.parse.quote(urllib.parse.unquote(parts.path), safe="/%:@")
    query = urllib.parse.quote(urllib.parse.unquote(parts.query), safe="=&?/:@,+")
    return urllib.parse.urlunsplit((parts.scheme, parts.netloc.encode("idna").decode("ascii"), path, query, ""))


def media_type(header: str | None, prefix: bytes) -> str:
    declared = (header or "").split(";", 1)[0].strip().lower()
    if prefix.startswith(b"%PDF-"):
        return "application/pdf"
    if prefix.startswith(b"PK\x03\x04") and declared == "application/epub+zip":
        return declared
    if prefix.lstrip().lower().startswith((b"<!doctype html", b"<html")):
        return "text/html"
    return declared or "application/octet-stream"


def stream_copy(response: BinaryIO, target: Path, maximum: int) -> tuple[str, int, bytes]:
    digest = hashlib.sha256()
    total = 0
    prefix = b""
    with target.open("wb") as handle:
        while True:
            block = response.read(1024 * 1024)
            if not block:
                break
            if not prefix:
                prefix = block[:512]
            total += len(block)
            if total > maximum:
                raise ValueError(f"body exceeds maximum size {maximum}")
            digest.update(block)
            handle.write(block)
        handle.flush()
        os.fsync(handle.fileno())
    if total == 0:
        raise ValueError("empty response body")
    return digest.hexdigest(), total, prefix


def retrieve(pack_path: Path, item_id: str, maximum: int) -> None:
    pack = json.loads(pack_path.read_text(encoding="utf-8"))
    target_id = pack.get("target_id")
    if not isinstance(target_id, str) or not SAFE_ID.fullmatch(target_id):
        raise ValueError("unsafe target_id")
    matches = [item for item in pack.get("items", []) if item.get("id") == item_id]
    if len(matches) != 1 or not SAFE_ID.fullmatch(item_id):
        raise ValueError("item must resolve exactly once and use a safe id")
    item = matches[0]
    if item.get("status") not in {"selected", "failed"}:
        raise ValueError("item must be selected or failed before retrieval")
    if item.get("access_status") not in ALLOWED_ACCESS:
        raise ValueError("access_status is not eligible for direct retrieval")
    url = item.get("download_url")
    if not isinstance(url, str):
        raise ValueError("download_url must use HTTP(S)")
    url = safe_http_url(url)

    destination_dir = ROOT / ".private-sources" / target_id
    destination_dir.mkdir(parents=True, exist_ok=True)
    partial = destination_dir / f"{item_id}.part"
    request = urllib.request.Request(url, headers={"User-Agent": "psychology-knowledge-atlas/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            digest, size, prefix = stream_copy(response, partial, maximum)
            kind = media_type(response.headers.get("Content-Type"), prefix)
            if kind not in EXTENSIONS:
                raise ValueError(f"unsupported media type {kind}")
            final = destination_dir / f"{item_id}{EXTENSIONS[kind]}"
            partial.replace(final)
            item["status"] = "retrieved"
            item.pop("failure", None)
            item["retrieval"] = {
                "retrieved_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
                "sha256": digest,
                "bytes": size,
                "media_type": kind,
                "cache_key": final.relative_to(ROOT).as_posix(),
            }
            pack["status"] = "retrieving"
            pack_path.write_text(json.dumps(pack, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(f"retrieved {item_id}: {size} bytes, sha256={digest}")
    except (OSError, ValueError, urllib.error.URLError) as exc:
        partial.unlink(missing_ok=True)
        item["status"] = "failed"
        item["failure"] = {"at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(), "reason": str(exc)}
        pack_path.write_text(json.dumps(pack, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        raise


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("target_id")
    parser.add_argument("item_id")
    parser.add_argument("--max-mib", type=int, default=100)
    args = parser.parse_args()
    pack = ROOT / "research" / "source-packs" / f"{args.target_id}.json"
    retrieve(pack, args.item_id, args.max_mib * 1024 * 1024)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
