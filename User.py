import sqlite3

connection = sqlite3.connect("ANIME.db")
c = connection.cursor()

class User:
    def __init__ (self, username, password):
        self.username = username
        self.password = password

    def rateAnime(self, rating, anime_id):
        c.execute("""UPDATE UserAnime
        SET my_score =?
        WHERE anime_id =? and Username =?""", (rating, anime_id, self.username))
        connection.commit()

    def changePassword(self, newpassword):
        self.password = newpassword
        c.execute("""UPDATE User
        SET pass_word = ?
        WHERE Username = ?""", (self.password, self.username))
        connection.commit()

    def changeUsername(self, newUsername):
        c.execute("""UPDATE UserAnime
        SET Username = ?
        WHERE Username = ?""", (newUsername, self.username))
        c.execute("""UPDATE User
        SET Username = ?
        WHERE Username = ?""", (newUsername, self.username))
        self.username = newUsername
        connection.commit()

def main():
    User1 = User("karthiga", "rrca242001")
    # User1.rateAnime(4, 21)
    # User1.changeUsername("Rance")
    User1.filterAnime("TV", "PG-13 - Teens 13 or older", "Winter 2012", "David Production")
    User1.changePassword("rrca242001")

if __name__ == "__main__":
    main()


