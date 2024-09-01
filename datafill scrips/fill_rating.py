import mysql.connector
from lxml import html
import random
import requests
import time



connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="yanovsky",
    database="final_project_db"
)
def add_rate(media_ID,is_movie,User_ID,rating):
    try:
        insert_query = f"INSERT INTO `final_project_db`.`rating` (`media_ID`,`is_movie`,`User_ID`,`rating`) VALUES (%s,%s,%s,%s) "
        cursor.execute(insert_query, (media_ID, is_movie, User_ID,rating))
        connection.commit()
        # print ("rev added")
        return "yes"
    except mysql.connector.Error as err:
        # print (err)
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:

            print("Something is wrong with your user name or password")
            return "fesfse"

        elif err.errno == errorcode.ER_BAD_DB_ERROR:

            print("Database does not exist")
            return "dfs"

        else:
            print(err)
            return err
def get_imdbid():
    try:
        query=f"SELECT  `imdb_id` ,`id`,`Is_movie` from `media_data` "
        cursor2.execute(query)
        return cursor2.fetchall()

    except mysql.connector.Error as err:
        print(err)
def get_users():
    try:
        query=f"SELECT  `id` ,`username` from `users` "
        cursor2.execute(query)
        return cursor2.fetchall()

    except mysql.connector.Error as err:
        print(err)

# Check if connection is successful
if connection.is_connected():
    print("Connected to MySQL database")
    cursor = connection.cursor()
    cursor2 = connection.cursor(dictionary=True)
imdb_id_arr=get_imdbid()
users=get_users()



def main():
    imdb_id_arr = get_imdbid()
    users = get_users()
   # u_index= next((index for index, obj in enumerate(users) if obj['username'] == 'ur9499808'), None)
    u_index=0
    print (users)
    for i in range(len(users)):
        if users[i]['username'] == 'ur5778839':
            u_index = i
            break
    users=users[u_index:]
    for user in users:
     try:
      #url = 'https://www.imdb.com/user/ur19484559/ratings'
      url = 'https://www.imdb.com/user/'+user['username']+'/reviews'
      response = requests.get(url)
      # print (response.content)
      tree = html.fromstring(response.content)
      rating_links = tree.xpath("//div[@class='lister-item-header']/a/@href")
      ranking=tree.xpath("//div[@class='ipl-ratings-bar']//span[@class='rating-other-user-rating']/span/text()")
      ranking=[s for s in ranking if '/' not in s]
      if rating_links and ranking:
      #print(f"Total reviews found: {len(rating_containers)}")
       count=0
       for i in range(len(rating_links)):
           link= rating_links[i].split("/")[2]
           rate= int(ranking[i])
           #print(link)
           found = any(item["imdb_id"] == link for item in imdb_id_arr)
           if found:
               tmdb_id = next((movie['id'] for movie in imdb_id_arr if movie['imdb_id'] == link ), None)
               is_movie= next((movie['Is_movie'] for movie in imdb_id_arr if movie['imdb_id'] == link ), None)
               add_rate(tmdb_id,is_movie,user['id'],rate)

       print ("added rating to "+user['id'] + " " + user['username'])
       time.sleep(2)
     except:
      print ("error at "+ user['username'] +" " +user['id'])


if __name__=="__main__":
    main()