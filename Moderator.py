import sqlite3

connection = sqlite3.connect("ANIME.db")
cursor = connection.cursor()

class Moderator:
    def __init__(self, username):
        self.username = username

    def addAnime(self, anime_id, title, typeOfAnime, aired_from, aired_to, rating, premiered, studio):
        table_columns = [anime_id, title, typeOfAnime, 
                        aired_from, aired_to, rating, 
                        premiered, studio] #saving variables into a list

        cursor.execute("INSERT INTO Anime VALUES (?,?,?,?,?,?,?,?)", table_columns)
        connection.commit()

    def updateAnime(self, anime_id, title, typeOfAnime, aired_from, aired_to, rating, premiered, studio):
        cursor.execute("""UPDATE Anime
        SET title=?,
            typeOfAnime=?,
            aired_from=?,
            aired_to=?,
            rating=?,
            premiered=?,
            studio=?
        WHERE anime_id=?""", (title, typeOfAnime, aired_from, aired_to, rating, premiered, studio, anime_id))
        connection.commit()

    def removeUser(self, id):
        cursor.execute("DELETE FROM User WHERE ID=?", (id,))
        connection.commit()

   
def main():
    anime1 = Moderator("sample")
    anime2 = Moderator("sample2")
    #anime1.addAnime(1, "Anipedia Anime","TV", "2021-05-05","2025-03-03", "PG-13", "Spring", "Anipedia Studio")
    #anime1.removeUser(2255153)
    #anime1.updateAnime(1, "Aniwikedia","PC", "2000-05-05","2055-03-03", "R18", "Winter", "Anipedia Group")
    anime2.updateAnime(721, "Prince Tata","PC", "2001-06-05","2145-03-03", "R52", "Spring", "Anipedia Group")

if __name__ == "__main__":
    main()