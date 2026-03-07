from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage


class NavPage(BasePage):
    """
    Handles the top navigation bar and burger menu
    present on all post-login pages of saucedemo.
    """

    # ── Burger menu ──────────────────────────────────────────
    BURGER_MENU       = (By.ID, "react-burger-menu-btn")
    MENU_CLOSE_BTN    = (By.ID, "react-burger-cross-btn")
    ALL_ITEMS_LINK    = (By.ID, "inventory_sidebar_link")
    ABOUT_LINK        = (By.ID, "about_sidebar_link")
    LOGOUT_LINK       = (By.ID, "logout_sidebar_link")
    RESET_LINK        = (By.ID, "reset_sidebar_link")
    MENU_PANEL        = (By.CLASS_NAME, "bm-menu-wrap")

    # ── Top bar ──────────────────────────────────────────────
    CART_ICON         = (By.CLASS_NAME, "shopping_cart_link")
    CART_BADGE        = (By.CLASS_NAME, "shopping_cart_badge")
    APP_LOGO          = (By.CLASS_NAME, "app_logo")

    # ── Open / close menu ────────────────────────────────────
    def open_menu(self):
        """Click burger menu and wait for it to slide open."""
        self.click(self.BURGER_MENU)
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.LOGOUT_LINK)
        )

    def close_menu(self):
        """Close the burger menu."""
        self.click(self.MENU_CLOSE_BTN)

    def logout(self):
        """Open menu and click Logout — waits for login page."""
        self.open_menu()
        self.click(self.LOGOUT_LINK)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.ID, "login-button")
            )
        )

    def go_to_all_items(self):
        """Navigate back to inventory via All Items link."""
        self.open_menu()
        self.click(self.ALL_ITEMS_LINK)

    def reset_app_state(self):
        """
        Click Reset App State — clears cart and resets
        all Add to Cart buttons back to default.
        """
        self.open_menu()
        self.click(self.RESET_LINK)
        self.close_menu()

    # ── Top bar helpers ──────────────────────────────────────
    def get_cart_count(self):
        """Return cart badge count, 0 if badge not visible."""
        if self.is_visible(self.CART_BADGE):
            return int(self.get_text(self.CART_BADGE))
        return 0

    def go_to_cart(self):
        """Click the cart icon in the top bar."""
        self.click(self.CART_ICON)

    def get_app_logo_text(self):
        """Return the logo text — should be 'Swag Labs'."""
        return self.get_text(self.APP_LOGO)