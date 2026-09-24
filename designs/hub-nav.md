# Hub 導覽列元件庫

[Pen 元件庫](hub-nav.lib.pen) · [預覽](hub-nav-assets/library-preview@2x.png) · [元件與素材清單](hub-nav.manifest.json) · [底部組合入口](hub-bottom-components.md)

本庫獨立維護導覽列，不依賴聊天元件庫。導覽順序為城市、事件、商會、排行、資產；圖示依使用者指定使用 Popboard v1 的 `city`、`event`、`shield`、`ranking`、`wallet-color`。

## 主元件

| 元件 | ID | 尺寸（px） |
|---|---|---|
| `Hub/Icon/City` | `k0x0N3` | 56 × 56 |
| `Hub/Nav/Label` | `gbZkt` | 67 × 20 |
| `Hub/Nav/Glyph` | `eKDvm` | 64 × 17 |
| `Hub/Nav/Item` | `GdqgX` | 67 × 64 |
| `Hub/Nav/Bar` | `W42XvN` | 430 × 84 |

五個入口共用項目主元件，圖示與名稱透過實例覆寫；字型、尺寸與外框結構保留連動。五份 PNG 原始位元組不變，置入尺寸為 56 × 56px，不再套用光學位移。

## 使用與維護

從倉庫根目錄的 pen.dev CLI 互動模式匯入：

```js
import_library({path:"designs/hub-nav.lib.pen"})
get_app_state()
```

使用工具回傳的代號與 `W42XvN` 建立 `type: "ref"` 實例。代號可能改變，不要固定使用其他文件的代號。搬移時一併攜帶 `hub-nav-assets/`，保留相對路徑。

文字維持 14px Noto Sans TC Black 與 1.5px 黑色外框。Pen CLI 不保留原生文字描邊，本庫以 24 個字形的黑色偏移實例組成外輪廓；[放大檢查圖](hub-nav-assets/outline-detail@12x.png)記錄呈現方式。更改單一入口名稱時，同步覆寫字面與其 24 個黑色實例的 `content`。目前五個入口已有各自的名稱覆寫，修改字形主元件文字不會蓋過它們。

維護時只修改本庫，再重新載入消費文件中的元件庫。不要在聊天庫或組合示例複製另一組導覽主元件。

## 驗證與界線

已檢查 5 個主元件、內部引用完整性、五項名稱及文字外框、圖層邊界、匯入與預覽。素材來源路徑及 SHA-256 見清單；字形高倍率輪廓不宣稱與 Figma 逐像素相同。

本庫是視覺參考。[Hub 正式規範](../docs/hub/AI-Tycoon-Hub-UI佈局與RWD行為規範.md)第 4.5 節仍記錄大廳、事件、商會、排行、我的；城市及資產是本次設計稿的使用者指定名稱，產品條款同步仍由維護者決定。沒有執行實機 RWD、鍵盤、焦點或無障礙驗收。
