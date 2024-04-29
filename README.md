**README - Server Program**

This server program provides an API for managing watchlists, posts, and retrieving streaming providers. Below are instructions on how to run the server and how to use its API.
Users are required to authenticate via Google OAuth2. To initiate the authentication flow, access /authorize endpoint. Upon successful authentication, users are redirected to /callback

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/awesome-flask-app.git
   ```

2. Install dependencies:
   ```bash
   pip install -r req.txt
   ```

3. Set up environment variables:
   - Create a `.env` file in the root directory.
   - Add the following variables:
     ```
     SECRET_KEY=your_secret_key
     GOOGLE_CLIENT_ID=your_google_client_id
     GOOGLE_CLIENT_SECRET=your_google_client_secret
     ```

4. Run the application:
   ```bash
   python app.py
   ```

## API Documentation

- **Get Watchlist:**
  - Endpoint: `GET /api/watchlists/<watchlist_id>`
  - Example: `GET /api/watchlists/1`
  - Description: Retrieves details of a specific watchlist by its ID.

- **Create Watchlist:**
  - Endpoint: `POST /api/watchlists`
  - Example: `POST /api/watchlists`
  - Description: Creates a new watchlist.
  - Request Body:
    ```json
    {
        "user_id": "1",
        "name": "My Watchlist",
        "description": "A list of my favorite movies"
    }
    ```
  - Response Body:
    ```json
    {
        "id": "2",
        "user_id": "1",
        "name": "My Watchlist",
        "description": "A list of my favorite movies",
        "movies": []
    }
    ```

- **Delete Watchlist:**
  - Endpoint: `DELETE /api/watchlists/<watchlist_id>`
  - Example: `DELETE /api/watchlists/2`
  - Description: Deletes a watchlist by its ID.

- **Update Watchlist:**
  - Endpoint: `PUT /api/watchlists/<watchlist_id>`
  - Example: `PUT /api/watchlists/2`
  - Description: Updates an existing watchlist by its ID.
  - Request Body:
    ```json
    {
        "name": "Updated Watchlist Name",
        "description": "Updated watchlist description"
    }
    ```

- **Create Post:**
  - Endpoint: `POST /api/posts`
  - Example: `POST /api/posts`
  - Description: Creates a new post.
  - Request Body:
    ```json
    {
        "text": "Hello, world!",
        "user_id": "1",
        "token": "your_access_token"
    }
    ```
  - Response Body:
    ```json
    {
        "text": "Hello, world!",
        "mentioned_user_id": null,
        "user_id": "1"
    }
    ```

- **Get Last 20 Posts:**
  - Endpoint: `GET /api/posts`
  - Example: `GET /api/posts`
  - Description: Retrieves the last 20 posts.

- **Get Mentioned Content ID:**
  - Endpoint: `GET /api/posts/<post_id>/mention`
  - Example: `GET /api/posts/123/mention`
  - Description: Retrieves the mentioned content ID from a post.

- **Get Last 20 Posts Mentioning Content ID:**
  - Endpoint: `GET /api/posts/mentions/<content_id>`
  - Example: `GET /api/posts/mentions/movie_123`
  - Description: Retrieves the last 20 posts mentioning a specific content ID.

- **Get Streaming Providers:**
  - Endpoint: `GET /api/streaming-providers`
  - Example: `GET /api/streaming-providers?content_id=movie_123&territory=US&content_type=movie`
  - Description: Retrieves the streaming providers for a given content ID in a specific territory.

**Note:** Ensure to replace placeholder values like `dummy_token`, `YOUR_TMDB_API_KEY`, etc., with actual values and implement necessary security measures before deploying this server in a production environment.
