# IREPS Tender Scraper — Developer Documentation

## 1) Project overview
This repository contains a scraper automation system for IREPS tenders with two runtime fronts:

- **`IREPS_Tenders.py`**: monolithic core scraper engine (Selenium + parsing + export + notification utilities).
- **`IREPS_scraping_gui.py`**: CustomTkinter control panel for config editing, organization management, and running/stopping scraper with streamed logs.

Supporting utilities and assets are in `Program_Files/`.

---

## 2) Repository structure

- `IREPS_Tenders.py` — core automation flow and orchestration.
- `IREPS_scraping_gui.py` — single-window GUI launcher/editor.
- `Program_Files/scraping_library.py` — helper utilities (internet check, cleanup, email utility, etc.).
- `Program_Files/captcha_solver.py` — CNN model definition/training/prediction for captcha.
- `Program_Files/Configration.json` — runtime config state.
- `Program_Files/Organization_list.txt` — active/commented organization controls.
- `requirements.txt` — unified dependencies.
- `run_menu.bat` — local run/bootstrap menu.
- `build_exe.bat` — Windows portable build pipeline.

---

## 3) Runtime architecture

## 3.1 GUI app (`IREPS_scraping_gui.py`)
Key classes:
- `ConfigStore`: resolves project paths, reads/writes config + organizations, selects script or EXE command.
- `PortalCard`: per-organization UI card with active/running/done/error statuses.
- `ScraperRunner`: subprocess wrapper to execute scraper and stream stdout into a thread-safe queue.
- `IREPSScrapingGUI`: main application window; binds UI, persistence, runtime control, and log rendering.

Execution model:
- GUI main thread handles rendering/user interactions.
- scraper runs in worker thread; underlying process output is consumed line-by-line.
- log queue bridges worker thread to UI loop.

## 3.2 Scraper engine (`IREPS_Tenders.py`)
High-level responsibilities:
- load config and organization selections
- initialize runtime directories and state flags
- perform webdriver operations and retries
- parse tender-related web/PDF content
- produce output artifacts
- trigger notifications and housekeeping utilities

The engine imports helper functions from `Program_Files/scraping_library.py` and captcha prediction from `Program_Files/captcha_solver.py`.

---

## 4) Configuration contract

Primary config file: `Program_Files/Configration.json`

Observed keys include:
- mode toggles: `browser`, `adb_device`, `captcha_manual_input`
- device/network: `adb_device_ip`, `mobile_no`
- messaging: `sender_email_id`, `sender_email_password`, `notification_emailids`, `receiver_emailids`
- output/runtime: `dump_location`, `max_org_workers`, `max_zone_workers`
- run-state markers: `signal_datelog`, `signal_ireps`, `otp`, `otp_date`

Notes:
- Scraper mutates some keys (`signal_ireps`, `signal_datelog`) at startup.
- Keep secrets out of VCS in production use; prefer env override patterns where available.

---

## 5) Dependency model

Install from root:
```bash
pip install -r requirements.txt
```

Highlights:
- Selenium/chromedriver automation
- data export and parsing (`openpyxl`, `XlsxWriter`, `pdfplumber`, `beautifulsoup4`)
- GUI stack (`customtkinter`)
- ML captcha stack (`torch`, `torchvision`, `Pillow`)

The `requirements.txt` comments explicitly describe Python 3.13 compatibility rationale and the choice to avoid legacy TensorFlow/Keras OCR dependencies.

---

## 6) Local development workflow

## 6.1 Setup
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

Or on Windows, use `run_menu.bat` option 1.

## 6.2 Run GUI
```bash
python IREPS_scraping_gui.py
```

## 6.3 Run scraper directly
```bash
python IREPS_Tenders.py
```

## 6.4 Captcha utility (interactive)
```bash
python Program_Files/captcha_solver.py
```

---

## 7) Packaging and distribution

Use `build_exe.bat` to create a portable Windows build.

Pipeline summary:
1. validate Python version (3.10–3.13)
2. install/upgrade build dependencies
3. clear previous build artifacts
4. build `IREPS_Tenders.exe` (PyInstaller onefile)
5. build `IREPS_scraping_gui.exe` (PyInstaller onefile windowed)
6. copy `Program_Files` runtime assets
7. generate portable starter batch + zip archive

Important:
- `Program_Files` must remain adjacent to EXEs in portable deployments.

---

## 8) Coding and maintenance guidance

- Preserve backward compatibility of config keys used by both GUI and engine.
- Avoid long blocking work on GUI main thread; keep runtime in worker/subprocess.
- Prefer bounded retries/timeouts for webdriver and network operations.
- Keep logging human-readable for non-developer operators.
- When adding new config keys, define defaults and migration behavior.

---

## 9) Security considerations

- Treat `sender_email_password`, OTP fields, and any credential-like values as secrets.
- Use environment variables for sensitive overrides where possible.
- Do not commit real credentials or personal data.
- Verify SMTP/auth changes against operational mail provider policies.

---

## 10) Suggested next improvements

- Split monolithic `IREPS_Tenders.py` into modules (config, browser, parsing, output, notifications).
- Add typed config schema validation (e.g., pydantic/dataclass layer).
- Add unit tests for `scraping_library.py` and config parsing.
- Add structured logging and rotating file handlers.
- Add CI for lint + import checks + smoke run.
