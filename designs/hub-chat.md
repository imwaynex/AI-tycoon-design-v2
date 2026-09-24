# Hub 聊天元件庫

[Pen 元件庫](hub-chat.lib.pen) · [預覽](hub-chat-preview@2x.png) · [元件清單](hub-chat.manifest.json) · [底部組合入口](hub-bottom-components.md)

本庫獨立維護三種訊息與聊天列表，不包含導覽元件，也不依賴圖示素材或其他元件庫。

## 主元件

| 元件 | ID | 尺寸（px） |
|---|---|---|
| `Hub/Chat/Guild` | `WtOGb` | 302 × 33 |
| `Hub/Chat/Direct` | `g3Ruw` | 227 × 33 |
| `Hub/Chat/World` | `zy4VC` | 398 × 50 |
| `Hub/Chat/Stack` | `lIpLK` | 430 × 128 |

聊天列表使用三個訊息主元件的連動實例，間距 6px。商會、私訊、世界的頻道色、透明背景與文字均保留拆分前的外觀。

## 使用與維護

從倉庫根目錄的 pen.dev CLI 互動模式匯入：

```js
import_library({path:"designs/hub-chat.lib.pen"})
get_app_state()
```

使用工具回傳的代號與 `lIpLK` 建立聊天列表的 `type: "ref"` 實例。搬移元件庫只需 `.lib.pen`，不需導覽圖示。

`Channel and sender`、`Message` 是可編輯文字；世界訊息另有 `Message continuation`。修改世界訊息內容後需調整分行。頻道共用外觀在相應訊息主元件維護，組合示例只保留引用。

## 驗證與界線

已檢查 4 個主元件、內部引用完整性、沒有影像節點、圖層邊界、匯入與預覽。字型使用 Noto Sans TC；首次載入時，pen.dev 可能需要下載字型。

保留原稿雙行世界訊息；[Hub 正式規範](../docs/hub/AI-Tycoon-Hub-UI佈局與RWD行為規範.md)第 4.4 節要求每則預覽一行，產品採用前由維護者決定摘要內容。本庫是固定 430px 視覺參考，未實作聊天操作，也未執行實機 RWD、鍵盤、焦點或無障礙驗收。
