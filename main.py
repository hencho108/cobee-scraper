import pandas as pd
from helium import Button, click

from src.preprocessing import preprocess_raw_data
from src.scraping import (
    is_previous_month_button_enabled,
    login_sequence,
    scrape_transactions,
    wait_until_page_loaded,
)

RAW_OUTPUT_FILE = "data/transactions_raw.csv"
PROCESSED_OUTPUT_FILE = "data/transactions_processed.csv"


def main():
    """
    Navigates through the transaction pages, collects data, and saves it to a CSV file.
    """
    print("Started scraping...")
    driver = login_sequence()
    all_transactions = []

    while is_previous_month_button_enabled():
        # Ensure the transactions for the current month are loaded
        wait_until_page_loaded(driver)

        # Collect transactions and move to the previous month
        page_transactions = scrape_transactions(driver)
        all_transactions.extend(page_transactions)
        click(Button("Anterior mes"))

    # Save all transactions to a CSV file
    transactions_df_raw = pd.DataFrame(all_transactions)
    transactions_df_raw.to_csv(RAW_OUTPUT_FILE, index=False)
    transactions_df_proc = preprocess_raw_data(RAW_OUTPUT_FILE)
    transactions_df_proc.to_csv(PROCESSED_OUTPUT_FILE, index=False)
    print("Done.")


if __name__ == "__main__":
    main()
