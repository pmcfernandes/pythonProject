import pandas as pd
from types import *


class DataSet:
    def __init__(self, df: pd.DataFrame):
        self.__df = df
        self.__df.convert_dtypes()
        pass

    @staticmethod
    def createDataFrame(data: None, columns: None):
        if columns is None:
            df = pd.DataFrame(data=data)
        else:
            df = pd.DataFrame(data=data, columns=columns)
        return df

    @staticmethod
    def createInstance(df: pd.DataFrame):
        return DataSet(df)

    def getDataFrame(self):
        return self.__df

    def getRow(self, i):
        df = self.__df.iloc[i]
        return DataSet.createInstance(df)

    def addRow(self, row):
        df2 = pd.Series(row).to_frame().T
        self.__df = pd.concat([self.__df, df2], ignore_index=True)
        pass

    def deleteRow(self, index: int):
        df = self.__df.drop(self.__df.index[index], inplace=False)
        return DataSet.createInstance(df)

    def deleteRows(self, condition: FunctionType):
        df = self.__df.drop(self.__df[condition].index, inplace=False)
        return DataSet.createInstance(df)

    def getValue(self, row, column: str):
        if isinstance(row, str):
            return self.__df.at[row, column];
        elif isinstance(row, int):
            return self.__df.iloc[row][column];
        else:
            return None

    def sliceColumns(self, columns: list):
        if all(isinstance(s, str) for s in columns):
            df = self.__df.loc[:, columns]
        if all(isinstance(s, int) for s in columns):
            df = self.__df.iloc[:, columns]
        return DataSet.createInstance(df)

    def getColumnNames(self):
        return self.__df.columns.values.tolist()

    def addColumn(self, column):
        df = self.__df.copy()
        df.assign(column)
        return DataSet.createInstance(df)

    def renameColumn(self, oldColumnName, columnName):
        df = self.__df.rename(columns={oldColumnName: columnName})
        return DataSet.createInstance(df)

    def setColumnType(self, column: str, t: type):
        self.__df.astype({column: t})
        pass

    def top(self, n: int):
        df = self.__df.head(n)
        return DataSet.createInstance(df)

    def latest(self, n: int):
        df = self.__df.tail(n)
        return DataSet.createInstance(df)

    def query(self, condition):
        if isinstance(condition, str):
            print("x")
            df = self.__df if len(condition) == 0 else self.__df.query(condition, inplace=False)
        else:
            df = self.__df.apply(condition)
        return DataSet.createInstance(df)

    def getCount(self):
        return len(self.__df.index) if self.__df.index is not None else self.__df.count()[0]

    def group(self, columns: list):
        df = self.__df.groupby(by=columns)
        return df

    def rows(self):
        for index, row in self.__df.iterrows():
            yield index, row

    def __str__(self):
        return str(self.__df)

