"""離線文件檢查；只檢查明確結構，不推斷需求語意，也不執行原型。"""
from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path, PurePosixPath
from typing import Any, Mapping, Sequence
from urllib.parse import unquote, urlsplit

ROLES = {"entry", "agent-contract", "governance", "normative", "guide", "reference", "history"}
SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__"}
DOCUMENT_SUFFIXES = {".md", ".html", ".htm"}


def load_json(path: Path) -> Any:
    """Reject duplicate keys rather than silently keeping the last value."""
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"{path}: 重複 JSON 鍵 {key!r}")
            result[key] = value
        return result
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique)


def document_paths(root: Path) -> list[Path]:
    paths = []
    for directory, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        paths.extend(Path(directory) / name for name in files
                     if Path(name).suffix.lower() in DOCUMENT_SUFFIXES)
    return sorted(paths)


def outside(root: Path, target: Path) -> bool:
    try:
        target.resolve().relative_to(root.resolve())
        return False
    except (ValueError, OSError, RuntimeError):
        return True


def without_fences(text: str) -> str:
    """Keep line positions while excluding fenced examples."""
    result, fence = [], None
    for line in text.splitlines():
        match = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if fence:
            if match and match[1][0] == fence[0] and len(match[1]) >= len(fence) and not match[2].strip():
                fence = None
            result.append("")
        elif match:
            fence = match[1]
            result.append("")
        else:
            result.append(line)
    return "\n".join(result)


def heading_ids(text: str) -> set[str]:
    ids, counts = set(), {}
    for line in without_fences(text).splitlines():
        match = re.match(r"^ {0,3}#{1,6}\s+(.+?)\s*#*\s*$", line)
        if not match:
            continue
        slug = re.sub(r"[^\w\- ]", "", match[1].lower()).replace(" ", "-")
        count = counts.get(slug, 0)
        ids.add(slug if not count else f"{slug}-{count}")
        counts[slug] = count + 1
    ids.update(re.findall(r'<(?:a|h[1-6])\b[^>]*\bid=["\']([^"\']+)', text, re.I))
    return ids


def markdown_links(text: str) -> list[tuple[int, str]]:
    """Supported forms: inline links/images, definitions and full reference links."""
    lines = without_fences(text).splitlines()
    definitions, found = {}, []
    for line_no, line in enumerate(lines, 1):
        line = re.sub(r"(`+).*?\1", "", line)
        definition = re.match(r"^\s*\[([^]]+)\]:\s*(<[^>]+>|\S+)", line)
        if definition:
            key = " ".join(definition[1].lower().split())
            definitions[key] = definition[2].strip("<>")
            found.append((line_no, definitions[key]))
            continue
        for match in re.finditer(r"\[[^]]*\]\(\s*(<[^>]+>|[^\s)]+)(?:\s+['\"][^\n]*?['\"])?\s*\)", line):
            found.append((line_no, match[1].strip("<>")))
    for line_no, line in enumerate(lines, 1):
        line = re.sub(r"(`+).*?\1", "", line)
        for match in re.finditer(r"\[([^]]+)\]\[([^]]*)\]", line):
            key = " ".join((match[2] or match[1]).lower().split())
            if key not in definitions:
                found.append((line_no, "missing-reference:" + key))
    return found


