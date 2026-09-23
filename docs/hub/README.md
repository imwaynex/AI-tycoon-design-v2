# AI Tycoon Hub 文件

本目錄收錄 Hub 已定稿的 RWD UI 佈局規範與互動參考原型。

| 檔案 | 職責 |
|---|---|
| [AI-Tycoon-Hub-UI佈局與RWD行為規範.md](AI-Tycoon-Hub-UI佈局與RWD行為規範.md) | Hub 的正式頁面級要求與 UX 驗收條件。 |
| [AI-Tycoon-Hub.html](AI-Tycoon-Hub.html) | 低保真互動原型；用來參照浮動 UI 的佈局與互動行為。 |

## 規範優先順序

1. Hub 的驗收以 `AI-Tycoon-Hub-UI佈局與RWD行為規範.md` 為準。
2. 共用的可用性、token、層級與互動基礎仍遵守根目錄的 [SPEC.md](../../SPEC.md) 與 [tokens/](../../tokens/)。
3. 參考原型若與 Hub 正式規範衝突，以 Hub 正式規範為準。
4. 原型中的城市建築數量、名稱、排列、位置與互動屬示意；目前正式規範只確認城市地圖與建築入口位於最底圖層，浮動 UI 位於其上。
5. Hub 的 `orientation: landscape` 與 `min-width: 36rem` 是頁面級配置切換條件，不改寫全域 `layout.breakpoint`。

原型與規範都不能取代目標手機瀏覽器上的實機驗證；發布前仍需覆蓋安全區、瀏覽器工具列、輸入鍵盤、旋轉及內容放大等情境。
