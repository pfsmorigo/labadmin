import sqlite3

class DatabaseManager(object):
    def __init__(self, db, verbose = False):
        self.conn = sqlite3.connect(db)
        #self.conn.execute('pragma foreign_keys = on')
        #self.conn.commit()
        self.cur = self.conn.cursor()
        self.verbose = verbose

    def query(self, arg):
        self.cur.execute(arg)
        self.conn.commit()
        if self.verbose == True:
            print arg
        return self.cur

    def __del__(self):
        self.conn.close()
