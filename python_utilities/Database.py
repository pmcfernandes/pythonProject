from pymssql import _mssql
import pandas as pd


class Database:
    def __init__(self, host: str, username: str, password: str, database: str):
        self.conn = None
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.connect()
        pass

    def connect(self) -> bool:
        """
        Connect to Database
        """
        try:
            self.conn = _mssql.connect(server=self.host, user=self.username, password=self.password, database=self.database)
        except _mssql.MssqlConnection as e:
            print(e)
            return False
        return True

    def close(self):
        self.conn.close()
        pass

    def executeNonQuery(self, sql: str, params=None) -> bool:
        """
        Execute non query
        """
        try:
            if params is None:
                self.conn.execute_non_query(sql)
            else:
                self.conn.execute_non_query(sql, params)
        except _mssql.MssqlDatabaseException as e:
            print(e)
            return False
        return True

    def executeScalar(self, sql: str, params=None):
        """
          Execute Scalar
        """
        result = None
        try:
            if params is None:
                result = self.conn.execute_scalar(sql);
            else:
                result = self.conn.execute_scalar(sql, params)
        except _mssql.MssqlDatabaseException as e:
            print(e)
            return None
        return result

    def execute(self, sql: str, params=None):
        """
        Execute data and create a iterator
        """
        try:
            if params is None:
                self.conn.execute_query(sql)
            else:
                self.conn.execute_query(sql, params)
        except _mssql.MssqlDatabaseException as e:
            print(e)
            return None
        return self.conn


class DataFrame:
    def __init__(self, conn):
        self.conn = conn
        pass

    def createDataFrame(self, columns):
        data = []

        for row in self.conn:
            data.append(row)

        df = pd.DataFrame(data, columns=columns)
        return df


