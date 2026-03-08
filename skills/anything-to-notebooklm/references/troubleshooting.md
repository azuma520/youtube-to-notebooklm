# anything-to-notebooklm 故障排查

## 快速診斷

遇到問題時，先跑這三個指令確認狀態：

```bash
notebooklm auth check --test    # 認證狀態
notebooklm status               # 當前 notebook 上下文
notebooklm artifact list        # 成品狀態
```

## 錯誤對照表

| 症狀 | 原因 | 修復 |
|------|------|------|
| "Not logged in" | session 過期 | `notebooklm login`（需在用戶自己的終端執行） |
| login 開不了瀏覽器 | 非互動終端（Claude Code 背景 Bash） | 請用戶在自己的終端（PowerShell / Terminal）執行 `notebooklm login` |
| DPAPI cookie 解密失敗 | Chrome/Edge 加密 cookie 無法存取 | 用 `notebooklm login` 重新認證（不依賴瀏覽器 cookie） |
| "No notebook context" | 沒有 active notebook | `notebooklm list` → `notebooklm use <id>` |
| GENERATION_FAILED | 速率限制 / 配額用盡 | 等待 5-10 分鐘，重新生成時加 `--retry 3` |
| 成品狀態 PENDING 超過 10 分鐘 | 服務端排隊 | `artifact list` 確認狀態；長時間無進展則到 NotebookLM 網頁端操作 |
| 下載失敗 | artifact 未完成 | `artifact list` 確認狀態為 COMPLETED 後再下載 |
| 來源內容不對（X.com 等） | 反爬蟲網站 | 先用 crawl4ai 抓取完整內容，再 `source add` 本地檔案 |
| markitdown 轉換失敗 | 未安裝 / 路徑有空格 | `pip install markitdown`；檔案路徑用雙引號包裹 |
| UnicodeEncodeError / cp950 | Windows 終端編碼問題 | 見 [windows-setup.md](windows-setup.md) |

## 來源上傳後生成失敗

1. 確認來源內容足夠（< 100 字效果差）
2. 確認來源已處理完成（用 `source wait <id>` 等待，不要跳過）
3. 內容過長（> 50 萬字）可能超時
4. 嘗試 `--retry 3` 重新生成

## markitdown 使用時機

| 格式 | 需要 markitdown？ |
|------|-------------------|
| PDF / DOCX / MD / CSV / TXT | 不需要 — 直接 `source add` |
| 圖片 / 音訊 | 不需要 — 直接 `source add`（自動 OCR / 轉錄） |
| PPTX / XLSX / EPUB | **需要** — 先 `markitdown` 轉 Markdown 再上傳 |

## 速率限制

- 每次請求間隔 > 2 秒
- 同時進行的生成任務最多 3 個
- 遇到限流時，用 `--retry 3` 自動指數退避重試

## 除錯模式

遇到難以診斷的問題，啟用詳細日誌：

```bash
NOTEBOOKLM_LOG_LEVEL=DEBUG notebooklm <command>
```

## 跨平台暫存目錄

| 平台 | 變數 | 典型路徑 |
|------|------|---------|
| Windows (PowerShell) | `$env:TEMP` | `C:\Users\<user>\AppData\Local\Temp` |
| Windows (Git Bash) | `$TEMP` | `/tmp` 或 Windows temp |
| macOS / Linux | `$TMPDIR` 或 `/tmp` | `/tmp` |

Agent 會自動處理，但手動執行指令時用對應平台的變數。
