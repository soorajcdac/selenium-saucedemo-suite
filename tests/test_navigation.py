import pytest
from pages.nav_page import NavPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.helpers import take_screenshot
from config.config import Config


class TestLogout:

    @pytest.mark.smoke
    def test_logout_returns_to_login_page(self, logged_in_driver):
        """Logout should redirect back to the login page."""
        nav = NavPage(logged_in_driver)
        nav.logout()
        assert "saucedemo.com" in logged_in_driver.current_url
        login = LoginPage(logged_in_driver)
        assert login.is_visible(login.LOGIN_BUTTON)

    @pytest.mark.regression
    def test_logout_shows_login_button(self, logged_in_driver):
        """After logout the login button must be visible."""
        nav = NavPage(logged_in_driver)
        nav.logout()
        login = LoginPage(logged_in_driver)
        assert login.is_visible(login.LOGIN_BUTTON), \
            "Login button not visible after logout"

    @pytest.mark.regression
    def test_logout_clears_session(self, logged_in_driver):
        """After logout, login page fields should be present."""
        nav = NavPage(logged_in_driver)
        nav.logout()
        login = LoginPage(logged_in_driver)
        login.navigate()
        assert login.is_visible(login.USERNAME_INPUT)

    @pytest.mark.regression
    def test_login_again_after_logout(self, logged_in_driver):
        """After logout, user should be able to log back in."""
        nav = NavPage(logged_in_driver)
        nav.logout()
        login = LoginPage(logged_in_driver)
        login.navigate()
        login.login(Config.VALID_USER, Config.PASSWORD)
        assert "inventory" in logged_in_driver.current_url


class TestNavigation:

    @pytest.mark.smoke
    def test_app_logo_is_swag_labs(self, logged_in_driver):
        """App logo text should read Swag Labs."""
        nav = NavPage(logged_in_driver)
        assert nav.get_app_logo_text() == "Swag Labs"

    @pytest.mark.smoke
    def test_burger_menu_opens(self, logged_in_driver):
        """Burger menu should open and show logout link."""
        nav = NavPage(logged_in_driver)
        nav.open_menu()
        assert nav.is_visible(nav.LOGOUT_LINK)

    @pytest.mark.regression
    def test_reset_app_state_clears_cart(self, logged_in_driver):
        """After adding items, Reset App State should clear cart."""
        inv = InventoryPage(logged_in_driver)
        inv.add_first_item_to_cart()
        assert inv.get_cart_badge_count() == 1
        nav = NavPage(logged_in_driver)
        nav.reset_app_state()
        assert nav.get_cart_count() == 0

    @pytest.mark.regression
    def test_all_items_link_goes_to_inventory(self, logged_in_driver):
        """All Items menu link should return to inventory page."""
        nav = NavPage(logged_in_driver)
        nav.go_to_cart()
        assert "cart" in logged_in_driver.current_url
        nav.go_to_all_items()
        assert "inventory" in logged_in_driver.current_url

    @pytest.mark.regression
    def test_screenshot_helper_saves_file(self, logged_in_driver):
        """Utils helper take_screenshot() should save a PNG file."""
        path = take_screenshot(logged_in_driver, "test_helper_screenshot")
        import os
        assert os.path.exists(path)
        assert path.endswith(".png")