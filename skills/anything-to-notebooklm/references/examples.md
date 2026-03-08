# anything-to-notebooklm 使用範例

## Workflow A：上傳 → 生成 → 下載

### 範例 1：網頁 → 播客（辯論風格）

```
用戶：把這篇文章生成播客，用辯論方式 https://example.com/article
```

```bash
notebooklm create "Article Discussion"
notebooklm source add "https://example.com/article"
notebooklm source wait <id>
notebooklm generate audio --format debate --wait
notebooklm download audio ./output.mp4
```

### 範例 2：YouTube → 思維導圖

```
用戶：這個視頻幫我畫個思維導圖 https://www.youtube.com/watch?v=abc123
```

```bash
notebooklm create "Video Mind Map"
notebooklm source add "https://www.youtube.com/watch?v=abc123"
notebooklm source wait <id>
notebooklm generate mind-map          # mind-map 預設同步，無需 --wait
notebooklm download mind-map ./mindmap.json
```

### 範例 3：本地 PDF → 可編輯 PPT

```
用戶：把這個 PDF 做成可以編輯的 PPT ~/Documents/research.pdf
```

```bash
notebooklm create "Research Slides"
notebooklm source add "~/Documents/research.pdf"
notebooklm source wait <id>
notebooklm generate slide-deck --format detailed --wait
notebooklm download slide-deck ./slides.pptx --format pptx
```

### 範例 4：混合多源 → 學習指南

```
用戶：把這些一起做成學習指南：
- https://example.com/article
- https://youtube.com/watch?v=xyz
- ~/Documents/research.pdf
```

```bash
notebooklm create "Study Guide"
notebooklm source add "https://example.com/article"
notebooklm source wait <id1>
notebooklm source add "https://youtube.com/watch?v=xyz"
notebooklm source wait <id2>
notebooklm source add "~/Documents/research.pdf"
notebooklm source wait <id3>
notebooklm generate report --format study-guide --wait
notebooklm download report ./guide.md
```

### 範例 5：關鍵詞 AI 研究 → 報告

```
用戶：搜索 'NFC juice market trends' 並生成報告
```

```bash
notebooklm create "NFC Juice Research"
notebooklm source add-research "NFC juice market trends 2026" --mode deep --from web --import-all
notebooklm research wait
notebooklm generate report --format briefing-doc --wait
notebooklm download report ./report.md
```

### 範例 6：生成高難度 Quiz

```
用戶：用這篇文章出一些難的題目 https://example.com/ml-paper
```

```bash
notebooklm create "ML Quiz"
notebooklm source add "https://example.com/ml-paper"
notebooklm source wait <id>
notebooklm generate quiz --difficulty hard --quantity more --wait
notebooklm download quiz ./quiz.md --format markdown
```

### 範例 7：anime 風格影片

```
用戶：把這篇文章做成 anime 風格的短影片 https://example.com/article
```

```bash
notebooklm create "Anime Explainer"
notebooklm source add "https://example.com/article"
notebooklm source wait <id>
notebooklm generate video --format explainer --style anime --wait
notebooklm download video ./video.mp4
```

### 範例 8：繁體中文播客

```
用戶：用繁體中文生成播客
```

```bash
notebooklm language set zh_Hant
notebooklm generate audio --wait
notebooklm download audio ./podcast.mp4    # 注意：音頻實際格式為 .mp4 容器
```

---

## Workflow B：瀏覽 → 閱讀 → 提問

### 範例 9：瀏覽 notebook + 提問

```
用戶：幫我看看之前的 notebook，我想問一些問題
```

```bash
notebooklm list                              # 列出所有 notebook
notebooklm use <id>                          # 切換到目標 notebook
notebooklm source list                       # 查看有哪些來源
notebooklm ask "這些來源的核心論點是什麼？"
```

### 範例 10：對來源提問 + 存為筆記

```
用戶：上傳完之後幫我問一下這篇論文的核心論點是什麼
```

```bash
# 接續上傳步驟後
notebooklm ask "What are the core arguments in this paper?" --save-as-note --note-title "Core Arguments"
```

### 範例 11：繼續對話 + 查看歷史

```
用戶：繼續剛才的對話，再問深一點
```

```bash
notebooklm history                           # 查看對話紀錄，找到 conversation_id
notebooklm ask "Can you elaborate on the second point?" -c <conversation_id>
```

### 範例 12：下載之前的成品

```
用戶：我之前有生成一個播客，幫我下載
```

```bash
notebooklm list                              # 找到 notebook
notebooklm use <id>
notebooklm artifact list                     # 查看成品清單
notebooklm download audio ./podcast.mp4 --latest
```

### 範例 13：跨 notebook 搜尋

```
用戶：我想找之前關於 AI 的 notebook，問一些問題
```

```bash
notebooklm list                              # 列出所有 notebook，找出與 AI 相關的
notebooklm use <id>                          # 切換到目標
notebooklm summary                           # 查看 notebook 摘要確認內容
notebooklm ask "問題"
```
