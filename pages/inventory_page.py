from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class InventoryPage(BasePage):
    # Locators
    PAGE_TITLE       = (By.CLASS_NAME, "title")
    INVENTORY_ITEMS  = (By.CLASS_NAME, "inventory_item")
    ITEM_NAMES       = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICES      = (By.CLASS_NAME, "inventory_item_price")
    ADD_TO_CART_BTNS = (By.CSS_SELECTOR, "button[data-test^='add-to-cart']")
    CART_BADGE       = (By.CLASS_NAME, "shopping_cart_badge")
    CART_ICON        = (By.CLASS_NAME, "shopping_cart_link")
    SORT_DROPDOWN    = (By.CLASS_NAME, "product_sort_container")
    BURGER_MENU      = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK      = (By.ID, "logout_sidebar_link")

    def get_page_title(self):
        """Return the page heading text."""
        return self.get_text(self.PAGE_TITLE)

    def get_item_count(self):
        """Return total number of products displayed."""
        items = self.driver.find_elements(*self.INVENTORY_ITEMS)
        return len(items)

    def get_all_item_names(self):
        """Return list of all product names."""
        elements = self.driver.find_elements(*self.ITEM_NAMES)
        return [el.text for el in elements]

    def get_all_prices(self):
        """Return list of all prices as floats."""
        elements = self.driver.find_elements(*self.ITEM_PRICES)
        return [float(el.text.replace("$", "")) for el in elements]

    def add_first_item_to_cart(self):
        """Click Add to Cart on the first product."""
        btns = self.driver.find_elements(*self.ADD_TO_CART_BTNS)
        btns[0].click()

    def add_item_to_cart_by_index(self, index=0):
        """Click Add to Cart on product at given index."""
        btns = self.driver.find_elements(*self.ADD_TO_CART_BTNS)
        btns[index].click()

    def get_cart_badge_count(self):
        """Return number shown on cart icon badge."""
        if self.is_visible(self.CART_BADGE):
            return int(self.get_text(self.CART_BADGE))
        return 0

    def go_to_cart(self):
        """Click the cart icon to open the cart page."""
        self.click(self.CART_ICON)

    def sort_by(self, option):
        """
        Sort products. Options:
        'az' | 'za' | 'lohi' | 'hilo'
        """
        from selenium.webdriver.support.ui import Select
        dropdown = self.driver.find_element(*self.SORT_DROPDOWN)
        Select(dropdown).select_by_value(option)

    def logout(self):
        """Open burger menu and click logout."""
        self.click(self.BURGER_MENU)
        self.click(self.LOGOUT_LINK)