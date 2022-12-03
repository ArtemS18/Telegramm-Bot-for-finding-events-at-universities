import sqlite3
from mytoken import univer_prof

class sql_manager:
    def __init__(self, name):
        self.name = name
        self.con = sqlite3.connect(f'{self.name}.db')
        self.sql = self.con.cursor()
        self.sql.execute(f'CREATE TABLE IF NOT EXISTS {self.name}(id INT, text_labl TEXT,text_date TEXT, hour TEXT, href TEXT,registered TEXT,univer TEXT, photo TEXT) ')
        self.con.commit()

    def add_event(self, arr):
        if arr != []:
            for i in arr:
                self.sql.execute(f"SELECT id FROM {self.name} WHERE id = '{i[0]}'")
                if self.sql.fetchone() is None:
                    self.sql.execute(f"INSERT INTO {self.name} VALUES(?, ?, ?,?, ?, ?, ?, ?)", (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]))
                    self.con.commit()
                else:
                    self.sql.execute(f"DELETE FROM {self.name} WHERE id = '{i[0]}'")
                    self.sql.execute(f"INSERT INTO {self.name} VALUES(?, ?, ?,?, ?, ?, ?, ?)", (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]))
                    '''self.sql.execute(f'UPDATE users SET events = {date} WHERE user = "{user}"')'''
                    self.con.commit()
    def order_by(self, val):
        self.sql.execute(f"SELECT * FROM {self.name} ORDER BY id")
        arr = self.sql.fetchall()
        last = arr[-1][0]
        for id in range(last):
            print(arr[id])
            self.sql.execute(f"UPDATE {self.name} SET id = '{arr[id][0]}', text_labl = '{arr[id][1]}',text_date = '{arr[id][2]}', hour = '{arr[id][3]}', href = '{arr[id][4]}',registered = '{arr[id][5]}',univer = '{arr[id][6]}', photo = '{arr[id][7]}' WHERE id = '{id}' and text_labl = 'null'")
            self.con.commit()

    def null(self, id):
        #self.sql.execute(f"SELECT * FROM {self.name} ORDER BY id")
        self.sql.execute(f"INSERT INTO {self.name} VALUES(?, ?, ?,?, ?, ?, ?, ?)", (id+1, 'null', 'null', 'null', 'null', 'null', 'null', 'null'))
        #print(self.sql.fetchall())
        self.con.commit()

    def cheak_date(self, date_arr, page, less):
        arr = []
        def search_less_and_date(tape, date, arr):
            self.sql.execute(f"SELECT * FROM {self.name} WHERE text_date = '{date}' AND univer = '{tape}'")
            if self.sql.fetchone() is None:
                pass
            else:
                for v in self.sql.execute(f"SELECT * FROM {self.name} WHERE text_date = '{date}' AND univer = '{tape}'"):
                    v = v[1:]
                    v = [v[0],  v[1]+" "+v[2], v[3], v[4], v[5], v[6]]
                    arr.append(list(v))
            return arr

        def search_less(tape, arr):
            self.sql.execute(f"SELECT * FROM {self.name} WHERE univer = '{tape}'")
            if self.sql.fetchone() is None:
                pass
            else:
                for v in self.sql.execute(f"SELECT * FROM {self.name} WHERE univer = '{tape}'"):
                    v = v[1:]
                    v = [v[0],  v[1]+" "+v[2], v[3], v[4], v[5], v[6]]
                    arr.append(list(v))
            return arr

        def returner(arr, page):
            if len(arr) == 1:
                return arr[0], 2
            if arr == [] or len(arr)-1 < page:
                return "empty", 0
            if page == len(arr)-1:
                return arr[page], 0
            else:
                return arr[page], 1

        if date_arr != [] and less !=[]:
            for key in less:
                if isinstance(univer_prof[key], list):
                    for unov in univer_prof[key]:
                        for date in date_arr:
                            arr = search_less_and_date(unov, date, arr)
                else:
                    for date in date_arr:
                        arr = search_less_and_date(univer_prof[key], date, arr)
            return returner(arr, page)

        elif date_arr != []:
            arr = []
            for date in date_arr:
                self.sql.execute(f"SELECT * FROM {self.name} WHERE text_date = '{date}'")
                if self.sql.fetchone() is None:
                    pass
                else:
                    for v in self.sql.execute(f"SELECT * FROM {self.name} WHERE text_date = '{date}'"):
                        v = v[1:]
                        v = [v[0],  v[1]+" "+v[2], v[3], v[4], v[5], v[6]]
                        arr.append(list(v))
                    #print(arr, page)
            #if date == "":
                #return arr, "date"
            return returner(arr, page)

        elif less !=[]:
            for key in less:
                if isinstance(univer_prof[key], list):
                    for unov in univer_prof[key]:
                        arr = search_less(unov, arr)
                else:
                    arr = search_less(univer_prof[key], arr)

            return returner(arr, page)

        else:
            self.sql.execute(f"SELECT * FROM {self.name} WHERE id = '{page}'")
            if self.sql.fetchone() is None:
                return "empty", 0
            else:
                for v in self.sql.execute(f"SELECT * FROM {self.name} WHERE id = '{page}'"):
                    v = v[1:]
                    v = [v[0],  v[1]+" "+v[2], v[3], v[4], v[5], v[6]]
                    return v, 1
        #print(arr)
    def cheak_event(self, user):
        self.sql.execute(f"SELECT user FROM users WHERE user = '{user}'")
        if self.sql.fetchone() is None:
            return []
        else:
            arr = []
            for v in self.sql.execute(f"SELECT * FROM users WHERE user = '{user}'"):
                arr.append(v)
            return arr

    def join_table(self, arr):
        if arr != []:
            for i in arr:
                print(int(str(self.sql.execute(f'SELECT MAX(`id`) FROM {self.name}'))))
                #max_id = int(str(self.sql.execute(f'SELECT MAX(`id`) FROM {self.name}')))

                self.sql.execute(f"INSERT INTO {self.name} VALUES(?, ?, ?,?, ?, ?, ?, ?)", (max_id+1, i[1], " ".join(i[2].split()[:2]), i[2].split()[2], i[3], i[4], i[5], i[6]))
        else:
            con2 = sqlite3.connect('doors.db')
            sql2 = con2.cursor()


    def delete(self, user):
        self.sql.execute(f"DELETE FROM users WHERE user = '{user}'")
        self.con.commit()
        arr = []
        for v in self.sql.execute("SELECT * FROM users"):
                arr.append(v)
        return (arr)



'''r = sql_manager("prof")
d = r.cheak_date("24 Ноября")
print(d)'''
