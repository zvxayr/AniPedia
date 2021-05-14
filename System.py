import sqlite3

connection = sqlite3.connect("ANIME.db")
c = connection.cursor()


class System:
    def __init__(self, theme):
        self.theme = theme

    def filterAnimeDisplay(self, typeofanime, age_rating, premiered, studio):
        c.execute("""IF EXISTS DROP filterTable""")
        c.execute("""CREATE TABLE filterTable(
            id int,
            title text,
            typeOfAnime text,
            aired_from date, 
            aired_to date,
            rating text,  
            premiered text,
            studio text,
            animeGenre text
            );""")
        c.execute("""INSERT INTO filterTable()
            SELECT * FROM 
            WHERE condition;""")

    def login(self, username, pass_word):
        c.execute("""SELECT username FROM User""")
        while True:
            currentu = c.fetchone()
            print(currentu[0])
            if currentu[0] == username:
                break
            if currentu == None:
                return "Sorry, username does not exist"

        c.execute("""SELECT pass_word FROM User WHERE username = ?""", (username,))
        currentpw = c.fetchone()
        if currentpw[0] != pass_word:
            return -1
        else:
            return 1

    def darkLightTheme(self, theme):
        self.theme = theme
        if self.theme != "Dark" or self.theme != "Light":
            return -1
        else:
            return self.theme


def main():
    System1 = System("Dark")
    print(System1.login('karthiga', "rrca242001"))


if __name__ == "__main__":
    main()
