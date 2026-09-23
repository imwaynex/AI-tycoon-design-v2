# Hub 直向 Sites

## RWD 修正

直向模板改為依內容增高的格線與彈性配置，移除固定 700px 最小高度及浮動 UI 的絕對座標。可點入口至少 44 × 44px，間距使用基礎級距，資源文字最低為 12px caption；文字及間距以 rem 取值。安全區在頁面外緣處理，手機面板各自處理自己的外緣。短於 500px 時保留底部導覽，摘要減為一則，必要時允許垂直捲動。

[Token 快照](../sites/hub-portrait/tokens/index.json) 沿用主倉數值；[產生器](../sites/hub-portrait/scripts/export-tokens.py) 產生 [CSS](../sites/hub-portrait/dist/tokens.css)。快照不新增正式 token；原稿色彩、畫幅與裝飾仍屬視覺參考。Hub 橫向模式與全域 token 的待決映射不因此結案。

已檢查 320 × 740px、390 × 844px 無頁面溢出；320 × 480px 可看到底部導覽且僅保留一則預覽。以本地測試副本把根字級設為 200%，確認 320px 寬度無水平溢出、文字可換行，聊天可展開並返回原焦點。此為文字縮放模擬，未取代手機系統文字設定與實機鍵盤／安全區驗收。手機事件面板實測為 390 × 844px、無圓角。

發布沿用網站目前的公開範圍，沒有變更分享權限。以下保留初版交付紀錄，其中私人狀態為初次發布時的狀態。

## 初版交付

- [私人網站](https://ai-tycoon-hub-portrait.imwaynex.chatgpt.site)
- [Figma 畫面來源](https://www.figma.com/design/G5qDSKMMzOrJNd3HTv8hai/Untitled?node-id=87-2)
- [HTML](../sites/hub-portrait/dist/index.html)、[樣式](../sites/hub-portrait/dist/style.css)、[展示互動](../sites/hub-portrait/dist/app.js)
- [Hub 規範及差異入口](../docs/hub/README.md)

## 範圍

依使用者要求先搭建直向畫面，桌面保持置中的直向畫幅。沿用原稿城市、頭像與既有彩色圖標。保留原稿入口名稱與 VIP 排列；此視覺參考未將原稿名稱改為正式規範的名稱。Figma 畫板的整體 20% 不透明度未套用於網站。聊天摘要限制為三則單行，長內容可點擊展開。熱門事件可展開三筆示意資料。其他按鈕只回饋入口名稱，未連接業務頁面、交易、聊天送出或即時資料。

此稿不是正式產品元件或全域 token 範例，不改變 Hub 定稿及其待決事項；城市位置只沿用指定視覺來源。橫向佈局、完整 RWD、字級放大與實機安全區／鍵盤驗收不在本次完成範圍。

## 驗證

已查看 430px 畫幅、390 × 844px 及 320 × 740px 視窗；320px 下所有圖片載入、沒有頁面水平溢位，五項導覽位於可用視窗內。已操作聊天展開與關閉。JavaScript 語法檢查通過。上述結果不代表所有 Hub UX 情境驗收通過。

Sites 已回報私人發布成功；Sites 來源提交為 `ff603725009e58a56a659159ed4298c82a2a5d88`。工作副本與網站來源維持獨立 Git 記錄；發布識別保存在該目錄的 `.openai/hosting.json`。
