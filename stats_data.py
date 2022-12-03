import sqlite3

class sql_manager:
    def __init__(self):
        self.con = sqlite3.connect('stats.db')
        self.sql = self.con.cursor()
    #def add(self):
        self.sql.execute(""" CREATE TABLE IF NOT EXISTS stats(
            id INTEGER,
            user TEXT,
            count1 INTEGER,
            count2 INTEGER
        ) """)
        self.con.commit()

    def add_stats(self, user, count):
        self.sql.execute(f"SELECT id FROM stats")
        if self.sql.fetchone() is None:
            id = 0
        else:
            for i in self.sql.execute('SELECT MAX(id) FROM stats'):
                id = int(i[0])+1

        self.sql.execute(f"SELECT user FROM stats WHERE user ='{user}'")

        if self.sql.fetchone() is None:
            self.sql.execute("INSERT INTO stats VALUES(?, ?, ?, ?)",(id, user, 0, 0))
            self.con.commit()
        else:
            for i in self.sql.execute(f"SELECT {count} FROM stats WHERE user ='{user}'"):
                count_id = int(i[0])+1

            self.sql.execute(f"UPDATE stats SET {count} = '{count_id}'")
            self.con.commit()

    def cheak_stats(self, user):
        arr = []
        self.sql.execute(f"SELECT id FROM stats")
        if self.sql.fetchone() is None:
            id = 0
        else:
            for i in self.sql.execute('SELECT MAX(id) FROM stats'):
                #print(i)
                id = int(i[0])+1
        self.sql.execute(f"SELECT user FROM stats WHERE user ='{user}'")
        if self.sql.fetchone() is None:
            self.sql.execute("INSERT INTO stats VALUES(?, ?, ?, ?)",(id, user, 0, 0))
            self.con.commit()
            arr.append((0, 0))
        else:
            for tupes in self.sql.execute(f"SELECT count1, count2 FROM stats WHERE user ='{user}'"):
                arr.append(tupes)
        #print(arr)
        return arr[0]
