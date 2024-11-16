import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import re

def get_cheapest_prices(url, month_input, year_input):
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

    response = requests.get(url, headers=headers)
    print("Status Code:", response.status_code)  # Check the response status

    if response.status_code != 200:
        print("Failed to retrieve the webpage.")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Check if the page contains a date for "costs as of"
    date_text = soup.get_text().lower()
    date_pattern = r"costs as of (\w+) (\d{4})"
    date_match = re.search(date_pattern, date_text)

    if date_match:
        page_month = date_match.group(1)
        page_year = int(date_match.group(2))

        # Compare dates
        input_date = datetime(year_input, datetime.strptime(month_input, '%B').month, 1)
        page_date = datetime(page_year, datetime.strptime(page_month, '%B').month, 1)

        if page_date <= input_date:
            print(f"Page data is older or the same as the input: {month_input} {year_input}. No scraping.")
            return None

        # Print the update date
        print(f"Page data is from: {page_month} {page_year}")
    else:
        print("No 'costs as of' date found on the page.")
        return None

    service_rows = soup.find_all('tr')
    print(f"Found {len(service_rows)} rows.")  # Print the number of rows found

    services = []
    prices = []

    for row in service_rows:
        cols = row.find_all('td')
        if len(cols) > 1:  # Skip header or empty rows
            service_name = cols[0].text.strip()
            basic_ads_price = cols[1].text.strip().replace('$', '').replace(',', '')
            ad_free_price = cols[2].text.strip().replace('$', '').replace(',', '')

            # Use try-except block to handle conversion to float
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
        df = pd.DataFrame({'Service': services, 'Cheapest Price': prices})
        return df
    else:
        print("No service data found.")
        return None


# Example usage
url = 'https://www.wsj.com/buyside/arts-entertainment/entertainment/best-streaming-services'
month_input = 'January'  # Example input month
year_input = 2024  # Example input year
df = get_cheapest_prices(url, month_input, year_input)
if df is not None:
    print(df)
