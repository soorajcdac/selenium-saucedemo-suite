from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    # Locators — saucedemo.com
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON   = (By.ID, "login-button")
    ERROR_MESSAGE  = (By.CSS_SELECTOR, "[data-test='error']")

    def navigate(self):
        """Open the saucedemo login page."""
        from config.config import Config
        self.driver.get(Config.BASE_URL)

    def login(self, username, password):
        """Enter credentials and click login."""
        self.type(self.USERNAME_INPUT, username)
        self.type(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def get_error_message(self):
        """Return the visible error message text."""
        return self.get_text(self.ERROR_MESSAGE)

    def is_error_displayed(self):
        """Return True if an error message is visible."""
        return self.is_visible(self.ERROR_MESSAGE)