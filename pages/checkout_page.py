import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """
    Covers all 3 checkout steps on saucedemo:
      Step 1 — Information (name, postal code)
      Step 2 — Overview    (order summary)
      Step 3 — Complete    (confirmation)
    """

    # ── Step 1: Information ──────────────────────────────────
    PAGE_TITLE      = (By.CLASS_NAME,   "title")
    FIRST_NAME      = (By.ID,           "first-name")
    LAST_NAME       = (By.ID,           "last-name")
    POSTAL_CODE     = (By.ID,           "postal-code")
    CONTINUE_BTN    = (By.ID,           "continue")
    CANCEL_BTN      = (By.ID,           "cancel")
    ERROR_MESSAGE   = (By.CSS_SELECTOR, "[data-test='error']")

    # ── Step 2: Overview ─────────────────────────────────────
    ITEM_TOTAL      = (By.CLASS_NAME, "summary_subtotal_label")
    TAX_LABEL       = (By.CLASS_NAME, "summary_tax_label")
    TOTAL_LABEL     = (By.CLASS_NAME, "summary_total_label")
    FINISH_BTN      = (By.ID,        "finish")
    OVERVIEW_ITEMS  = (By.CLASS_NAME, "cart_item")

    # ── Step 3: Complete ─────────────────────────────────────
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    COMPLETE_TEXT   = (By.CLASS_NAME, "complete-text")
    BACK_HOME_BTN   = (By.ID,        "back-to-products")

    # ── longer wait for slow page transitions ────────────────
    SLOW_WAIT = 30

    # ── Step 1 actions ───────────────────────────────────────
    def get_page_title(self):
        return self.get_text(self.PAGE_TITLE)

    def enter_information(self, first, last, postal):
        """Fill in the checkout information form."""
        self.type(self.FIRST_NAME,  first)
        self.type(self.LAST_NAME,   last)
        self.type(self.POSTAL_CODE, postal)

    def click_continue(self):
        self.click(self.CONTINUE_BTN)

    def click_cancel(self):
        self.click(self.CANCEL_BTN)

    def get_error_message(self):
        return self.get_text(self.ERROR_MESSAGE)

    def is_error_displayed(self):
        return self.is_visible(self.ERROR_MESSAGE)

    def fill_and_continue(self, first="John", last="Doe", postal="12345"):
        """
        Fill form, click Continue, then wait until the
        FINISH button is visible — confirming we are on Overview.
        """
        self.enter_information(first, last, postal)
        time.sleep(0.5)                  # let form settle
        self.click(self.CONTINUE_BTN)

        # Wait for FINISH button — proof we are on Overview page
        WebDriverWait(self.driver, self.SLOW_WAIT).until(
            EC.presence_of_element_located(self.FINISH_BTN)
        )

    # ── Step 2 actions ───────────────────────────────────────
    def get_item_total(self):
        text = self.get_text(self.ITEM_TOTAL)
        return float(text.split("$")[-1])

    def get_tax(self):
        text = self.get_text(self.TAX_LABEL)
        return float(text.split("$")[-1])

    def get_total(self):
        text = self.get_text(self.TOTAL_LABEL)
        return float(text.split("$")[-1])

    def get_overview_item_count(self):
        items = self.driver.find_elements(*self.OVERVIEW_ITEMS)
        return len(items)

    def click_finish(self):
        """
        Click Finish, then wait until COMPLETE_HEADER
        is visible — confirming we reached the confirmation page.
        """
        time.sleep(0.5)
        self.click(self.FINISH_BTN)

        # Wait for confirmation header — proof order is complete
        WebDriverWait(self.driver, self.SLOW_WAIT).until(
            EC.visibility_of_element_located(self.COMPLETE_HEADER)
        )

    # ── Step 3 actions ───────────────────────────────────────
    def get_confirmation_header(self):
        """Return the confirmation page header text."""
        return WebDriverWait(self.driver, self.SLOW_WAIT).until(
            EC.visibility_of_element_located(self.COMPLETE_HEADER)
        ).text

    def get_confirmation_text(self):
        return self.get_text(self.COMPLETE_TEXT)

    def click_back_home(self):
        """Click Back Home and wait until inventory is visible."""
        self.click(self.BACK_HOME_BTN)
        WebDriverWait(self.driver, self.SLOW_WAIT).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "inventory_list")
            )
        )