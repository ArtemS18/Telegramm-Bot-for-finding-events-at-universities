import sqlite3

class sql_manager:
    def __init__(self):
        self.con = sqlite3.connect('s1.db')
        self.sql = self.con.cursor()
    #def add(self):
        self.sql.execute(""" CREATE TABLE IF NOT EXISTS users(
            user TEXT,
            events TEXT,
            title TEXT,
            url TEXT,
            date TEXT,
            id INTEGER,
            tape INTEGER
        ) """)
        self.con.commit()
    def reg(self, user, events, arr, tape):#user, date1.split()[0], text_labl, date, description, href, tape, spots
        url = arr[1]
        title = arr[0]
        date = arr[2]
        id = 0
        #self.sql.execute(f"SELECT id FROM users WHERE url = '{url}'")
        self.sql.execute(f"SELECT id FROM users")
        if self.sql.fetchone() is None:
            id = 0
        else:
            for i in self.sql.execute('SELECT MAX(id) FROM users'):
                #print(i[0])
                id = int(i[0])+1

        self.sql.execute(f"SELECT user FROM users WHERE url = '{url}' AND user = '{user}'AND events = '{events}'")
        if self.sql.fetchone() is None:
            self.sql.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?)",(user, events,title, url,date, id,tape))
            self.con.commit()
        else:
            #print(date)
            self.sql.execute(f"DELETE FROM users WHERE url = '{url}' AND user = '{user}' AND events = '{events}'")
            self.sql.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?)",(user, events,title, url,date, id,tape))
            '''self.sql.execute(f'UPDATE users SET events = {date} WHERE user = "{user}"')'''
            self.con.commit()
        return id
    def cheak(self):
        arr = []
        for v in self.sql.execute("SELECT user, events, id, tape  FROM users"):
            arr.append(v)
        #print(arr)
        return arr
    def cheak_user(self, user):
        self.sql.execute(f"SELECT user FROM users WHERE user = '{user}' AND tape = 0")
        if self.sql.fetchone() is None:
            return []
        else:
            arr = []
            for v in self.sql.execute(f"SELECT * FROM users WHERE user = '{user}' AND tape = 0"):
                arr.append(v)
            return arr
    def cheak_event(self, user, events):
        self.sql.execute(f"SELECT user FROM users WHERE user = '{user}'")
        if self.sql.fetchone() is None:
            return []
        else:
            arr = []
            for v in self.sql.execute(f"SELECT * FROM users WHERE user = '{user}' and events = '{events}'"):
                arr.append(v)
            return arr
    def user(self, user, id):
        self.sql.execute(f"SELECT user FROM users WHERE user = '{user}'")


    def delete(self, id):
        id = int(id)
        url = '___'
        self.sql.execute(f"SELECT url FROM users WHERE id = '{id}'")
        if self.sql.fetchone() is None:
            for i in self.sql.execute(f"SELECT url FROM users WHERE id = '{id-1}'"):
                url = i[0]
        else:
            for i in self.sql.execute(f"SELECT url FROM users WHERE id = '{id}'"):
                url = i[0]
        #for i in self.sql.execute(f"SELECT * FROM users"):
            #print(i)
        #print(url, id)
        self.sql.execute(f"DELETE FROM users WHERE url = '{url}'")
        self.con.commit()
        #if self.sql.execute(f"SELECT url FROM users WHERE id = '{id+1}'") == self.sql.execute(f"SELECT url FROM users WHERE id = '{id}'"):
        #    self.sql.execute(f"DELETE FROM users WHERE id = '{id+1}'")
        #    self.con.commit()
        #self.sql.execute(f"DELETE FROM users WHERE id = '{id}'")
        #self.con.commit()

    def delete_once(self, id):
        self.sql.execute(f"DELETE FROM users WHERE id = '{id}'")
        self.con.commit()
        #arr = []
        #for v in self.sql.execute("SELECT * FROM users"):
                #arr.append(v)
        #return (arr)
