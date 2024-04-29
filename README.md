# Flask API README

This Flask API provides endpoints for managing user watchlists, creating posts, fetching posts, and retrieving streaming providers, all while performing authorization of client requests via Google OAuth.

## Installation

To run this API, make sure you have Python installed on your system. Clone the repository and install the dependencies using the `requirements.txt` file:

```bash
git clone https://github.com/yuvalgoldman23/Final_Project_API.git
cd Final_Project_API
pip install -r requ.txt
```

## Usage

To start the Flask server, run the following command:

```bash
python app.py
```

By default, the server will run on `http://127.0.0.1:5000/`.

## Endpoints

### 1. Create Watchlist

- **URL:** `/api/watchlists`
- **Method:** `POST`
- **Description:** Creates a new watchlist for the authenticated user.
- **Parameters:**
  - `name`: (Optional) Name of the watchlist (default: "Untitled Watchlist").
  - `description`: (Optional) Description of the watchlist.
- **Authorization:** Token-based authentication required.
- **Response:** Returns the newly created watchlist object with status code `201 Created`.

### 2. Get Watchlist

- **URL:** `/api/watchlists/<watchlist_id>`
- **Method:** `GET`
- **Description:** Retrieves details of a specific watchlist.
- **Parameters:**
  - `watchlist_id`: ID of the watchlist to retrieve.
- **Authorization:** Token-based authentication required.
- **Response:** Returns the watchlist object if found, else returns an error with status code `404 Not Found`.

### 3. Get User's Watchlists

- **URL:** `/api/users/<user_id>/watchlists`
- **Method:** `GET`
- **Description:** Retrieves all watchlists of a specific user.
- **Parameters:**
  - `user_id`: ID of the user whose watchlists to retrieve.
- **Authorization:** Token-based authentication required.
- **Response:** Returns an array of watchlist objects belonging to the specified user.

### 4. Delete Watchlist

- **URL:** `/api/watchlists/<watchlist_id>`
- **Method:** `DELETE`
- **Description:** Deletes a specific watchlist.
- **Parameters:**
  - `watchlist_id`: ID of the watchlist to delete.
- **Authorization:** Token-based authentication required.
- **Response:** Returns a success message if the watchlist is deleted successfully.

### 5. Update Watchlist

- **URL:** `/api/watchlists/<watchlist_id>`
- **Method:** `PUT`
- **Description:** Updates details of a specific watchlist.
- **Parameters:**
  - `watchlist_id`: ID of the watchlist to update.
  - `name`: (Optional) New name for the watchlist.
  - `description`: (Optional) New description for the watchlist.
  - `movie_id`: (Optional) ID of the movie to add to the watchlist.
- **Authorization:** Token-based authentication required.
- **Response:** Returns the updated watchlist object.

### 6. Delete Movie from Watchlist

- **URL:** `/api/watchlists/<watchlist_id>/movies/<movie_id>`
- **Method:** `DELETE`
- **Description:** Removes a specific movie from the specified watchlist.
- **Parameters:**
  - `watchlist_id`: ID of the watchlist from which to remove the movie.
  - `movie_id`: ID of the movie to remove from the watchlist.
- **Authorization:** Token-based authentication required.
- **Response:** Returns a success message if the movie is deleted from the watchlist.

### 7. Create Post

- **URL:** `/api/posts`
- **Method:** `POST`
- **Description:** Creates a new post with optional mentioned content ID.
- **Parameters:**
  - `text`: Text content of the post.
  - `mentioned_id`: (Optional) ID of the mentioned content.
- **Authorization:** Token-based authentication required.
- **Response:** Returns the newly created post object.

### 8. Load Last 20 Posts

- **URL:** `/api/posts`
- **Method:** `GET`
- **Description:** Retrieves the last 20 posts.
- **Authorization:** Not required.
- **Response:** Returns an array of the last 20 posts.

### 9. Get Mentioned Content ID

- **URL:** `/api/posts/<post_id>/mention`
- **Method:** `GET`
- **Description:** Retrieves the mentioned content ID from a specific post.
- **Parameters:**
  - `post_id`: ID of the post to retrieve the mentioned content ID from.
- **Authorization:** Not required.
- **Response:** Returns the mentioned content ID.

### 10. Get Last 20 Posts Mentioning Content ID

- **URL:** `/api/posts/mentions/<content_id>`
- **Method:** `GET`
- **Description:** Retrieves the last 20 posts mentioning a specific content ID.
- **Parameters:**
  - `content_id`: ID of the content being mentioned.
- **Authorization:** Not required.
- **Response:** Returns an array of the last 20 posts mentioning the specified content ID.

### 11. Get Streaming Providers

- **URL:** `/api/streaming-providers`
- **Method:** `GET`
- **Description:** Retrieves streaming providers for a specific content ID and territory.
- **Parameters:**
  - `content_id`: ID of the content.
  - `territory`: Territory code for streaming availability.
  - `content_type`: Type of content ('tv' or 'movie').
- **Authorization:** Not required.
- **Response:** Returns an array of streaming provider names.
- **Note:** this endpoint requires a TMDB API key. Replace the dummy key before usage.
