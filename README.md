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

To start the Flask server in development mode, run the following command:

```bash
python app.py
```

By default, the server will run on `http://127.0.0.1:5000/`.

To start the Flask server in production mode, run the following command instead:

```bash
waitress-serve --host=127.0.0.1 --port=5000 app:app
```

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
A session cookie will also be provided to the client for future usage.

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
## 2. Logout
**URL:** `/api/logout`  
**Method:** `POST`  
**Description:** Logs-out the user whose session cookie was provided, while deleting the session.

**Authorization:** Session Cookie, handled by the browser.
```

**Success Response:**
- **Status Code:** `200 OK`
- **Content Type:** `application/json`
- **Response Body:**
  ```json
  {
    "message": Logged out successfully
  }
  ```
## 3. Is User Logged In?
**URL:** `/api/is_logged_in`  
**Method:** `GET`  
**Description:** Checks whether the user whose session cookie has been provided is logged in or not.

**Request Body:**
```json
{
  // No request body parameters required.
}
```

**Success Response:**
- **Status Code:** `200 OK`
- **Content Type:** `application/json`
- **Response Body:**
  ```json
  {
    "logged_in: "boolean"
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
        "large_poster_path": string (original sized poster)
  "small_poster_path":, "string (w200 image)g" (or null in case of no image in TMDB's response)',
        "tmdb_id":  "string",
        "overview": "string",
        "release_date": "string" (yyyy-mm-dd format)
        "tmdb_rating": "float", (or null in case of no tmdb rating)
        "user_rating": "int" (or null in case of no user rating)
      }
    ],
    "Name": "string",
    "ID": "string"
  }
  ```
- **Response Example:**
  ```json
    {
    "Content": [
        {
            "genres": [
                "Music"
            ],
            "overview": "Propagandhi play a benefit show for the Grassy Narrows First Nation Blockade and the International Solidarity Movement at the Zoo (the venue, not the animal prison numb-nuts) in Winnipeg, Canada in 2003.  Set features songs from all their full-length records in addition to some rare cover tunes along with early incarnations of tracks from Potemkin City Limits, which was released 2 years later. Show is video-taped by crowd-members and recorded and mixed by the band 100% DIY-like.",
            "large_poster_path":string (original sized poster)
                       "small_poster_path": null,
  (w200 image)           "release_date": "2007-04-24",
            "title": "Propagandhi: Live from Occupied Territory",
            "tmdb_id": "114924",
            "tmdb_rating": null,
            "user_rating": null,
            "watchlist_item_id": "0dc079e7da6b"
        },
        {
            "genres": [
                "War",
                "History"
            ],
            "overview": "The Americans are swiftly closing on Okinawa, an island just south of the Japanese mainland. The Imperial command sends top generals and several army divisions to defend it at all costs. The mission quickly degenerates as vital resources and troops are diverted to other islands. After a civilian evacuation ends in tragedy most of non-combatants are forced to remain on the island. Many convert to soldier status. Tokyo sends mixed messages that squander time and resources, as when they order the defenders to build an airstrip for aircraft that never come. The truth soon becomes obvious: the high command decides that the island cannot be held and effectively abandons the Okinawan defenders. When the Americans land many troops are deployed in the wrong places. As the slaughter mounts, a suicidal attitude takes hold. Okinawa becomes a death trap, for civilian volunteers and non-combatants as well.",
            "large_poster_path":string (original sized poster)
                       "small_poster_path": "https: (w200 image)//image.tmdb.org/t/p/original//dq2g8cBDH8i5vNOZ7xJbIrmO5Y5.jpg",
            "release_date": "1971-08-14",
            "title": "激動の昭和史　沖縄決戦",
            "tmdb_id": "130853",
            "tmdb_rating": 7.458,
            "user_rating": null,
            "watchlist_item_id": "5bcb92a6b8e5"
        }
    ],
    "ID": "246d697c378a",
    "Name": "Main"
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
  "watchlist_id": "string" (Optional - if none received, remove from main watchlist),
  "content_id": "string"
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
        "large_poster_path": string (original sized poster)
  "small_poster_path":, "strin (w200 image)g" (or null in case of no image in TMDB's response)',
        "tmdb_id":  "string",
        "overview": "string",
        "release_date": "string" (yyyy-mm-dd format)
        "tmdb_rating": "float", (or null in case of no tmdb rating)
        "user_rating": "int" (or null in case of no user rating)
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
        "large_poster_path": string (original sized poster)
  "small_poster_path":, "strin (w200 image)g" (or null in case of no image in TMDB's response)',
        "tmdb_id":  "string",
        "overview": "string",
        "release_date": "string" (yyyy-mm-dd format)
        "tmdb_rating": "float", (or null in case of no tmdb rating)
        "user_rating": "int" (or null in case of no user rating)
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
**Method:** `POST`  
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
  

**Duplicate Content Response:**
- **Status Code:** `204`
- **Content Type:** `application/json`
- **Response Body:**
  ```json
  {
    "Message": "string"
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
### 10. Write Review
**URL:** `/api/reviews`  
**Method:** `POST`  
**Description:** Adds a review for a specific content item.  
**Authorization:** Token-based authentication required.

**Request Body:**
```json
{
  "text": "string",
  "content_id": "string"
}
```

**Success Response:**
- **Status Code:** `201 Created`
- **Content Type:** `application/json`
- **Response Body:**
  ```json
  {
    "success": "added a review for content_id",
    "review_id": "string"
  }
  ```

**Failure Response:**
- **Status Code:** `400 Bad Request`
- **Content Type:** `application/json`
- **Response Body:**
  ```json
  {
    "status": "error",
    "message": "Missing text or content_id"
  }
  ```

- **Status Code:** Varies (e.g., `500 Internal Server Error`)
- **Content Type:** `application/json`
- **Response Body:**
  ```json
  {
    "status": "error",
    "message": "string"
  }
  ```
---
### 11. Get Reviews by User
**URL:** `/api/users/reviews`  
**Method:** `GET`  
**Description:** Retrieves all reviews written by a specific user.  
**Authorization:** Not required.

**Request Body:**
```json
{
  "user_id": "string"
}
```

**Success Response:**
- **Status Code:** `200 OK`
- **Content Type:** `application/json`
- **Response Body:**
  ```json
  {
    "reviews": [
      {
        "ID": "string",
        "Parent_ID": "string",
        "Text": "string",
        "updated_at": "TIMESTAMP"
      },
      ...
    ]
  }
  ```

**Failure Response:**
- **Status Code:** `400 Bad Request`
- **Content Type:** `application/json`
- **Response Body:**
  ```json
  {
    "status": "error",
    "message": "Missing user_id"
  }
  ```

- **Status Code:** Varies (e.g., `500 Internal Server Error`)
- **Content Type:** `application/json`
- **Response Body:**
  ```json
  {
    "status": "error",
    "message": "string"
  }
  ```
---
### 11. Get Reviews by Content
**URL:** `/api/reviews/content`  
**Method:** `GET`  
**Description:** Retrieves all reviews for a specific content item.  
**Authorization:** Not required.

**Request Body:**
```json
{
  "content_id": "string"
}
```

**Success Response:**
- **Status Code:** `200 OK`
- **Content Type:** `application/json`
- **Response Body:**
  ```json
  {
    "reviews": [
      {
        "ID": "string",
        "User_ID": "string",
        "Text": "string",
        "updated_at": "TIMESTAMP"
      },
      ...
    ]
  }
  ```

**Failure Response:**
- **Status Code:** `400 Bad Request`
- **Content Type:** `application/json`
- **Response Body:**
  ```json
  {
    "status": "error",
    "message": "Missing content_id"
  }
  ```

- **Status Code:** Varies (e.g., `500 Internal Server Error`)
- **Content Type:** `application/json`
- **Response Body:**
  ```json
  {
    "status": "error",
    "message": "string"
  }
  ```
---
### 12. Delete Review
**URL:** `/api/reviews`  
**Method:** `DELETE`  
**Description:** Deletes a specific review written by the logged-in user.  
**Authorization:** Token-based authentication required.

**Request Body:**
```json
{
  "review_id": "string"
}
```

**Success Response:**
- **Status Code:** `200 OK`
- **Content Type:** `application/json`
- **Response Body:**
  ```json
  {
    "success": "deleted review of id review_id"
  }
  ```

**Failure Response:**
- **Status Code:** `400 Bad Request`
- **Content Type:** `application/json`
- **Response Body:**
  ```json
  {
    "status": "error",
    "message": "Missing review_id"
  }
  ```

- **Status Code:** Varies (e.g., `500 Internal Server Error`)
- **Content Type:** `application/json`
- **Response Body:**
  ```json
  {
    "status": "error",
    "message": "string"
  }
  ```
---
### 13. Add Rating
**URL:** `/api/ratings`  
**Method:** `POST`  
**Description:** Adds a rating for a specific content item.  
**Authorization:** Token-based authentication required.

**Request Body:**
```json
{
  "content_id": "string",
  "rating": "number",
  "is_movie": "boolean"
}
```

**Success Response:**
- **Status Code:** `201 Created`
- **Content Type:** `application/json`
- **Response Body:**
  ```json
  {
    "rating_id": "string"
  }
  ```

**Failure Response:**
- **Status Code:** `400 Bad Request`
- **Content Type:** `application/json`
- **Response Body:**
  ```json
  {
    "error": "Content ID and Rating must be provided"
  }
  ```

- **Status Code:** Varies (e.g., `500 Internal Server Error`)
- **Content Type:** `application/json`
- **Response Body:**
  ```json
  {
    "status": "string"
  }
  ```

### 14. Get Ratings by User
**URL:** `/api/users/ratings`  
**Method:** `GET`  
**Description:** Retrieves ratings given by a specific user. If no user_id is provided in the request, it returns the ratings for the logged-in user.
If no content id or "is_movie" value provided, returns all ratings by given user. Otherwise, returns rating for specificed content only.
**Authorization:** Token-based authentication required if no user_id provided.

**Request Body (Optional):**
```json
{
  "user_id": "string",
  "content_id":"string",
  "is_movie": "boolean" (content_id AND is_movie are both requried - only one of them would result returning all ratings)
}
```

**Success Response:**
- **Status Code:** `200 OK`
- **Content Type:** `application/json`
- **Response Body:**
  ```json
  {
    "ratings": [
      {
        "rating_id": "string",
        "content_id": "string",
        "rating": "number",
        "is_movie": "boolean",
        "timestamp": "string"
      },
      ...
    ]
  }
  ```

**Failure Response:**
- **Status Code:** Varies (e.g., `500 Internal Server Error`)
- **Content Type:** `application/json`
- **Response Body:**
  ```json
  {
    "status": "string"
  }
  ```

### 15. Remove Rating
**URL:** `/api/ratings`  
**Method:** `DELETE`  
**Description:** Deletes a specific rating given by the logged-in user.  
**Authorization:** Token-based authentication required.

**Request Body:**
```json
{
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
    "status": "string"
  }
  ```

**Failure Response:**
- **Status Code:** `404 Not Found`
- **Content Type:** `application/json`
- **Response Body:**
  ```json
  {
    "status": "Must provide content id to be deleted"
  }
  ```

- **Status Code:** Varies (e.g., `500 Internal Server Error`)
- **Content Type:** `application/json`
- **Response Body:**
  ```json
  {
    "status": "string"
  }
  ```
---


### 16. Update Rating
**URL:** `/api/ratings`  
**Method:** `PUT`  
**Description:** Updates a specific rating given by the logged-in user.  
**Authorization:** Token-based authentication required.

**Request Body:**
```json
{
  "content_id": "string",
  "is_movie": "boolean",
  "new_rating": "number" (decimal number between 1 and 10)
}
```

**Success Response:**
- **Status Code:** `200 OK`
- **Content Type:** `application/json`
- **Response Body:**
  ```json
  {
    "status": "string"
  }
  ```

**Failure Response:**
- **Status Code:** `404 Not Found`
- **Content Type:** `application/json`
- **Response Body:**
  ```json
  {
    "status": "Must provide content id, is_movie to be updated"
  }
  ```
  
-- **Status Code:** '304 Not Modified' (Happens when the new rating is same as existing)

- **Status Code:** Varies (e.g., `500 Internal Server Error`)
- **Content Type:** `application/json`
- **Response Body:**
  ```json
  {
    "status": "string"
  }
  ```
---
### 17. Get User's Rating List
**URL:** `/api/users/ratings_list`
**Method:** `GET`
**Description:** Returns the user's list of rated content, including all relevant details.
**Authorization:** Token-based authentication required.

**Request Body:**
Empty

**Success Response:**:
- **Status Code:** `200 OK`
- **Content Type:** `application/json`
- **Response Body:**
```json

{
    "content": [
        {
            "genres": [
                "Action & Adventure",
                "Comedy",
                "Animation"
            ],
            "is_movie": 0,
            "item_id": "460102f4cc57",
            "list_id": null,
            "overview": "Years ago, the fearsome Pirate King, Gol D. Roger was executed leaving a huge pile of treasure and the famous \"One Piece\" behind. Whoever claims the \"One Piece\" will be named the new King of the Pirates.\n\nMonkey D. Luffy, a boy who consumed a \"Devil Fruit,\" decides to follow in the footsteps of his idol, the pirate Shanks, and find the One Piece. It helps, of course, that his body has the properties of rubber and that he's surrounded by a bevy of skilled fighters and thieves to help him along the way.\n\nLuffy will do anything to get the One Piece and become King of the Pirates!",
            "poster_path": "https://image.tmdb.org/t/p/original/https://image.tmdb.org/t/p/original/cMD9Ygz11zjJzAovURpO75Qg7rT.jpg",
            "release_date": "1999-10-20",
            "small_poster_path": "https://image.tmdb.org/t/p/w200/https://image.tmdb.org/t/p/original/cMD9Ygz11zjJzAovURpO75Qg7rT.jpg",
            "streaming_services": null,
            "title": "One Piece",
            "tmdb_id": "37854",
            "tmdb_rating": 8.7,
            "user_id": "113749586527602021810",
            "user_rating": 9,
            "video_links": [
                {
                    "id": "65e7a4a542f19f01878c703f",
                    "iso_3166_1": "US",
                    "iso_639_1": "en",
                    "key": "LrCmsOAgvxk",
                    "name": "Opening 25 | The Peak - SEKAI NO OWARI [Subtitled]",
                    "official": true,
                    "published_at": "2023-09-11T22:24:28.000Z",
                    "site": "YouTube",
                    "size": 1080,
                    "type": "Opening Credits"
                },
                {
                    "id": "65f3d0d93852020186e2723f",
                    "iso_3166_1": "US",
                    "iso_639_1": "en",
                    "key": "u59DSmF20Dg",
                    "name": "Opening 15 | We Go! - Hiroshi Kitadani [Subtitled]",
                    "official": false,
                    "published_at": "2020-05-13T10:40:46.000Z",
                    "site": "YouTube",
                    "size": 1080,
                    "type": "Opening Credits"
                },
                {
                    "id": "65eca1438cfcc7016461fd1a",
                    "iso_3166_1": "US",
                    "iso_639_1": "en",
                    "key": "PwVT67T5Xt4",
                    "name": "Opening 22 | OVER THE TOP - Hiroshi Kitadani",
                    "official": true,
                    "published_at": "2019-08-01T14:30:00.000Z",
                    "site": "YouTube",
                    "size": 1080,
                    "type": "Opening Credits"
                },
                {
                    "id": "65eca1b978570e0187fab7fc",
                    "iso_3166_1": "US",
                    "iso_639_1": "en",
                    "key": "t7xHamn5inQ",
                    "name": "Opening 21 | Super Powers - V6",
                    "official": true,
                    "published_at": "2018-10-16T02:00:02.000Z",
                    "site": "YouTube",
                    "size": 1080,
                    "type": "Opening Credits"
                },
                {
                    "id": "65eca189a9b9a4017dd49041",
                    "iso_3166_1": "US",
                    "iso_639_1": "en",
                    "key": "Oo52vQyAR6w",
                    "name": "Opening 20 | Hope - Namie Amuro [Subtitled]",
                    "official": true,
                    "published_at": "2018-02-26T02:00:01.000Z",
                    "site": "YouTube",
                    "size": 1080,
                    "type": "Opening Credits"
                },
                {
                    "id": "65f8b34f85b10501866335ad",
                    "iso_3166_1": "US",
                    "iso_639_1": "en",
                    "key": "yAtUSvVayM0",
                    "name": "Opening 1 (Special Edition) | We Are! - Hiroshi Kitadani [Subtitled]",
                    "official": false,
                    "published_at": "2016-09-27T11:21:50.000Z",
                    "site": "YouTube",
                    "size": 1080,
                    "type": "Opening Credits"
                },
                {
                    "id": "65f8b3e3160e730183f955b0",
                    "iso_3166_1": "US",
                    "iso_639_1": "en",
                    "key": "CFM_zypYFHM",
                    "name": "Opening 10 | We Are! - TVXQ [Creditless]",
                    "official": false,
                    "published_at": "2013-07-28T22:25:16.000Z",
                    "site": "YouTube",
                    "size": 1080,
                    "type": "Opening Credits"
                },
                {
                    "id": "65c495050c4c16016402d214",
                    "iso_3166_1": "US",
                    "iso_639_1": "en",
                    "key": "LzC0HSOOauI",
                    "name": "Opening 11 | Share the World - TVXQ [Subtitled]",
                    "official": false,
                    "published_at": "2012-07-24T10:06:47.000Z",
                    "site": "YouTube",
                    "size": 1080,
                    "type": "Opening Credits"
                },
                {
                    "id": "65f8b4ce4d0e8d017c321c29",
                    "iso_3166_1": "US",
                    "iso_639_1": "en",
                    "key": "dmtK7RiIz1A",
                    "name": "English Opening 1 | We Are! - Vic Mignogna",
                    "official": false,
                    "published_at": "2011-10-06T11:36:23.000Z",
                    "site": "YouTube",
                    "size": 1080,
                    "type": "Opening Credits"
                },
                {
                    "id": "65f3d201293835018728aecb",
                    "iso_3166_1": "US",
                    "iso_639_1": "en",
                    "key": "NZv-BKl4qEo",
                    "name": "Opening 5 | Map of the Heart - BOYSTYLE [Subtitled]",
                    "official": false,
                    "published_at": "2010-11-04T17:58:25.000Z",
                    "site": "YouTube",
                    "size": 1080,
                    "type": "Opening Credits"
                },
                {
                    "id": "65f3d24224f2ce018516c4bc",
                    "iso_3166_1": "US",
                    "iso_639_1": "en",
                    "key": "FZ26zR5EGEA",
                    "name": "Opening 6 | BRAND NEW WORLD - D-51 [Subtitled]",
                    "official": false,
                    "published_at": "2006-07-21T07:22:09.000Z",
                    "site": "YouTube",
                    "size": 1080,
                    "type": "Opening Credits"
                }
            ]
        },
        {
            "genres": [],
            "is_movie": 1,
            "item_id": "694aa97847dc",
            "list_id": null,
            "overview": "",
            "poster_path": "https://image.tmdb.org/t/p/original/https://image.tmdb.org/t/p/original/6upxSiukqIvPhHQ8FoOlN4bZciY.jpg",
            "release_date": "",
            "small_poster_path": "https://image.tmdb.org/t/p/w200/https://image.tmdb.org/t/p/original/6upxSiukqIvPhHQ8FoOlN4bZciY.jpg",
            "streaming_services": null,
            "title": "אותיות מצחיקות",
            "tmdb_id": "992127",
            "tmdb_rating": 0.0,
            "user_id": "113749586527602021810",
            "user_rating": 4,
            "video_links": []
        },
        {
            "genres": [],
            "is_movie": 0,
            "item_id": "8e9e43733379",
            "list_id": null,
            "overview": "System Crash was a television show on YTV about a group of students in a media club telling the events of their fictional school, Lambton High, in the past week.\n\nThe show was of the sketch comedy genre, with many short segments. Each episode usually had a theme, i.e. parents. Many of the recurring sketches had familiar titles such as Fly on the Wall, Sports Update, Burnbaum Helps, and Lambton Home Shopping.",
            "poster_path": "https://image.tmdb.org/t/p/original/https://image.tmdb.org/t/p/original/oEMskC0OFilELHGsDfRFM84gU8C.jpg",
            "release_date": "1999-02-04",
            "small_poster_path": "https://image.tmdb.org/t/p/w200/https://image.tmdb.org/t/p/original/oEMskC0OFilELHGsDfRFM84gU8C.jpg",
            "streaming_services": null,
            "title": "System Crash",
            "tmdb_id": "99",
            "tmdb_rating": 0.0,
            "user_id": "113749586527602021810",
            "user_rating": 4,
            "video_links": []
        },
        {
            "genres": [
                "Action",
                "Comedy"
            ],
            "is_movie": 1,
            "item_id": "ff6b8d5ee6f2",
            "list_id": null,
            "overview": "A New Jersey construction worker goes from regular guy to aspiring spy when his long-lost high school sweetheart recruits him for an espionage mission.",
            "poster_path": "https://image.tmdb.org/t/p/original/https://image.tmdb.org/t/p/original/d9CTnTHip1RbVi2OQbA2LJJQAGI.jpg",
            "release_date": "2024-08-15",
            "small_poster_path": "https://image.tmdb.org/t/p/w200/https://image.tmdb.org/t/p/original/d9CTnTHip1RbVi2OQbA2LJJQAGI.jpg",
            "streaming_services": null,
            "title": "The Union",
            "tmdb_id": "704239",
            "tmdb_rating": 6.271,
            "user_id": "113749586527602021810",
            "user_rating": 7,
            "video_links": [
                {
                    "id": "66cd835e16d5538e68c420e5",
                    "iso_3166_1": "US",
                    "iso_639_1": "en",
                    "key": "PnX0e2CJUhQ",
                    "name": "Car Chase Finale",
                    "official": true,
                    "published_at": "2024-08-24T15:00:00.000Z",
                    "site": "YouTube",
                    "size": 1080,
                    "type": "Clip"
                },
                {
                    "id": "66c43c1f2185dcbce75d18b7",
                    "iso_3166_1": "US",
                    "iso_639_1": "en",
                    "key": "tjlLyJUGPEM",
                    "name": "Halle Berry and Mark Wahlberg Take You Behind The Scenes",
                    "official": true,
                    "published_at": "2024-08-17T16:00:00.000Z",
                    "site": "YouTube",
                    "size": 1080,
                    "type": "Behind the Scenes"
                },
                {
                    "id": "66bd41749a3172dc508003bd",
                    "iso_3166_1": "US",
                    "iso_639_1": "en",
                    "key": "T3t4NzfxZfI",
                    "name": "Kitchen Fight Scene - Sneak Peek",
                    "official": true,
                    "published_at": "2024-08-14T15:00:00.000Z",
                    "site": "YouTube",
                    "size": 1080,
                    "type": "Clip"
                },
                {
                    "id": "66b4411a3139e04832888441",
                    "iso_3166_1": "US",
                    "iso_639_1": "en",
                    "key": "far_Oqw4a4M",
                    "name": "Halle Berry and Mark Wahlberg Compare Action Movie Injuries",
                    "official": true,
                    "published_at": "2024-08-07T13:00:00.000Z",
                    "site": "YouTube",
                    "size": 1080,
                    "type": "Featurette"
                },
                {
                    "id": "66ad699e78e48634d5cd86c7",
                    "iso_3166_1": "US",
                    "iso_639_1": "en",
                    "key": "Xk9RlH0g37I",
                    "name": "Roxanne and Mike Reunite",
                    "official": true,
                    "published_at": "2024-08-02T16:30:00.000Z",
                    "site": "YouTube",
                    "size": 1080,
                    "type": "Clip"
                },
                {
                    "id": "667c391e2bb283e831478f23",
                    "iso_3166_1": "US",
                    "iso_639_1": "en",
                    "key": "vea9SdnRMyg",
                    "name": "Official Trailer",
                    "official": true,
                    "published_at": "2024-06-26T15:30:01.000Z",
                    "site": "YouTube",
                    "size": 1080,
                    "type": "Trailer"
                }
            ]
        }
    ],
    "list_id": null,
    "user_id": "113749586527602021810"
}
```

### 16. Add Post
**URL:** `/api/feed`  
**Method:** `POST`  
**Description:** Creates a new post in the feed with optional mentions and tags.  
**Authorization:** Token-based authentication required.

**Request Body:**
```json
{
  "text_content": "string",        // The content of the post.
  "parent_id": "string" (optional),// The ID of the parent post (if this is a reply).
  "is_child": "boolean",           // Indicates if this post is a child post.
  "mentions": [                    // Array of mentions, each containing:
    {
      "mentioned_user_id": "string", // ID of the mentioned user.
      "start_position": "integer",   // Start index of the mention in the text.
      "length": "integer"            // Length of the mention in the text.
    }
  ],
  "tags": [                        // Array of tags, each containing:
    {
      "tagged_media_id": "string",  // ID of the tagged media.
      "start_position": "integer",  // Start index of the tag in the text.
      "length": "integer"           // Length of the tag in the text.
    }
  ]
}
```

**Success Response:**

- **Status Code:** `200 OK`
- **Content Type:** `application/json`
- **Response Body:**
  ```json
  {
    "post_id": "string",        // The ID of the newly created post.
    "mentions": [               // Array of mentions added, each containing:
      {
        "mention_id": "string",    // ID of the mention.
        "mentioned_user_id": "string" // ID of the mentioned user.
      }
    ],
    "tags": [                   // Array of tags added, each containing:
      {
        "tag_id": "string",     // ID of the tag.
        "tagged_media_id": "string" // ID of the tagged media.
      }
    ],
    "is_child": "boolean",      // Indicates if this post is a child post.
    "parent_id": "string"       // The ID of the parent post (if this is a reply).
  }
  ```

**Failure Responses:**

- **Status Code:** `400 Bad Request`
  - **Content Type:** `application/json`
  - **Response Body:**
    ```json
    {
      "error": "No text content provided" // When 'text_content' is missing.
    }
    ```
  - **Response Body:**
    ```json
    {
      "error": "No is_child provided" // When 'is_child' is missing.
    }
    ```
  - **Response Body:**
    ```json
    {
      "error": "This is a child post, but no parent_id was provided" // When 'is_child' is true but 'parent_id' is missing.
    }
    ```
  - **Response Body:**
    ```json
    {
      "error": "Invalid parent post id" // When 'parent_id' is invalid.
    }
    ```
  - **Response Body:**
    ```json
    {
      "error": "Error adding mention to post, please try sending request again" // When a mention cannot be added.
    }
    ```
  - **Response Body:**
    ```json
    {
      "error": "Error adding tag to post, please try sending request again" // When a tag cannot be added.
    }
    ```

- **Status Code:** `500 Internal Server Error`
  - **Content Type:** `application/json`
  - **Response Body:**
    ```json
    {
      "error": "string" // Error message describing the server issue.
    }
    ```

---
### 17. Get Child Posts
**URL:** `/api/feed/child_posts`  
**Method:** `GET`  
**Description:** Retrieves child posts for a given parent post.  
**Authorization:** No authentication required.

**Request Body:**
```json
{
  "parent_id": "string",                     // The ID of the parent post.
  "requested_num_of_posts": "integer" (optional) // Number of child posts to retrieve.
}
```

**Success Response:**

- **Status Code:** `200 OK`
- **Content Type:** `application/json`
- **Response Body:**
  ```json
  {
    "posts": [                  // Array of child posts, each containing:
      {
        "post_id": "string",     // The ID of the child post.
        "user_id": "string",     // The ID of the user who created the post.
        "text_content": "string", // The content of the post.
        "parent_id": "string",   // The ID of the parent post.
        "is_child": "boolean",   // Indicates if this post is a child post.
        "mentions": [            // Array of mentions, each containing:
          {
            "mention_id": "string",       // ID of the mention.
            "mentioned_user_id": "string" // ID of the mentioned user.
          }
        ],
        "tags": [                // Array of tags, each containing:
          {
            "tag_id": "string",     // ID of the tag.
            "tagged_media_id": "string" // ID of the tagged media.
          }
        ]
      }
    ]
  }
  ```

**Failure Responses:**

- **Status Code:** `400 Bad Request`
  - **Content Type:** `application/json`
  - **Response Body:**
    ```json
    {
      "error": "No parent_id was provided" // When 'parent_id' is missing.
    }
    ```
  - **Response Body:**
    ```json
    {
      "error": "Invalid parent post id" // When 'parent_id' is invalid.
    }
    ```

- **Status Code:** `500 Internal Server Error`
  - **Content Type:** `application/json`
  - **Response Body:**
    ```json
    {
      "error": "string" // Error message describing the server issue.
    }
    ```
---
### 19. Get Posts by User
**URL:** `/api/feed/user`  
**Method:** `GET`  
**Description:** Retrieves posts created by a specific user.  
**Authorization:** No authentication required.

**Request Body:**
```json
{
  "user_id": "string",                    // The ID of the user whose posts are being requested.
  "requested_num_of_posts": "integer" (optional) // The number of posts to retrieve.
}
```

**Success Response:**

- **Status Code:** `200 OK`
- **Content Type:** `application/json`
- **Response Body:**
  ```json
  {
    "user_posts": [           // Array of posts created by the user, each containing:
      {
        "post_id": "string",      // The ID of the post.
        "text_content": "string", // The content of the post.
        "parent_id": "string" (optional), // The ID of the parent post (if this is a reply).
        "is_child": "boolean",    // Indicates if this post is a child post.
        "mentions": [             // Array of mentions, each containing:
          {
            "mention_id": "string",       // ID of the mention.
            "mentioned_user_id": "string" // ID of the mentioned user.
          }
        ],
        "tags": [                 // Array of tags, each containing:
          {
            "tag_id": "string",      // ID of the tag.
            "tagged_media_id": "string" // ID of the tagged media.
          }
        ]
      }
    ],
    "user_id": "string"          // The ID of the user whose posts are returned.
  }
  ```

**Failure Responses:**

- **Status Code:** `400 Bad Request`
  - **Content Type:** `application/json`
  - **Response Body:**
    ```json
    {
      "error": "Invalid number of posts requested" // When 'requested_num_of_posts' is negative.
    }
    ```

- **Status Code:** `500 Internal Server Error`
  - **Content Type:** `application/json`
  - **Response Body:**
    ```json
    {
      "error": "string" // Error message describing the server issue.
    }
    ```
---
### 20. Get Last N Posts
**URL:** `/api/feed/`  
**Method:** `GET`  
**Description:** Retrieves the last N posts from the feed. Optionally, it can retrieve the last N posts created before a certain timestamp - usable for loading earlier feed posts.
**Authorization:** No authentication required.

**Request Body:**
```json
{
  "number_of_posts": "integer",     // The number of posts to retrieve.
  "earlier_than": "string" (optional) // Optional timestamp of the post to retrieve posts earlier than.
}
```

**Success Response:**

- **Status Code:** `200 OK`
- **Content Type:** `application/json`
- **Response Body:**
  ```json
  {
    "posts": [                // Array of posts, each containing:
      {
        "post_id": "string",      // The ID of the post.
        "user_id": "string",      // The ID of the user who created the post.
        "text_content": "string", // The content of the post.
        "parent_id": "string" (optional), // The ID of the parent post (if this is a reply).
        "is_child": "boolean",    // Indicates if this post is a child post.
        "mentions": [             // Array of mentions, each containing:
          {
            "mention_id": "string",       // ID of the mention.
            "mentioned_user_id": "string" // ID of the mentioned user.
          }
        ],
        "tags": [                 // Array of tags, each containing:
          {
            "tag_id": "string",      // ID of the tag.
            "tagged_media_id": "string" // ID of the tagged media.
          }
        ]
      }
    ]
  }
  ```

**Failure Responses:**

- **Status Code:** `400 Bad Request`
  - **Content Type:** `application/json`
  - **Response Body:**
    ```json
    {
      "error": "Invalid number of posts" // When 'number_of_posts' is missing or negative.
    }
    ```

- **Status Code:** `500 Internal Server Error`
  - **Content Type:** `application/json`
  - **Response Body:**
    ```json
    {
      "error": "string" // Error message describing the server issue.
    }
    ```
---
### 21. Delete Post
**URL:** `/api/feed`  
**Method:** `DELETE`  
**Description:** Deletes a post identified by its ID.  
**Authorization:** Token-based authentication required.

**Request Body:**
```json
{
  "post_id": "string"  // The ID of the post to delete.
}
```

**Success Response:**

- **Status Code:** `201 Created`
- **Content Type:** `application/json`
- **Response Body:**
  ```json
  {
    "post_id": "string",       // The ID of the deleted post.
    "success": "string"  // Success message indicating the post has been successfully deleted.
  }
  ```

**Failure Responses:**

- **Status Code:** `400 Bad Request`
  - **Content Type:** `application/json`
  - **Response Body:**
    ```json
    {
      "error": "No post id provided" // When 'post_id' is missing.
    }
    ```

- **Status Code:** `500 Internal Server Error`
  - **Content Type:** `application/json`
  - **Response Body:**
    ```json
    {
      "error": "string" // Error message describing the server issue.
    }
    ```
---
### 24. Get Streaming Services Recommendation
**URL:** `/api/watchlists/streaming_recommendation`  
**Method:** `GET`  
**Description:** Returns a streaming service recommendation based on the service with the most content available from the watchlist. 

**Authorization:** Token-based authentication required.

**Request Body:**
```json
{
  "watchlist_id": "string"  // Optional - when no id is provided, the recommendation will be based on the main watchlist.
  "territory": "string"     // Optional - "US" by default. The country codes are based on TMDB's codes.
}
```

**Success Response:**

- **Status Code:** `200 Success`
- **Content Type:** `application/json`
- **Response Body:**
  ```json
  {
    "providers": {
        "Amazon Prime Video": {
            "count": 1,
            "tmdb_ids": [
                {
                    "is_movie": 0,
                    "tmdb_id": "62017"
                }
            ]
        },
        "Amazon Prime Video with Ads": {
            "count": 1,
            "tmdb_ids": [
                {
                    "is_movie": 0,
                    "tmdb_id": "62017"
                }
            ]
        },
        "Apple TV Plus": {
            "count": 1,
            "tmdb_ids": [
                {
                    "is_movie": 0,
                    "tmdb_id": "95396"
                }
            ]
        },
        "Disney Plus": {
            "count": 1,
            "tmdb_ids": [
                {
                    "is_movie": 1,
                    "tmdb_id": "1022789"
                }
            ]
        },
        "Hulu": {
            "count": 2,
            "tmdb_ids": [
                {
                    "is_movie": 1,
                    "tmdb_id": "550"
                },
                {
                    "is_movie": 0,
                    "tmdb_id": "111800"
                }
            ]
        },
        "Max": {
            "count": 1,
            "tmdb_ids": [
                {
                    "is_movie": 1,
                    "tmdb_id": "473033"
                }
            ]
        },
        "Max Amazon Channel": {
            "count": 1,
            "tmdb_ids": [
                {
                    "is_movie": 1,
                    "tmdb_id": "473033"
                }
            ]
        },
        "Netflix": {
            "count": 3,
            "tmdb_ids": [
                {
                    "is_movie": 1,
                    "tmdb_id": "704239"
                },
                {
                    "is_movie": 1,
                    "tmdb_id": "646097"
                },
                {
                    "is_movie": 1,
                    "tmdb_id": "569547"
                }
            ]
        },
        "Netflix basic with Ads": {
            "count": 3,
            "tmdb_ids": [
                {
                    "is_movie": 1,
                    "tmdb_id": "704239"
                },
                {
                    "is_movie": 1,
                    "tmdb_id": "646097"
                },
                {
                    "is_movie": 1,
                    "tmdb_id": "569547"
                }
            ]
        },
        "Paramount Plus": {
            "count": 1,
            "tmdb_ids": [
                {
                    "is_movie": 1,
                    "tmdb_id": "762441"
                }
            ]
        },
        "Paramount Plus Apple TV Channel ": {
            "count": 1,
            "tmdb_ids": [
                {
                    "is_movie": 1,
                    "tmdb_id": "762441"
                }
            ]
        },
        "Paramount+ Amazon Channel": {
            "count": 1,
            "tmdb_ids": [
                {
                    "is_movie": 1,
                    "tmdb_id": "762441"
                }
            ]
        },
        "Paramount+ Roku Premium Channel": {
            "count": 1,
            "tmdb_ids": [
                {
                    "is_movie": 1,
                    "tmdb_id": "762441"
                }
            ]
        },
        "fuboTV": {
            "count": 1,
            "tmdb_ids": [
                {
                    "is_movie": 0,
                    "tmdb_id": "111800"
                }
            ]
        }
    }
}

**Failure Responses:**

- **Status Code:** `400 Bad Request`
  - **Content Type:** `application/json`
  - **Response Body:**
    ```json
    {
      "error": "No watchlist id or user token provided" // When 'watchlist_id' and token info are missing.
    }
    ```

- **Status Code:** `404 Not Found`
  - **Content Type:** `application/json`
  - **Response Body:**
    ```json
    {
      "error": "Watchlist not found" // When the watchlist cannot be retrieved from the database.
    }
    ```

- **Status Code:** `404 Not Found`
  - **Content Type:** `application/json`
  - **Response Body:**
    ```json
    {
      "error": "No streaming providers found" // When no streaming providers are found for the watchlist.
    }
    ```

- **Status Code:** `500 Internal Server Error`
  - **Content Type:** `application/json`
  - **Response Body:**
    ```json
    {
      "error": "Database error" // When there's an issue fetching the main watchlist or other database errors occur.
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


### 21. Get Actor Information
- **URL:** `/api/actor/<string:actor_id>`
- **Method:** `GET`
- **Description:** Retrieves information about a specific Actor.
- **Parameters:** 
  - `actor_id` (string, required): The ID of the Actor.
- **Authorization:** Not required.
- **Response:** 
  - **200 OK** - Successfully retrieved actor information.
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

### 22. Get Actor media aperance  Information

- **URL:** `/api/actor/combine_credits/<string:actor_id>`
- **Method:** `GET`
- **Description:** Retrieves information about the aperance of an actor in a media
- **Parameters:** 
  - `actor_id` (string, required): The ID of the actor.
- **Authorization:** Not required.
- **Response:** 
  - **200 OK** - Successfully retrieved media apperance.
    - Content example:
```Json
{
 "cast": [
    {
      "adult": false, 
      "character": "Self", 
      "first_air_date": "1996-07-22", 
      "id": 2224, 
      "name": "The Daily Show", 
      "original_name": "The Daily Show", 
      "popularity": 2067.696, 
      "large_poster_path": string (original sized poster)
      "small_poster_path":,"/ixcfy (w200 image)K7it6FjRM36Te4OdblAq4X.jpg"
    }, 
    {
      "adult": false, 
      "character": "Himself", 
      "first_air_date": "2003-01-26", 
      "id": 1489,
      "media_kind": "tv",           ,
      "name": "Jimmy Kimmel Live!", 
      "original_name": "Jimmy Kimmel Live!", 
      "popularity": 494.357, 
      "large_poster_path": string (original sized poster)
      "small_poster_path":,"/6uKEY (w200 image)ejjR88GwHgNq6NAQ30glTx.jpg"
    }
        ],
    "crew": [
    {
      "adult": false, 
      "department": "Writing", 
      "id": 9428,
      "media_kind": "tv",           
      "job": "Writer", 
      "original_title": "The Royal Tenenbaums", 
      "popularity": 26.071, 
      "large_poster_path": string (original sized poster)
      "small_poster_path":,"/hwklE (w200 image)whBhLVI6v3ISlquFTeQIml.jpg", 
      "release_date": "2001-10-05", 
      "title": "The Royal Tenenbaums", 
      "video": false
    }, 
    {
      "adult": false, 
      "department": "Production", 
      "id": 9428, 
      "job": "Executive Producer", 
      "original_title": "The Royal Tenenbaums", 
      "popularity": 26.071, 
      "large_poster_path": string (original sized poster)
      "small_poster_path": string (w200 image),
      "release_date": "2001-10-05", 
      "title": "The Royal Tenenbaums", 
      "video": false
    }
  ]
}
```
  
  - **500 Internal Server Error** - The server encountered an unexpected condition which prevented it from fulfilling the request.
    - Content: Empty object.

### 23. Get combine serch result:

- **URL:** `/api/Media_search?query={query}`
- **Method:** `GET`
- **Description:** Retrieves information about a specific movie.
- **Parameters:** 
  - `query` (string,get varible, required): the media you want to serch.
- **Authorization:** Not required.
- **Response:** 
  - **200 OK** - Successfully retrieved serch results.
    - Content: example
```Json
[
{
    "adult": false, 
    "backdrop_path": "/fY3lD0jM5AoHJMunjGWqJ0hRteI.jpg", 
    "genre_ids": [
      878, 
      27, 
      28
    ],
    "media_kind": "tv", 
    "id": 940721, 
    "original_language": "ja", 
    "original_title": "\u30b4\u30b8\u30e9-1.0", 
    "overview": "In postwar Japan, Godzilla brings new devastation to an already scorched landscape. With no military intervention or government help in sight, the survivors must join together in the face of despair and fight back against an unrelenting horror.", 
    "popularity": 487.791, 
    "large_poster_path": string (original sized poster),
    "small_poster_path": string (w200 image), 
    "release_date": "2023-11-03", 
    "title": "Godzilla Minus One", 
    "video": false, 
    "vote_average": 7.619, 
    "vote_count": 1716
  }, 
  {
    "adult": false, 
    "backdrop_path": "/ftiQHOrAGTGXVsJ1pcAVC5Dau78.jpg", 
    "first_air_date": "1999-10-25", 
    "genre_ids": [
      10766, 
      35, 
      18
    ],
    "media_kind": "tv",     
    "id": 16286, 
    "name": "I am Betty, the Ugly one", 
    "origin_country": [
      "CO"
    ], 
    "original_language": "es", 
    "original_name": "Yo soy Betty, la fea", 
    "overview": "Taking place mainly in Bogot\u00e1, Colombia, Betty La Fea is essentially a Cinderella comedy about the rise of poor, ugly 'Betty' Pinz\u00f3n and the fall of rich, handsome Armando Mendoza. Armando is a very incompetent playboy with a scheme to turn a huge profit as the new President of Eco Moda, a famous clothing manufacturing company, but his scheme is doomed because of his faulty mathematics. Because Betty, his secretary (and economics wizard), is in love with him, she helps Armando deceive the Board of Directors as he loses money and brings the company to ruin.\n\nBetty, la Fea is arguably the most successful telenovela of all time and one of the most popular television shows in the world. It is the first telenovela to have been remade worldwide and has been regarded as bringing the telenovela to new levels of success.", 
    "popularity": 234.021, 
    "large_poster_path":string (original sized poster) string,
    "small_poster_path": string, (w200 image)
    "vote_average": 8.35, 
    "vote_count": 3283
  }
]
```
  - **500 Internal Server Error** - The server encountered an unexpected condition which prevented it from fulfilling the request.
    - Content: Empty object.

### 24. Get media recomandation:

- **URL:** `/api/Media_recomandation?usr_id={user_id}`
- **Method:** `GET`
- **Description:** Get recomandation for a user
- **Parameters:** 
  - `usr_id` : The id of the user that wants recomandation
- **Authorization:** Not required.
- **Response:** 
  - **200 OK** - Successfully retrieved serch results.
    - Content: example
```Json
[
  {
    "Is_movie": 1,
    "Recomended_by": "Algorithem1",
    "id": 10537,
    "overview": "The story of the famous and influential 1960s rock band and its lead singer and composer, Jim Morrison.",
    "poster_path": "/x1LM3dzGuG6xOz0aT2e71o11vhu.jpg",
    "release_date": "1991-03-01",
    "title": "The Doors",
    "trailer": "qJu9nfVCQmk",
    "vote_average": 7.128
  },
  {
    "Is_movie": 1,
    "Recomended_by": "Algorithem1",
    "id": 678512,
    "overview": "The story of Tim Ballard, a former US government agent, who quits his job in order to devote his life to rescuing children from global sex traffickers.",
    "poster_path": "/kSf9svfL2WrKeuK8W08xeR5lTn8.jpg",
    "release_date": "2023-07-03",
    "title": "Sound of Freedom",
    "trailer": "Rt0kp4VW1cI",
    "vote_average": 8.003
  },
  {
    "Is_movie": 1,
    "Recomended_by": "Algorithem1",
    "id": 2897,
    "overview": "Based on the famous book by Jules Verne the movie follows Phileas Fogg on his journey around the world. Which has to be completed within 80 days, a very short period for those days.",
    "poster_path": "/kk6Rrwh0toMz9tjuUHdS4O3v2Rk.jpg",
    "release_date": "1956-10-17",
    "title": "Around the World in Eighty Days",
    "trailer": "vjiCO8k6Jhg",
    "vote_average": 6.6
  },
  {
    "Is_movie": 1,
    "Recomended_by": "Algorithem1",
    "id": 330459,
    "overview": "A rogue band of resistance fighters unite for a mission to steal the Death Star plans and bring a new hope to the galaxy.",
    "poster_path": "/i0yw1mFbB7sNGHCs7EXZPzFkdA1.jpg",
    "release_date": "2016-12-14",
    "title": "Rogue One: A Star Wars Story",
    "trailer": "sC9abcLLQpI",
    "vote_average": 7.492
  },
  {
    "Is_movie": 0,
    "Recomended_by": "Algorithem1",
    "id": 96129,
    "name": "Don't F**k with Cats: Hunting an Internet Killer",
    "overview": "A group of online justice seekers track down a guy who posted a video of him killing kittens.",
    "poster_path": "/Crc4XkhLddMTNJfj1iLca0w1Bb.jpg",
    "trailer": "tgkXpowex-g",
    "vote_average": 7.6
  }
]

```
### 25. FeedBack for recomandation:

- **URL:** `/api/recomandation_feedback`
- **Method:** `GET`
- **Description:** Get recomandation for a user
- **Body:**
  ```Json
  
  {
  
  "is_movie" :  1,
  "media_id" : "945961",
  "is_liked":1,
  "algorithm":"algo1"
  }
  ```
- **Authorization:** Not required.
- **Response:** 
  - **200 OK** - Successfully retrieved serch results.
      ```Json
      
    "Content": [
        {
            "genres": [
                "Science Fiction",
                "Horror"
            ],
            "is_movie": 1,
            "overview": "While scavenging the deep ends of a derelict space station, a group of young space colonizers come face to face with the most terrifying life form in the universe.",
            "poster_path": "https://image.tmdb.org/t/p/original//b33nnKl1GSFbao4l3fZDDqsMx0F.jpg",
            "release_date": "2024-08-13",
            "small_poster_path": "https://image.tmdb.org/t/p/w200//b33nnKl1GSFbao4l3fZDDqsMx0F.jpg",
            "title": "Alien: Romulus",
            "tmdb_id": "945961",
            "tmdb_rating": 7.3,
            "user_rating": null,
            "video_links": [
                "H68iU7fqW-w"
            ],
            "watchlist_item_id": "bb88295414e7"
        }
    ],
    "ID": "1806f2f489f2"
    
      ```
      "0" other wise
    
### 26. Get Recommendation Watchlist
**URL:** `/api/watchlists/recommendation`  
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
            "genres": [
                "Horror",
                "Thriller"
            ],
            "is_movie": 1,
            "overview": "Five years after surviving Art the Clown's Halloween massacre, Sienna and Jonathan are still struggling to rebuild their shattered lives. As the holiday season approaches, they try to embrace the Christmas spirit and leave the horrors of the past behind. But just when they think they're safe, Art returns, determined to turn their holiday cheer into a new nightmare. The festive season quickly unravels as Art unleashes his twisted brand of terror, proving that no holiday is safe.",
            "poster_path": "https://image.tmdb.org/t/p/original//63xYQj1BwRFielxsBDXvHIJyXVm.jpg",
            "release_date": "2024-10-09",
            "small_poster_path": "https://image.tmdb.org/t/p/w200//63xYQj1BwRFielxsBDXvHIJyXVm.jpg",
            "title": "Terrifier 3",
            "tmdb_id": "1034541",
            "tmdb_rating": 7.189,
            "user_rating": null,
            "video_links": [
                "zb2P9y70lJE"
            ],
            "watchlist_item_id": "ca3aa35509de"
        }
    ],
    "ID": "7bc95103afe4"
}
  ```
