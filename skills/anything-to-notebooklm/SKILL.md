---
name: anything-to-notebooklm
description: 'Upload content to Google NotebookLM and generate podcasts, slides, mind maps, quizzes, reports, videos, and more. Also browse, search, and query existing notebooks. Supports URLs (web, YouTube), local files (PDF, DOCX, PPTX, XLSX, EPUB, Markdown, images, audio, CSV, JSON, ZIP), AI research, and Google Drive. Use when the user says: "上傳到 NotebookLM", "生成播客", "做成 PPT", "畫思維導圖", "generate podcast", "make slides", "create mind map", "upload to NotebookLM", "做成報告", "出題", "生成 Quiz", "turn this into a podcast", "summarize this as slides", "把這個做成播客", "幫我整理成報告", "ask NotebookLM", "問筆記本", "找之前的筆記本", "NotebookLM 上的", "check my notebooks", "download the podcast", "what notebooks do I have", "搜尋 notebook", "之前的 notebook", "下載播客", "瀏覽筆記本". Activate this skill whenever the user wants to push content to NotebookLM, generate outputs, browse or query existing notebooks, or download previously generated artifacts.'
---

# 多源內容 → NotebookLM 處理器

從多種來源取得內容，上傳到 NotebookLM 生成各類成品；或瀏覽、查詢、提問既有 notebook。

依賴：`notebooklm-py`（CLI v0.3.3+）、`markitdown`（僅限 PPTX/XLSX/EPUB 轉換）。首次使用須 `notebooklm login`。

## Decision Tree

```
用戶請求
├── 想找/瀏覽/查詢/下載既有 notebook 或成品？
│   └── Workflow B：瀏覽 → 閱讀 → 提問
├── 有內容要上傳 / 要生成新東西？
│   └── Workflow A：上傳 → 生成 → 下載
└── 不確定 → 詢問用戶
```

---

## Workflow A：上傳 → 生成 → 下載

### Step 1：識別內容源

| 輸入特徵 | 處理方式 |
|---------|---------|
| YouTube URL | `source add "URL"` → `source wait <id>` |
| 網頁 URL | `source add "URL"` → `source wait <id>` |
| Google Drive 文件 | `source add-drive <file_id> "title"` |
| 本地 `.pdf/.docx/.md/.csv/.txt` | `source add "filepath"` → `source wait <id>` |
| 本地 `.pptx/.xlsx/.epub` | `markitdown "file" -o "$TEMP/converted.md"` → `source add` |
| 本地圖片/音訊 | `source add "filepath"` → `source wait <id>`（自動 OCR/轉錄）|
| 純關鍵詞 | `source add-research "query"`（見下方） |

### Step 2：建立 notebook + 添加來源

```bash
notebooklm create "筆記本標題"
notebooklm source add "來源"          # 上傳來源
notebooklm source wait <source_id>    # 等待處理完成
```

- 一個 notebook 最多 50 個 source，全部 `source wait` 完再生成
- **上傳前確認**：告知用戶即將建立的 notebook 名稱，確認後再執行

### Step 3：生成

**預設行為是非阻塞**（除 mind-map 外）。互動場景加 `--wait` 等待完成。

| 用戶意圖 | 指令 |
|---------|------|
| 播客/音頻 | `generate audio --wait` |
| PPT/簡報 | `generate slide-deck --wait` |
| 思維導圖 | `generate mind-map`（同步，自動等待） |
| Quiz/出題 | `generate quiz --wait` |
| 報告/總結 | `generate report --wait` |
| 視頻 | `generate video --wait` |
| 信息圖 | `generate infographic --wait` |
| 閃卡 | `generate flashcards --wait` |
| 數據表 | `generate data-table "description" --wait` |

用戶沒指定生成什麼 → 只上傳不生成，等後續指令。

各類型的 format/style/length 參數 → 見 [references/generate-options.md](references/generate-options.md)。

### Step 4：下載

```bash
notebooklm download <type> ./output.<ext>
```

常用選項：`--latest`（最新成品）、`--format <fmt>`（輸出格式）、`--all`（全部下載）。

完整下載選項 → 見 [references/generate-options.md](references/generate-options.md)。

### AI 研究搜尋

用戶給的是純關鍵詞時，用 NotebookLM 內建研究功能：

```bash
notebooklm source add-research "query" --mode deep --from web --import-all
notebooklm research wait    # 等待研究完成
```

- `--mode fast`（快速）/ `deep`（深度）
- `--from web`（網路）/ `drive`（Google Drive）

---

## Workflow B：瀏覽 → 閱讀 → 提問

### 瀏覽與切換

```bash
notebooklm list                              # 列出所有 notebook
notebooklm use <id>                          # 切換（支援部分 ID 匹配）
notebooklm status                            # 當前上下文
notebooklm rename "新名稱"                   # 重新命名
```

### 來源管理

```bash
notebooklm source list                       # 來源清單
notebooklm source fulltext <id>              # 完整索引文本
notebooklm source guide <id>                 # AI 摘要
```

### 提問與對話

```bash
notebooklm ask "問題"                        # 對整個 notebook 提問
notebooklm ask "問題" -s <source_id>         # 指定來源提問
notebooklm ask "問題" -c <conversation_id>   # 繼續既有對話
notebooklm ask "問題" --save-as-note --note-title "標題"  # 答案存為筆記
```

### 歷史與成品

```bash
notebooklm history                           # 對話紀錄
notebooklm summary                           # notebook 摘要
notebooklm artifact list                     # 已生成成品清單
notebooklm note list                         # 筆記清單
```

### 分享

```bash
notebooklm share public --enable             # 公開分享
notebooklm share add user@email.com          # 邀請特定用戶
```

---

## NEVER List

- **NEVER** use `source add --wait` — this flag does not exist. Use `source wait <id>` instead
- **NEVER** assume `generate` blocks — it is async by default (except mind-map). Add `--wait` for interactive use
- **NEVER** use `--style retro` — the correct value is `retro-print`
- **NEVER** use 1-based slide index — `revise-slide --slide 0` = first slide (zero-based)
- **NEVER** create a notebook without confirming the name with the user first
- **NEVER** assume audio downloads are `.wav` — the actual format is `.mp4` container
- **NEVER** poll artifact status in the main conversation for extended periods — use a subagent or inform the user of estimated wait time

---

## 整合銜接

- **yt-search**：YouTube URL 直接 `source add`；已有字幕文字檔也可直接 `source add`
- **markitdown**：僅用於 PPTX/XLSX/EPUB（NotebookLM 不直接支援的格式）。PDF/DOCX/MD/CSV/TXT/圖片/音訊直接 `source add`
- **Obsidian vault**：讀取筆記內容後 `source add` 檔案路徑
- **crawl4ai**：反爬蟲網站（X.com 等）先用 crawl4ai 抓取，再 `source add` 本地檔案

## 語言設定

```bash
notebooklm language set zh_Hant    # 繁體中文
notebooklm language set ja         # 日文
```

也可在個別指令加 `--language zh_Hant`。

## 暫存檔清理

生成完成、用戶確認收到輸出後，清理暫存檔：`rm -f "$TEMP"/converted.md`

---

## 參考資料

| 需要什麼 | 看哪裡 |
|----------|--------|
| 生成/下載參數明細 | [references/generate-options.md](references/generate-options.md) |
| 完整工作流範例 | [references/examples.md](references/examples.md) |
| Windows 設定 | [references/windows-setup.md](references/windows-setup.md) |
| 錯誤排查 | [references/troubleshooting.md](references/troubleshooting.md) |
