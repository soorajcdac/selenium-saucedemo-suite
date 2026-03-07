from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait   = WebDriverWait(driver, 20)

    def click(self, locator):
        """Wait for element to be clickable then click it."""
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator, text):
        """Wait for element then clear and type into it."""
        el = self.wait.until(EC.visibility_of_element_located(locator))
        el.clear()
        el.send_keys(text)

    def get_text(self, locator):
        """Wait for element and return its visible text."""
        return self.wait.until(
            EC.visibility_of_element_located(locator)
        ).text

    def is_visible(self, locator, timeout=5):
        """Return True if element is visible within timeout."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def get_current_url(self):
        return self.driver.current_url

    def get_title(self):
        return self.driver.title