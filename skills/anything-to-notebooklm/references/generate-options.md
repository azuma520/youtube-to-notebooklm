# 生成與下載參數明細

## 共通生成選項

所有 `generate` 指令都支援：

| 選項 | 說明 |
|------|------|
| `--wait` | 等待生成完成（預設非阻塞，mind-map 除外） |
| `--no-wait` | 強制非阻塞（mind-map 預設同步時可用） |
| `-s <source_id>` / `--source` | 僅用指定來源生成 |
| `--language <code>` | 指定語言（如 `zh_Hant`、`ja`） |
| `--json` | JSON 格式輸出 |
| `--retry N` | 失敗時自動重試 N 次（指數退避） |

---

## Audio 播客

**生成：**

```bash
notebooklm generate audio [options] --wait
```

| 選項 | 值 | 說明 |
|------|----|------|
| `--format` | `deep-dive`（預設）、`brief`、`critique`、`debate` | 對談風格 |
| `--length` | `short`、`default`、`long` | 播客長度 |

**下載：**

```bash
notebooklm download audio ./output.mp4
```

> 注意：音頻實際格式為 `.mp4` 容器，不是 `.wav`。

---

## Video 影片

**生成：**

```bash
notebooklm generate video [options] --wait
```

| 選項 | 值 | 說明 |
|------|----|------|
| `--format` | `explainer`（解說）、`brief`（簡短） | 影片類型 |
| `--style` | `auto`、`classic`、`whiteboard`、`kawaii`、`anime`、`watercolor`、`retro-print`、`heritage`、`paper-craft` | 視覺風格 |

> 注意：風格值是 `retro-print`，不是 `retro`。

**下載：**

```bash
notebooklm download video ./output.mp4
```

---

## Slide Deck 簡報

**生成：**

```bash
notebooklm generate slide-deck [options] --wait
```

| 選項 | 值 | 說明 |
|------|----|------|
| `--format` | `detailed`、`presenter` | 簡報風格 |

**下載：**

```bash
notebooklm download slide-deck ./output.pdf              # 預設 PDF
notebooklm download slide-deck ./output.pptx --format pptx  # 可編輯 PowerPoint
```

### 修改單一投影片

```bash
notebooklm generate revise-slide "修改要求" --artifact <id> --slide <N> --wait
```

> 注意：`--slide` 使用 **zero-based** 索引。`--slide 0` = 第一張投影片。

---

## Report 報告

**生成：**

```bash
notebooklm generate report [options] --wait
```

| 選項 | 值 | 說明 |
|------|----|------|
| `--format` | `briefing-doc`、`study-guide`、`blog-post`、`custom` | 報告類型 |
| `--append` | `"額外指示"` | 附加自訂要求 |

**下載：**

```bash
notebooklm download report ./output.md
```

---

## Quiz 測驗

**生成：**

```bash
notebooklm generate quiz [options] --wait
```

| 選項 | 值 | 說明 |
|------|----|------|
| `--difficulty` | `easy`、`medium`、`hard` | 難度 |
| `--quantity` | `fewer`、`standard`、`more` | 題目數量 |

**下載：**

```bash
notebooklm download quiz ./quiz.json                      # 預設 JSON
notebooklm download quiz ./quiz.md --format markdown       # Markdown
notebooklm download quiz ./quiz.html --format html         # HTML
```

---

## Flashcards 閃卡

**生成：**

```bash
notebooklm generate flashcards [options] --wait
```

| 選項 | 值 | 說明 |
|------|----|------|
| `--difficulty` | `easy`、`medium`、`hard` | 難度 |
| `--quantity` | `fewer`、`standard`、`more` | 數量 |

**下載：**

```bash
notebooklm download flashcards ./cards.json                # 預設 JSON
notebooklm download flashcards ./cards.md --format markdown
notebooklm download flashcards ./cards.html --format html
```

---

## Infographic 信息圖

**生成：**

```bash
notebooklm generate infographic [options] --wait
```

| 選項 | 值 | 說明 |
|------|----|------|
| `--orientation` | `landscape`、`portrait`、`square` | 方向 |
| `--detail` | `concise`、`standard`、`detailed` | 詳細程度 |

**下載：**

```bash
notebooklm download infographic ./output.png
```

---

## Data Table 數據表

**生成：**

```bash
notebooklm generate data-table "表格描述" [options] --wait
```

**下載：**

```bash
notebooklm download data-table ./table.csv
```

---

## Mind Map 思維導圖

**生成：**

```bash
notebooklm generate mind-map    # 預設同步（自動等待）
```

**下載：**

```bash
notebooklm download mind-map ./map.json
```

---

## 共通下載選項

所有 `download` 指令都支援：

| 選項 | 說明 |
|------|------|
| `--latest` | 下載最新成品 |
| `--earliest` | 下載最早成品 |
| `--all` | 下載所有同類型成品 |
| `-a <id>` / `--artifact` | 指定 artifact ID |
| `--name <pattern>` | 按名稱篩選 |
| `--force` | 覆蓋已存在的檔案 |
| `--no-clobber` | 不覆蓋已存在的檔案 |
| `--dry-run` | 預覽下載（不實際下載） |
| `--format <fmt>` | 輸出格式（可用值依類型而異） |
