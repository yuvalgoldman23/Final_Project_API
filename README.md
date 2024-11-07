# Flask Server README

This Flask server + MySQL Database provides endpoints for managing user watchlists, creating posts, fetching posts, performing content related queries and retrieving streaming providers, all while performing authorization of client requests via Google OAuth.

## Installation

**Database Setup:**

To run the database, make sure you have a MySQL server program, such as MySQL Workbench, installed. In that program, create a new connection, then run the following SQL command:
```sql
CREATE DATABASE final_project_DB;
```
Now, download the following database file: https://drive.google.com/file/d/1jFzXS_ro0xRgpkI-i8vOAGr4AcKMBVh-/view?usp=drive_link

Then, through the program, import the downloaded data into the SQL server.
After finishing this step, you're all set to continue to setting up the Flask server.

**Flask server Setup:**

To run this server, make sure you have Python installed on your system. Clone the repository and install the dependencies using the `requirements.txt` file:

```bash
git clone https://github.com/yuvalgoldman23/Final_Project_API.git
cd Final_Project_API
pip install -r requirements.txt
python -m spacy download en_core_web_md
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

        Authroization: Google OAuth 2.0 User Login access token
        Content Type "application/json"


## Endpoints

## 1. Login
**URL:** `/api/login`  
**Method:** `POST`  
**Description:** Logs the user in using Google authentication, creating a new user if necessary.
The response will contain the user's watchlist, ratings-list and streaming-services list.

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
  "main_watchlist": {  
    "Content": {  
      "Content": [  
        {  
          "genres": [  
            "Science Fiction",  
            "Action",  
            "Adventure"  
          ],  
          "is_movie": 1,  
          "overview": "Eddie and Venom are on the run. Hunted by both of their worlds and with the net closing in, the duo are forced into a devastating decision that will bring the curtains down on Venom and Eddie's last dance.",  
          "poster_path": "https://image.tmdb.org/t/p/original//k42Owka8v91trK1qMYwCQCNwJKr.jpg",  
          "release_date": "2024-10-22",  
          "small_poster_path": "https://image.tmdb.org/t/p/w200//k42Owka8v91trK1qMYwCQCNwJKr.jpg",  
          "title": "Venom: The Last Dance",  
          "tmdb_id": "912649",  
          "tmdb_rating": 6.7,  
          "user_rating": null,  
          "video_links": [  
            "y1M-nGQblmw"  
          ],  
          "watchlist_item_id": "111842b80c3e"  
        },  
        {  
          "genres": [  
            "Adventure",  
            "Comedy",  
            "Fantasy",  
            "Action"  
          ],  
          "is_movie": 1,  
          "overview": "When an old card game comes to life, a family jumps back in time to a medieval village where they must unmask werewolves to secure their return home.",  
          "poster_path": "https://image.tmdb.org/t/p/original//uL1dR0L65GZgy3h2gvZcxDu0bRG.jpg",  
          "release_date": "2024-10-22",  
          "small_poster_path": "https://image.tmdb.org/t/p/w200//uL1dR0L65GZgy3h2gvZcxDu0bRG.jpg",  
          "title": "Family Pack",  
          "tmdb_id": "1091181",  
          "tmdb_rating": 5.74,  
          "user_rating": null,  
          "video_links": [  
            "bqd702kNnRk"  
          ],  
          "watchlist_item_id": "18c43f65d326"  
        }  
      ],  
      "ID": "7f3af4a2c18d"  
    },  
    "ID": "7f3af4a2c18d"  
  },  
  "main_watchlist_id": "7f3af4a2c18d",  
  "ratings_list": {  
    "Content": [  
      {  
        "genres": [  
          "Comedy"  
        ],  
        "is_movie": 0,  
        "list_item_id": "27204a8ce0dc",  
        "overview": "Jimmy is struggling to grieve the loss of his wife while being a dad, friend, and therapist. He decides to try a new approach with everyone in his path: unfiltered, brutal honesty.",  
        "poster_path": "https://image.tmdb.org/t/p/original//cVmrNYgm5wcEexbXg4laNn3u4vq.jpg",  
        "release_date": "2023-01-26",  
        "small_poster_path": "https://image.tmdb.org/t/p/w200//cVmrNYgm5wcEexbXg4laNn3u4vq.jpg",  
        "title": "Shrinking",  
        "tmdb_id": "136311",  
        "tmdb_rating": 7.8,  
        "user_id": "113749586527602021810",  
        "user_rating": 8,  
        "video_links": "1oxk9A44Z-g"  
      },  
      {  
        "genres": [  
          "Thriller",  
          "Action"  
        ],  
        "is_movie": 1,  
        "list_item_id": "9ae5b1833efb",  
        "overview": "As storm season intensifies, the paths of former storm chaser Kate Carter and reckless social-media superstar Tyler Owens collide when terrifying phenomena never seen before are unleashed. The pair and their competing teams find themselves squarely in the paths of multiple storm systems converging over central Oklahoma in the fight of their lives.",  
        "poster_path": "https://image.tmdb.org/t/p/original//pjnD08FlMAIXsfOLKQbvmO0f0MD.jpg",  
        "release_date": "2024-07-10",  
        "small_poster_path": "https://image.tmdb.org/t/p/w200//pjnD08FlMAIXsfOLKQbvmO0f0MD.jpg",  
        "title": "Twisters",  
        "tmdb_id": "718821",  
        "tmdb_rating": 7.0,  
        "user_id": "113749586527602021810",  
        "user_rating": 7,  
        "video_links": "-JFEf1qtns0"  
      },  
      {  
        "genres": [  
          "Drama",  
          "Comedy"  
        ],  
        "is_movie": 0,  
        "list_item_id": "9bb73946cb56",  
        "overview": "Chicagoan Frank Gallagher is the proud single dad of six smart, industrious, independent kids, who without him would be... perhaps better off. When Frank's not at the bar spending what little money they have, he's passed out on the floor. But the kids have found ways to grow up in spite of him. They may not be like any family you know, but they make no apologies for being exactly who they are.",  
        "poster_path": "https://image.tmdb.org/t/p/original//9akij7PqZ1g6zl42DQQTtL9CTSb.jpg",  
        "release_date": "2011-01-09",  
        "small_poster_path": "https://image.tmdb.org/t/p/w200//9akij7PqZ1g6zl42DQQTtL9CTSb.jpg",  
        "title": "Shameless",  
        "tmdb_id": "34307",  
        "tmdb_rating": 8.157,  
        "user_id": "113749586527602021810",  
        "user_rating": 5,  
        "video_links": "9tvkYS5cA58"  
      }  
    ]  
  },  
  "watchlist_streaming_data": {  
    "best_providers": {  
      "Netflix": {  
        "count": 1,  
        "tmdb_ids": [  
          {  
            "is_movie": 1,  
            "tmdb_id": "1091181"  
          }  
        ]  
      }  
    },  
    "providers": {  
      "Netflix": {  
        "count": 1,  
        "tmdb_ids": [  
          {  
            "is_movie": 1,  
            "tmdb_id": "1091181"  
          }  
        ]  
      }  
    }  
  }  
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
    "logged_in": boolean
  }

  ```


