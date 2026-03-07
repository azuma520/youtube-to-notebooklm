#!/bin/bash
# YouTube → NotebookLM 研究工作流 安裝腳本
# 適用於 macOS / Linux / Git Bash on Windows

set -e

if [ ! -d "skills/yt-search" ] || [ ! -d "skills/anything-to-notebooklm" ]; then
  echo "Error: Must run from project root directory (youtube-to-notebooklm/)"
  exit 1
fi

echo "=== YouTube → NotebookLM 研究工作流 ==="
echo ""

# 1. 安裝 Python 依賴
echo "[1/3] 安裝 Python 依賴..."
pip install "yt-dlp>=2024.0" "notebooklm-py>=0.1" "markitdown>=0.1" || {
  echo "  ✗ pip install 失敗，請確認 Python 3.10+ 已安裝"
  exit 1
}
echo "  ✓ yt-dlp, notebooklm-py, markitdown 安裝完成"
echo ""

# 2. 偵測 Skills 目標目錄
if [ -d "${HOME}/.cursor/skills" ]; then
  SKILL_DIR="${HOME}/.cursor/skills"
elif [ -d "${HOME}/.windsurf/skills" ]; then
  SKILL_DIR="${HOME}/.windsurf/skills"
else
  SKILL_DIR="${HOME}/.claude/skills"
fi

echo "[2/3] 複製 Skills 到 ${SKILL_DIR}..."

mkdir -p "${SKILL_DIR}/yt-search/scripts"
mkdir -p "${SKILL_DIR}/anything-to-notebooklm/references"
mkdir -p "${SKILL_DIR}/whisper-transcribe/scripts"
mkdir -p "${SKILL_DIR}/whisper-transcribe/references"

cp skills/yt-search/skill.md "${SKILL_DIR}/yt-search/skill.md"
cp skills/yt-search/scripts/parse_vtt.py "${SKILL_DIR}/yt-search/scripts/parse_vtt.py"
cp skills/anything-to-notebooklm/skill.md "${SKILL_DIR}/anything-to-notebooklm/skill.md"
cp skills/anything-to-notebooklm/references/examples.md "${SKILL_DIR}/anything-to-notebooklm/references/examples.md"
cp skills/anything-to-notebooklm/references/troubleshooting.md "${SKILL_DIR}/anything-to-notebooklm/references/troubleshooting.md"
cp skills/whisper-transcribe/skill.md "${SKILL_DIR}/whisper-transcribe/skill.md"
cp skills/whisper-transcribe/scripts/transcribe.py "${SKILL_DIR}/whisper-transcribe/scripts/transcribe.py"
cp skills/whisper-transcribe/scripts/translate_srt.py "${SKILL_DIR}/whisper-transcribe/scripts/translate_srt.py"
cp skills/whisper-transcribe/references/setup.md "${SKILL_DIR}/whisper-transcribe/references/setup.md"
echo "  ✓ yt-search + anything-to-notebooklm + whisper-transcribe Skills 已安裝"
echo ""

# 3. NotebookLM 登入
echo "[3/3] NotebookLM 登入..."
echo "  執行 notebooklm login 開啟瀏覽器登入 Google 帳號"
echo "  （登入一次即可，之後不用再登）"
echo ""
notebooklm login
echo ""

# 驗證
echo "=== 驗證安裝 ==="
echo -n "  yt-dlp: "; yt-dlp --version
echo -n "  notebooklm: "; notebooklm --version 2>/dev/null || echo "(installed)"
echo -n "  markitdown: "; markitdown --version 2>/dev/null || echo "(installed)"
echo ""
echo "✓ 安裝完成！重啟你的 AI Agent 即可使用。"
echo ""
echo "試試看："
echo "  「幫我搜 YouTube 上關於 cold pressed juice 的影片」"
echo "  「把這個影片上傳到 NotebookLM 生成播客 https://youtube.com/watch?v=...」"
