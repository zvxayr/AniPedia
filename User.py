import sqlite3

connection = sqlite3.connect("ANIME.db")
c = connection.cursor()

class User:
    def __init__ (self, Username):
        self.Username = Username

    def rateAnime(self, rate, anime_id):
        c.execute("""SELECT my_score FROM UserAnime 
        WHERE Username = :Username and anime_id = :anime_id""", {'Username': self.Username, 'anime_id': anime_id})
        Username = c.fetchone()
        c.execute("""UPDATE UserAnime
        SET my_score =:rate
        WHERE anime_id =:anime_id and Username =:Username""", {'rate': rate, 'anime_id': anime_id, 'Username': self.Username})
        connection.commit()

def main():
    User1 = User("karthiga")
    User1.rateAnime(4, 21)

if __name__ == "__main__":
    main()


