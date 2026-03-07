# whisper-transcribe 安裝指南

## 本地模式（faster-whisper + GPU）

### NVIDIA GPU（推薦）

```bash
pip install faster-whisper
```

需要：
- NVIDIA GPU，6GB+ VRAM（large-v3 需要 10GB）
- CUDA 12 + cuDNN 9（通常隨 PyTorch 一起安裝）

驗證 GPU 可用：

```python
import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))
```

### CPU only

同樣 `pip install faster-whisper`，使用時加 `--device cpu`。速度慢很多（1 小時音頻約需 15 分鐘），但不需要 GPU。

### 模型選擇

| 模型 | 大小 | VRAM | 品質 | 適用場景 |
|------|------|------|------|---------|
| `tiny` | 40MB | 1GB | 一般 | 快速預覽 |
| `base` | 140MB | 2GB | 中等 | 輕量使用 |
| `small` | 460MB | 3GB | 好 | 日常使用 |
| `medium` | 1.5GB | 5GB | 很好 | 多語言 |
| `large-v3` | 3GB | 10GB | 最佳 | 預設推薦 |

模型會在首次使用時自動下載。

## 雲端模式（Groq API）

```bash
pip install groq
```

設定 API Key：

```bash
export GROQ_API_KEY="your-key-here"
```

取得 Key：https://console.groq.com/keys

Groq Whisper 每日有免費額度，超過後按量計費。速度極快（300x realtime）。

## 翻譯引擎

### DeepL（推薦，品質最佳）

```bash
pip install deepl
export DEEPL_API_KEY="your-key-here"
```

免費方案：每月 50 萬字元。取得 Key：https://www.deepl.com/pro-api

### OpenAI 相容 API（Claude、GPT 等）

```bash
pip install openai
export OPENAI_API_KEY="your-key-here"
export OPENAI_BASE_URL="https://api.openai.com/v1"  # 或 Anthropic/其他
export OPENAI_MODEL="gpt-4o-mini"  # 可改為其他模型
```

## 投遞設定

### Gmail

Claude Code 用戶：已有 Gmail MCP，可直接使用 `gmail_create_draft`。

其他 Agent：需設定 Gmail API 或 SMTP。

### Google Drive

選項 1 — `rclone`（推薦）：

```bash
# 安裝（選一）
brew install rclone          # macOS
sudo apt install rclone      # Ubuntu/Debian
winget install Rclone.Rclone  # Windows

# 設定 Google Drive
rclone config  # 選 Google Drive，按指示授權
# 上傳
rclone copy ./transcript.srt gdrive:/Transcripts/
```

選項 2 — `gdrive` CLI：

```bash
# 安裝 https://github.com/glotlabs/gdrive
gdrive files upload ./transcript.srt --parent <folder_id>
```

## 音頻下載依賴

yt-dlp 下載音頻時需要 ffmpeg（用於格式轉換）：

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Windows (winget)
winget install ffmpeg

# Windows (choco)
choco install ffmpeg
```
