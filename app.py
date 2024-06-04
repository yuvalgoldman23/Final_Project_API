# app.py

from flask import Flask
from routes import watchlists_routes, feed_routes, streaming_providers_routes, user_routes, tmdb_routes
from flask_cors import CORS
import database_connector

app = Flask(__name__)
CORS(app)

# Register blueprints for each set of routes
app.register_blueprint(watchlists_routes)
app.register_blueprint(feed_routes)
app.register_blueprint(streaming_providers_routes)
app.register_blueprint(user_routes)
app.register_blueprint(tmdb_routes)

if __name__ == '__main__':
    app.run(debug=True)
