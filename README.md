# Flask API README

This Flask API provides endpoints for managing user watchlists, creating posts, fetching posts, performing content related queries and retrieving streaming providers, all while performing authorization of client requests via Google OAuth.

## Installation

To run this API, make sure you have Python installed on your system. Clone the repository and install the dependencies using the `requirements.txt` file:

```bash
git clone https://github.com/yuvalgoldman23/Final_Project_API.git
cd Final_Project_API
pip install -r requirements.txt
```

## Usage

To start the Flask server, run the following command:

```bash
python basic_server_user_api.py
```

By default, the server will run on `http://127.0.0.1:5000/`.

**IMPORTANT**
For the purpose of testing, API endpoints that require authorization should be accessed via Postman with the following fields:
Headers: 
        Authroization "Google OAuth 2.0 User Login token"
        Content Type "application/json"


## Endpoints

### 0. Login

- **URL:** `/api/login`
- **Method:** `POST`
- **Description:** Logs the user in, registers a new user along the way.
- **Authorization:** Token-based authentication required.
- **Response:** 
  - **Status Code:**     
    - 200 Success if new user created
    - 201 Success if existing user logged in
  - **Content Type:** application/json
  - **Description:** Returns a success or failure JSON message.
---
### 1. Create Watchlist

- **URL:** `/api/watchlists`
- **Method:** `POST`
- **Description:** Creates a new watchlist for the authenticated user.
- **Authorization:** Token-based authentication required.
- **Request Body:**
  - `name` (string, text): (Optional) Name of the watchlist (default: "Untitled Watchlist").
  - `description` (string, text): (Optional) Description of the watchlist.
- **Success Response:**
  - **Status Code:** 201 Created
  - **Content Type:** application/json
  - **Description:** Returns the newly created watchlist object.
- **Failure Response:**
  - **Status Code:** 404 Not Found
  - **Content Type:** application/json
  - **Description:** Returns an error if the user is not found.
---
### 2. Get Watchlist

- **URL:** `/api/watchlists/<watchlist_id>`
- **Method:** `GET`
- **Description:** Retrieves details of a specific watchlist.
- **Parameters:**
  - `watchlist_id` (string, text): ID of the watchlist to retrieve.
- **Authorization:** Token-based authentication required.
- **Success Response:**
  - **Status Code:** 200 OK if watchlist found
  - **Content Type:** application/json
  - **Description:** Returns the watchlist object if found.
- **Failure Response:**
  - **Status Code:** 404 Not Found if watchlist not found
  - **Content Type:** application/json
  - **Description:** Returns an error if the watchlist is not found.
---
### 3. Get Logged-In User's Watchlists

- **URL:** `/api/users/watchlists`
- **Method:** `GET`
- **Description:** Retrieves all watchlists of the logged-in user.
- **Authorization:** Token-based authentication required.
- **Success Response:**
  - **Status Code:** 200 OK
  - **Content Type:** application/json
  - **Description:** Returns an array of watchlist objects belonging to the specified user.
- **Failure Response:**
  - **Status Code:** 404 Not Found
  - **Content Type:** application/json
  - **Description:** Returns an error if the user is not found.
---
### 4. Delete Watchlist

- **URL:** `/api/watchlists/<watchlist_id>`
- **Method:** `DELETE`
- **Description:** Deletes a specific watchlist.
- **Parameters:**
  - `watchlist_id` (string, number): ID of the watchlist to delete.
- **Authorization:** Token-based authentication required.
- **Success Response:**
  - **Status Code:** 200 OK
  - **Content Type:** application/json
  - **Description:** Returns a success message if the watchlist is deleted successfully.
- **Failure Response:**
  - **Status Code:** 404 Not Found
  - **Content Type:** application/json
  - **Description:** Returns an error if the watchlist is not found.
---
### 5. Update Watchlist

- **URL:** `/api/watchlists/<watchlist_id>`
- **Method:** `PUT`
- **Description:** Updates details and/or adds movies to a specific watchlist.
- **Parameters:**
  - `watchlist_id` (string, text): ID of the watchlist to update.
- **Authorization:** Token-based authentication required.
- **Request Body:**
  - `name` (string, text): (Optional) New name for the watchlist.
  - `description` (string, text): (Optional) New description for the watchlist.
  - `movie_id` (string, text): (Optional) ID of a new movie to add to the watchlist.