def validate_documents(root: Path, banned: Mapping[str, str], vague: Sequence[str]) -> tuple[list[str], dict[str, int]]:
    root = root.resolve()
    errors: list[str] = []
    counts = {"documents": 0, "local_links": 0}
    try:
        index = load_json(root / "docs/index.json")
    except (OSError, ValueError, UnicodeError) as exc:
        return [f"DOC001: 無法讀取文件登記：{exc}"], counts
    if not isinstance(index, dict) or index.get("schemaVersion") != 1 or set(index) != {"schemaVersion", "documents"} or not isinstance(index.get("documents"), list):
        return ["DOC001: docs/index.json 必須使用 schemaVersion 1 與 documents 陣列"], counts
    records: dict[str, dict] = {}
    normative_scopes = {}
    for record in index["documents"]:
        if not isinstance(record, dict):
            errors.append("DOC001: 文件登記必須是物件")
            continue
        name, role, scope = (record.get(key) for key in ("path", "role", "scope"))
        if not isinstance(name, str) or not name or PurePosixPath(name).is_absolute() or ".." in PurePosixPath(name).parts or "\\" in name or str(PurePosixPath(name)) != name:
            errors.append(f"DOC002: 無效的倉庫相對路徑 {name!r}")
            continue
        if name in records:
            errors.append(f"DOC003: 重複登記 {name}")
            continue
        records[name] = record
        if not isinstance(role, str) or role not in ROLES or not isinstance(scope, str) or not re.fullmatch(r"[a-z][a-z0-9-]*", scope):
            errors.append(f"DOC003: {name} 的 role／scope 無效")
            continue
        allowed = {"path", "role", "scope"} | ({"source", "sha256"} if role == "reference" else set())
        if set(record) != allowed:
            errors.append(f"DOC001: {name} 登記欄位不符角色 {role}")
        path = root / name
        if outside(root, path) or not path.is_file() or path.suffix.lower() not in DOCUMENT_SUFFIXES:
            errors.append(f"DOC002: 文件不存在、超出倉庫或類型不符：{name}")
        if path.suffix.lower() in {".html", ".htm"} and role != "reference":
            errors.append(f"DOC003: HTML 只能登記為 reference：{name}")
        if role == "normative":
            if scope in normative_scopes:
                errors.append(f"DOC003: {scope} 同時有兩份主規範：{normative_scopes[scope]}、{name}")
            normative_scopes[scope] = name
    for name, record in records.items():
        if record.get("role") != "reference":
            continue
        source_name = record.get("source")
        source = records.get(source_name, {}) if isinstance(source_name, str) else {}
        if source.get("role") != "normative" or source.get("scope") != record.get("scope"):
            errors.append(f"DOC006: {name} 必須指向同範圍正式規範")
        digest = record.get("sha256")
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
            errors.append(f"DOC006: {name} 缺少有效 sha256")
        else:
            path = root / name
            if not outside(root, path) and path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                errors.append(f"DOC006: {name} 內容與登記雜湊不符；確認變更理由後同步登記")
    for path in document_paths(root):
        name = path.relative_to(root).as_posix()
        counts["documents"] += 1
        if name not in records:
            errors.append(f"DOC004: 文件未登記：{name}")
        if outside(root, path):
            errors.append(f"DOC002: 文件連結超出倉庫：{name}")
            continue
        if path.suffix.lower() != ".md":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"DOC002: {name} 無法讀取：{exc}")
            continue
        for line_no, line in enumerate(without_fences(text).splitlines(), 1):
            prose = re.sub(r"(`+).*?\1", "", line)
            for bad, good in banned.items():
                if bad in prose:
                    errors.append(f"DOC007: {name}:{line_no}：「{bad}」改用「{good}」")
            if records.get(name, {}).get("role") == "normative":
                for term in vague:
                    if term in prose:
                        errors.append(f"DOC007: {name}:{line_no}：規範句不使用「{term}」")
        for line_no, target in markdown_links(text):
            if target.startswith("missing-reference:"):
                errors.append(f"DOC005: {name}:{line_no}：缺少連結定義 {target.partition(':')[2]}")
                continue
            url = urlsplit(target)
            if url.scheme or url.netloc:
                continue  # Deliberately offline: do not claim external URLs work.
            counts["local_links"] += 1
            dest = path.parent / unquote(url.path) if url.path else path
            if outside(root, dest) or not dest.exists():
                errors.append(f"DOC005: {name}:{line_no}：相對連結不存在或越界 {target}")
            elif url.fragment and dest.suffix.lower() == ".md" and unquote(url.fragment) not in heading_ids(dest.read_text(encoding="utf-8")):
                errors.append(f"DOC005: {name}:{line_no}：標題錨點不存在 {target}")
        if name == "CLAUDE.md":
            imports = re.findall(r"^@([^\s]+)\s*$", text, re.M)
            if imports != ["AGENTS.md"] or not (root / "AGENTS.md").is_file():
                errors.append("DOC008: CLAUDE.md 必須匯入存在的 @AGENTS.md")
    return errors, counts
