import sqlite3 as sql




many_doors = 1
db = sql.connect("mock_database.db")
c = db.cursor()
c.execute("INSERT INTO userdata VALUES (?, ?, ?)", ("rmlameiras@ua.pt", "normal", "None"))
db.commit()
db.close()