- **Success Response:**
  - **Status Code:** 200 OK
  - **Content Type:** application/json
  - **Description:** Returns the updated watchlist object.
- **Failure Response:**
  - **Status Code:** 404 Not Found
  - **Content Type:** application/json
  - **Description:** Returns an error if the watchlist is not found.
---
### 6. Delete Movie from Watchlist

- **URL:** `/api/watchlists/<watchlist_id>/movies`
- **Method:** `DELETE`
- **Description:** Removes a specific movie from the specified watchlist.
- **Parameters:**
  - `watchlist_id` (string, text): ID of the watchlist from which to remove the movie.
- **Authorization:** Token-based authentication required.
- **Request Body:**
  - `movie_id` (string, text): ID of the movie to remove from the watchlist.
- **Success Response:**
  - **Status Code:** 200 OK
  - **Content Type:** application/json
  - **Description:** Returns a success message if the movie is deleted from the watchlist.
- **Failure Response:**
  - **Status Code:** 404 Not Found
  - **Content Type:** application/json
  - **Description:** Returns an error if the movie or watchlist is not found.
---
### 7. Create Post

- **URL:** `/api/posts`
- **Method:** `POST`
- **Description:** Creates a new post with optional mentioned content ID.
- **Authorization:** Token-based authentication required.
- **Request Body:**
  - `text` (string, text): Text content of the post.
  - `mentioned_id` (string, text): (Optional) ID of the mentioned content.
- **Success Response:**
  - **Status Code:** 201 Created
  - **Content Type:** application/json
  - **Description:** Returns the newly created post object.
- **Failure Response:**
  - **Status Code:** 400 Bad Request
  - **Content Type:** application/json
  - **Description:** Returns an error if required fields are missing in the request body.
---
### 8. Load Last 20 Posts

- **URL:** `/api/posts`
- **Method:** `GET`
- **Description:** Retrieves the last 20 posts.
- **Authorization:** Not required.
- **Success Response:**
  - **Status Code:** 200 OK
  - **Content Type:** application/json
  - **Description:** Returns an array of the last 20 posts.
- **Failure Response:** None
---
### 9. Get Mentioned Content ID

- **URL:** `/api/posts/<post_id>/mention`
- **Method:** `GET`
- **Description:** Retrieves the mentioned content ID from a specific post.
- **Parameters:**
  - `post_id` (string, number): ID of the post to retrieve the mentioned content ID from.
- **Authorization:** Not required.
- **Success Response:**
  - **Status Code:** 200 OK
  - **Content Type:** application/json
  - **Description:** Returns the mentioned content ID.
- **Failure Response:** None
---
### 10. Get Last 20 Posts Mentioning Content ID

- **URL:** `/api/posts/mentions/<content_id>`
- **Method:** `GET`
- **Description:** Retrieves the last 20 posts mentioning a specific content ID.
- **Parameters:**
  - `content_id` (string, number): ID of the content being mentioned.
- **Authorization:** Not required.
- **Success Response:**
  - **Status Code:** 200 OK
  - **Content Type:** application/json
  - **Description:** Returns an array of the last 20 posts mentioning the specified content ID.
- **Failure Response:** None
---
### 11. Delete Post

- **URL:** `/api/posts/<post_id>`
- **Method:** `DELETE`
- **Description:** Deletes a post.
- **Parameters:**
  - `post_id` (string, number): ID of the post to be removed.
- **Authorization:** Required.
- **Success Response:**
  - **Status Code:** 201 Created
  - **Content Type:** application/json
  - **Description:** Returns a success message if the post is deleted successfully.
- **Failure Response:**
  - **Status Code:** 400 Bad Request
  - **Content Type:** application/json
  - **Description:** Returns an error if the post ID provided doesn't exist or if the post does not belong to the currently logged-in user.
---
### 12. Edit Post

- **URL:** `/api/posts/<post_id>`
- **Method:** `PUT`
- **Description:** Allows an authenticated user to edit a specific post identified by its `post_id`.
- **Parameters:**
  - `post_id`: The unique identifier of the post to be edited.
- **Authorization:** Required. A valid Google OAuth token should be included in the request headers.
- **Request Body:**
  - `text` (string, text) (optional): Updated text content of the post.
  - `content_id` (string, text) (optional): Updated content ID of the post.
- **Response:**
  - `200 OK`: If the post is successfully edited.
  - `400 Bad Request`: If the post ID provided does not exist or if the user is not authorized to edit the post.
