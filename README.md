# Cobee Scraper

Cobee is a popular platform utilized by numerous employers across Spain to offer flexible compensation plans to their employees. A notable limitation of Cobee, however, is its lack of functionality for exporting transaction data directly from the platform. The Cobee Scraper project is designed to bridge this gap, providing users with a convenient means to extract their transactions data for personal analysis and record-keeping.

## Usage

1. Create virtual environment. `python -m venv .venv`
2. Activate virtual environment. `source .venv/bin/activate`
3. Install dependencies. `pip install -r requirements.txt`
4. Create `.env` file and provide login credentials. `cp .env.example .env`
5. Run script. `python main.py`

## Technologies

- Python 3.10.13: The core programming language used.
- Selenium: A powerful tool for automating web browsers, enabling the script to interact with the Cobee platform as a human user would.
- Helium: A high-level wrapper for Selenium that simplifies browser automation tasks.
- Beautiful Soup: A library for parsing HTML documents, facilitating the extraction of transaction data from web pages.

## Disclaimer

This tool is intended for educational purposes only. It is crucial to be aware that the use of web scrapers may be restricted by some websites. Users should consult Cobee's terms of service and use the Cobee Scraper responsibly and ethically. The developers of this script do not condone unauthorized or unethical use of the tool and will not be liable for any consequences resulting from such use.
