import pytest
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from config.config import Config

# ── Track suite start time for duration reporting ────────────────
_suite_start = time.time()


def get_driver():
    """Create and return a configured Chrome WebDriver instance."""
    options = Options()

    if Config.HEADLESS:
        options.add_argument("--headless")

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-save-password-bubble")
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    })

    drv = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    drv.implicitly_wait(Config.IMPLICIT_WAIT)
    drv.maximize_window()
    return drv


@pytest.fixture(scope="function")
def driver():
    """Fresh browser for every test. Auto-closes after test."""
    drv = get_driver()
    yield drv
    drv.quit()


@pytest.fixture(scope="function")
def logged_in_driver(driver):
    """Driver pre-logged-in as standard_user."""
    from pages.login_page import LoginPage
    page = LoginPage(driver)
    page.navigate()
    page.login(Config.VALID_USER, Config.PASSWORD)
    yield driver


# ── Auto-screenshot on failure ───────────────────────────────────
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report  = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver") or \
                 item.funcargs.get("logged_in_driver")
        if driver:
            os.makedirs("reports/screenshots", exist_ok=True)
            path = f"reports/screenshots/{item.name}.png"
            driver.save_screenshot(path)
            print(f"\n📸 Screenshot saved: {path}")


# ── Suite startup banner ─────────────────────────────────────────
def pytest_configure(config):
    """Print suite info at the start of every run."""
    print("\n")
    print("=" * 60)
    print("  🧪  SELENIUM SUITE — saucedemo.com")
    print(f"  📍  Base URL : {Config.BASE_URL}")
    print(f"  🌐  Browser  : {Config.BROWSER}")
    print(f"  👁️   Headless : {Config.HEADLESS}")
    print("=" * 60)


# ── Suite finish summary ─────────────────────────────────────────
def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Print a rich summary at the end of every run."""
    passed  = len(terminalreporter.stats.get("passed",  []))
    failed  = len(terminalreporter.stats.get("failed",  []))
    error   = len(terminalreporter.stats.get("error",   []))
    skipped = len(terminalreporter.stats.get("skipped", []))
    total   = passed + failed + error
    duration = round(time.time() - _suite_start, 2)

    # Save JSON summary
    from utils.report_helper import save_run_summary
    save_run_summary(passed, failed, duration)

    # Print final banner
    print("\n")
    print("=" * 60)
    print("  📊  TEST RUN COMPLETE")
    print("=" * 60)
    print(f"  ✅  Passed  : {passed}")
    print(f"  ❌  Failed  : {failed}")
    print(f"  ⚠️   Errors  : {error}")
    print(f"  ⏭️   Skipped : {skipped}")
    print(f"  📦  Total   : {total}")
    print(f"  ⏱️   Duration: {duration}s")
    print(f"  🏆  Status  : {'PASS ✅' if failed == 0 else 'FAIL ❌'}")
    print("=" * 60)
    print(f"\n  📄  Report  : reports/report.html")
    print(f"  📸  Screenshots: reports/screenshots/\n")