---

### 13. Get Streaming Providers

- **URL:** `/api/streaming-providers`
- **Method:** `GET`
- **Description:** Retrieves streaming providers for a specific content ID and territory.
- **Body:**
  - `content_id` (string, required): ID of the content.
  - `territory` (string, required): Territory code for streaming availability.
  - `content_type` (string, required): Type of content ('tv' or 'movie').
- **Authorization:** Not required.

#### Responses

- **200 OK** - 200 OK - Successfully retrieved streaming providers.
  - Content: List of streaming provider objects, each containing the following fields:
    - `name` (string): The name of the streaming provider.
    - `logo_path` (string): The path to the logo of the streaming provider.
    - `provider_id` (string): The ID of the streaming provider.
    - `display_priority` (int): The priority of the provider's display.
- **500 Internal Server Error** - The server encountered an unexpected condition which prevented it from fulfilling the request.
  - Content: Empty array.

---

### 14. Get All Movies

- **URL:** `/api/movie/all`

#### Description

Retrieves all movies available in the database.

#### Parameters

None

#### Responses

- **200 OK** - Successfully retrieved all movies.
  - Content: List of movie objects.
- **500 Internal Server Error** - The server encountered an unexpected condition which prevented it from fulfilling the request.
  - Content: Empty array.

---

### 15. Get Trending TV Shows

- **URL:** `/api/tv/trending`
- **Method:** `GET`
- **Description:** Retrieves the list of trending TV shows for the week.
- **Parameters:** None
- **Authorization:** Not required.
- **Response:** 
  - **200 OK** - Successfully retrieved trending TV shows.
    - Content: List of TV show objects.
  - **500 Internal Server Error** - The server encountered an unexpected condition which prevented it from fulfilling the request.
    - Content: Empty array.

---

### 16. Get Trending Movies

- **URL:** `/api/movie/trending`
- **Method:** `GET`
- **Description:** Retrieves the list of trending movies for the week.
- **Parameters:** None
- **Authorization:** Not required.
- **Response:** 
  - **200 OK** - Successfully retrieved trending movies.
    - Content: List of movie objects.
  - **500 Internal Server Error** - The server encountered an unexpected condition which prevented it from fulfilling the request.
    - Content: Empty array.

---

### 17. Get TV Show Information

- **URL:** `/api/tv/{tv_show_id}`
- **Method:** `GET`
- **Description:** Retrieves information about a specific TV show.
- **Parameters:** 
  - `tv_show_id` (string, required): The ID of the TV show.
- **Authorization:** Not required.
- **Response:** 
  - **200 OK** - Successfully retrieved TV show information.
    - Content: TV show object.
  - **500 Internal Server Error** - The server encountered an unexpected condition which prevented it from fulfilling the request.
    - Content: Empty object.

---

### 18. Get TV Show Cast

- **URL:** `/api/tv/cast/{tv_show_id}`
- **Method:** `GET`
- **Description:** Retrieves the cast of a specific TV show.
- **Parameters:** 
  - `tv_show_id` (string, required): The ID of the TV show.
- **Authorization:** Not required.
- **Response:** 
  - **200 OK** - Successfully retrieved TV show cast.
    - Content: List of cast members.
  - **500 Internal Server Error** - The server encountered an unexpected condition which prevented it from fulfilling the request.
    - Content: Empty array.

---

### 19. Get Movie Cast

- **URL:** `/api/movie/cast/{movie_id}`
- **Method:** `GET`
- **Description:** Retrieves the cast of a specific movie.
- **Parameters:** 
  - `movie_id` (string, required): The ID of the movie.
- **Authorization:** Not required.
- **Response:** 
  - **200 OK** - Successfully retrieved movie cast.
    - Content: List of cast members.
  - **500 Internal Server Error** - The server encountered an unexpected condition which prevented it from fulfilling the request.
    - Content: Empty array.

---

### 20. Get Movie Information

- **URL:** `/api/movie/{movie_id}`
- **Method:** `GET`
- **Description:** Retrieves information about a specific movie.
- **Parameters:** 
  - `movie_id` (string, required): The ID of the movie.
- **Authorization:** Not required.
- **Response:** 
  - **200 OK** - Successfully retrieved movie information.
    - Content: Movie object.
  - **500 Internal Server Error** - The server encountered an unexpected condition which prevented it from fulfilling the request.
    - Content: Empty object.
