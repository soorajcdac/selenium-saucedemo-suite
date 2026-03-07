from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartPage(BasePage):
    # Locators
    PAGE_TITLE       = (By.CLASS_NAME, "title")
    CART_ITEMS       = (By.CLASS_NAME, "cart_item")
    ITEM_NAMES       = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICES      = (By.CLASS_NAME, "inventory_item_price")
    REMOVE_BUTTONS   = (By.CSS_SELECTOR, "button[data-test^='remove']")
    CONTINUE_BTN     = (By.ID, "continue-shopping")
    CHECKOUT_BTN     = (By.ID, "checkout")

    def get_page_title(self):
        return self.get_text(self.PAGE_TITLE)

    def get_cart_item_count(self):
        """Return number of items currently in cart."""
        items = self.driver.find_elements(*self.CART_ITEMS)
        return len(items)

    def get_cart_item_names(self):
        """Return list of item names in cart."""
        elements = self.driver.find_elements(*self.ITEM_NAMES)
        return [el.text for el in elements]

    def remove_first_item(self):
        """Click Remove on the first cart item."""
        btns = self.driver.find_elements(*self.REMOVE_BUTTONS)
        if btns:
            btns[0].click()

    def continue_shopping(self):
        """Click Continue Shopping to go back to inventory."""
        self.click(self.CONTINUE_BTN)

    def proceed_to_checkout(self):
        """Click Checkout button."""
        self.click(self.CHECKOUT_BTN)

    def is_empty(self):
        """Return True if cart has no items."""
        return self.get_cart_item_count() == 0