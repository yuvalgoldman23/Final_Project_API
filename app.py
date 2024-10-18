# app.py

from flask import Flask
from flask_session import Session
from routes import watchlists_routes, feed_routes, streaming_providers_routes, user_routes, tmdb_routes, reviews_routes, ratings_routes, recommendation_routes
from flask_cors import CORS
from datetime import timedelta
import database_connector

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
# Erase the session after 60 minutes
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60)

# Initialize the session
Session(app)

CORS(app, supports_credentials=True ,resources={r"/*": {"origins": "http://localhost:3000"}})


# Register blueprints for each set of routes
app.register_blueprint(watchlists_routes)
app.register_blueprint(feed_routes)
app.register_blueprint(streaming_providers_routes)
app.register_blueprint(user_routes)
app.register_blueprint(tmdb_routes)
app.register_blueprint(reviews_routes)
app.register_blueprint(ratings_routes)

app.register_blueprint(recommendation_routes)

if __name__ == '__main__':
    app.run(debug=True, )
