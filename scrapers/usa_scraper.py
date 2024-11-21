import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import re
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import threading
from database_connector import connection_pool , semaphore, handle_mysql_error

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class USAScraper:
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
                    timestamp DATETIME NOT NULL,
                    version INT NOT NULL
                )
            ''')

            # Create streaming services prices table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS streaming_prices (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    record_id INT,
                    service_name VARCHAR(100) NOT NULL,
                    cheapest_price DECIMAL(10,2) NOT NULL,
                    FOREIGN KEY (record_id) REFERENCES price_records(id) ON DELETE CASCADE
                )
            ''')

            connection.commit()
            logger.info("Database tables initialized successfully")

        except Exception as e:
            logger.error(f"Error setting up database: {e}")
            handle_mysql_error(e)

    def get_cheapest_prices(self, url, month_input, year_input):
        """Scrape and return cheapest streaming service prices"""
        headers = {
            'User-Agent': 'Chrome/41.0.2272.96 Mobile Safari/537.36 (compatible ; Googlebot/2.1 ; +http://www.google.com/bot.html)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'en-US,en;q=0.9,he;q=0.8',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Referer': 'https://www.google.com/',
            'Sec-CH-UA': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
            'Sec-CH-UA-Arch': '',
            'Sec-CH-UA-Full-Version-List': '"Chromium";v="130.0.6723.117", "Google Chrome";v="130.0.6723.117", "Not?A_Brand";v="99.0.0.0"',
            'Sec-CH-UA-Mobile': '?1',
            'Sec-CH-UA-Model': '"Nexus 5"',
            'Sec-CH-UA-Platform': '"Android"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'X-Forwarded-For': '66.249.66.1'
        }

        try:
            response = requests.get(url, headers=headers)
            print("Status Code:", response.status_code)  # Check the response status
        except requests.RequestException as e:
            logger.error(f"Failed to retrieve {url}: {e}")
            return None

        if response.status_code != 200:
            print("Failed to retrieve the webpage.")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')

        # Check date validation
        date_text = soup.get_text().lower()
        date_pattern = r"costs as of (\w+) (\d{4})"
        date_match = re.search(date_pattern, date_text)

        if date_match:
            page_month = date_match.group(1)
            page_year = int(date_match.group(2))

            input_date = datetime(year_input, datetime.strptime(month_input, '%B').month, 1)
            page_date = datetime(page_year, datetime.strptime(page_month, '%B').month, 1)

            if page_date <= input_date and self.check_existing_data():
                print(f"Page data is older or the same as the input: {month_input} {year_input}. No scraping.")
                return None

            print(f"Page data is from: {page_month} {page_year}")
        else:
            print("No 'costs as of' date found on the page.")
            return None

        service_rows = soup.find_all('tr')
        print(f"Found {len(service_rows)} rows.")

        services = []
        prices = []

        for row in service_rows:
            cols = row.find_all('td')
            if len(cols) > 1:  # Skip header or empty rows
                service_name = cols[0].text.strip()
                basic_ads_price = cols[1].text.strip().replace('$', '').replace(',', '')
                ad_free_price = cols[2].text.strip().replace('$', '').replace(',', '')

                # Handle price conversion
                try:
                    basic_ads_price = float(basic_ads_price) if basic_ads_price else float('inf')
                except ValueError:
                    basic_ads_price = float('inf')

                try:
                    ad_free_price = float(ad_free_price) if ad_free_price else float('inf')
                except ValueError:
                    ad_free_price = float('inf')

                # Find the cheapest price
                cheapest_price = min(basic_ads_price, ad_free_price)
                services.append(service_name)
                prices.append(cheapest_price)

        if services:  # Check if data was found
            return pd.DataFrame({'Service': services, 'Cheapest Price': prices})
        else:
            print("No service data found.")
            return None

    def save_to_database(self, services_prices):
        """Save scraped prices to database"""
        try:
            cursor = connection.cursor()

            # Get the latest version
            cursor.execute('SELECT MAX(version) FROM price_records WHERE type   = %s', ('US', ))
            latest_version = cursor.fetchone()[0] or 0
            new_version = latest_version + 1

            # Create a new record with timestamp and version
            cursor.execute('INSERT INTO price_records (timestamp, version, type) VALUES (%s, %s, %s)',
                           (datetime.now(), new_version, "US"))
            record_id = cursor.lastrowid

            # Insert all prices
            for _, row in services_prices.iterrows():
                # Normalize the service name
                normalized_service_name = row['Service'].replace('+', ' Plus').strip()

                # Insert the normalized name into the database
                cursor.execute('''
                    INSERT INTO streaming_prices (record_id, service_name, cheapest_price)
                    VALUES (%s, %s, %s)
                ''', (record_id, normalized_service_name, row['Cheapest Price']))

            # Commit the new version
            connection.commit()
            logger.info(f"Prices saved to database with version {new_version}")

            # Keep only the latest two versions
            cursor.execute('''
                                DELETE FROM price_records
                                WHERE type = %s
                                AND version NOT IN (
                                    SELECT version FROM (
                                        SELECT version
                                        FROM price_records
                                        WHERE type = %s
                                        ORDER BY version DESC
                                        LIMIT 2
                                    ) AS subquery

                )
            ''', ('US', 'US'))
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
            cursor.execute('SELECT id FROM price_records WHERE type = %s ORDER BY version DESC LIMIT 1', ('US',))
            latest_record_id = cursor.fetchone()['id']

            # Get the prices associated with the latest record
            cursor.execute('SELECT service_name, cheapest_price FROM streaming_prices WHERE record_id = %s',
                           (latest_record_id,))
            prices = cursor.fetchall()

            # Transform the list of prices into a dictionary
            price_dict = {price['service_name']: price['cheapest_price'] for price in prices}

            print("Successfully returning streaming service pricing records", price_dict)
            return price_dict

        except Exception as e:
            print("Error:", str(e))
            logger.error(f"Error fetching latest prices: {e}")
            return {"error": "Unable to retrieve data"}

    def scrape_prices(self, url='https://www.wsj.com/buyside/arts-entertainment/entertainment/best-streaming-services'):
        """Scrape prices and save to database"""
        logger.info("Starting streaming services price scraping...")
        month_input = datetime.now().strftime('%B')
        year_input = datetime.now().year

        prices_df = self.get_cheapest_prices(url, month_input, year_input)

        if prices_df is not None and not prices_df.empty:
            self.save_to_database(prices_df)
            print(prices_df)
            logger.info("Streaming services prices scraped and saved successfully")
            return prices_df
        else:
            logger.warning("No prices scraped")
            return None

    def run_scraper(self):
        print("Starting usa scraping")
        """Run the scraper in a separate thread."""
        thread = threading.Thread(target=self.scrape_prices)
        thread.daemon = True
        thread.start()
        logger.info("Scraper thread started")

    def schedule_scraping(self, hours=24):
        """Schedule regular scraping at specified interval."""
        self.scheduler.add_job(
            self.run_scraper,
            trigger=IntervalTrigger(hours=hours),
            id='streaming_services_scraping',
            name='Scrape Streaming Services Prices',
            replace_existing=True
        )

        # Start the scheduler
        self.scheduler.start()
        logger.info(f"Scheduled scraping every {hours} hours")

        # Run initial scraping if no data exists
        if not self.check_existing_data():
            logger.info("No existing data found. Running initial scraping...")
            self.run_scraper()
            return

    def check_existing_data(self):
        """Check if there's any existing price data in the database."""
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM streaming_prices")
        count = cursor.fetchone()[0]
        return count > 0

    def initialize_scraper(self, hours=24):
        """Initialize the streaming services price scraper with scheduled execution."""
        scraper = USAScraper()
        scraper.schedule_scraping(hours)
        return scraper