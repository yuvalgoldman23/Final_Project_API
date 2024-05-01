# app.py

from flask import Flask
from routes import watchlists_routes, feed_routes, streaming_providers_routes

app = Flask(__name__)

# Register blueprints for each set of routes
app.register_blueprint(watchlists_routes)
app.register_blueprint(feed_routes)
app.register_blueprint(streaming_providers_routes)

if __name__ == '__main__':
    app.run(debug=True)
