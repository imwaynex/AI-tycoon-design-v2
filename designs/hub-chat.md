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

所有頻道名稱、發話者、正文及世界訊息第二行均補上原稿的 1.5px 黑色圓角外框。2026-09-26 直接核對 Figma 文字節點 `113:3584`、`113:3586`、`113:3588`，三者皆為黑色、OUTSIDE、ROUND、1.5px。

## 使用與維護

從倉庫根目錄的 pen.dev CLI 互動模式匯入：

```js
import_library({path:"designs/hub-chat.lib.pen"})
get_app_state()
```

使用工具回傳的代號與 `lIpLK` 建立聊天列表的 `type: "ref"` 實例。搬移元件庫只需 `.lib.pen`，不需導覽圖示。

每則訊息的 `Full message` 包含頻道、發話者與完整正文，使用同一個可用寬度連續換行；第二行從左側文字起點開始。世界訊息不再拆出固定的 `Message continuation`。`Channel color overlay` 只覆蓋第一行的頻道與發話者色彩。

修改正文時只編輯 `Full message`；若修改頻道或發話者，也同步更新 `Channel color overlay`，使其與完整文字的前綴一致。每則完整文字連動 24 個黑色實例，近似 1.5px 圓角外輪廓；三則共 72 層。外框與前景共用相同寬度，因此換行位置相同。重疊輔助列高 1px、間距 -1px，且不裁切；其完整文字均落在外層訊息容器內。

使用端可覆寫三個訊息實例的寬度為 `fill_container`，高度維持 `fit_content`。主稿只需要這三個寬度覆寫，不再保留獨立正文欄或分行文字。舊使用端如有對 `First line`、`Message continuation` 或舊外框子層的覆寫，需移除；公開的四個主元件 ID 不變。字形前綴須能容納於第一行，本次已驗證現有名稱在 320px 以上的主稿寬度。

## 驗證與界線

元件庫包含 4 個主元件與 6 個內部文字來源（3 個完整訊息、3 個頻道色彩層），合計 10 個可重用節點。已檢查內部引用完整性、外框容納範圍、儲存後匯入與預覽。字型使用 Noto Sans TC；首次載入時，pen.dev 可能需要下載字型。

保留原稿全文並依寬度換行；[Hub 正式規範](../docs/hub/AI-Tycoon-Hub-UI佈局與RWD行為規範.md)第 4.4 節要求每則預覽一行，產品採用前由維護者決定摘要內容。本庫是視覺參考，未實作聊天操作，也未執行實機 RWD、鍵盤、焦點或無障礙驗收。
