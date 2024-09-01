import mysql.connector
from lxml import html
import random
import requests
import time

def create_user(user,nick):
    try:
        query = f"SELECT EXISTS(SELECT 1 FROM `final_project_db`.`users` WHERE username = %s)"
        cursor.execute(query, (user,))
        exists = cursor.fetchone()[0]
        if not exists:
            insert_query = f"INSERT INTO `final_project_db`.`users` (id,username,password,email,google_auth,nickname) VALUES (%s,%s,%s,%s,%s,%s)"
            random_number = random.randint(10 ** 20, 10 ** 21 - 1)
            email=user+"@fake.com"
            cursor.execute(insert_query, (str(random_number), user, str(random_number), email, 1,nick))
            connection.commit()
           # print(f"ID {id} + {user} was added to the table .")
            return str(random_number)

        else:
           # print(f"ID {user} already exists in the table .")
            query = f"SELECT  `id` from `users` WHERE username = %s  "
            cursor2.execute(query,(user,))
            return cursor2.fetchall()[0]['id']
    except mysql.connector.Error as err:
        return "no"
        print(err)


def get_imdbid():
    try:
        query=f"SELECT  `imdb_id` ,`id` from `media_data` "
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
connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="yanovsky",
    database="final_project_db"
)

# Check if connection is successful
if connection.is_connected():
    print("Connected to MySQL database")
    cursor = connection.cursor()
    cursor2 = connection.cursor(dictionary=True)

def add_rev(user,review,tmdb_id):

        try:
            insert_query = f"INSERT INTO `final_project_db`.`reviews` (`User_ID`,`TText`,`Parent_ID`) VALUES (%s,%s,%s) "
            cursor.execute(insert_query, (user, review, tmdb_id))
            connection.commit()
            #print ("rev added")
            return "yes"
        except mysql.connector.Error as err:
            #print (err)
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:

                print("Something is wrong with your user name or password")
                return  "fesfse"

            elif err.errno == errorcode.ER_BAD_DB_ERROR:

                print("Database does not exist")
                return "dfs"

            else:
                print(err)
                return err

imdb_id_arr=get_imdbid()
users=get_users()
def main():
   '''
   for imdb_type in  imdb_id_arr:
    try:
     url = 'https://www.imdb.com/title/'+imdb_type['imdb_id']+'/reviews'
     response = requests.get(url)
     tree = html.fromstring(response.content)
     review_containers = tree.xpath("//div[@class='review-container']")
     print(f"Total reviews found: {len(review_containers)}")
    except:
        continue
    if review_containers:
       # print(html.tostring(review_containers[0], pretty_print=True).decode('utf-8'))


        for review in  review_containers:
         try:
          review_text = review.xpath(".//div[@class='text show-more__control']/text()")
          review_rate = review.xpath(".//div[@class='ipl-ratings-bar']//span[1]/text()")[2].strip()
          review_text = " ".join(review_text)
          review_date=review.xpath(".//span[@class='review-date']/text()")
          writer_id=review.xpath(".//span[@class='display-name-link']/a/@href")[0]
          writer_username= review.xpath(".//span[@class='display-name-link']/a/text()")[0]
          realid=writer_id.split("/")[2]
          userid=create_user( realid,  writer_username)
          #print (   realid)
         # movie_id = next((movie['id'] for movie in imdb_id_arr if movie['imdb_id'] == "tt11389872" ), None)
          add_rev( userid, review_text,  imdb_type['id'])
         except:
          t=5
    print ("finnish "+imdb_type['id'])
    time.sleep(1)
    '''









if __name__=="__main__":
    main()
