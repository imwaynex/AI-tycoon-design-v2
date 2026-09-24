# 變更紀錄

格式與版本規則見 [GOVERNANCE.md](GOVERNANCE.md)。

## 未發布

### 新增

- 依 Figma `113:3581` 以 pen.dev CLI 建立 Hub 底部 Pen 元件庫：10 個可重用主元件、五項導覽連動實例、原始城市素材、預覽與來源清單；保留原稿雙行世界訊息及城市佔位，記錄與正式規範的差異。此為視覺參考，未發布或宣稱產品驗收通過。

- `docs/index.json`：登記文件角色、範圍與參考來源；不複製設計條款或版本。
- `scripts/check_docs.py`、`scripts/test_check_docs.py`：補上文件角色、來源完整性、相對連結與遞迴用詞檢查及回歸測試；由既有統一檢查入口執行。
- `.github/workflows/validate.yml`：讓 PR 與 `main` 使用和本地相同的檢查及測試；不代表已設定分支保護。

- `docs/hub/`：整合 Hub UI 佈局與 RWD 行為定稿規範，以及低保真互動參考原型；正式驗收以頁面規範為準，原型中的城市與建築配置維持非規範性示意。
- `SPEC.md`：加入頁面級命名配置條件的範圍規則，明確讓 Hub 的方向與 36rem 門檻只在 Hub 生效，不改寫全域 `layout.breakpoint`。
- `README.md`、`GOVERNANCE.md`、`AGENTS.md`：加入頁面級文件的閱讀、維護與審查責任。
- `AGENTS.md`：定義 Agent 的任務範圍、資料來源、工作步驟、同步修改、決策、完成標準與交付規則。
- `CLAUDE.md`：匯入 `AGENTS.md`，讓 Claude Code 共用完整工作契約。同步更新 README 與管理規範的文件索引；既有設計系統消費者不需要修改。

### 修正

- 依使用者指定替換 Hub 底部元件庫的導覽組：城市（city）、事件（event）、商會（shield）、排行（ranking）、資產（wallet-color）。使用正式圖標 PNG 副本並保留 1.5px 文字外框、連動實例與原尺寸；更新預覽和素材雜湊，正式產品目的地規範尚未同步。

- 修正 Hub 底部 Pen 元件庫遺漏的導覽文字黑色外框：依 Figma 原稿補上 1.5px 圓角外輪廓，新增共用可編輯字形主元件，同步五個導覽實例與預覽；確認儲存後重新開啟仍保留外框。

- `README.md`、`AGENTS.md` 與 `GOVERNANCE.md`：集中來源分工、精簡 Agent 閱讀路徑，補上固定 commit、並行修改保護與實際驗證結果的交付要求。
- `SPEC.md` 與 Hub 導讀：釐清頁面配置和全域寬度帶、城市底圖和一般正文、原型和正式實作之間的界線；列出仍需維護者決策的 token 映射，不改動定稿內容與既有 token。
- `CLAUDE.md` 移除容易過期的節數敘述；本地 hook 同步執行回歸測試，忽略 Python 暫存檔。
- 文件檢查通過不代表語意衝突或實機 UX 全部通過；保留原始 Hub 規範及 HTML，不以原型示意補完城市設計。既有 token 消費者無須遷移，發布版本維持不變。

## [0.2.0] - 2026-09-23

### 不相容

- `layer.z` 順序改為 `base`、`sticky`、`dropdown`、`toast`、`scrim`、`modal`。`toast` 移到遮罩之下，不再蓋住對話框。`layer.z.overlay` 改名為 `layer.z.scrim`。
- `elevation.usage.overlay` 改名為 `elevation.usage.dropdown`。
- `color.primitive.blue.600` 與 `blue.700` 對調名稱，色值不變，讓色階符合數字越大越深。引用 `blue.700` 的語意 token 改為引用 `blue.600`。
- 刪除沒有用到的 `color.primitive.neutral.800`。
- `motion.reduced.allowOpacity` 改為 `motion.reduced.opacityMs`。
- `tokens/layout.json` 改為宣告 `unit: "px"`，長度寫成數字。`measure` 維持 `68ch` 字串。
- 刪除 `type.rootPx`，`rootPx` 只保留在 `tokens/index.json`。
- `color.contrast` 的 `fg` 與 `bg` 改用 `{檔案id.物件路徑}` 引用語法。
- 視窗與容器斷點改為以 em 實作，系統放大預設文字時寬度帶會降檔。
- 非文字元素的對比至少 3:1；控制項邊界必須使用 `border.strong`。

### 新增

- `color.semantic.focus.ringInverse`，用於深色或強調色底上的焦點環。
- `radius.usage`：`control`、`container`、`dialog`、`pill`。
- `tokens/index.json` 的 `deprecated` 棄用登記。
- `sm` 寬度帶的對話框改用居中面板。
- 從某一層內開啟的暫時層，沿用開啟者所在的層。
- compact 密度在粗指標下改以留白收緊。
- icon、控制項 comfortable、點擊目標 comfortable、邊框寬度、`label`、等寬字、圓角、動效時長與曲線的使用規則。
- 更高對比偏好與強制色彩模式的規則。
- 元件狀態新增「選取」與「唯讀」。
- `color.contrast` 從 10 組擴充為 36 組，涵蓋下沉底色、連結、資訊色、懸停、邊框與焦點環。
- `scripts/check.py` 驗證腳本與 pre-commit hook。
- `GOVERNANCE.md` 與本檔。

### 修正

- `SPEC.md` 用詞改為台灣用語：`全屏` 改為全螢幕，`導航` 改為導覽，`支持` 改為支援。

## [0.1.0]

- 建立響應式設計系統的底層：解析順序、寬度帶、容器帶、短高度、佈局、token 分層與元件契約。
