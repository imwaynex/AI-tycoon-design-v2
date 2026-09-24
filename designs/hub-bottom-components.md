# Hub 底部元件庫

使用 pen.dev CLI 0.3.8 的 `interactive` 模式建立，共 11 個可重用主元件（含內部字形元件）。這是可編輯的 Pen 設計元件庫，屬視覺參考；不是產品程式元件或正式 UX 驗收結果。

- [元件庫檔案](hub-bottom-components.lib.pen)
- [元件總覽](hub-bottom-assets/library-preview@2x.png)
- [完整底部預覽](hub-bottom-assets/bottom-preview@2x.png)
- [導覽文字外框放大檢查](hub-bottom-assets/nav-outline-detail@12x.png)
- [元件 ID、來源對照與素材雜湊](hub-bottom-assets/manifest.json)
- [Figma 來源：Frame 57，113:3581](https://www.figma.com/design/G5qDSKMMzOrJNd3HTv8hai/Untitled?node-id=113-3581)，擷取日期：2026-09-23。

## 元件清單

| 名稱 | 尺寸（px） | 內容 |
|---|---|---|
| `Hub/Icon/City` | 56 × 56 | 使用指定 Popboard v1 的 city.png。 |
| `Hub/Nav/Label` | 67 × 20 | 城市文字標籤，含 1.5px 黑色外框。 |
| `Hub/Nav/Glyph` | 64 × 17 | 字面與外框共用的可編輯文字；標籤內保留 1.5px 外框空間。 |
| `Hub/Nav/Item` | 67 × 64 | 圖示與標籤的連動實例。 |
| `Hub/Bottom/Backdrop` | 430 × 224 | 透明至深藍的漸層底板。 |
| `Hub/Chat/Guild` | 302 × 33 | 商會訊息，紫藍頻道與發言者文字。 |
| `Hub/Chat/Direct` | 227 × 33 | 私訊訊息，粉紫頻道與發言者文字。 |
| `Hub/Chat/World` | 398 × 50 | 世界訊息，青色頻道與原稿雙行文字。 |
| `Hub/Chat/Stack` | 430 × 128 | 三種訊息主元件的實例，間距 6px。 |
| `Hub/Nav/Bar` | 430 × 84 | 五個導覽項目實例，間距 8px，底部留白 20px。 |
| `Hub/Bottom/Block` | 430 × 224 | 底板、聊天列表與導覽列的完整組合。 |

五個入口共用 `Hub/Nav/Item`，其內再引用圖示與標籤。尺寸、字型與外框結構沿用主元件；每個入口以實例覆寫圖示、字面與全部黑色輪廓的文字。每個來源物件的 Figma ID 可由清單追溯。

## 導覽項目

依使用者於 2026-09-24 指定的順序與本地素材替換。五份 PNG 直接複製，沒有裁切、縮放原檔或重複套用光學校準；顯示框保持 56 × 56px，使用等比例置入。

| 由左至右 | 文字 | 圖示 |
|---|---|---|
| 1 | 城市 | `city.png` |
| 2 | 事件 | `event.png` |
| 3 | 商會 | `shield.png` |
| 4 | 排行 | `ranking.png` |
| 5 | 資產 | `wallet-color.png` |

來源：`assets/icons/popboard-v1/png/`；本庫素材副本位於 `hub-bottom-assets/nav/`，來源路徑與 SHA-256 記錄在清單。

## 使用方式

用 pen.dev 開啟 `.lib.pen` 可檢視及編輯全部主元件。搬移時保留整個 `hub-bottom-assets/nav/` 與檔案的相對位置。

在倉庫根目錄啟動另一份檔案：

```sh
pen interactive --out designs/my-screen.pen
```

在 CLI 互動模式匯入：

```js
import_library({path:"designs/hub-bottom-components.lib.pen"})
get_app_state()
```

工具會回傳元件庫代號及元件 ID。使用回傳值建立 `type: "ref"` 的實例；例如代號為 `H` 時，完整底部元件為 `H:i2XRNO`。不要假設每次匯入的代號相同。聊天文字可覆寫 `Channel and sender`、`Message` 等子圖層；世界訊息另有 `Message continuation`，變更內容後需調整分行。完成後執行 `save()`。

## 來源差異與適用界線

依 [Hub 正式規範](../docs/hub/AI-Tycoon-Hub-UI佈局與RWD行為規範.md) 判定產品要求，本庫保留使用者指定稿的外觀：

| 原稿 | 正式來源 | 影響與待決內容 |
|---|---|---|
| 世界訊息為兩行。 | 第 4.4 節要求每則預覽一行。 | 本庫保存原稿，產品採用前由維護者決定單行摘要內容。 |
| 使用者此次指定城市、事件、商會、排行、資產。 | 第 4.5 節仍記錄大廳、事件、商會、排行、我的。 | 本次授權更新設計元件庫；正式產品目的地條款的同步決策仍由維護者處理。 |
| 430px 固定寬度與原稿樣式值。 | 共用規範及 token；Hub 導讀的待決映射。 | 本庫不新增全域 token；自適應配置、橫向模式與產品映射仍待維護者決定。 |

導覽原稿使用 14px Noto Sans TC Black、1.5px 黑色外側圓角描邊。Pen CLI 儲存時未保留文字原生描邊，因此改用 24 個 `Hub/Nav/Glyph` 的黑色實例，以 1.5px 半徑環繞字面，形成可保存的外框。`Hub/Nav/Glyph` 提供共用字型與字形結構；目前五個入口各自覆寫名稱，修改主元件文字不會蓋過這些覆寫。勿只覆寫其中一個黑色實例。若單一導覽需不同名稱，需在其標籤實例內同時覆寫字面與 24 個輪廓實例的 `content`。

文字保持可編輯；沒有點陣化文字。高倍率輪廓取樣與 Figma 不是逐像素相同。聊天文字未在本次修正範圍內。

## 驗證

已透過 CLI 完成主元件列舉、連動組合與圖層邊界檢查，並檢視元件總覽和完整區塊截圖。另啟動空白 Pen 文件匯入本庫，確認全部 11 個主元件可用，完整區塊的巢狀實例與城市素材可正常顯示。

外框修正後另檢查 12 倍放大圖、五個連動實例與重新開檔後的輪廓保存結果。倉庫檢查命令與結果見交付 PR。尚未執行產品實機 RWD、鍵盤、焦點及無障礙驗收；本庫沒有加入點擊或聊天互動。
