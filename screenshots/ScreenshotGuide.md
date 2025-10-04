# Windows Step-by-Step Screenshot Guide
## Complete Commands for Windows Users

---

## 🪟 Windows Setup

### Open Command Prompt or PowerShell
**Recommended: Use PowerShell** (better formatting)

**How to open:**
1. Press `Win + X`
2. Select "Windows PowerShell" or "Terminal"
3. Or press `Win + R`, type `powershell`, press Enter

---

## 📁 Current Project Structure
```
code_smell_detector\
├── smelly_code.py
├── test_smelly_code.py
├── smell_detector.py
├── config.yaml
├── docs\
│   └── smells.md
├── README.md
└── Assignment_Report.pdf
```

---

## 🚀 STEP 1: Initial Setup

### Commands (PowerShell):
```powershell
# Navigate to project directory
cd C:\path\to\code_smell_detector
# Replace with your actual path, example:
# cd C:\Users\YourName\Desktop\code_smell_detector

# Verify all files are present
dir

# Or for better view:
Get-ChildItem

# Install dependencies
pip install pyyaml
```

### Commands (Command Prompt - cmd):
```cmd
# Navigate to project directory
cd C:\path\to\code_smell_detector

# Verify all files are present
dir

# Install dependencies
pip install pyyaml
```

### 📸 SCREENSHOT 1: Project Structure
**File Name:** `01_project_structure.png`

**PowerShell Command:**
```powershell
Get-ChildItem
```

**Or CMD Command:**
```cmd
dir
```

**How to take screenshot:**
- Press `Win + Shift + S` (Snipping Tool)
- Or press `PrtScn` key
- Or use `Win + G` (Game Bar) → Screenshot button

**What to capture:**
- The command you typed
- All files listed (smelly_code.py, test_smelly_code.py, etc.)
- docs folder visible

**Expected output (PowerShell):**
```
Directory: C:\Users\YourName\Desktop\code_smell_detector

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----        10/4/2025   2:30 PM                docs
-a----        10/4/2025   2:30 PM           1234 config.yaml
-a----        10/4/2025   2:30 PM           5678 README.md
-a----        10/4/2025   2:30 PM          12345 smell_detector.py
-a----        10/4/2025   2:30 PM           8901 smelly_code.py
-a----        10/4/2025   2:30 PM           4567 test_smelly_code.py
```

---

## 🚀 STEP 2: Run the Smelly Code

### Commands (Both PowerShell & CMD):
```powershell
# Make sure you're in the correct directory
cd

# Run the smelly code
python smelly_code.py
```

### 📸 SCREENSHOT 2: Smelly Code Execution
**File Name:** `02_smelly_code_output.png`

**Command:**
```powershell
python smelly_code.py
```

**What to capture:**
- The command: `python smelly_code.py`
- Complete output:
  - "Library Management System Running..."
  - "Total Books: 2"
  - "Total Members: 2"
  - "Total Transactions: 1"

**Expected output:**
```
Library Management System Running...
Total Books: 2
Total Members: 2
Total Transactions: 1
```

**✅ This proves:** The smelly code runs successfully!

---

## 🚀 STEP 3: Run Unit Tests

### Commands:
```powershell
# Run tests with verbose output
python test_smelly_code.py -v
```

### 📸 SCREENSHOT 3: Unit Test Results
**File Name:** `03_unit_tests_passing.png`

**Command:**
```powershell
python test_smelly_code.py -v
```

**What to capture:**
- Command: `python test_smelly_code.py -v`
- All 8 test names with "ok" status
- Test summary at bottom:
  - "Tests Run: 8"
  - "Successes: 8"
  - "✅ ALL TESTS PASSED!"

**TIP for Windows:** If output is too long, you can:
1. Take multiple screenshots and stitch them
2. Or redirect to file first: `python test_smelly_code.py -v > test_output.txt`
3. Then open test_output.txt and screenshot it

