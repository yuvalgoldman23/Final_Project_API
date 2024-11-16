import requests
from bs4 import BeautifulSoup
import re
import pycountry
import json
import sqlite3
from datetime import datetime
import argparse


def get_all_country_codes():
    return [country.alpha_2.lower() for country in pycountry.countries]


def get_all_currency_codes():
    currency_codes_2 = [currency.alpha_2 for currency in pycountry.currencies if hasattr(currency, 'alpha_2')]
    currency_codes_3 = [currency.alpha_3 for currency in pycountry.currencies if hasattr(currency, 'alpha_3')]
    return currency_codes_2 + currency_codes_3 + ['czk', 'huf', 'kč']


def clean_price_string(price_string):
    cleaned_price = price_string.replace(",", "")
    return cleaned_price


def scrape_pricing(url, country_code):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to retrieve {url}: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    pricing_section = soup.find('h3', string=re.compile(r'^Pricing \('))

    if not pricing_section:
        print(f"No pricing section found for {url}")
        return []

    pricing_paragraph = pricing_section.find_next('p') or pricing_section.find_next('div') or pricing_section.find_next(
        'ul')
    currency_codes = get_all_currency_codes()

    prices = re.findall(
        r'(\d+(?:[ ,]\d{3})*(?:[\.,]\d{1,2})?)\s?([€$£₹¥]|' + '|'.join(currency_codes) + r')|\s?([€$£₹¥]|' + '|'.join(
            currency_codes) + r')(\d+(?:[ ,]\d{3})*(?:[\.,]\d{1,2})?)', pricing_paragraph.text)

    if not prices:
        print(f"No recognizable currency symbol found for {url}, trying ' / month' approach.")
        price_items = pricing_paragraph.find_all(string=re.compile(r'/\s*month'))
        formatted_prices = []

        for item in price_items:
            parent = item.parent
            price_text = re.search(r'(.*?)/\s*month', parent.text)
            if price_text:
                price_part = re.search(r'((?:\w+\s+)?\d+(?:[ ,]\d{3})*(?:[\.,]\d{2})?(?:\s+\w+)?)', price_text.group(1))
                if price_part:
                    formatted_prices.append(price_part.group(1))

        return formatted_prices

    formatted_prices = []
    for price in prices:
        if price[1]:  # Currency after number
            formatted_prices.append(f"{price[1]}{clean_price_string(price[0])}")
        elif price[2]:  # Currency before number
            formatted_prices.append(f"{price[2]}{clean_price_string(price[3])}")

    return formatted_prices


def save_to_json(data, filename='netflix_prices.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Data saved to {filename}")


def init_database(db_name='netflix_prices.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS price_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        record_id INTEGER,
        country_code TEXT NOT NULL,
        price_index INTEGER NOT NULL,
        price TEXT NOT NULL,
        FOREIGN KEY (record_id) REFERENCES price_records(id)
    )
    ''')

    conn.commit()
    return conn


def save_to_db(data, db_name='netflix_prices.db'):
    conn = init_database(db_name)
    cursor = conn.cursor()

    # Create a new record with timestamp
    cursor.execute('INSERT INTO price_records (timestamp) VALUES (?)', (datetime.now(),))
    record_id = cursor.lastrowid

    # Insert all prices
    for country_code, prices in data.items():
        for idx, price in enumerate(prices):
            cursor.execute('''
            INSERT INTO prices (record_id, country_code, price_index, price)
            VALUES (?, ?, ?, ?)
            ''', (record_id, country_code, idx, price))

    conn.commit()
    conn.close()
    print(f"Data saved to {db_name}")


def main():
    parser = argparse.ArgumentParser(description='Scrape Netflix prices and save them to JSON or SQLite')
    parser.add_argument('--output', choices=['json', 'sql', 'both', 'print'],
                        default='print', help='Output format (default: print)')
    parser.add_argument('--filename', help='Output filename (without extension)',
                        default='netflix_prices')
    args = parser.parse_args()

    country_codes = get_all_country_codes()
    country_prices = {}

    print("Scraping Netflix prices...")
    for country_code in country_codes:
        url = f"https://help.netflix.com/en/node/24926/{country_code}"
        prices = scrape_pricing(url, country_code)
        if prices:
            country_prices[country_code.upper()] = prices
            print(f"Found prices for {country_code.upper()}")

    if args.output == 'print' or args.output == 'both':
        print("\nPrices:")
        print(json.dumps(country_prices, indent=2, ensure_ascii=False))

    if args.output in ['json', 'both']:
        json_filename = f"{args.filename}.json"
        save_to_json(country_prices, json_filename)

    if args.output in ['sql', 'both']:
        db_filename = f"{args.filename}.db"
        save_to_db(country_prices, db_filename)


if __name__ == "__main__":
    main()