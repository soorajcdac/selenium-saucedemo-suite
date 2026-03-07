import pytest
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from config.config import Config


@pytest.fixture
def checkout_ready(logged_in_driver):
    """
    Logs in → adds 1 item → goes to cart → clicks Checkout.
    Lands on Step 1 (Information page).
    """
    inv = InventoryPage(logged_in_driver)
    inv.add_first_item_to_cart()
    inv.go_to_cart()

    cart = CartPage(logged_in_driver)
    cart.proceed_to_checkout()

    yield logged_in_driver


@pytest.fixture
def overview_ready(logged_in_driver):
    """
    Logs in → adds item → cart → checkout → fills info → lands on Overview.
    """
    inv = InventoryPage(logged_in_driver)
    inv.add_first_item_to_cart()
    inv.go_to_cart()

    cart = CartPage(logged_in_driver)
    cart.proceed_to_checkout()

    # fill_and_continue now waits for step-two URL internally
    checkout = CheckoutPage(logged_in_driver)
    checkout.fill_and_continue("John", "Doe", "12345")

    yield logged_in_driver


class TestCheckoutInformation:

    @pytest.mark.smoke
    def test_checkout_step1_page_loads(self, checkout_ready):
        """Step 1 page title should be Checkout: Your Information."""
        page = CheckoutPage(checkout_ready)
        assert "Checkout: Your Information" in page.get_page_title()

    @pytest.mark.smoke
    def test_valid_info_proceeds_to_overview(self, checkout_ready):
        """Valid info should advance to Step 2 overview page."""
        page = CheckoutPage(checkout_ready)
        page.fill_and_continue("Jane", "Doe", "94105")
        assert "Checkout: Overview" in page.get_page_title()

    @pytest.mark.regression
    def test_missing_firstname_shows_error(self, checkout_ready):
        """Empty first name should show a validation error."""
        page = CheckoutPage(checkout_ready)
        page.enter_information("", "Doe", "12345")
        page.click_continue()
        assert page.is_error_displayed()
        assert "First Name is required" in page.get_error_message()

    @pytest.mark.regression
    def test_missing_lastname_shows_error(self, checkout_ready):
        """Empty last name should show a validation error."""
        page = CheckoutPage(checkout_ready)
        page.enter_information("Jane", "", "12345")
        page.click_continue()
        assert page.is_error_displayed()
        assert "Last Name is required" in page.get_error_message()

    @pytest.mark.regression
    def test_missing_postal_shows_error(self, checkout_ready):
        """Empty postal code should show a validation error."""
        page = CheckoutPage(checkout_ready)
        page.enter_information("Jane", "Doe", "")
        page.click_continue()
        assert page.is_error_displayed()
        assert "Postal Code is required" in page.get_error_message()

    @pytest.mark.regression
    def test_cancel_returns_to_cart(self, checkout_ready):
        """Cancel on Step 1 should return to cart page."""
        page = CheckoutPage(checkout_ready)
        page.click_cancel()
        assert "cart" in checkout_ready.current_url


class TestCheckoutOverview:

    @pytest.mark.smoke
    def test_overview_page_loads(self, overview_ready):
        """Step 2 title should be Checkout: Overview."""
        page = CheckoutPage(overview_ready)
        assert "Checkout: Overview" in page.get_page_title()

    @pytest.mark.smoke
    def test_total_equals_subtotal_plus_tax(self, overview_ready):
        """Total must equal item subtotal + tax exactly."""
        page     = CheckoutPage(overview_ready)
        subtotal = page.get_item_total()
        tax      = page.get_tax()
        total    = page.get_total()
        expected = round(subtotal + tax, 2)
        assert round(total, 2) == expected, \
            f"Total {total} != subtotal {subtotal} + tax {tax}"

    @pytest.mark.smoke
    def test_finish_completes_order(self, overview_ready):
        """Clicking Finish should reach the confirmation page."""
        page = CheckoutPage(overview_ready)
        page.click_finish()
        header = page.get_confirmation_header()
        assert "Thank you for your order" in header, \
            f"Unexpected header: '{header}'"

    @pytest.mark.regression
    def test_confirmation_page_has_back_home_button(self, overview_ready):
        """After order, Back Home button should return to inventory."""
        page = CheckoutPage(overview_ready)
        page.click_finish()
        page.click_back_home()
        assert "inventory" in overview_ready.current_url


class TestCheckoutEndToEnd:

    @pytest.mark.smoke
    def test_full_checkout_flow(self, logged_in_driver):
        """
        Complete end-to-end: login → add item → cart →
        checkout info → overview → finish → confirm → home.
        """
        # 1. Add item
        inv = InventoryPage(logged_in_driver)
        inv.add_first_item_to_cart()
        assert inv.get_cart_badge_count() == 1

        # 2. Go to cart
        inv.go_to_cart()
        cart = CartPage(logged_in_driver)
        assert cart.get_cart_item_count() == 1

        # 3. Checkout info
        cart.proceed_to_checkout()
        checkout = CheckoutPage(logged_in_driver)
        checkout.fill_and_continue("John", "Doe", "12345")

        # 4. Overview — verify totals
        assert "Overview" in checkout.get_page_title()
        assert checkout.get_total() > 0

        # 5. Finish — waits for checkout-complete URL internally
        checkout.click_finish()
        assert "Thank you for your order" in \
               checkout.get_confirmation_header()

        # 6. Back home — waits for inventory URL internally
        checkout.click_back_home()
        assert "inventory" in logged_in_driver.current_url