**Expected output:**
```
test_add_book (test_smelly_code.TestLibraryManagementSystem) ... ok
test_calculate_overdue_fees (test_smelly_code.TestLibraryManagementSystem) ... ok
test_checkout_book_success (test_smelly_code.TestLibraryManagementSystem) ... ok
test_checkout_book_unavailable (test_smelly_code.TestLibraryManagementSystem) ... ok
test_generate_member_report (test_smelly_code.TestLibraryManagementSystem) ... ok
test_register_member (test_smelly_code.TestLibraryManagementSystem) ... ok
test_search_books_by_author (test_smelly_code.TestLibraryManagementSystem) ... ok
test_search_books_by_category (test_smelly_code.TestLibraryManagementSystem) ... ok

======================================================================
TEST SUMMARY
======================================================================
Tests Run: 8
Successes: 8
Failures: 0
Errors: 0

✅ ALL TESTS PASSED!
======================================================================
```

---

## 🚀 STEP 4: View Configuration File

### Commands (PowerShell):
```powershell
# Display the configuration file
Get-Content config.yaml

# Or simply:
type config.yaml

# Or open in Notepad:
notepad config.yaml
```

### Commands (CMD):
```cmd
type config.yaml

REM Or open in Notepad:
notepad config.yaml
```

### 📸 SCREENSHOT 4: Configuration File
**File Name:** `04_config_file.png`

**Best approach:** Open in Notepad for clean screenshot
```powershell
notepad config.yaml
```

**What to capture:**
- Notepad window with config.yaml
- All 6 smell types visible
- Thresholds and comments visible

**Alternative:** Use PowerShell command
```powershell
type config.yaml
```

**✅ This proves:** Configurable thresholds with rationale.

---

## 🚀 STEP 5: Run Full Code Smell Detection

### Commands:
```powershell
# Run detector on smelly code
python smell_detector.py smelly_code.py
```

### 📸 SCREENSHOT 5: Full Detection Report
**File Name:** `05_full_detection_console.png`

**Command:**
```powershell
python smell_detector.py smelly_code.py
```

**IMPORTANT for Windows:** The output is LONG. Here's how to handle it:

**Option 1: Scroll and take multiple screenshots**
```powershell
python smell_detector.py smelly_code.py
# Then scroll up and take screenshots of different sections
```

**Option 2: Save to file and view (RECOMMENDED)**
```powershell
# Save output to file
python smell_detector.py smelly_code.py | Out-File -FilePath detection_output.txt

# Then open in Notepad
notepad detection_output.txt
```

**What to capture:**
- Beginning: "Analyzing 1 file(s)..."
- "Active smells: LongMethod, GodClass, ..." (all 6)
- A few smell sections (LongMethod, GodClass, etc.)
- End: "Total Code Smells Found: 17"
- "Report saved to smell_report.txt"

**You can take 2-3 screenshots:**
1. Top of output (header)
2. Middle (showing some smells)
3. Bottom (total count)

---

## 🚀 STEP 6: View Generated Report File

### Commands (PowerShell):
```powershell
# Open report in Notepad
notepad smell_report.txt

# Or view in console:
type smell_report.txt

# Or with paging:
Get-Content smell_report.txt | more
```

### Commands (CMD):
```cmd
notepad smell_report.txt

REM Or:
type smell_report.txt
```

### 📸 SCREENSHOT 6: Report File Content
**File Name:** `06_report_file_content.png`

**Best Command:**
```powershell
notepad smell_report.txt
```

**What to capture:**
- Notepad window showing smell_report.txt
- Header section with "CODE SMELL DETECTION REPORT"
- At least 2-3 smell sections visible
- Clean, formatted view

**Alternative:** If using console, capture sections showing:
- Report header
- 2-3 different smell types with details

---

## 🚀 STEP 7: Test Selective Detection

### Commands:
```powershell
# Run detector for only specific smells
python smell_detector.py smelly_code.py --only LongMethod,GodClass --output selective_report.txt
```

### 📸 SCREENSHOT 7: Selective Detection
**File Name:** `07_selective_detection.png`

**Command:**
```powershell
python smell_detector.py smelly_code.py --only LongMethod,GodClass
```

**What to capture:**
- Command with `--only LongMethod,GodClass`
- Output showing:
  - "Active smells: LongMethod, GodClass" (ONLY these 2)
  - Only 2 smell sections in report
  - "Total Code Smells Found: 2"

