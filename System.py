import sqlite3

connection = sqlite3.connect("ANIME.db")
c = connection.cursor()

class System:
    def __init__ (self, theme):
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
        c.execute("""INSERT INTO filterTable
            SELECT * FROM 
            WHERE condition;""")

        

    def darkLightTheme(self, theme):
        self.theme = theme
        if self.theme != "Dark" or self.theme != "Light":
            return -1
        else:
            return self.theme