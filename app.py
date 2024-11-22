# app.py

from flask import Flask
from flask_session import Session
from routes import (watchlists_routes,  streaming_providers_routes, user_routes, tmdb_routes,
                     ratings_routes, recommendation_routes, discover_routes)
from flask_cors import CORS
import asyncio
from datetime import timedelta
import database_connector
from scrapers.netflix_scraper import NetflixPriceScraper
from scrapers.usa_scraper import USAScraper

app = Flask(__name__)
'''
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
# Erase the session after 60 minutes
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60)

# Initialize the session
Session(app)'''

CORS(app, supports_credentials=True ,resources={r"/*": {"origins": "http://localhost:3000"}})

# Scrapers setup
netflix_scraper = NetflixPriceScraper()
netflix_scraper.initialize_netflix_scraper(hours=24)
# Setting up a global instance of the netflix scraper
app.netflix_scraper = netflix_scraper
# Setting up the usa scraper as a global instance
usa_scraper = USAScraper()
usa_scraper.initialize_scraper(hours=24)
app.usa_scraper = usa_scraper


# Register blueprints for each set of routes
app.register_blueprint(watchlists_routes)
#app.register_blueprint(feed_routes)
app.register_blueprint(streaming_providers_routes)
app.register_blueprint(user_routes)
app.register_blueprint(tmdb_routes)
#app.register_blueprint(reviews_routes)
app.register_blueprint(ratings_routes)

app.register_blueprint(recommendation_routes)
app.register_blueprint(discover_routes)
app.permanent_session_lifetime = timedelta(days=1)  # Set session lifetime
Session.permanent = True  # Mark this session as permanent
app.secret_key = 'your_fixed_secret_key'
if __name__ == '__main__':
    app.run(debug=True,use_reloader=False )
