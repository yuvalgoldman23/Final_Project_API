**README - Server Program**

This server program provides an API for managing users, watchlists, posts, and retrieving streaming providers. Below are instructions on how to run the server and how to use its API.

**Running the Server:**
1. Ensure you have Python installed on your system. If not, download and install it from [python.org](https://www.python.org/).
2. Install Flask, a Python web framework, by running `pip install Flask` in your terminal or command prompt.
3. Copy the provided server code into a Python file, for example, `server.py`.
4. Open a terminal or command prompt in the directory containing `server.py`.
5. Run the server by executing the command `python server.py`.

**Using the API:**
- **Create User:**
  - Endpoint: `POST /api/users`
  - Request Body: JSON object containing `username`, `email`, and `password`.
  - Example: `{"username": "john_doe", "email": "john.doe@example.com", "password": "your_password"}`
  
- **Get User Details:**
  - Endpoint: `GET /api/users/<user_id>`
  - Example: `GET /api/users/1`

- **Update User Details:**
  - Endpoint: `PUT /api/users/<user_id>/details`
  - Request Body: JSON object containing fields to be updated.
  - Example: `PUT /api/users/1/details`
  
- **Delete User:**
  - Endpoint: `DELETE /api/users/<user_id>`
  - Example: `DELETE /api/users/1`

- **User Login:**
  - Endpoint: `POST /api/login`
  - Request Body: JSON object containing `email` and `password`.
  - Example: `{"email": "john.doe@example.com", "password": "your_password"}`

- **Forgot Password:**
  - Endpoint: `POST /api/forgot-password`
  - Request Body: JSON object containing `email`.
  - Example: `{"email": "john.doe@example.com"}`

- **Reset Password:**
  - Endpoint: `POST /api/reset-password`
  - Request Body: JSON object containing `email` and `new_password`.
  - Example: `{"email": "john.doe@example.com", "new_password": "new_password"}`

- **Create Watchlist:**
  - Endpoint: `POST /api/watchlists`
  - Request Body: JSON object containing `user_id`, `token`, `name`, and `description`.
  - Example: `{"user_id": "1", "token": "dummy_token", "name": "My Watchlist", "description": "Favorite movies"}`

- **Get Watchlist:**
  - Endpoint: `GET /api/watchlists/<watchlist_id>`
  - Example: `GET /api/watchlists/1`

- **Get User's Watchlists:**
  - Endpoint: `GET /api/users/<user_id>/watchlists`
  - Example: `GET /api/users/1/watchlists`

- **Delete Watchlist:**
  - Endpoint: `DELETE /api/watchlists/<watchlist_id>`
  - Example: `DELETE /api/watchlists/1`

- **Update Watchlist:**
  - Endpoint: `PUT /api/watchlists/<watchlist_id>`
  - Request Body: JSON object containing fields to be updated.
  - Example: `PUT /api/watchlists/1`

- **Delete Movie from Watchlist:**
  - Endpoint: `DELETE /api/watchlists/<watchlist_id>/movies/<movie_id>`
  - Example: `DELETE /api/watchlists/1/movies/123`

- **Create Post:**
  - Endpoint: `POST /api/posts`
  - Request Body: JSON object containing `text`, `user_id`, and `token`.
  - Example: `{"text": "Hello, world!", "user_id": "1", "token": "dummy_token"}`

- **Load Last 20 Posts:**
  - Endpoint: `GET /api/posts`

- **Get Mentioned Content ID:**
  - Endpoint: `GET /api/posts/<post_id>/mention`
  - Example: `GET /api/posts/1/mention`

- **Get Posts Mentioning Content ID:**
  - Endpoint: `GET /api/posts/mentions/<content_id>`
  - Example: `GET /api/posts/mentions/movie_123`

- **Get Streaming Providers:**
  - Endpoint: `GET /api/streaming-providers`
  - Query Parameters: `content_id`, `territory`, and `content_type`.
  - Example: `GET /api/streaming-providers?content_id=123&territory=US&content_type=movie`

**Note:** Ensure to replace placeholder values like `dummy_token`, `YOUR_TMDB_API_KEY`, etc., with actual values and implement necessary security measures before deploying this server in a production environment.