**Expected output:**
```
Analyzing 1 file(s)...
Active smells: LongMethod, GodClass

Analyzing: smelly_code.py

================================================================================
CODE SMELL DETECTION REPORT
================================================================================

Active Smells Evaluated: LongMethod, GodClass

Total Code Smells Found: 2

--------------------------------------------------------------------------------
LongMethod: 1 occurrence(s)
--------------------------------------------------------------------------------
  [... details ...]

--------------------------------------------------------------------------------
GodClass: 1 occurrence(s)
--------------------------------------------------------------------------------
  [... details ...]

Report saved to smell_report.txt
```

**✅ This proves:** CLI filtering works!

---

## 🚀 STEP 8: Test Exclusion

### Commands:
```powershell
# Run detector excluding specific smells
python smell_detector.py smelly_code.py --exclude MagicNumbers --output exclude_report.txt
```

### 📸 SCREENSHOT 8: Exclusion Detection
**File Name:** `08_exclusion_detection.png`

**Command:**
```powershell
python smell_detector.py smelly_code.py --exclude MagicNumbers
```

**What to capture:**
- Command with `--exclude MagicNumbers`
- "Active smells:" showing 5 types (NO MagicNumbers)
- "Total Code Smells Found: 5"
- No MagicNumbers section in output

**Expected output:**
```
Analyzing 1 file(s)...
Active smells: LongMethod, GodClass, DuplicatedCode, LargeParameterList, FeatureEnvy

Total Code Smells Found: 5
```

---

## 🚀 STEP 9: View Smells Documentation

### Commands (PowerShell):
```powershell
# View the documentation
notepad docs\smells.md

# Or in console:
type docs\smells.md

# Or:
Get-Content docs\smells.md
```

### Commands (CMD):
```cmd
notepad docs\smells.md

REM Or:
type docs\smells.md
```

### 📸 SCREENSHOT 9: Smells Documentation
**File Name:** `09_smells_documentation.png`

**Best Command:**
```powershell
notepad docs\smells.md
```

**What to capture:**
- Notepad showing docs\smells.md
- At least 2-3 smell descriptions visible
- Line numbers shown
- Justifications visible

---

## 🚀 STEP 10: Verify Line Count

### Commands (PowerShell):
```powershell
# Count lines in smelly_code.py
(Get-Content smelly_code.py).Count

# Or with more details:
Get-Content smelly_code.py | Measure-Object -Line
```

### Commands (CMD):
```cmd
REM Count lines
find /c /v "" smelly_code.py

REM Or use PowerShell from CMD:
powershell "(Get-Content smelly_code.py).Count"
```

### 📸 SCREENSHOT 10: Line Count Verification
**File Name:** `10_line_count.png`

**PowerShell Command:**
```powershell
(Get-Content smelly_code.py).Count
```

**What to capture:**
- The command
- Result showing approximately 250 lines

**Expected output:**
```
250
```

**✅ This proves:** Meets 200-250 LOC requirement!

---

## 🎯 WINDOWS SCREENSHOT SHORTCUTS

### Built-in Windows Screenshot Tools:

1. **Snipping Tool (Best for precise screenshots)**
   - Press `Win + Shift + S`
   - Select area to capture
   - Opens in clipboard, paste to Paint or Word

2. **Print Screen**
   - `PrtScn` - Capture entire screen
   - `Alt + PrtScn` - Capture active window
   - `Win + PrtScn` - Save to Pictures\Screenshots

3. **Game Bar**
   - Press `Win + G`
   - Click camera icon or `Win + Alt + PrtScn`

4. **Snip & Sketch**
   - Press `Win + Shift + S`
   - Choose rectangular, freeform, window, or fullscreen

### Recommended: Use Snipping Tool
```
1. Press Win + Shift + S
2. Select rectangular snip
3. Capture the terminal area
4. Paste into Paint
5. Save as PNG
```

---

## 📊 WINDOWS DEMO SCRIPT

Save this as `demo.bat`:

