import mysql.connector as mysql


class QueryManager:
    def __init__(self, _host, _user, _password, _database):
        self.conn = mysql.connect(host=_host, user=_user, password=_password, database=_database)

    def query(self, query_string, params=None):
        if params is not None:
            for name, value in params.items():
                query_string = query_string.replace("{" + name + "}", value)
        cursor = self.conn.cursor()
        cursor.execute(query_string)
        return cursor

    def dispose(self, disposable=None):
        if disposable is None:
            self.conn.close()
        else:
            if hasattr(disposable, 'close'):
                disposable.close()
