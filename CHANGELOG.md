# 變更紀錄

格式與版本規則見 [GOVERNANCE.md](GOVERNANCE.md)。

## 未發布

### 新增

- `AGENTS.md`：定義 Agent 的任務範圍、資料來源、工作步驟、同步修改、決策、完成標準與交付規則。
- `CLAUDE.md`：匯入 `AGENTS.md`，讓 Claude Code 共用完整工作契約。同步更新 README 與管理規範的文件索引；既有設計系統消費者不需要修改。

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
