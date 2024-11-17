# netflix_scraper.py

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
import threading
import requests
from bs4 import BeautifulSoup
import re
import pycountry
import json
from database_connector import connection, handle_mysql_error
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NetflixPriceScraper:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.setup_database()

    def setup_database(self):
        """Initialize the database tables if they don't exist."""
        try:
            cursor = connection.cursor()

            # Create price records table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS price_records (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    timestamp DATETIME NOT NULL
                )
            ''')

            # Create prices table
            cursor.execute('''
                                CREATE TABLE IF NOT EXISTS netflix_prices (
                                    id INT AUTO_INCREMENT PRIMARY KEY,
                                    record_id INT,
                                    country_code VARCHAR(2) NOT NULL,
                                    price_index INT NOT NULL,
                                    price VARCHAR(50) NOT NULL,
                                    FOREIGN KEY (record_id) REFERENCES price_records(id) ON DELETE CASCADE
                                );
            ''')

            connection.commit()
            logger.info("Database tables initialized successfully")

        except Exception as e:
            logger.error(f"Error setting up database: {e}")
            handle_mysql_error(e)

    def get_all_country_codes(self):
        return [country.alpha_2.lower() for country in pycountry.countries]

    def get_all_currency_codes(self):
        currency_codes_2 = [currency.alpha_2 for currency in pycountry.currencies if hasattr(currency, 'alpha_2')]
        currency_codes_3 = [currency.alpha_3 for currency in pycountry.currencies if hasattr(currency, 'alpha_3')]
        return currency_codes_2 + currency_codes_3 + ['czk', 'huf', 'kč']

    def clean_price_string(self, price_string):
        return price_string.replace(",", "")

    def scrape_pricing(self, url, country_code):
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Failed to retrieve {url}: {e}")
            return []

        soup = BeautifulSoup(response.content, 'html.parser')
        pricing_section = soup.find('h3', string=re.compile(r'^Pricing \('))

        if not pricing_section:
            logger.warning(f"No pricing section found for {url}")
            return []

        pricing_paragraph = pricing_section.find_next('p') or pricing_section.find_next(
            'div') or pricing_section.find_next('ul')
        currency_codes = self.get_all_currency_codes()

        prices = re.findall(
            r'(\d+(?:[ ,]\d{3})*(?:[\.,]\d{1,2})?)\s?([€$£₹¥]|' + '|'.join(
                currency_codes) + r')|\s?([€$£₹¥]|' + '|'.join(
                currency_codes) + r')(\d+(?:[ ,]\d{3})*(?:[\.,]\d{1,2})?)', pricing_paragraph.text)

        if not prices:
            price_items = pricing_paragraph.find_all(string=re.compile(r'/\s*month'))
            formatted_prices = []

            for item in price_items:
                parent = item.parent
                price_text = re.search(r'(.*?)/\s*month', parent.text)
                if price_text:
                    price_part = re.search(r'((?:\w+\s+)?\d+(?:[ ,]\d{3})*(?:[\.,]\d{2})?(?:\s+\w+)?)',
                                           price_text.group(1))
                    if price_part:
                        formatted_prices.append(price_part.group(1))

            return formatted_prices

        formatted_prices = []
        for price in prices:
            if price[1]:  # Currency after number
                formatted_prices.append(f"{price[1]}{self.clean_price_string(price[0])}")
            elif price[2]:  # Currency before number
                formatted_prices.append(f"{price[2]}{self.clean_price_string(price[3])}")

        return formatted_prices

    def save_to_database(self, country_prices):
        try:
            cursor = connection.cursor()

            # Get the latest version
            cursor.execute('SELECT MAX(version) FROM price_records')
            latest_version = cursor.fetchone()[0] or 0
            new_version = latest_version + 1

            # Create a new record with timestamp and version
            cursor.execute('INSERT INTO price_records (timestamp, version) VALUES (%s, %s)',
                           (datetime.now(), new_version))
            record_id = cursor.lastrowid

            # Insert all prices
            for country_code, prices in country_prices.items():
                for idx, price in enumerate(prices):
                    cursor.execute('''
                        INSERT INTO netflix_prices (record_id, country_code, price_index, price)
                        VALUES (%s, %s, %s, %s)
                    ''', (record_id, country_code, idx, price))

            # Commit the new version
            connection.commit()
            logger.info(f"Prices saved to database with version {new_version}")

            # Keep only the latest two versions
            cursor.execute('''
                DELETE FROM price_records
                WHERE version NOT IN (
                    SELECT version
                    FROM price_records
                    ORDER BY version DESC
                    LIMIT 2
                )
            ''')
            connection.commit()
            logger.info("Old versions beyond the latest two deleted from database")

        except Exception as e:
            logger.error(f"Error saving to database: {e}")
            handle_mysql_error(e)

    def get_latest_prices(self):
        """Retrieve the latest pricing data from the database."""
        cursor = connection.cursor(dictionary=True)
        try:
            # Get the latest version
            cursor.execute('SELECT id FROM price_records ORDER BY version DESC LIMIT 1')
            latest_record_id = cursor.fetchone()['id']

            # Get the prices associated with the latest record
            cursor.execute('SELECT * FROM netflix_prices WHERE record_id = %s', (latest_record_id,))
            prices = cursor.fetchall()

            return {"record_id": latest_record_id, "prices": prices}

        except Exception as e:
            logger.error(f"Error fetching latest prices: {e}")
            return {"error": "Unable to retrieve data"}
    def scrape_all_prices(self):
        """Scrape prices for all countries and save to database."""
        country_codes = self.get_all_country_codes()
        country_prices = {}

        logger.info("Starting Netflix price scraping...")
        for country_code in country_codes:
            url = f"https://help.netflix.com/en/node/24926/{country_code}"
            prices = self.scrape_pricing(url, country_code)
            if prices:
                country_prices[country_code.upper()] = prices
                logger.info(f"Found prices for {country_code.upper()}")

        if country_prices:
            self.save_to_database(country_prices)

        return country_prices

    def check_existing_data(self):
        """Check if there's any existing price data in the database."""
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM price_records")
        count = cursor.fetchone()[0]
        return count > 0

    def run_scraper(self):
        """Run the scraper in a separate thread."""
        thread = threading.Thread(target=self.scrape_all_prices)
        thread.daemon = True
        thread.start()
        logger.info("Scraper thread started")

    def schedule_scraping(self, hours=24):
        """Schedule regular scraping at specified interval."""
        self.scheduler.add_job(
            self.run_scraper,
            trigger=IntervalTrigger(hours=hours),
            id='netflix_price_scraping',
            name='Scrape Netflix Prices',
            replace_existing=True
        )

        # Start the scheduler
        self.scheduler.start()
        logger.info(f"Scheduled scraping every {hours} hours")

        # Run initial scraping if no data exists
        if not self.check_existing_data():
            logger.info("No existing data found. Running initial scraping...")
            self.run_scraper()
        # Run the scheduled scan if the datat is over 'xx' hours old
        if self.is_data_stale():
            logger.info("Data is stale. Running initial scraping...")
            self.run_scraper()


    def is_data_stale(self):
        """Check if the latest data is older than 24 hours."""
        cursor = connection.cursor()
        cursor.execute("SELECT MAX(timestamp) FROM price_records")
        latest_timestamp = cursor.fetchone()[0]
        if not latest_timestamp:
            return True  # No data exists, so it's stale by default
        return (datetime.now() - latest_timestamp).total_seconds() > 24 * 3600



    def initialize_netflix_scraper(self, hours=24):
        """Initialize the Netflix price scraper with scheduled execution."""
        scraper = NetflixPriceScraper()
        scraper.schedule_scraping(hours)
        return scraper