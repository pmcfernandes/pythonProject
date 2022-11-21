from pymssql import _mssql
import pymssql
import pandas as pd


class Database:
    def __init__(self, host: str, username: str, password: str, database: str):
        self.__conn = None
        self.__host = host
        self.__username = username
        self.__password = password
        self.__database = database
        self.connect()
        pass

    def connect(self) -> bool:
        """
        Connect to Database
        """
        try:
            self.__conn = _mssql.connect(server=self.__host, user=self.__username, password=self.__password, database=self.__database)
        except _mssql.MssqlConnection as e:
            print(e)
            return False
        return True

    def close(self):
        self.__conn.close()
        pass

    def createCursor(self):
        """
        Create a cursor to free use of data
        """
        con = pymssql.connect(server=self.__host, user=self.__username, password=self.__password, database=self.__database)
        cur = con.cursor()
        return cur, con

    def executeNonQuery(self, sql: str, params=None) -> bool:
        """
        Execute non query
        """
        try:
            if params is None:
                self.__conn.execute_non_query(sql)
            else:
                self.__conn.execute_non_query(sql, params)
        except _mssql.MssqlDatabaseException as e:
            print(e)
            return False
        return True

    def executeScalar(self, sql: str, params=None):
        """
        Execute Scalar
        """
        try:
            if params is None:
                result = self.__conn.execute_scalar(sql);
            else:
                result = self.__conn.execute_scalar(sql, params)
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
                self.__conn.execute_query(sql)
            else:
                self.__conn.execute_query(sql, params)
        except _mssql.MssqlDatabaseException as e:
            print(e)
            return None
        return self.__conn


class DataFrame:
    def __init__(self, conn):
        self.__conn = conn
        pass

    def createDataFrame(self, columns):
        data = []

        for row in self.__conn:
            data.append(row)

        df = pd.DataFrame(data, columns=columns)
        return df


