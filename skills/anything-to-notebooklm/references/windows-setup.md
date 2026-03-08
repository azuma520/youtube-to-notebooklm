# Windows 設定指南

## PYTHONUTF8 編碼

notebooklm-py CLI 啟動時會自動設定 `PYTHONUTF8=1`。若仍出現 `UnicodeEncodeError` 或 `cp950` 相關錯誤，手動加前綴：

```bash
PYTHONUTF8=1 notebooklm <command>
```

PowerShell 中：

```powershell
$env:PYTHONUTF8 = "1"; notebooklm <command>
```

## PATH 設定

pip 安裝後，`notebooklm` 執行檔位於：

```
%USERPROFILE%\AppData\Roaming\Python\Python3XX\Scripts\
```

若 `notebooklm` 指令找不到，將上述路徑加入系統 PATH。

確認安裝：

```bash
notebooklm --version
```

## Login 注意事項

`notebooklm login` 需要：
1. **互動終端**（能接收鍵盤輸入）
2. **瀏覽器**（會自動開啟進行 Google 認證）

**Claude Code 中無法直接執行 login**（背景 Bash 不是互動終端）。請用戶在自己的終端操作：

- PowerShell：`notebooklm login`
- Git Bash：`notebooklm login`
- Windows Terminal：`notebooklm login`

登入後的 session 會自動被 Claude Code 的 Bash 繼承。

## 暫存目錄

| 終端 | 變數 | 說明 |
|------|------|------|
| PowerShell | `$env:TEMP` | `C:\Users\<user>\AppData\Local\Temp` |
| Git Bash | `$TEMP` | 通常對應 Windows temp |

markitdown 轉換時的暫存檔路徑：

```bash
# Git Bash
markitdown "file.pptx" -o "$TEMP/converted.md"

# PowerShell
markitdown "file.pptx" -o "$env:TEMP\converted.md"
```

## 檔案路徑

CLI 同時接受正斜線（`/`）和反斜線（`\`），自動處理。路徑含空格時用雙引號包裹：

```bash
notebooklm source add "C:\Users\user\My Documents\file.pdf"
```
