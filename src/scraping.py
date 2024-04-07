import os
from time import sleep

from bs4 import BeautifulSoup
from dotenv import find_dotenv, load_dotenv
from helium import Button, click, start_chrome, wait_until, write
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# Load environment variables
load_dotenv(find_dotenv())

# Constants for user authentication and browser behavior
START_PAGE = "https://app.cobee.io/sign-up"
EMAIL = os.getenv("COBEE_EMAIL")
PASSWORD = os.getenv("COBEE_PASSWORD")
SHOW_BROWSER = True
WAIT_AFTER_PAGE_LOAD = 3  # Seconds to wait after loading a new page


def login_sequence():
    """
    Opens a browser and logs into Cobee
    """
    driver = start_chrome(START_PAGE, headless=not SHOW_BROWSER)
    wait_until(Button("Entra en Cobee").exists)
    click(Button("Entra en Cobee"))
    write(EMAIL, into="Email address")
    click(Button("Continue"))
    write(PASSWORD, "Password")
    click(Button("Continue"))
    click("Transacciones")
    return driver


def scrape_transactions(driver):
    """
    Scrapes transaction data from the page source using BeautifulSoup.
    """
    soup = BeautifulSoup(driver.page_source, "html.parser")
    transactions = []

    # CSS selector for the transactions container
    # fmt: off
    transaction_selector = "div.flex.flex-col.justify-center.p-4.rounded-3xl.bg-white.max-w-\[600px\] > div"
    date_div_selector = "div.flex.mb-2.mt-4.py-0.px-4.items-center.gap-2.self-stretch"
    date_selector = "p.text-gray-700.text-xs.font-normal.tracking-wider.leading-4"
    description_selector = "p.text-neutrals-gray-900.font-medium.text-sm"
    amount_selector = "p.text-neutrals-gray-900.text-right.font-medium.text-base"
    savings_selector = "p.text-right.text-gray-500.text-xs"
    # fmt: on

    transactions_container = soup.select(transaction_selector)

    for transaction in transactions_container:
        date_div = transaction.select_one(date_div_selector)
        if date_div:
            date = transaction.select_one(date_selector).text

        description = transaction.select_one(description_selector).text
        amount = transaction.select_one(amount_selector).text

        savings_element = transaction.select_one(savings_selector)
        savings = savings_element.text if savings_element else None

        status = None
        for status_class in ["text-info-dark", "text-accent-dark", "text-gray-700"]:
            status_element = transaction.select_one(
                f"p.font-medium.text-xs.{status_class}"
            )
            if status_element:
                status = status_element.text
                break

        transactions.append(
            {
                "date": date,
                "description": description,
                "amount": amount,
                "savings": savings,
                "status": status,
            }
        )

    return transactions


def is_previous_month_button_enabled():
    """
    Checks if the "Previous Month" button is present and enabled.
    """
    try:
        # Attempt to find the "Anterior mes" button and check if it's enabled
        previous_month_button = Button("Anterior mes")
        return previous_month_button.is_enabled()
    except Exception as e:
        # If any error occurs (e.g., element not found), assume the button is not enabled
        return False


def wait_until_page_loaded(driver):
    """
    Ensures the transactions for the current month are loaded
    """
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "p.text-gray-700.text-xs"))
    )
    sleep(WAIT_AFTER_PAGE_LOAD)
