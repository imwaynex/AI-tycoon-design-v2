# Hub 導覽列與聊天元件庫

底部元件已拆成兩份獨立的維護來源。兩份庫互不引用，各自保留全部必要子元件；導覽的五項順序、圖示、文字外框及聊天內容保持不變。

| 元件庫 | 主元件 | 文件與預覽 |
|---|---|---|
| [導覽列](hub-nav.lib.pen) | 圖示、標籤、字形、導覽項目、導覽列，共 5 個。 | [維護說明](hub-nav.md) · [預覽](hub-nav-assets/library-preview@2x.png) |
| [聊天](hub-chat.lib.pen) | 商會、私訊、世界訊息及聊天列表，共 4 個；另含 6 個內部文字來源。 | [維護說明](hub-chat.md) · [預覽](hub-chat-preview@2x.png) |

## 組合示例

[hub-bottom-example.pen](hub-bottom-example.pen) 使用兩份元件庫的匯入實例，沒有重複的聊天或導覽主元件。[組合清單](hub-bottom-example.manifest.json)記錄引用與驗證；[底部預覽](hub-bottom-assets/bottom-preview@2x.png)保留 430 × 224px 的配置。

示例只負責漸層底板、12px 間距與兩個元件的位置。底板及完整底部容器不再作為元件庫中的主元件。導覽修改回到 `hub-nav.lib.pen`，聊天修改回到 `hub-chat.lib.pen`，更新後重新載入使用端的元件庫。

搬移示例時，兩份 `.lib.pen` 與示例放在同一層，並攜帶 `hub-nav-assets/`。已在另一個資料夾重開示例，確認相對引用指向搬移後的兩份庫。

## 直向 Hub 主稿

[hub-portrait.pen](hub-portrait.pen) 已遷移聊天及導覽設計，保留對兩份庫的引用。[主稿清單](hub-portrait.manifest.json)記錄節點、尺寸及驗證；預覽提供 [320px](hub-portrait-assets/preview-320@2x.png)、[375px](hub-portrait-assets/preview-375@2x.png)、[430px](hub-portrait-assets/preview-430@2x.png)。

直接調整主畫框 `IRZ3G` 的寬度即可重排。底部及聊天列表使用 `fill_container`；導覽左右各留 16px，五項平均分配剩餘寬度，圖示保持 56px、文字保持 14px。垂直彈性留白讓底部隨裝置高度貼底，保留合計 34px 的底部空間與置中的 Home indicator；此為裝置稿的固定安全區示意，不是執行期環境讀取。

聊天將頻道、發話者及正文合成完整段落，依聊天容器全寬連續換行；第二行回到左側，不再使用固定第二行或右側正文欄。聊天庫內維護完整文字、頻道色彩層及 24 層連動外框，主稿只覆寫三個訊息的寬度，無本地文字排版副本。外框的 1px 重疊輔助列刻意允許內容超出自身，已確認 72 層外框均落在完整文字容器內。

已實測 320、360、375、390、414、430、768px 的底部容器寬度、五項等寬及文字外框邊界；另確認 430 × 568px 時底部仍貼底。320px 時底部高 241px，430px 時高 224px，均不含最下方 14px 的裝置指示區。

此次維護範圍是底部。原有頂部漸變模糊與其 -83px 位移保留，未宣稱整張稿已完成 RWD；也未實作橫向配置切換、鍵盤、焦點或實機安全區。全文換行仍是與正式規範單行摘要的既有差異，產品採用方式由維護者決定。

## 從舊庫移轉

原 `hub-bottom-components.lib.pen` 已由兩份庫取代，不再保留第三份可獨立修改的元件來源。舊檔及歷史預覽可從 Git 歷史取得。

- 既有導覽使用端：匯入新導覽庫，以工具回傳的代號引用 `W42XvN`。
- 既有聊天使用端：匯入新聊天庫，以工具回傳的代號引用 `lIpLK`。
- 既有完整底部使用端：使用組合示例，或以聊天列表與導覽列組合。舊 `Hub/Bottom/Block` 與 `Hub/Bottom/Backdrop` 不再列為主元件。

在倉庫根目錄的 pen.dev CLI 互動模式按需求匯入：

```js
import_library({path:"designs/hub-nav.lib.pen"})
import_library({path:"designs/hub-chat.lib.pen"})
get_app_state()
```

ID 在拆分後保留；元件庫代號依匯入結果而定。既有文件需更新引用，不能只替換檔名。

## 來源與驗證

原始圖層來源：[Figma Frame 57，113:3581](https://www.figma.com/design/G5qDSKMMzOrJNd3HTv8hai/Untitled?node-id=113-3581)。使用者指定的導覽及原稿聊天與正式規範的差異，各自在元件庫維護文件記錄。

已透過 pen.dev CLI 建立兩份庫，檢查主元件數量、內部引用、圖層邊界、匯入、相對路徑及預覽。2026-09-25 拆分時，組合示例匯出的 860 × 448px PNG 與拆分前逐像素一致；2026-09-26 另依原稿補齊聊天文字 1.5px 黑色外框，並更新組合預覽。倉庫檢查命令與結果見交付 PR。

本交付拆分設計維護來源並補齊文字外框，沒有修改正式規範或全域 token，也不代表產品實機 RWD、鍵盤、焦點或無障礙驗收通過。
