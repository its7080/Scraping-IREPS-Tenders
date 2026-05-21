# IREPS Tender Scraper — User Guide

## 1) What this tool does
The IREPS Tender Scraper automates tender discovery from the IREPS portal and generates structured outputs (Excel/data dumps) based on your configured organizations and run settings.

You can use it in two ways:
- **Main GUI (`IREPS_scraping_gui.py`)**: configure + run from a single interface.
- **Console engine (`IREPS_Tenders.py`)**: run scraper directly from terminal/cmd.

---

## 2) Prerequisites

### Windows (recommended for regular users)
- Windows 10/11
- Google Chrome installed
- Internet connectivity
- Optional: Android device with ADB enabled (only if your workflow needs mobile OTP/captcha support)

### Python runtime (if running source, not EXE)
- Python **3.10–3.13**
- Ability to install Python packages from `requirements.txt`

> The repository includes `run_menu.bat`, which can create a virtual environment and install dependencies for you.

---

## 3) Quick start (recommended)

1. Open this project folder.
2. Double-click **`run_menu.bat`**.
3. Choose **Option 1** (create/update venv + install requirements).
4. Choose **Option 2** (run GUI).
5. In the GUI:
   - Review/edit configuration fields.
   - Review/edit organization list.
   - Save changes.
   - Start scraper.

---

## 4) Important project files

- `IREPS_scraping_gui.py` → user-facing control panel.
- `IREPS_Tenders.py` → core scraping engine.
- `Program_Files/Configration.json` → runtime configuration.
- `Program_Files/Organization_list.txt` → organizations to include/exclude.
- `Program_Files/captcha_model.pth` → ML model used by captcha solver.
- `Program_Files/captcha_solver.py` → captcha model code and prediction utility.

---

## 5) Configure before first run

Edit the following in **`Program_Files/Configration.json`** (or via GUI config editor):

### Core toggles
- `browser`: browser behavior mode used by scraper.
- `adb_device`: enable/disable ADB-backed flow.
- `captcha_manual_input`: if enabled, allows manual captcha behavior.

### Connectivity / device
- `adb_device_ip`: IP used for ADB-connected device, if enabled.
- `mobile_no`: mobile number used in OTP-related workflows.

### Email notifications
- `sender_email_id`
- `sender_email_password`
- `notification_emailids` (list)
- `receiver_emailids` (list)

### Output and throughput
- `dump_location`: where output data is stored.
- `max_org_workers`: org-level parallelism.
- `max_zone_workers`: zone-level parallelism.

---

## 6) Organization selection

`Program_Files/Organization_list.txt` controls which organizations are scraped:
- Format: `NN: Organization Name`
- Prefix a line with `#` to disable it.

Example:
- `10: RAIL VIKAS NIGAM LIMITED` → active
- `#02: KRCL` → disabled

---

## 7) How to run

## A) GUI mode (recommended)
- Run from `run_menu.bat` option 2, or:
  - `python IREPS_scraping_gui.py`

What you get:
- Config and organization editing
- Live run logs
- Start/stop control
- Status-oriented workflow

## B) Console mode
- `python IREPS_Tenders.py`

Use this for:
- automation scripts
- troubleshooting with full terminal output

---

## 8) Outputs and logs

Expect outputs in your configured dump/output locations (for example under your `dump_location` path and runtime output folders).

For diagnostics, review:
- GUI live logs
- terminal logs (console mode)
- files in `Program_Files` used by runtime

---

## 9) Common issues and fixes

## Issue: GUI starts but scraper does not run
- Verify `IREPS_Tenders.py` exists beside GUI script.
- Ensure dependencies installed (`run_menu.bat` option 1).

## Issue: Browser automation fails
- Ensure Chrome is installed and up to date.
- Re-run dependency install to refresh webdriver helper.
- Close orphan Chrome/driver processes and retry.

## Issue: Email notification not working
- Check sender credentials in config.
- Validate SMTP/network access.
- Confirm recipient lists are not empty.

## Issue: ADB device not detected
- Install Android platform-tools (adb).
- Enable USB debugging on phone.
- Verify connection with `adb devices`.

## Issue: No useful results
- Confirm organizations are enabled (no `#` prefix).
- Check network stability and IREPS site availability.

---

## 10) Portable EXE usage (if built)

If you receive/build the portable package:
- Keep `Program_Files` in the same folder as EXEs.
- Start from `Start_IREPS_Tenders.bat` or `IREPS_scraping_gui.exe`.
- Do not separate `Configration.json`, `Organization_list.txt`, or `captcha_model.pth` from the EXEs.

---

## 11) Safety and operations tips
- Keep secrets (email password, OTP values) private.
- Use a dedicated service mailbox for automation.
- Start with lower worker counts (`max_org_workers`, `max_zone_workers`) before scaling.
- Back up `Configration.json` before large changes.