### 4. Get Main Watchlist
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
        "poster_path": string (original sized poster)
  "small_poster_path":, "string (w200 image)g" (or null in case of no image in TMDB's response)',
        "tmdb_id":  "string",
        "overview": "string",
        "release_date": "string" (yyyy-mm-dd format)
        "tmdb_rating": "float", (or null in case of no tmdb rating)
        "user_rating": "int" (or null in case of no user rating)
        "video_links": "[string]"
      }
    ],
    "Name": "string",
    "ID": "string"
  }
  ```
- **Response Example:**
  ```json{
    {
  "Content": [
        {
            "genres": [
                "Science Fiction",
                "Action",
                "Adventure"
            ],
            "is_movie": 1,
            "overview": "Eddie and Venom are on the run. Hunted by both of their worlds and with the net closing in, the duo are forced into a devastating decision that will bring the curtains down on Venom and Eddie's last dance.",
            "poster_path": "https://image.tmdb.org/t/p/original//k42Owka8v91trK1qMYwCQCNwJKr.jpg",
            "release_date": "2024-10-22",
            "small_poster_path": "https://image.tmdb.org/t/p/w200//k42Owka8v91trK1qMYwCQCNwJKr.jpg",
            "title": "Venom: The Last Dance",
            "tmdb_id": "912649",
            "tmdb_rating": 6.7,
            "user_rating": null,
            "video_links": [
                "y1M-nGQblmw"
            ],
            "watchlist_item_id": "111842b80c3e"
        },
        {
            "genres": [
                "Adventure",
                "Comedy",
                "Fantasy",
                "Action"
            ],
            "is_movie": 1,
            "overview": "When an old card game comes to life, a family jumps back in time to a medieval village where they must unmask werewolves to secure their return home.",
            "poster_path": "https://image.tmdb.org/t/p/original//uL1dR0L65GZgy3h2gvZcxDu0bRG.jpg",
            "release_date": "2024-10-22",
            "small_poster_path": "https://image.tmdb.org/t/p/w200//uL1dR0L65GZgy3h2gvZcxDu0bRG.jpg",
            "title": "Family Pack",
            "tmdb_id": "1091181",
            "tmdb_rating": 5.74,
            "user_rating": null,
            "video_links": [
                "bqd702kNnRk"
            ],
            "watchlist_item_id": "18c43f65d326"
        }
    ],
    "ID": "7f3af4a2c18d"
  }
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

### 5. Create Watchlist
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

### 6. Delete Content from Watchlist
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

### 7. Get Watchlist by ID
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

### 8. Get All User Watchlists
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

### 9. Add Movie/Show to Watchlist
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

### 10. Delete User Watchlist
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

### 11. Add Rating
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

### 12. Get Ratings by User
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

### 13. Remove Rating
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


### 14. Update Rating
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
### 15. Get User's Rating List
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
---
### 16. Get Streaming Services Recommendation
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

### 17. Get Streaming Providers

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

### 18. Get Trending TV Shows

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

### 19. Get Trending Movies

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

### 20. Get TV Show Information

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

### 21. Get TV Show Cast

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

### 22. Get Movie Cast

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

### 23. Get Movie Information

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


### 24. Get Actor Information
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

### 25. Get Actor media aperance  Information

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

### 26. Get combine search result:

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

### 27. Get machine-learning-based media recommendation:

- **URL:** `/api/Media_recomandation?usr_id={user_id}`
- **Method:** `GET`
- **Description:** Get recommendation for a user
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
### 28. Get user feedBack for recommendations:

- **URL:** `/api/recomandation_feedback`
- **Method:** `GET`
- **Description:** Get recommendation for a user
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
      "0" otherwise
    
### 29. Get Recommendation Watchlist
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


---
### 30. Content Discovery Wizard
**URL:** `/api/discover`

**Method:** `POST`

**Description:** Returns content filtered according to user-set parameters delivered by client.

**Authorization:** Not required.

**Request Body:**
```json
{
  "content_type": "string" ("movie", "tv" or "mixed"),
  "year": "string", (optional. The earliest year to consider content from.),
  "vote_average": "number", (optional. The lowest average rating to show content with.),
  "genres": ["number"], (optional. An array of IDs of the genres the content shall be of),
  "region": "string", (optional. The region to look for availability in streaming services),
  "provider": "number", (optional, but must come together with a region. The id of the streaming service the user would like to find content available on) 
}
```

**Success Response:**:
- **Status Code:** `200 OK`
- **Content Type:** `application/json`
- **Response Body:**
```json

[
    {
        "adult": false,
        "backdrop_path": "/gMQibswELoKmB60imE7WFMlCuqY.jpg",
        "genre_ids": [
            27,
            53,
            9648
        ],
        "id": 1034541,
        "original_language": "en",
        "original_title": "Terrifier 3",
        "overview": "Five years after surviving Art the Clown's Halloween massacre, Sienna and Jonathan are still struggling to rebuild their shattered lives. As the holiday season approaches, they try to embrace the Christmas spirit and leave the horrors of the past behind. But just when they think they're safe, Art returns, determined to turn their holiday cheer into a new nightmare. The festive season quickly unravels as Art unleashes his twisted brand of terror, proving that no holiday is safe.",
        "popularity": 6883.159,
        "poster_path": "/63xYQj1BwRFielxsBDXvHIJyXVm.jpg",
        "release_date": "2024-10-09",
        "title": "Terrifier 3",
        "video": false,
        "vote_average": 7.306,
        "vote_count": 586
    },
    {
        "adult": false,
        "backdrop_path": "/3V4kLQg0kSqPLctI5ziYWabAZYF.jpg",
        "genre_ids": [
            878,
            28,
            12
        ],
        "id": 912649,
        "original_language": "en",
        "original_title": "Venom: The Last Dance",
        "overview": "Eddie and Venom are on the run. Hunted by both of their worlds and with the net closing in, the duo are forced into a devastating decision that will bring the curtains down on Venom and Eddie's last dance.",
        "popularity": 5590.757,
        "poster_path": "/k42Owka8v91trK1qMYwCQCNwJKr.jpg",
        "release_date": "2024-10-22",
        "title": "Venom: The Last Dance",
        "video": false,
        "vote_average": 6.72,
        "vote_count": 473
    },
    {
        "adult": false,
        "backdrop_path": "/4zlOPT9CrtIX05bBIkYxNZsm5zN.jpg",
        "genre_ids": [
            16,
            878,
            10751
        ],
        "id": 1184918,
        "original_language": "en",
        "original_title": "The Wild Robot",
        "overview": "After a shipwreck, an intelligent robot called Roz is stranded on an uninhabited island. To survive the harsh environment, Roz bonds with the island's animals and cares for an orphaned baby goose.",
        "popularity": 4321.421,
        "poster_path": "/wTnV3PCVW5O92JMrFvvrRcV39RU.jpg",
        "release_date": "2024-09-12",
        "title": "The Wild Robot",
        "video": false,
        "vote_average": 8.543,
        "vote_count": 2370
    },
    {
        "adult": false,
        "backdrop_path": "/9oYdz5gDoIl8h67e3ccv3OHtmm2.jpg",
        "genre_ids": [
            18,
            27,
            878
        ],
        "id": 933260,
        "original_language": "en",
        "original_title": "The Substance",
        "overview": "Have you ever dreamt of a better version of yourself? You, only better in every way. You should try this new product, it's called The Substance. IT CHANGED MY LIFE.",
        "popularity": 2881.789,
        "poster_path": "/lqoMzCcZYEFK729d6qzt349fB4o.jpg",
        "release_date": "2024-09-07",
        "title": "The Substance",
        "video": false,
        "vote_average": 7.3,
        "vote_count": 1369
    },
    {
        "adult": false,
        "backdrop_path": "/uGmYqxh8flqkudioyFtD7IJSHxK.jpg",
        "genre_ids": [
            18,
            80,
            53
        ],
        "id": 889737,
        "original_language": "en",
        "original_title": "Joker: Folie à Deux",
        "overview": "While struggling with his dual identity, Arthur Fleck not only stumbles upon true love, but also finds the music that's always been inside him.",
        "popularity": 2614.505,
        "poster_path": "/if8QiqCI7WAGImKcJCfzp6VTyKA.jpg",
        "release_date": "2024-10-01",
        "title": "Joker: Folie à Deux",
        "video": false,
        "vote_average": 5.688,
        "vote_count": 1339
    },
    {
        "adult": false,
        "backdrop_path": "/oPUOpnl3pqD8wuidjfUn17mO1yA.jpg",
        "genre_ids": [
            16,
            878,
            12,
            10751
        ],
        "id": 698687,
        "original_language": "en",
        "original_title": "Transformers One",
        "overview": "The untold origin story of Optimus Prime and Megatron, better known as sworn enemies, but once were friends bonded like brothers who changed the fate of Cybertron forever.",
        "popularity": 2550.704,
        "poster_path": "/iHPIBzrjJHbXeY9y7VVbEVNt7LW.jpg",
        "release_date": "2024-09-11",
        "title": "Transformers One",
        "video": false,
        "vote_average": 8.17,
        "vote_count": 529
    },
    {
        "adult": false,
        "backdrop_path": "/jWXrQstj7p3Wl5MfYWY6IHqRpDb.jpg",
        "first_air_date": "1952-12-26",
        "genre_ids": [
            10763
        ],
        "id": 94722,
        "name": "Tagesschau",
        "origin_country": [
            "DE"
        ],
        "original_language": "de",
        "original_name": "Tagesschau",
        "overview": "German daily news program, the oldest still existing program on German television.",
        "popularity": 2533.645,
        "poster_path": "/7dFZJ2ZJJdcmkp05B9NWlqTJ5tq.jpg",
        "vote_average": 6.739,
        "vote_count": 207
    },
    {
        "adult": false,
        "backdrop_path": "/aizbHLcKVWvJ7jxkflJzTu5Z8GE.jpg",
        "first_air_date": "2018-08-27",
        "genre_ids": [
            10766
        ],
        "id": 81329,
        "name": "Chronicles of the Sun",
        "origin_country": [
            "FR"
        ],
        "original_language": "fr",
        "original_name": "Un si grand soleil",
        "overview": "Claire is surprised when she gets arrested for the murder of her childhood friend after she returns to Montpellier.",
        "popularity": 2477.93,
        "poster_path": "/t6jVlbPMtZOJoAOfeoR4yQmnjXM.jpg",
        "vote_average": 7.0,
        "vote_count": 106
    },
    {
        "adult": false,
        "backdrop_path": "/l7LRGYJY3NzIGBlpvHpMsNXHbm5.jpg",
        "first_air_date": "2023-01-09",
        "genre_ids": [
            10751,
            35
        ],
        "id": 218145,
        "name": "Mom for rent",
        "origin_country": [
            "SK"
        ],
        "original_language": "sk",
        "original_name": "Mama na prenájom",
        "overview": "Abandoned by his wife, Martin is lying to his daughter not to be upset. But as Hanka grows, these lies become unbearable. Martin meets Nada unexpectedly, asked her to be a rent-a-mother and all lives are completely changed.",
        "popularity": 2318.998,
        "poster_path": "/fH7PP2Rkdlo414IHvZABBHhtoqd.jpg",
        "vote_average": 5.379,
        "vote_count": 29
    },
    {
        "adult": false,
        "backdrop_path": "/vgeDRVpSUa4Hvovg4C6dgm4dfUW.jpg",
        "first_air_date": "2020-11-02",
        "genre_ids": [
            10766,
            18
        ],
        "id": 112470,
        "name": "Ici tout commence",
        "origin_country": [
            "FR"
        ],
        "original_language": "fr",
        "original_name": "Ici tout commence",
        "overview": "This television drama series is centered around the prestigious culinary school of renowned chef Auguste Armand. The show follows the lives of students and staff as they navigate the challenges and pressures of the culinary world—delving into their personal and professional lives, revealing secrets, rivalries, and complex relationships.",
        "popularity": 2299.023,
        "poster_path": "/yuTHx38jpogXovMhqNatvozigMJ.jpg",
        "vote_average": 6.9,
        "vote_count": 57
    },
    {
        "adult": false,
        "backdrop_path": "/mlX6SG7lJ0BiLui5x5Nu4agetBA.jpg",
        "first_air_date": "2014-05-26",
        "genre_ids": [
            10766,
            18
        ],
        "id": 82708,
        "name": "The First Years",
        "origin_country": [
            "NL"
        ],
        "original_language": "nl",
        "original_name": "Brugklas",
        "overview": "The First Years is a Dutch series for young people in which real-life situations are recreated. The series sheds light on subjects that pupils in the first year of secondary school may be confronted with.",
        "popularity": 2215.697,
        "poster_path": "/klPqN1oITjVub0Yss0Kqnx8NfY3.jpg",
        "vote_average": 4.6,
        "vote_count": 10
    },
    {
        "adult": false,
        "backdrop_path": "/q3UGWifvIpdey1T2efX4dSmbZpU.jpg",
        "first_air_date": "2022-02-20",
        "genre_ids": [
            9648,
            18,
            10765
        ],
        "id": 124364,
        "name": "FROM",
        "origin_country": [
            "US"
        ],
        "original_language": "en",
        "original_name": "FROM",
        "overview": "Unravel the mystery of a nightmarish town in middle America that traps all those who enter. As the unwilling residents fight to keep a sense of normalcy and search for a way out, they must also survive the threats of the surrounding forest – including the terrifying creatures that come out when the sun goes down.",
        "popularity": 2189.686,
        "poster_path": "/cjXLrg4R7FRPFafvuQ3SSznQOd9.jpg",
        "vote_average": 8.178,
        "vote_count": 1363
    },
    {
        "adult": false,
        "backdrop_path": "/llIXQAndg5kB6SWlp6ouUdO7Zxd.jpg",
        "genre_ids": [
            12,
            36,
            28,
            18,
            10749,
            53
        ],
        "id": 1084736,
        "original_language": "fr",
        "original_title": "Le Comte de Monte-Cristo",
        "overview": "Edmond Dantes becomes the target of a sinister plot and is arrested on his wedding day for a crime he did not commit. After 14 years in the island prison of Château d’If, he manages a daring escape. Now rich beyond his dreams, he assumes the identity of the Count of Monte-Cristo and exacts his revenge on the three men who betrayed him.",
        "popularity": 2126.371,
        "poster_path": "/r7iCXrXmq4hKpB4QfDzZd8vsJ7l.jpg",
        "release_date": "2024-06-28",
        "title": "The Count of Monte-Cristo",
        "video": false,
        "vote_average": 8.3,
        "vote_count": 732
    },
    {
        "adult": false,
        "backdrop_path": "/ookJ1LS8Uc0ji7cSDuJfV7Qh6Lb.jpg",
        "first_air_date": "2000-04-23",
        "genre_ids": [
            10764
        ],
        "id": 18770,
        "name": "Gran Hermano",
        "origin_country": [
            "ES"
        ],
        "original_language": "es",
        "original_name": "Gran Hermano",
        "overview": "Gran Hermano is a reality television series broadcast in Spain on Telecinco and La Siete produced by Endemol. It is part of the Big Brother franchise first developed in the Netherlands. As of February 2012, 19 editions of the show have aired.",
        "popularity": 2023.539,
        "poster_path": "/gQ0Emh2LT047Fip2HWye3NkrkQB.jpg",
        "vote_average": 4.667,
        "vote_count": 6
    },
    {
        "adult": false,
        "backdrop_path": "/rCK96UqOllqGzm7f6qnhFRF7aHV.jpg",
        "first_air_date": "2023-10-08",
        "genre_ids": [
            10764
        ],
        "id": 237019,
        "name": "Big Brother: Live Stream",
        "origin_country": [
            "GB"
        ],
        "original_language": "en",
        "original_name": "Big Brother: Live Stream",
        "overview": "Big Brother sees it all - and so can you.",
        "popularity": 1994.517,
        "poster_path": "/me84uR1iE9SoSl6tZo1iO9OYKIt.jpg",
        "vote_average": 3.0,
        "vote_count": 2
    },
    {
        "adult": false,
        "backdrop_path": "/6vn6K9oX82i6E86ZiHVxqVEMQqP.jpg",
        "genre_ids": [
            878,
            27
        ],
        "id": 945961,
        "original_language": "en",
        "original_title": "Alien: Romulus",
        "overview": "While scavenging the deep ends of a derelict space station, a group of young space colonizers come face to face with the most terrifying life form in the universe.",
        "popularity": 1992.724,
        "poster_path": "/b33nnKl1GSFbao4l3fZDDqsMx0F.jpg",
        "release_date": "2024-08-13",
        "title": "Alien: Romulus",
        "video": false,
        "vote_average": 7.3,
        "vote_count": 2129
    },
    {
        "adult": false,
        "backdrop_path": "/3e0Mi0DoVTtERiYzaf6eG15S7Vj.jpg",
        "first_air_date": "2023-10-08",
        "genre_ids": [
            10764
        ],
        "id": 236594,
        "name": "Big Brother: Late & Live",
        "origin_country": [
            "GB"
        ],
        "original_language": "en",
        "original_name": "Big Brother: Late & Live",
        "overview": "Big Brother hosts AJ Odudu and Will Best present from a studio just a stone's throw from the Big Brother house, featuring celebrity guests and a live studio audience.",
        "popularity": 1967.526,
        "poster_path": "/4neSwqJjJLtK6Zuqpx5j70z5CPs.jpg",
        "vote_average": 4.2,
        "vote_count": 5
    },
    {
        "adult": false,
        "backdrop_path": "/7ZBNbpkLhC2fS90j6onLS8qqfRX.jpg",
        "first_air_date": "2004-10-25",
        "genre_ids": [],
        "id": 4682,
        "name": "Strictly Come Dancing: It Takes Two",
        "origin_country": [
            "GB"
        ],
        "original_language": "en",
        "original_name": "Strictly Come Dancing: It Takes Two",
        "overview": "The companion show to the popular BBC One programme Strictly Come Dancing which features interviews and training footage of the couples competing in the main Saturday night show, opinions from the judges on the previous Saturday show and the training footage for the next, and interviews with celebrities who have been watching the show.",
        "popularity": 1962.285,
        "poster_path": "/1UOKLsJ3bopZHg6ntRfmO4C5Gcm.jpg",
        "vote_average": 3.8,
        "vote_count": 5
    },
    {
        "adult": false,
        "backdrop_path": "/87aqAZuW3HV7smlQtZA8srcW4aq.jpg",
        "first_air_date": "2023-10-08",
        "genre_ids": [
            10764
        ],
        "id": 237243,
        "name": "Big Brother",
        "origin_country": [
            "GB"
        ],
        "original_language": "en",
        "original_name": "Big Brother",
        "overview": "Britain’s ultimate social experiment. Follow every twist and turn as a group of housemates live under the gaze of 24/7 cameras and try to avoid eviction. Big Brother sees it all...",
        "popularity": 1940.766,
        "poster_path": "/Tg2g7XvPLWsEbNH0hM1jxMfOmk.jpg",
        "vote_average": 4.9,
        "vote_count": 9
    },
    {
        "adult": false,
        "backdrop_path": "/VuukZLgaCrho2Ar8Scl9HtV3yD.jpg",
        "genre_ids": [
            878,
            28
        ],
        "id": 335983,
        "original_language": "en",
        "original_title": "Venom",
        "overview": "Investigative journalist Eddie Brock attempts a comeback following a scandal, but accidentally becomes the host of Venom, a violent, super powerful alien symbiote. Soon, he must rely on his newfound powers to protect the world from a shadowy organization looking for a symbiote of their own.",
        "popularity": 1917.653,
        "poster_path": "/2uNW4WbgBXL25BAbXGLnLqX71Sw.jpg",
        "release_date": "2018-09-28",
        "title": "Venom",
        "video": false,
        "vote_average": 6.835,
        "vote_count": 15877
    },
    {
        "adult": false,
        "backdrop_path": "/mLcD1v4sfoa1juOsBat7Vik7wEe.jpg",
        "first_air_date": "2024-03-18",
        "genre_ids": [
            10764
        ],
        "id": 248890,
        "name": "Ready Steady Cook South Africa",
        "origin_country": [
            "ZA"
        ],
        "original_language": "en",
        "original_name": "Ready Steady Cook South Africa",
        "overview": "In Ready Steady Cook, two teams - a Red Tomato and a Green Pepper - compete in a Red Kitchen and a Green Kitchen, together with a South African chef on each side and paired with enthusiastic home cooks, as they are challenged creatively with a mystery bag of ingredients in a 20-minute cook-off.",
        "popularity": 1910.832,
        "poster_path": "/30xX4IMbgnMbQwo76xM4BOSokZO.jpg",
        "vote_average": 2.1,
        "vote_count": 4
    },
    {
        "adult": false,
        "backdrop_path": "/yDHYTfA3R0jFYba16jBB1ef8oIt.jpg",
        "genre_ids": [
            28,
            35,
            878
        ],
        "id": 533535,
        "original_language": "en",
        "original_title": "Deadpool & Wolverine",
        "overview": "A listless Wade Wilson toils away in civilian life with his days as the morally flexible mercenary, Deadpool, behind him. But when his homeworld faces an existential threat, Wade must reluctantly suit-up again with an even more reluctant Wolverine.",
        "popularity": 1885.377,
        "poster_path": "/8cdWjvZQUExUUTzyp4t6EDMubfO.jpg",
        "release_date": "2024-07-24",
        "title": "Deadpool & Wolverine",
        "video": false,
        "vote_average": 7.707,
        "vote_count": 5026
    },
    {
        "adult": false,
        "backdrop_path": "/9s9o9RT9Yj6nDuRJjnJm78WFoFl.jpg",
        "genre_ids": [
            28,
            27,
            53,
            878
        ],
        "id": 1051896,
        "original_language": "en",
        "original_title": "Arcadian",
        "overview": "In the near future, on a decimated Earth, Paul and his twin sons face terror at night when ferocious creatures awaken. When Paul is nearly killed, the boys come up with a plan for survival, using everything their father taught them to keep him alive.",
        "popularity": 1844.021,
        "poster_path": "/spWV1eRzlDxvai8LbxwAWR0Vst4.jpg",
        "release_date": "2024-04-12",
        "title": "Arcadian",
        "video": false,
        "vote_average": 6.0,
        "vote_count": 382
    },
    {
        "adult": false,
        "backdrop_path": null,
        "first_air_date": "2024-10-14",
        "genre_ids": [],
        "id": 274136,
        "name": "Stardance XIII ...kolem dokola",
        "origin_country": [
            "CZ"
        ],
        "original_language": "cs",
        "original_name": "Stardance XIII ...kolem dokola",
        "overview": "",
        "popularity": 1786.965,
        "poster_path": "/iJPk8DSr2NVpfeFxembWxROqQNW.jpg",
        "vote_average": 10.0,
        "vote_count": 1
    },
    {
        "adult": false,
        "backdrop_path": "/rotcih1fY3UOYejNbiTmz36og12.jpg",
        "first_air_date": "2024-01-22",
        "genre_ids": [
            18,
            10751
        ],
        "id": 242722,
        "name": "Shrimad Ramayan",
        "origin_country": [
            "IN"
        ],
        "original_language": "hi",
        "original_name": "श्रीमद् रामायण",
        "overview": "Shrimad Ramayan is an ambitious television series that brings to life the timeless epic, the Ramayan, with a deep commitment to authenticity, cultural reverence and a contemporary sensibility.",
        "popularity": 1759.592,
        "poster_path": "/aCDK83ykQYnQGFOTfiLjnoqXv1b.jpg",
        "vote_average": 9.3,
        "vote_count": 3
    },
    {
        "adult": false,
        "backdrop_path": "/ohJTnu93hJ0Uonl86Wn3mOSlWXN.jpg",
        "first_air_date": "2017-02-06",
        "genre_ids": [
            10751,
            35,
            18
        ],
        "id": 91759,
        "name": "Come Home Love: Lo and Behold",
        "origin_country": [
            "HK"
        ],
        "original_language": "cn",
        "original_name": "愛·回家之開心速遞",
        "overview": "Hung Sue Gan starting from the bottom, established his own logistics company, which is now running smoothly. His only concern now are his three daughters. His eldest daughter has immigrated overseas. His second daughter Hung Yeuk Shui has reached the marriageable age, but has no hopes for marriage anytime soon. She is constantly bickering with her younger sister Hung Sum Yue, who is an honour student, over trivial matters, causing their father to not know whether to laugh or cry. Hung Sue Yan, Hung Sue Gan's brother, moves in with the family, temporarily ending his life as a nomadic photographer. He joins Hung Yeuk Shui's company and encounters Ko Pak Fei, the director of an online shop. The two appear to be former lovers, making for lots of laughter. Since Hung Sue Yan moved in, a series of strange events have occurred in the family. Upon investigation, the source is traced to Lung Ging Fung, a promising young man who is the son of department store mogul Lung Gam Wai.",
        "popularity": 1734.628,
        "poster_path": "/lgD4j9gUGmMckZpWWRJjorWqGVT.jpg",
        "vote_average": 5.1,
        "vote_count": 38
    },
    {
        "adult": false,
        "backdrop_path": null,
        "first_air_date": "2005-09-05",
        "genre_ids": [
            18,
            35
        ],
        "id": 36361,
        "name": "Ulice",
        "origin_country": [
            "CZ"
        ],
        "original_language": "cs",
        "original_name": "Ulice",
        "overview": "Ulice is a Czech soap opera produced and broadcast by Nova. In the Czech language Ulice means street.\n\nThe show describes the lives of the Farský, Jordán, Boháč, Nikl, and Liška families and many other people that live in Prague. Their daily battle against real problems of living in a modern world like divorce, love, betrayal and illness or disease. Ulice often shows crime.",
        "popularity": 1703.092,
        "poster_path": "/gFEHva8Csx18hMGJJZ6gi4sFSKR.jpg",
        "vote_average": 3.619,
        "vote_count": 21
    },
    {
        "adult": false,
        "backdrop_path": "/p5ozvmdgsmbWe0H8Xk7Rc8SCwAB.jpg",
        "genre_ids": [
            16,
            10751,
            12,
            35,
            18
        ],
        "id": 1022789,
        "original_language": "en",
        "original_title": "Inside Out 2",
        "overview": "Teenager Riley's mind headquarters is undergoing a sudden demolition to make room for something entirely unexpected: new Emotions! Joy, Sadness, Anger, Fear and Disgust, who’ve long been running a successful operation by all accounts, aren’t sure how to feel when Anxiety shows up. And it looks like she’s not alone.",
        "popularity": 1676.036,
        "poster_path": "/vpnVM9B6NMmQpWeZvzLvDESb2QY.jpg",
        "release_date": "2024-06-11",
        "title": "Inside Out 2",
        "video": false,
        "vote_average": 7.61,
        "vote_count": 4590
    },
    {
        "adult": false,
        "backdrop_path": "/u4Lh4viuwHGVLFyUnY7YvwOTwl0.jpg",
        "first_air_date": "2024-06-18",
        "genre_ids": [
            18
        ],
        "id": 252373,
        "name": "A Promessa",
        "origin_country": [
            "PT"
        ],
        "original_language": "pt",
        "original_name": "A Promessa",
        "overview": "",
        "popularity": 1665.005,
        "poster_path": "/uptgxt2apx5wwWItQzqL0HwhjZC.jpg",
        "vote_average": 4.5,
        "vote_count": 2
    },
    {
        "adult": false,
        "backdrop_path": "/93R3gd0iNqnib1JKwbWXksDcMY.jpg",
        "first_air_date": "2024-05-06",
        "genre_ids": [
            35,
            18,
            10751
        ],
        "id": 255150,
        "name": "Pituca Sin Lucas",
        "origin_country": [
            "PE"
        ],
        "original_language": "es",
        "original_name": "Pituca Sin Lucas",
        "overview": "",
        "popularity": 1519.342,
        "poster_path": "/cjqJqODyUbul2GZL7ti2B5SVv7I.jpg",
        "vote_average": 8.5,
        "vote_count": 2
    },
    {
        "adult": false,
        "backdrop_path": "/sCTlziZeyf4eWXh09pt63zMtJRw.jpg",
        "first_air_date": "2024-08-18",
        "genre_ids": [
            10759,
            18
        ],
        "id": 261033,
        "name": "The Agent",
        "origin_country": [
            "SY"
        ],
        "original_language": "ar",
        "original_name": "العميل",
        "overview": "A police captain infiltrates a notorious gang, only to find himself going deeper down the rabbit hole.",
        "popularity": 1506.056,
        "poster_path": "/qUtgaa43jTELs0Tdw55aIukt9yn.jpg",
        "vote_average": 1.8,
        "vote_count": 2
    },
    {
        "adult": false,
        "backdrop_path": "/zk3UqXnnK7cpUv6LsD9DS8FtUxb.jpg",
        "first_air_date": "2024-09-02",
        "genre_ids": [
            18,
            10759
        ],
        "id": 256121,
        "name": "Lavender Fields",
        "origin_country": [
            "PH"
        ],
        "original_language": "tl",
        "original_name": "Lavender Fields",
        "overview": "Jasmin loved her idyllic life in her mountain town, but a brush with a criminal empire took it all away. Now she's out for revenge with a new identity.",
        "popularity": 1498.811,
        "poster_path": "/lphvsr062SlxWM6XegsV2dLGaiE.jpg",
        "vote_average": 0.0,
        "vote_count": 0
    },
    {
        "adult": false,
        "backdrop_path": "/vIgyYkXkg6NC2whRbYjBD7eb3Er.jpg",
        "genre_ids": [
            878,
            28,
            12
        ],
        "id": 580489,
        "original_language": "en",
        "original_title": "Venom: Let There Be Carnage",
        "overview": "After finding a host body in investigative reporter Eddie Brock, the alien symbiote must face a new enemy, Carnage, the alter ego of serial killer Cletus Kasady.",
        "popularity": 1488.305,
        "poster_path": "/1MJNcPZy46hIy2CmSqOeru0yr5C.jpg",
        "release_date": "2021-09-30",
        "title": "Venom: Let There Be Carnage",
        "video": false,
        "vote_average": 6.799,
        "vote_count": 10102
    },
    {
        "adult": false,
        "backdrop_path": "/begseNUKhZcc05Bc1UggaX5GeES.jpg",
        "genre_ids": [
            28,
            53,
            80
        ],
        "id": 976734,
        "original_language": "en",
        "original_title": "Canary Black",
        "overview": "Top level CIA agent Avery Graves is blackmailed by terrorists into betraying her own country to save her kidnapped husband. Cut off from her team, she turns to her underworld contacts to survive and help locate the coveted intelligence that the kidnappers want.",
        "popularity": 1301.295,
        "poster_path": "/hhiR6uUbTYYvKoACkdAIQPS5c6f.jpg",
        "release_date": "2024-10-10",
        "title": "Canary Black",
        "video": false,
        "vote_average": 6.371,
        "vote_count": 170
    },
    {
        "adult": false,
        "backdrop_path": "/naNXYdBzTEb1KwOdi1RbBkM9Zv1.jpg",
        "genre_ids": [
            27,
            53
        ],
        "id": 420634,
        "original_language": "en",
        "original_title": "Terrifier",
        "overview": "A maniacal clown named Art terrorizes three young women on Halloween night and everyone else who stands in his way.",
        "popularity": 1298.546,
        "poster_path": "/sFaPj5UyIAsiRuIgVl60pCYUzmR.jpg",
        "release_date": "2018-01-25",
        "title": "Terrifier",
        "video": false,
        "vote_average": 6.4,
        "vote_count": 2343
    },
    {
        "adult": false,
        "backdrop_path": "/csQSGH0QU8D3Ov5YLEYuHep8ihA.jpg",
        "genre_ids": [
            53,
            12,
            28,
            878
        ],
        "id": 1196470,
        "original_language": "fr",
        "original_title": "Survivre",
        "overview": "A couple celebrates their son’s birthday in the middle of the ocean on their boat. A violent storm hits and it brings up hungry creatures from the depths and they fight for their survival.",
        "popularity": 1262.118,
        "poster_path": "/7fR3KxswtY8OHHZuOUB9td58CRX.jpg",
        "release_date": "2024-06-19",
        "title": "Survive",
        "video": false,
        "vote_average": 5.0,
        "vote_count": 36
    },
    {
        "adult": false,
        "backdrop_path": "/lgkPzcOSnTvjeMnuFzozRO5HHw1.jpg",
        "genre_ids": [
            16,
            10751,
            35,
            28
        ],
        "id": 519182,
        "original_language": "en",
        "original_title": "Despicable Me 4",
        "overview": "Gru and Lucy and their girls—Margo, Edith and Agnes—welcome a new member to the Gru family, Gru Jr., who is intent on tormenting his dad. Gru also faces a new nemesis in Maxime Le Mal and his femme fatale girlfriend Valentina, forcing the family to go on the run.",
        "popularity": 1225.064,
        "poster_path": "/wWba3TaojhK7NdycRhoQpsG0FaH.jpg",
        "release_date": "2024-06-20",
        "title": "Despicable Me 4",
        "video": false,
        "vote_average": 7.113,
        "vote_count": 2106
    },
    {
        "adult": false,
        "backdrop_path": "/askg3SMvhqEl4OL52YuvdtY40Yb.jpg",
        "genre_ids": [
            10751,
            16,
            10402,
            12
        ],
        "id": 354912,
        "original_language": "en",
        "original_title": "Coco",
        "overview": "Despite his family’s baffling generations-old ban on music, Miguel dreams of becoming an accomplished musician like his idol, Ernesto de la Cruz. Desperate to prove his talent, Miguel finds himself in the stunning and colorful Land of the Dead following a mysterious chain of events. Along the way, he meets charming trickster Hector, and together, they set off on an extraordinary journey to unlock the real story behind Miguel's family history.",
        "popularity": 1121.64,
        "poster_path": "/gGEsBPAijhVUFoiNpgZXqRVWJt2.jpg",
        "release_date": "2017-10-27",
        "title": "Coco",
        "video": false,
        "vote_average": 8.2,
        "vote_count": 19388
    },
    {
        "adult": false,
        "backdrop_path": "/uLqNGzJwnj8JKkKuRM2dHWJKCtc.jpg",
        "genre_ids": [
            28,
            27,
            53
        ],
        "id": 1029235,
        "original_language": "en",
        "original_title": "Azrael",
        "overview": "In a world where no one speaks, a devout female hunts down a young woman who has escaped her imprisonment. Recaptured by its ruthless leaders, Azrael is due to be sacrificed to pacify an ancient evil deep within the surrounding wilderness.",
        "popularity": 1063.12,
        "poster_path": "/qpdFKDvJS7oLKTcBLXOaMwUESbs.jpg",
        "release_date": "2024-09-27",
        "title": "Azrael",
        "video": false,
        "vote_average": 6.149,
        "vote_count": 114
    },
    {
        "adult": false,
        "backdrop_path": "/9msuazXGWAyl7vhxVFU7e7Bb5Ik.jpg",
        "genre_ids": [
            18,
            10749
        ],
        "id": 179387,
        "original_language": "tl",
        "original_title": "Heavenly Touch",
        "overview": "Jonard is having trouble making ends meet. His mother is suffering from depression, and he and his sister are forced to quit school in order to take care of her. One day, Jonard meets up his friend Rodel, and Rodel introduces him to the world of massage parlors. Rodel teaches him massage, and brings him to Heavenly Touch, a syndicate-run massage parlor that mostly caters to homosexuals.",
        "popularity": 1028.191,
        "poster_path": "/ory8WuAqznTE7lfopTSymHpop2t.jpg",
        "release_date": "2009-05-12",
        "title": "Heavenly Touch",
        "video": false,
        "vote_average": 6.3,
        "vote_count": 21
    }
]
```

---
<h1>Endpoints not currently in Client use</h1>
<h2>Reviews</h2>

### 1. Write Review
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
### 2. Get Reviews by User
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
### 3. Get Reviews by Content
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
### 4. Delete Review
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
<h2>Feed / Posts Endpoints</h2>
### 1. Add Post
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
### 2. Get Child Posts
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
### 3. Get Posts by User
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
### 4. Get Last N Posts
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
### 5. Delete Post
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
