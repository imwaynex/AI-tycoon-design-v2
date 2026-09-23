# design_v2

這是一套響應式介面的底層設計系統，並收錄第一份頁面級 Hub 佈局規範與低保真參考原型。本倉仍沒有產品元件實作與品牌主題；Hub 原型只作為規範參照，不代表已完成產品畫面。

規範由兩部分一起成立，另有工具與流程文件維持它們一致：

| 檔案 | 職責 |
|---|---|
| [SPEC.md](SPEC.md) | 共用行為與約束。定義介面如何隨寬度、高度、容器與輸入方式變化。 |
| [docs/hub/](docs/hub/) | Hub 頁面級規範與互動參考原型；正式要求以目錄內的 RWD 行為規範為準。 |
| [tokens/](tokens/) | 數值。間距、字級、斷點、色彩、尺寸、圓角、海拔、動效與層級。 |
| [scripts/check.py](scripts/check.py) | 驗證。檢查引用、對比、色階方向、疊層順序、數值格式、版本紀錄、棄用登記、用詞，以及每個 token 是否都有規則。 |
| [GOVERNANCE.md](GOVERNANCE.md) | 管理規範。變更分類、版本、棄用、提交、發布與寫作。 |
| [CHANGELOG.md](CHANGELOG.md) | 每個版本的變更與對消費者的影響。 |
| [AGENTS.md](AGENTS.md) | Agent 工作契約：任務範圍、資料來源、工作步驟、同步修改、決策、驗證與交付。 |
| [CLAUDE.md](CLAUDE.md) | Claude Code 入口，匯入 `AGENTS.md` 共用完整工作契約。 |

`tokens/index.json` 的 `version` 是這套底層的版本。規則與數值衝突時，先改正衝突，再使用。畫面與元件實作不得另寫一套斷點或色值。

閱讀順序：本頁，然後 `SPEC.md`，需要數值時再查對應的 token 檔；處理 Hub 時再讀 `docs/hub/README.md` 與 Hub 正式規範。要修改本倉之前，先讀 `GOVERNANCE.md`。

Agent 開始工作前先讀 `AGENTS.md`；共同規則只維護這一份，Claude Code 透過 `CLAUDE.md` 匯入。

修改規範或 token 後執行：

```sh
python3 scripts/check.py
```

只需要 Python 3 標準函式庫，有任何問題時結束碼為 1。複製倉庫後執行一次下列指令，提交前就會自動檢查：

```sh
git config core.hooksPath .githooks
```