```batch
@echo off
color 0A
cls

echo =============================================
echo SOFTWARE REENGINEERING - ASSIGNMENT 2
echo Code Smell Detection System Demo
echo Team: Zain, Yusuf, Ahmed
echo =============================================
echo.
echo.

echo [STEP 1] Project Structure
echo Command: dir
echo =============================================
dir
echo.
echo Press any key for next step...
pause > nul
cls

echo [STEP 2] Running Smelly Code
echo Command: python smelly_code.py
echo =============================================
python smelly_code.py
echo.
echo Press any key for next step...
pause > nul
cls

echo [STEP 3] Running Unit Tests
echo Command: python test_smelly_code.py -v
echo =============================================
python test_smelly_code.py -v
echo.
echo Press any key for next step...
pause > nul
cls

echo [STEP 4] Configuration File
echo Command: type config.yaml
echo =============================================
type config.yaml
echo.
echo Press any key for next step...
pause > nul
cls

echo [STEP 5] Full Code Smell Detection
echo Command: python smell_detector.py smelly_code.py
echo =============================================
python smell_detector.py smelly_code.py
echo.
echo Press any key for next step...
pause > nul
cls

echo [STEP 6] Selective Detection
echo Command: python smell_detector.py smelly_code.py --only LongMethod,GodClass
echo =============================================
python smell_detector.py smelly_code.py --only LongMethod,GodClass
echo.
echo Press any key for next step...
pause > nul
cls

echo [STEP 7] Exclusion Detection
echo Command: python smell_detector.py smelly_code.py --exclude MagicNumbers
echo =============================================
python smell_detector.py smelly_code.py --exclude MagicNumbers
echo.
echo.

echo =============================================
echo DEMO COMPLETE!
echo All commands executed successfully.
echo =============================================
echo.
pause
```

### To run the demo:
```cmd
demo.bat
```

---

## 💡 WINDOWS-SPECIFIC TIPS

### Making Terminal Look Better:

**PowerShell:**
```powershell
# Make terminal wider (so output doesn't wrap)
$host.UI.RawUI.WindowSize = New-Object System.Management.Automation.Host.Size(120, 50)

# Or use this at start:
mode con: cols=120 lines=50
```

**CMD:**
```cmd
REM Make window bigger
mode con: cols=120 lines=50
```

### Increase Font Size:
1. Right-click terminal title bar
2. Click "Properties"
3. Go to "Font" tab
4. Select size 16 or 18
5. Click OK

### Change Colors (Optional):
1. Right-click terminal title bar
2. Click "Properties"
3. Go to "Colors" tab
4. Choose high-contrast colors

---

## ✅ WINDOWS PRE-SCREENSHOT CHECKLIST

- [ ] Python installed? Run: `python --version`
- [ ] PyYAML installed? Run: `pip list | findstr PyYAML`
- [ ] In correct directory? Run: `cd` to check
- [ ] Terminal font size 14-16pt
- [ ] Terminal window sized appropriately
- [ ] Close unnecessary programs (clean desktop)

---

## 🎓 QUICK START FOR WINDOWS

**Copy-paste these commands one by one:**

```powershell
# 1. Navigate to project (CHANGE PATH!)
cd C:\Users\YourName\Desktop\code_smell_detector

# 2. Install dependency
pip install pyyaml

# 3. Take Screenshot 1
dir

# 4. Take Screenshot 2
python smelly_code.py

# 5. Take Screenshot 3
python test_smelly_code.py -v

# 6. Take Screenshot 4
notepad config.yaml

# 7. Take Screenshot 5
python smell_detector.py smelly_code.py

# 8. Take Screenshot 6
notepad smell_report.txt

# 9. Take Screenshot 7
python smell_detector.py smelly_code.py --only LongMethod,GodClass

# 10. Take Screenshot 8
python smell_detector.py smelly_code.py --exclude MagicNumbers

# 11. Take Screenshot 9
notepad docs\smells.md

# 12. Take Screenshot 10
(Get-Content smelly_code.py).Count
```

---

## 🚀 YOU'RE READY!

After taking all 10 screenshots, organize them in a folder named `screenshots` and follow the submission guide!

Good luck! 🎉