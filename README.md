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

### 1. Login

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
  ### 2. Get User Details

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
### 3. Get Watchlist

- **URL:** `/api/watchlists`
- **Method:** `GET`
- **Description:** Retrieves details of a watchlist.
- **Parameters:**
  - (Optional) `wathclist_id` (string, numbers):  returns the watchlist. If no ID has been provided, returns the user's 'Main' watchlist.
- **Authorization:** Token-based authentication required.
- **Success Response:**
  - **Status Code:** 200 OK if watchlist found
  - **Content Type:** application/json
  - **Description:** Returns the watchlist object if found.
- **Failure Response:**
  - **Status Code:** 404 Not Found if watchlist not found
  - **Content Type:** application/json
  - **Description:** Returns an error if the watchlist is not found.
  - If watchlist found, returns an object like this:
    - { "Comment": "fefse", "ID": "4741735bb7e6", "Is_Movie": 1, "Media_ID": "123", "Owner_ID": "2", "Progress": "fefs", "Rating": 10.0, "Time_Updated": "Tue, 04 Jun 2024 20:45:42 GMT", "Watched": 1 }, { "Comment": "fefse", "ID": "ad85ef514915", "Is_Movie": 1, "Media_ID": "65656", "Owner_ID": "2", "Progress": "fefs", "Rating": 10.0, "Time_Updated": "Tue, 04 Jun 2024 20:46:43 GMT", "Watched": 1 }
---

### 4. Add Movie/Show to Watchlist

- **URL:** `/api/watchlists/content`
- **Method:** `PUT`
- **Description:** Adds a new movie/show to the logged-in user's watchlist.
- **Authorization:** Token-based authentication required.
- **Request Body:**
  - `content_id` (string, text): ID of a new movie/show to add to the watchlist.
    - `is_movie` (boolean): True if movie, False otherwise
    - `comment` (Optional: string, text): User's personal comment on media
- **Success Response:**
  - **Status Code:** 200 OK
  - **Content Type:** application/json
  - **Description:** Returns the updated watchlist object.
- **Failure Response:**
  - **Status Code:** 404 Not Found
  - **Content Type:** application/json
  - **Description:** Returns an error if the watchlist is not found.
---
### 5. Delete Movie/Show from Watchlist

- **URL:** `/api/watchlists/content`
- **Method:** `DELETE`
- **Description:** Removes a specific movie/show from the logged-in user's watchlist.
- **Authorization:** Token-based authentication required.
- **Request Body:**
  - `watchlist_item_id` (string, text): ID of the watchlist item to be removed. Specific to each watchlist.
- **Success Response:**
  - **Status Code:** 200 OK
  - **Content Type:** application/json
  - **Description:** Returns a success message if the movie/show is deleted from the watchlist.
- **Failure Response:**
  - **Status Code:** 404 Not Found
  - **Content Type:** application/json
  - **Description:** Returns an error if the movie or watchlist is not found.
---

### 6. Create new watchlist

- **URL:** `/api/watchlists`
- **Method:** `POST`
- **Description:** Removes a specific movie/show from the logged-in user's watchlist.
- **Authorization:** Token-based authentication required.
- **Request Body:**
  - `watchlist_name` (Optional: string, text): the new watchlist's name.
- **Success Response:**
  - **Status Code:** 200 OK
  - **Content Type:** application/json
  - **Description:** 'ID': Returns the new watchlist's ID upon success.
- **Failure Response:**
  - **Status Code:** 404 Not Found
  - **Content Type:** application/json
  - **Description:** Returns an error if the movie or watchlist is not found.
---
### 7. Get all of user's watchlist's

- **URL:** `/api/watchlists/all`
- **Method:** `GET`
- **Description:** Returns all the logged-in user's watchlists.
- **Authorization:** Token-based authentication required.
- **Success Response:**
  - **Status Code:** 200 OK
  - **Content Type:** application/json
  - **Description:** 'watchlists' :Returns an object of watchlists.
- **Failure Response:**
  - **Status Code:** 404 Not Found
  - **Content Type:** application/json
  - **Description:** Returns an error if there's a DB issue.
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


### 21. Get Actor Information
    - **URL:** `/api/actor/<string:actor_id>`
- **Method:** `GET`
- **Description:** Retrieves information about a specific Actor.
- **Parameters:** 
  - `actor_id` (string, required): The ID of the Actor.
- **Authorization:** Not required.
- **Response:** 
  - **200 OK** - Successfully retrieved movie information.
    - Content:
      example:
```Json
{
  "adult": false, 
  
  "biography": "Jackie Chan (Chinese: \u6210\u9f8d; born 7 April 1954), Chan Kong-sang, is a Hong Kong actor, action choreographer, filmmaker, comedian, producer, martial artist, screenwriter, entrepreneur, singer and stunt performer. In his movies, he is known for his acrobatic fighting style, comic timing, use of improvised weapons, and innovative stunts. Jackie Chan has been acting since the 1970s and has appeared in over 100 films.\n\nChan has received stars on the Hong Kong Avenue of Stars and the Hollywood Walk of Fame. As a cultural icon, Chan has been referenced in various pop songs, cartoons, and video games. Chan is also a Cantopop and Mandopop star, having released a number of albums and sung many of the theme songs for the films in which he has starred.\n\nChan was born on April 7, 1954, in Victoria Peak, in the former Crown colony of Hong Kong, as Chan Kong-sang (meaning \"born in Hong Kong\") to Charles and Lee-Lee Chan, refugees from the Chinese Civil War. He was nicknamed Paopao (Chinese: \u70ae\u70ae, literally meaning \"Cannonball\") because he was such a big baby, weighing 12 pounds, or about 5.4 kgs. Since his parents worked for the French Consul to Hong Kong, Chan spent his formative years within the grounds of the consul's residence in the Victoria Peak district. Chan attended the Nah-Hwa Primary School on Hong Kong Island, where he failed his first year, after which his parents withdrew him from the school.\n\nIn 1960, his father immigrated to Canberra, Australia, to work as the head cook for the American embassy, and Chan was sent to the China Drama Academy, a Peking Opera School run by Master Yu Jim-yuen. Chan trained rigorously for the next decade, excelling in martial arts and acrobatics. He eventually became part of the Seven Little Fortunes, a performance group made up of the school's best students, gaining the stage name Yuen Lo in homage to his master. Chan became close friends with fellow group members Sammo Hung and Yuen Biao, the three of them later to be known as the Three Brothers or Three Dragons. At the age of 17, he worked as a stuntman in the Bruce Lee films Fist of Fury and Enter the Dragon under the stage name Chan Yuen Lung. He received his first starring role later that year, in Little Tiger of Canton, which had a limited release in Hong Kong in 1973.", 
  "birthday": "1954-04-07", 
  "deathday": null, 
  "gender": 2, 
  "homepage": "http://jackiechan.com", 
  "id": 18897, 
  "imdb_id": "nm0000329", 
  "known_for_department": "Acting", 
  "name": "Jackie Chan", 
  "place_of_birth": "Victoria Peak, Hong Kong", 
  "popularity": 72.36, 
  "profile_path": "/nraZoTzwJQPHspAVsKfgl3RXKKa.jpg"
}

```
  - **500 Internal Server Error** - The server encountered an unexpected condition which prevented it from fulfilling the request.
    - Content: Empty object.


