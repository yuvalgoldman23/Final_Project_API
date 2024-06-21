# Flask Server README

This Flask server + MySQL Database provides endpoints for managing user watchlists, creating posts, fetching posts, performing content related queries and retrieving streaming providers, all while performing authorization of client requests via Google OAuth.

## Installation

**Database Setup:**

To run the database, make sure you have a MySQL server program, such as MySQL Workbench, installed. In that program, create a new connection, then run the following SQL command:
```sql
CREATE DATABASE final_project_DB;
```
Then, through the program, import the data from the "DataBase_Export" directory into the SQL server.
After finishing this step, you're all set to continue to setting up the Flask server.

**Flask server Setup:**

To run this server, make sure you have Python installed on your system. Clone the repository and install the dependencies using the `requirements.txt` file:

```bash
git clone https://github.com/yuvalgoldman23/Final_Project_API.git
cd Final_Project_API
pip install -r requirements.txt
```

## Usage

To start the Flask server, run the following command:

```bash
python app.py
```

By default, the server will run on `http://127.0.0.1:5000/`.

**IMPORTANT**
For the purpose of testing, API endpoints that require authorization should be accessed via Postman with the following fields:
Headers: 
        Authroization "Google OAuth 2.0 User Login token"
        Content Type "application/json"


## Endpoints

## 1. Login
**URL:** `/api/login`  
**Method:** `POST`  
**Description:** Logs the user in using Google authentication, creating a new user if necessary, and returns the ID of the main watchlist.  
**Authorization:** Token-based authentication required.

**Request Body:**
```json
{
  // No request body parameters required as the user information is derived from the token.
}
```

**Success Response:**
- **Status Code:** `200 OK`
- **Content Type:** `application/json`
- **Response Body:**
  ```json
  {
    "main_watchlist_id": "string"
  }
  ```

**Failure Response:**
- **Status Code:** Varies (e.g., `400 Bad Request`, `401 Unauthorized`, `500 Internal Server Error`)
- **Content Type:** `application/json`
- **Response Body:**
  ```json
  {
    "Message": "string"
  }
  ```
  ### 2. Get User Details (Inactive as of now!)

- **URL:** `/api/user`
- **Method:** `GET`
- **Description:** Returns some of the logged-in user's details.
- **Authorization:** Token-based authentication required.
- **Response:** 
  - **Status Code:**     
    - 200 Success
  - **Content Type:** application/json
  - **Description:** Returns a success or failure JSON message. 
  - In case of success, returns the following details:  "email", "firstname", "lastname", "username"
---

### 3. Get Main Watchlist
**URL:** `/api/watchlists`  
**Method:** `GET`  
**Description:** Retrieves the main watchlist of the logged-in user.  
**Authorization:** Token-based authentication required.

**Success Response:**
- **Status Code:** `200 OK`
- **Content Type:** `application/json`
- **Response Body:**
  ```json
  {
    "Content": [
      {
        "watchlist_item_id": "string",
        "title": "string",
        "genres": ["string"],
        "poster_path": "string"
      }
    ],
    "Name": "string",
    "ID": "string"
  }
  ```

**Failure Response:**
- **Status Code:** `404 Not Found`
- **Content Type:** `application/json`
- **Response Body:**
  ```json
  {
    "Error": "string"
  }
  ```

### 4. Create Watchlist
**URL:** `/api/watchlists`  
**Method:** `POST`  
**Description:** Creates a new watchlist for the logged-in user.  
**Authorization:** Token-based authentication required.  

**Request Body:**
```json
{
  "watchlist_name": "string (optional)"
}
```

**Success Response:**
- **Status Code:** `201 Created`
- **Content Type:** `application/json`
- **Response Body:**
  ```json
  {
    "watchlist_id": "string"
  }
  ```

**Failure Response:**
- **Status Code:** `404 Not Found`
- **Content Type:** `application/json`
- **Response Body:**
  ```json
  {
    "Error": "string"
  }
  ```

### 5. Delete Content from Watchlist
**URL:** `/api/watchlists/content`  
**Method:** `DELETE`  
**Description:** Removes a specific content item from the logged-in user's watchlist.  
**Authorization:** Token-based authentication required.  

**Request Body:**
```json
{
  "watchlist_item_id": "string"
}
```

**Success Response:**
- **Status Code:** `200 OK`
- **Content Type:** `application/json`
- **Response Body:**
  ```json
  {
    "Success": "string"
  }
  ```

**Failure Response:**
- **Status Code:** `404 Not Found`
- **Content Type:** `application/json`
- **Response Body:**
  ```json
  {
    "Error": "string"
  }
  ```

### 6. Get Watchlist by ID
**URL:** `/api/watchlists/{watchlist_id}`  
**Method:** `GET`  
**Description:** Retrieves the watchlist by its ID.  
**Authorization:** Not required.  

**Success Response:**
- **Status Code:** `200 OK`
- **Content Type:** `application/json`
- **Response Body:**
  ```json
  {
    "Content": [
      {
        "watchlist_item_id": "string",
        "title": "string",
        "genres": ["string"],
        "poster_path": "string"
      }
    ],
    "Name": "string",
    "ID": "string"
  }
  ```

**Failure Response:**
- **Status Code:** `404 Not Found`
- **Content Type:** `application/json`
- **Response Body:**
  ```json
  {
    "Error": "string"
  }
  ```

### 7. Get All User Watchlists
**URL:** `/api/watchlists/all`  
**Method:** `GET`  
**Description:** Retrieves all watchlists of the logged-in user.  
**Authorization:** Token-based authentication required.  

**Success Response:**
- **Status Code:** `200 OK`
- **Content Type:** `application/json`
- **Response Body:**
  ```json
  {
    "watchlists": [
      {
        "Content": [
          {
            "watchlist_item_id": "string",
            "title": "string",
            "genres": ["string"],
            "poster_path": "string"
          }
        ],
        "Name": "string",
        "ID": "string"
      }
    ]
  }
  ```

**Failure Response:**
- **Status Code:** `404 Not Found`
- **Content Type:** `application/json`
- **Response Body:**
  ```json
  {
    "Error": "string"
  }
  ```

### 8. Add Movie/Show to Watchlist
**URL:** `/api/watchlists/content`  
**Method:** `PUT`  
**Description:** Adds a new movie/show to the logged-in user's watchlist.  
**Authorization:** Token-based authentication required.  

**Request Body:**
```json
{
  "watchlist_id": "string",
  "content_id": "string",
  "is_movie": "boolean"
}
```

**Success Response:**
- **Status Code:** `200 OK`
- **Content Type:** `application/json`
- **Response Body:**
  ```json
  {
    "Success": "string",
    "watchlist_object_id": "string"
  }
  ```

**Failure Response:**
- **Status Code:** `404 Not Found`
- **Content Type:** `application/json`
- **Response Body:**
  ```json
  {
    "Error": "string"
  }
  ```

### 9. Delete User Watchlist
**URL:** `/api/watchlists`  
**Method:** `DELETE`  
**Description:** Deletes a specific watchlist of the logged-in user.  
**Authorization:** Token-based authentication required.  

**Request Body:**
```json
{
  "watchlist_id": "string"
}
```

**Success Response:**
- **Status Code:** `200 OK`
- **Content Type:** `application/json`
- **Response Body:**
  ```json
  {
    "Success": "string"
  }
  ```

**Failure Response:**
- **Status Code:** `404 Not Found`
- **Content Type:** `application/json`
- **Response Body:**
  ```json
  {
    "Error": "string"
  }
  ```
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
- **Authorization:** Required. A valid JWT token should be included in the request headers.
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

