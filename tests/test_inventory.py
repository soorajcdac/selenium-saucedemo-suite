import pytest
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from config.config import Config


class TestInventory:

    @pytest.mark.smoke
    def test_inventory_page_loads(self, logged_in_driver):
        """After login, inventory page title should be Products."""
        page = InventoryPage(logged_in_driver)
        assert page.get_page_title() == "Products"

    @pytest.mark.smoke
    def test_inventory_shows_six_products(self, logged_in_driver):
        """Saucedemo always shows exactly 6 products."""
        page = InventoryPage(logged_in_driver)
        assert page.get_item_count() == 6

    @pytest.mark.regression
    def test_all_product_names_are_non_empty(self, logged_in_driver):
        """Every product must have a visible name."""
        page  = InventoryPage(logged_in_driver)
        names = page.get_all_item_names()
        assert len(names) == 6
        for name in names:
            assert name.strip() != "", f"Empty product name found!"

    @pytest.mark.regression
    def test_all_prices_are_positive(self, logged_in_driver):
        """Every product price must be a positive number."""
        page   = InventoryPage(logged_in_driver)
        prices = page.get_all_prices()
        for price in prices:
            assert price > 0, f"Invalid price: {price}"

    @pytest.mark.smoke
    def test_add_one_item_updates_cart_badge(self, logged_in_driver):
        """Adding one item should show badge count of 1."""
        page = InventoryPage(logged_in_driver)
        page.add_first_item_to_cart()
        assert page.get_cart_badge_count() == 1

    @pytest.mark.regression
    def test_add_two_items_updates_cart_badge(self, logged_in_driver):
        """Adding two items should show badge count of 2."""
        page = InventoryPage(logged_in_driver)
        page.add_item_to_cart_by_index(0)
        page.add_item_to_cart_by_index(1)
        assert page.get_cart_badge_count() == 2

    @pytest.mark.regression
    def test_sort_price_low_to_high(self, logged_in_driver):
        """Products sorted low→high should be in ascending order."""
        page = InventoryPage(logged_in_driver)
        page.sort_by("lohi")
        prices = page.get_all_prices()
        assert prices == sorted(prices), \
            f"Prices not sorted ascending: {prices}"

    @pytest.mark.regression
    def test_sort_price_high_to_low(self, logged_in_driver):
        """Products sorted high→low should be in descending order."""
        page = InventoryPage(logged_in_driver)
        page.sort_by("hilo")
        prices = page.get_all_prices()
        assert prices == sorted(prices, reverse=True), \
            f"Prices not sorted descending: {prices}"


class TestCart:

    @pytest.mark.smoke
    def test_cart_page_loads(self, logged_in_driver):
        """Cart page title should be Your Cart."""
        inv  = InventoryPage(logged_in_driver)
        inv.add_first_item_to_cart()
        inv.go_to_cart()
        cart = CartPage(logged_in_driver)
        assert cart.get_page_title() == "Your Cart"

    @pytest.mark.smoke
    def test_added_item_appears_in_cart(self, logged_in_driver):
        """Item added from inventory should appear in cart."""
        inv   = InventoryPage(logged_in_driver)
        names = inv.get_all_item_names()
        inv.add_item_to_cart_by_index(0)
        inv.go_to_cart()
        cart       = CartPage(logged_in_driver)
        cart_names = cart.get_cart_item_names()
        assert names[0] in cart_names

    @pytest.mark.regression
    def test_remove_item_from_cart(self, logged_in_driver):
        """Removing only item should leave cart empty."""
        inv = InventoryPage(logged_in_driver)
        inv.add_first_item_to_cart()
        inv.go_to_cart()
        cart = CartPage(logged_in_driver)
        assert cart.get_cart_item_count() == 1
        cart.remove_first_item()
        assert cart.is_empty()

    @pytest.mark.regression
    def test_continue_shopping_returns_to_inventory(self, logged_in_driver):
        """Continue Shopping button should go back to inventory."""
        inv = InventoryPage(logged_in_driver)
        inv.go_to_cart()
        cart = CartPage(logged_in_driver)
        cart.continue_shopping()
        assert "inventory" in logged_in_driver.current_url