import sqlite3


class DataBase:
    def __init__(self, db_name) -> None:
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def create(self):
        script1 = f"CREATE TABLE IF NOT EXISTS 'Task' " \
                  f"(id INTEGER PRIMARY KEY AUTOINCREMENT,test TEXT, admin INT NOT NULL)"
        with self.connection:
            self.cursor.execute(script1)
        return 1

    def create2(self):
        script2 = f"CREATE TABLE IF NOT EXISTS 'Javoblar' " \
                  f"(ido INT, user_id TEXT, fullname TEXT, true INT, false INT)"
        with self.connection:
            self.cursor.execute(script2)
        return 1

    def create3(self):
        script2 = f"CREATE TABLE IF NOT EXISTS 'Tugaganlar' " \
                  f"(id INT PRIMARY KEY)"
        with self.connection:
            self.cursor.execute(script2)
        return 1

    def user_exists(self, taskid):
        with self.connection:
            result = self.cursor.execute(f"SELECT * FROM Task WHERE id = '{taskid}'").fetchall()
            return bool(len(result))

    def add_task(self, test, admin):
        with self.connection:
            return self.cursor.execute(f"INSERT INTO Task ("
                                       f" 'test', 'admin') VALUES ('{test}', '{admin}')")

    def add_stop(self, id3):
        with self.connection:
            return self.cursor.execute(f"INSERT INTO Tugaganlar ("
                                       f" 'id') VALUES ('{id3}')")

    def add_submit(self, id2, us_id, fullname, true, false):
        with self.connection:
            return self.cursor.execute(f"INSERT INTO Javoblar ("
                                       f" 'ido', 'user_id', 'fullname', 'true', 'false') VALUES "
                                       f"('{id2}', '{us_id}', '{fullname}', '{true}', '{false}')")

    def get_task(self, taskid):
        with self.connection:
            return self.cursor.execute(f"SELECT * FROM Task WHERE id='{taskid}'").fetchone()

    def get_stop(self, taskid):
        with self.connection:
            return self.cursor.execute(f"SELECT * FROM Tugaganlar WHERE id='{taskid}'").fetchone()

    def check_submit(self, task_id):
        with self.connection:
            return self.cursor.execute(f"SELECT * FROM Javoblar WHERE "
                                       f"ido='{task_id}'").fetchall()

    def get_taskid(self):
        with self.connection:
            return self.cursor.execute(f"SELECT id FROM Task").fetchall()[-1]
