#!/usr/bin/env python3
"""檢查規範、token 與管理規範是否一致。只用標準函式庫。

檢查項目：
  1. index.json 列出的檔案存在，且每個檔案的 id 與檔名相同。
  2. 每個 {檔案id.物件路徑} 引用都能解析，且沒有循環。
  3. color.contrast 的每一組都達到 min（WCAG 相對對比）。
  4. 原始色板在同一色相內，數字越大越深。
  5. layer.z 依宣告順序嚴格遞增。
  6. 每個 token 不是被其他 token 引用，就是被 SPEC.md 以反引號提及。
  7. 數值格式：宣告 unit 的檔案，同單位長度寫成數字；全域設定不重複。
  8. 版本：status 與主版本一致，CHANGELOG 最新版本等於 index.json。
  9. 棄用登記：token 存在、引用 replacedBy，且尚未到達 removeIn。
 10. 用詞：Markdown 使用台灣用語；SPEC.md 不使用無法驗證的詞。

有錯誤時結束碼為 1。
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOKENS = ROOT / "tokens"
SPEC = ROOT / "SPEC.md"
CHANGELOG = ROOT / "CHANGELOG.md"

INDEX_OWN_KEYS = {"name", "version", "status", "files", "deprecated"}
# 不使用的詞 → 應使用的詞。見 GOVERNANCE.md 第 8 節。
BANNED_TERMS = {
    "全屏": "全螢幕", "屏幕": "螢幕", "支持": "支援", "導航": "導覽", "默認": "預設",
    "信息": "資訊", "設置": "設定", "文檔": "文件", "數據": "資料", "視頻": "影片",
    "接口": "介面", "用戶": "使用者", "實現": "實作", "兼容": "相容", "菜單": "選單",
    "鼠標": "滑鼠", "加載": "載入", "模塊": "模組", "組件": "元件",
}
VAGUE_TERMS = ("盡量", "盡可能", "建議", "酌情")

META_KEYS = {"id", "unit"}
# 寬度帶名稱與分層用的群組名稱在規範裡到處出現，單獨出現時不算提及任何 token。
GENERIC_NAMES = {"base", "sm", "md", "lg", "primitive", "semantic", "scale", "usage", "role", "z"}
REF = re.compile(r"^\{([^{}]+)\}$")

errors = []


def err(msg):
    errors.append(msg)


def load():
    index = json.loads((TOKENS / "index.json").read_text())
    files = {}
    for name in index["files"]:
        path = TOKENS / f"{name}.json"
        if not path.exists():
            err(f"index.json 列出 {name}，但 {path.name} 不存在")
            continue
        data = json.loads(path.read_text())
        if data.get("id") != name:
            err(f"{path.name} 的 id 是 {data.get('id')!r}，應為 {name!r}")
        files[name] = data
    listed = set(index["files"])
    for path in TOKENS.glob("*.json"):
        if path.stem != "index" and path.stem not in listed:
            err(f"{path.name} 沒有列在 index.json")
    return index, files


def lookup(files, dotted):
    parts = dotted.split(".")
    node = files.get(parts[0])
    for key in parts[1:]:
        if not isinstance(node, dict) or key not in node:
            return None, False
        node = node[key]
    return node, node is not None


def resolve(files, value, seen=()):
    m = REF.match(value) if isinstance(value, str) else None
    if not m:
        return value
    target = m.group(1)
    if target in seen:
        raise ValueError("循環引用：" + " → ".join((*seen, target)))
    node, ok = lookup(files, target)
    if not ok:
        raise KeyError(target)
    if isinstance(node, dict):
        raise ValueError(f"{target} 指向物件，不是單一值")
    return resolve(files, node, (*seen, target))


def leaves(node, path):
    """列出所有 token 葉節點的路徑與值。color.contrast 是檢查表，不是 token。"""
    if isinstance(node, dict):
        for key, child in node.items():
            if len(path) == 1 and key in META_KEYS:
                continue
            if path == ["color"] and key == "contrast":
                continue
            yield from leaves(child, path + [key])
    else:
        yield path, node


def luminance(hex_color):
    h = hex_color.lstrip("#")
    rgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contrast(a, b):
    hi, lo = sorted((luminance(a), luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def spec_terms():
    terms = set()
    for term in re.findall(r"`([^`\n]+)`", SPEC.read_text()):
        if re.fullmatch(r"[A-Za-z][\w]*(\.[\w]+)*", term):
            terms.add(tuple(term.split(".")))
    return terms


def mentioned(path, terms):
    """反引號裡的名稱等於路徑中任一段連續片段，就算提及，並涵蓋其下所有 token。
    單一段名稱不得是檔案 id、寬度帶或分層群組名稱，避免 `sm`、`primitive` 這類詞誤判。"""
    for term in terms:
        n = len(term)
        if n == 1 and term[0] in GENERIC_NAMES:
            continue
        start = 1 if n == 1 else 0
        for i in range(start, len(path) - n + 1):
            if tuple(path[i:i + n]) == term:
                return True
    return False


def parse_version(v):
    m = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", str(v))
    return tuple(int(x) for x in m.groups()) if m else None


def check_format(index, files):
    for key in index:
        if key in INDEX_OWN_KEYS:
            continue
        for name, data in files.items():
            if key in data:
                err(f"{name}.json 重複定義全域設定 {key}，只保留在 index.json")
    for name, data in files.items():
        unit = data.get("unit")
        if not unit:
            continue
        pattern = re.compile(rf"^-?\d+(\.\d+)?{re.escape(unit)}$")
        for path, value in leaves(data, [name]):
            if isinstance(value, str) and pattern.match(value):
                err(f"{'.'.join(path)}：{name}.json 的單位是 {unit}，{value!r} 應寫成數字")


def check_version(index):
    version = parse_version(index.get("version"))
    if not version:
        err(f"index.json 的 version {index.get('version')!r} 不是 主.次.修 格式")
        return None
    expected = "foundation" if version[0] == 0 else "stable"
    if index.get("status") != expected:
        err(f"index.json 的 status 應為 {expected!r}（主版本 {version[0]}），實際是 {index.get('status')!r}")
    if not CHANGELOG.exists():
        err("缺少 CHANGELOG.md")
        return version
    released = re.findall(r"^## \[(\d+\.\d+\.\d+)\]", CHANGELOG.read_text(), re.M)
    if not released:
        err("CHANGELOG.md 沒有任何 ## [主.次.修] 版本段落")
    elif parse_version(released[0]) != version:
        err(f"CHANGELOG.md 最新版本是 {released[0]}，index.json 是 {index['version']}")
    return version


def check_deprecated(index, files, version):
    for dotted, info in (index.get("deprecated") or {}).items():
        node, ok = lookup(files, dotted)
        if not ok:
            err(f"棄用登記的 {dotted} 不存在；已刪除的 token 要一併移除登記")
            continue
        replaced = info.get("replacedBy")
        if replaced is not None:
            if not lookup(files, replaced)[1]:
                err(f"{dotted} 的 replacedBy {replaced} 不存在")
            elif node != "{" + replaced + "}":
                err(f"已棄用的 {dotted} 必須引用 {{{replaced}}}，實際是 {node!r}")
        for field in ("since", "removeIn"):
            if not parse_version(info.get(field)):
                err(f"{dotted} 的 {field} 必須是 主.次.修 格式")
        remove_in = parse_version(info.get("removeIn"))
        if version and remove_in and version >= remove_in:
            err(f"{dotted} 預定在 {info['removeIn']} 刪除，目前已是 {index['version']}")


def check_wording():
    for md in sorted(ROOT.glob("*.md")):
        for lineno, line in enumerate(md.read_text().splitlines(), 1):
            text = re.sub(r"`[^`]*`", "", line)  # 反引號內是引用，不檢查
            for bad, good in BANNED_TERMS.items():
                if bad in text:
                    err(f"{md.name}:{lineno}：「{bad}」改用「{good}」")
            if md == SPEC:
                for vague in VAGUE_TERMS:
                    if vague in text:
                        err(f"{md.name}:{lineno}：規範句不使用「{vague}」，改寫成可驗證的要求")


def main():
    index, files = load()
    check_format(index, files)
    version = check_version(index)
    check_deprecated(index, files, version)
    check_wording()
    deprecated = set(index.get("deprecated") or {})
    all_leaves = [(p, v) for name, data in files.items() for p, v in leaves(data, [name])]

    # 2. 引用
    referenced = set()
    ref_sources = list(all_leaves)
    for i, entry in enumerate(files.get("color", {}).get("contrast", [])):
        for side in ("fg", "bg"):
            ref_sources.append(([f"color.contrast[{i}]", side], entry.get(side)))
    cycles = set()
    for path, value in ref_sources:
        m = REF.match(value) if isinstance(value, str) else None
        if isinstance(value, str) and ("{" in value or "}" in value) and not m:
            err(f"{'.'.join(path)}：引用必須是整個值 {{檔案id.物件路徑}}，得到 {value!r}")
            continue
        if not m:
            continue
        referenced.add(m.group(1))
        try:
            resolve(files, value)
        except KeyError as e:
            # 只在斷點本身回報；經由它間接失敗的引用不重複列出。
            if e.args[0] == m.group(1):
                err(f"{'.'.join(path)}：引用 {{{e.args[0]}}} 不存在")
        except ValueError as e:
            if "循環" not in str(e):
                err(f"{'.'.join(path)}：{e}")
            else:
                members = frozenset(str(e).split("：", 1)[1].split(" → "))
                if members not in cycles:
                    cycles.add(members)
                    err(f"{'.'.join(path)}：{e}")

    # 3. 對比
    color = files.get("color", {})
    for entry in color.get("contrast", []):
        try:
            fg, bg = resolve(files, entry["fg"]), resolve(files, entry["bg"])
        except (KeyError, ValueError):
            continue  # 已在引用檢查中回報
        ratio = contrast(fg, bg)
        if ratio + 1e-9 < entry["min"]:
            err(f"對比不足 {ratio:.2f}:1 < {entry['min']}:1：{entry['fg']} 在 {entry['bg']} 上")

    # 4. 色階方向
    for hue, ramp in color.get("primitive", {}).items():
        steps = sorted(ramp.items(), key=lambda kv: int(kv[0]))
        for (k1, v1), (k2, v2) in zip(steps, steps[1:]):
            if luminance(v2) >= luminance(v1):
                err(f"color.primitive.{hue}.{k2} 應比 .{k1} 深，實際更淺或相同")

    # 5. 疊層順序
    z = files.get("layer", {}).get("z", {})
    values = list(z.items())
    for (n1, v1), (n2, v2) in zip(values, values[1:]):
        if not v2 > v1:
            err(f"layer.z.{n2}（{v2}）必須大於前一層 layer.z.{n1}（{v1}）")

    # 6. 覆蓋
    terms = spec_terms()
    for path, _ in all_leaves:
        dotted = ".".join(path)
        if dotted in referenced or dotted in deprecated or mentioned(path, terms):
            continue
        err(f"{dotted} 沒有被任何 token 引用，SPEC.md 也沒有提及")

    if errors:
        print(f"✗ {len(errors)} 個問題（tokens {index.get('version')}）")
        for e in errors:
            print("  - " + e)
        return 1
    print(f"✓ tokens {index.get('version')}：{len(all_leaves)} 個 token，"
          f"{len(color.get('contrast', []))} 組對比，文件用詞與版本紀錄全部通過")
    return 0


if __name__ == "__main__":
    sys.exit(main())
