# YouTube → NotebookLM 研究工作流 安裝腳本 (Windows PowerShell)
# 適用於 Windows 10/11

$ErrorActionPreference = "Stop"

if (-not (Test-Path "skills\yt-search") -or -not (Test-Path "skills\anything-to-notebooklm")) {
    Write-Host "Error: Must run from project root directory (youtube-to-notebooklm\)" -ForegroundColor Red
    exit 1
}

Write-Host "=== YouTube → NotebookLM 研究工作流 ===" -ForegroundColor Cyan
Write-Host ""

# 1. 安裝 Python 依賴
Write-Host "[1/3] 安裝 Python 依賴..." -ForegroundColor Yellow
try {
    pip install "yt-dlp>=2024.0" "notebooklm-py>=0.1" "markitdown>=0.1"
    Write-Host "  ✓ yt-dlp, notebooklm-py, markitdown 安裝完成" -ForegroundColor Green
} catch {
    Write-Host "  ✗ pip install 失敗，請確認 Python 3.10+ 已安裝" -ForegroundColor Red
    exit 1
}
Write-Host ""

# 2. 複製 Skills
$SkillDir = "$env:USERPROFILE\.claude\skills"
if (Test-Path "$env:USERPROFILE\.cursor\skills") {
    $SkillDir = "$env:USERPROFILE\.cursor\skills"
} elseif (Test-Path "$env:USERPROFILE\.windsurf\skills") {
    $SkillDir = "$env:USERPROFILE\.windsurf\skills"
}

Write-Host "[2/3] 複製 Skills 到 $SkillDir..." -ForegroundColor Yellow

New-Item -ItemType Directory -Force -Path "$SkillDir\yt-search\scripts" | Out-Null
New-Item -ItemType Directory -Force -Path "$SkillDir\anything-to-notebooklm\references" | Out-Null
# Clean up old skill.md if upgrading from v1.x
if (Test-Path "$SkillDir\anything-to-notebooklm\skill.md") { Remove-Item "$SkillDir\anything-to-notebooklm\skill.md" -Force }
New-Item -ItemType Directory -Force -Path "$SkillDir\whisper-transcribe\scripts" | Out-Null
New-Item -ItemType Directory -Force -Path "$SkillDir\whisper-transcribe\references" | Out-Null

Copy-Item "skills\yt-search\skill.md" "$SkillDir\yt-search\skill.md" -Force
Copy-Item "skills\yt-search\scripts\parse_vtt.py" "$SkillDir\yt-search\scripts\parse_vtt.py" -Force
Copy-Item "skills\anything-to-notebooklm\SKILL.md" "$SkillDir\anything-to-notebooklm\SKILL.md" -Force
Copy-Item "skills\anything-to-notebooklm\references\examples.md" "$SkillDir\anything-to-notebooklm\references\examples.md" -Force
Copy-Item "skills\anything-to-notebooklm\references\generate-options.md" "$SkillDir\anything-to-notebooklm\references\generate-options.md" -Force
Copy-Item "skills\anything-to-notebooklm\references\troubleshooting.md" "$SkillDir\anything-to-notebooklm\references\troubleshooting.md" -Force
Copy-Item "skills\anything-to-notebooklm\references\windows-setup.md" "$SkillDir\anything-to-notebooklm\references\windows-setup.md" -Force
Copy-Item "skills\whisper-transcribe\skill.md" "$SkillDir\whisper-transcribe\skill.md" -Force
Copy-Item "skills\whisper-transcribe\scripts\transcribe.py" "$SkillDir\whisper-transcribe\scripts\transcribe.py" -Force
Copy-Item "skills\whisper-transcribe\scripts\translate_srt.py" "$SkillDir\whisper-transcribe\scripts\translate_srt.py" -Force
Copy-Item "skills\whisper-transcribe\references\setup.md" "$SkillDir\whisper-transcribe\references\setup.md" -Force

Write-Host "  ✓ yt-search + anything-to-notebooklm + whisper-transcribe Skills 已安裝" -ForegroundColor Green
Write-Host ""

# 3. NotebookLM 登入
Write-Host "[3/3] NotebookLM 登入..." -ForegroundColor Yellow
Write-Host "  執行 notebooklm login 開啟瀏覽器登入 Google 帳號"
Write-Host "  （登入一次即可，之後不用再登）"
Write-Host ""
notebooklm login
Write-Host ""

# 驗證
Write-Host "=== 驗證安裝 ===" -ForegroundColor Cyan
Write-Host -NoNewline "  yt-dlp: "; yt-dlp --version
try { Write-Host -NoNewline "  notebooklm: "; notebooklm --version } catch { Write-Host "  notebooklm: (installed)" }
try { Write-Host -NoNewline "  markitdown: "; markitdown --version } catch { Write-Host "  markitdown: (installed)" }
Write-Host ""
Write-Host "✓ 安裝完成！重啟你的 AI Agent 即可使用。" -ForegroundColor Green
Write-Host ""
Write-Host "試試看："
Write-Host '  「幫我搜 YouTube 上關於 cold pressed juice 的影片」'
Write-Host '  「把這個影片上傳到 NotebookLM 生成播客 https://youtube.com/watch?v=...」'
