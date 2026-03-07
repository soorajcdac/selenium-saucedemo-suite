import pytest
from pages.login_page import LoginPage
from config.config import Config


class TestLogin:

    @pytest.mark.smoke
    def test_valid_login_opens_inventory(self, driver):
        """Standard user should reach the inventory page."""
        page = LoginPage(driver)
        page.navigate()
        page.login(Config.VALID_USER, Config.PASSWORD)
        assert "inventory" in driver.current_url

    @pytest.mark.smoke
    def test_invalid_password_shows_error(self, driver):
        """Wrong password should show an error message."""
        page = LoginPage(driver)
        page.navigate()
        page.login(Config.VALID_USER, "wrong_password")
        assert page.is_error_displayed()
        assert "Username and password do not match" in \
               page.get_error_message()

    @pytest.mark.regression
    def test_locked_user_cannot_login(self, driver):
        """Locked out user should see a specific error."""
        page = LoginPage(driver)
        page.navigate()
        page.login(Config.LOCKED_USER, Config.PASSWORD)
        assert "Sorry, this user has been locked out" in \
               page.get_error_message()

    @pytest.mark.regression
    def test_empty_username_shows_error(self, driver):
        """Empty username should show a validation error."""
        page = LoginPage(driver)
        page.navigate()
        page.login("", Config.PASSWORD)
        assert page.is_error_displayed()

    @pytest.mark.regression
    def test_empty_password_shows_error(self, driver):
        """Empty password should show a validation error."""
        page = LoginPage(driver)
        page.navigate()
        page.login(Config.VALID_USER, "")
        assert page.is_error_displayed()