# design_v2

## Hub Sites 視覺參考

[Hub 直向網站交付與 RWD 說明](designs/hub-portrait-sites.md) 記錄網站連結、來源、測試與限制。`sites/hub-portrait/` 保存可發布的視覺參考及 token 快照；不代表正式產品元件、品牌主題或 Hub 全項驗收完成。


本倉維護響應式設計規範、token 與驗證工具，並收錄 Hub 定稿佈局規範及低保真參考原型。尚未建立產品元件庫、品牌主題或業務資料模型；原型不是正式產品實作。

## 依任務閱讀

| 任務 | 入口與後續來源 |
|---|---|
| Agent 修改倉庫 | [AGENTS.md](AGENTS.md) → [GOVERNANCE.md](GOVERNANCE.md)。 |
| 共用 RWD／元件行為 | [SPEC.md](SPEC.md) → [tokens/index.json](tokens/index.json) → 受影響的 token 檔。 |
| Hub 佈局與驗收 | [Hub 文件入口](docs/hub/README.md) → 正式規範；只有需要互動參照時才讀 HTML。 |
| 文件角色與來源定位 | [docs/index.json](docs/index.json)；只登記路徑、角色與範圍，不複製設計條款或版本。 |
| 版本與變更影響 | [CHANGELOG.md](CHANGELOG.md)；發布流程見管理規範。 |
| Claude Code | [CLAUDE.md](CLAUDE.md) 匯入同一份 Agent 工作契約。 |

來源分工與衝突處理集中在 [管理規範第 1 節](GOVERNANCE.md#1-文件職責)。共用規則與 token 共同成立；頁面規範補充自己的行為，不授權任意覆寫全域 token。HTML 與歷史紀錄不作為現行設計規則。

## 驗證

在倉庫根目錄執行，僅需 Python 3 標準函式庫：

```sh
python3 scripts/check.py
python3 -m unittest discover -s scripts -p 'test_*.py'
```

[check.py](scripts/check.py) 保留 token 引用、對比、色階、層級、格式、版本與棄用檢查，並呼叫 [check_docs.py](scripts/check_docs.py) 驗證文件登記、角色、相對連結、參考原型完整性與遞迴用詞。[回歸測試](scripts/test_check_docs.py) 驗證錯誤確實會被攔截。

檢查通過不代表文件語意完全一致，也不代表 RWD、鍵盤、對比實際呈現或實機 UX 已驗收；人工審查仍依管理規範與各頁驗收條件執行。外部網址可達性不在離線檢查範圍。

啟用本地提交檢查：

```sh
git config core.hooksPath .githooks
```

[CI](.github/workflows/validate.yml) 執行相同兩個指令；是否設定為合併必要條件由維護者管理。系統版本只讀取 `tokens/index.json`，不要從 Hub 文件或原型版本推算。
