import os
import time
from datetime import datetime
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def take_screenshot(driver, name=None):
    """
    Save a screenshot to reports/screenshots/.
    Returns the file path.
    """
    os.makedirs("reports/screenshots", exist_ok=True)
    ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
    name = name or f"screenshot_{ts}"
    path = f"reports/screenshots/{name}.png"
    driver.save_screenshot(path)
    print(f"\n📸 Screenshot: {path}")
    return path


def select_dropdown_by_text(driver, locator, visible_text):
    """Select a dropdown option by its visible text."""
    el = driver.find_element(*locator)
    Select(el).select_by_visible_text(visible_text)


def select_dropdown_by_value(driver, locator, value):
    """Select a dropdown option by its value attribute."""
    el = driver.find_element(*locator)
    Select(el).select_by_value(value)


def scroll_to_element(driver, element):
    """Scroll the page until element is in view."""
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});",
        element
    )
    time.sleep(0.3)


def wait_for_url(driver, partial_url, timeout=20):
    """Wait until the current URL contains partial_url."""
    WebDriverWait(driver, timeout).until(
        EC.url_contains(partial_url)
    )


def wait_for_element(driver, locator, timeout=20):
    """Wait for element to be visible and return it."""
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(locator)
    )


def get_timestamp():
    """Return a clean timestamp string for file naming."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def clear_and_type(driver, locator, text):
    """Find element, clear it, then type text into it."""
    el = driver.find_element(*locator)
    el.clear()
    el.send_keys(text)


def is_element_present(driver, locator, timeout=5):
    """Return True if element appears within timeout seconds."""
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
        return True
    except Exception:
        return False