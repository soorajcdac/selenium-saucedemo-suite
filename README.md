# 🧪 Selenium Automated Testing Suite
**Target:** https://www.saucedemo.com  
**Stack:** Python 3.13 • Selenium 4.41 • pytest 9.0 • Chrome  
**Platform:** Windows • Cursor IDE

---

## 📁 Project Structure
```
selenium_suite/
├── config/          # Base URL, credentials, timeouts
├── pages/           # Page Object Model classes
├── tests/           # All test files + conftest.py
├── utils/           # Helpers, screenshot, report utilities
├── reports/         # HTML reports + screenshots + JSON summaries
└── pytest.ini       # pytest configuration
```

---

## ⚡ Quick Start
```bash
# 1. Activate virtual environment
venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run full suite (parallel)
pytest -n 3

# 4. Run smoke tests only
pytest -m smoke

# 5. Open HTML report
start reports\report.html
```

---

## 🧪 Test Coverage — 37 Tests

| Module | Tests | Markers |
|---|---|---|
| `test_login.py` | 5 | smoke, regression |
| `test_inventory.py` | 12 | smoke, regression |
| `test_checkout.py` | 11 | smoke, regression |
| `test_navigation.py` | 9 | smoke, regression |

---

## 🏷️ Running by Marker
```bash
pytest -m smoke          # 16 tests — quick sanity check
pytest -m regression     # 21 tests — full coverage
pytest -m login          # login tests only
pytest -m checkout       # checkout tests only
```

---

## ⚡ Parallel Execution
```bash
pytest -n 3              # 3 workers — ~2.5x faster
pytest -n auto           # auto-detect CPU cores
pytest -m smoke -n 3     # smoke + parallel
```

---

## 📊 Reports

| File | Description |
|---|---|
| `reports/report.html` | Full HTML report with pass/fail |
| `reports/screenshots/` | Auto-captured on test failure |
| `reports/run_summary_*.json` | JSON run history per execution |

---

## 🌐 Test Users (saucedemo.com)

| User | Type |
|---|---|
| `standard_user` | Normal user ✅ |
| `locked_out_user` | Blocked user 🔒 |
| `problem_user` | Buggy UI user 🐛 |
| Password for all | `secret_sauce` |