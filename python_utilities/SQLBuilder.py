from enum import Enum

from .Date import Date


class BracketType(Enum):
    NoBracket = 0
    LeftBracket = 1
    RightBracket = 2


class ClauseType(Enum):
    All = 0
    Top = 1
    Distinct = 2


class FieldType(Enum):
    Numeric = 0
    Text = 1
    Date = 2
    Boolean = 3
    Currency = 4
    Empty = 5
    Image = 6
    Memo = 7
    Decimal4 = 8
    Decimal18 = 9
    Parameter = 10


class JoinType(Enum):
    Inner = 0
    Left = 1
    Right = 2
    Full = 3


class LogicalOperator(Enum):
    AND = 0
    OR = 1


class OrderByDirection(Enum):
    Asc = 0
    Desc = 1


class WhereOperator(Enum):
    Equal = 0
    IsNull = 1
    IsNotNull = 2
    Like = 3
    In = 4
    NotLike = 5
    NotEqual = 6
    Greater = 7
    Less = 8
    Greater_OR_Equal = 9
    Less_OR_Equal = 10
    NotIn = 11
    Contains = 12
    BeginsWith = 13
    EndsWith = 14
    NotContains = 15
    NotBeginsWith = 16
    NotEndsWith = 17


class SQLField:
    def __init__(self, fieldName: str, value="", fieldType=FieldType.Numeric, whereOperator=WhereOperator.Equal, logicalOperator=LogicalOperator.AND, bracketType=BracketType.NoBracket):
        self.fieldName = fieldName
        self.value = value
        self.fieldType = fieldType
        self.whereOperator = whereOperator
        self.logicalOperator = logicalOperator
        self.bracketType = bracketType
        pass


class SQLBase:
    def __init__(self):
        self.whereClauses = []
        self.strTableName = None
        self.strLogicalOperator = None
        pass

    def getTableName(self) -> str:
        return self.strTableName

    def setTableName(self, name: str):
        self.strTableName = name
        pass

    def _AddJoin(self, tableName: str, joinTableName: str, jointType: JoinType = JoinType.Left) -> str:
        if jointType == JoinType.Inner:
            strJoin = "INNER"
        elif jointType == JoinType.Full:
            strJoin = "FULL"
        elif jointType == JoinType.Right:
            strJoin = "RIGHT"
        else:
            strJoin = "LEFT"

        self.strLogicalOperator = ""
        return f"{tableName} {strJoin} JOIN {joinTableName}"

    def _AddOn(self, fieldName: str, value, fieldType=FieldType.Numeric, whereOperator=WhereOperator.Equal, logicalOperator=LogicalOperator.AND):
        if len(fieldName) == 0:
            pass

        if len(self.strLogicalOperator) == 0:
            self.strLogicalOperator = "ON"
        else:
            self.strLogicalOperator = self.__getLogicalOperator(logicalOperator)

        self.strTableName = f"{self.strTableName} {self.strLogicalOperator} {fieldName} {self._enclose(value, fieldType, whereOperator)} "
        pass

    def _AddWhere(self, fieldName: str, value, fieldType=FieldType.Numeric, whereOperator=WhereOperator.Equal, logicalOperator=LogicalOperator.AND, bracketType=BracketType.NoBracket):
        if len(fieldName) == 0:
            pass

        self.whereClauses.append(SQLField(fieldName, value, fieldType, whereOperator, logicalOperator, bracketType))
        pass

    def _getFields(self, fields) -> str:
        if len(fields) == 0:
            return ""

        strSQL = ""
        for f in fields:
            strSQL += f"{f.fieldName}, "

        return strSQL.strip()[:-1];

    def _getSet(self, fields) -> str:
        if len(fields) == 0:
            return ""

        strSQL = " SET "

        for f in fields:
            strEncloseSet = self._encloseSet(f.value, f.fieldType)
            strSQL += f"{f.fieldName} = {strEncloseSet}, "

        return strSQL.strip()[:-1]

    def _getWheres(self, fields) -> str:
        strSQL = ""
        if len(fields) == 0:
            return ""

        logicalOperator = " WHERE "

        for f in fields:
            if type(f) == SQLField:
                whereClause, logicalOperator = self.__getWhere(f, logicalOperator)
                strSQL += whereClause
            else:
                if logicalOperator == " WHERE ":
                    strSQL = logicalOperator + f.fieldName
                else:
                    if f.startswith("AND ") or f.startswith("OR "):
                        logicalOperator = " "
                    else:
                        logicalOperator = "AND "

                    strSQL += strSQL + logicalOperator + f

            logicalOperator = ""

        return strSQL

    def __getWhere(self, field: SQLField, logicalOperator: str):
        if logicalOperator != " WHERE ":
            logicalOperator = SQLBase.__getLogicalOperator(field.logicalOperator)

        strSQL = logicalOperator + SQLBase.__getBracket(field.bracketType)

        if field.fieldType != FieldType.Text:
            strSQL += field.fieldName + self._enclose(field.value, field.fieldType, field.whereOperator)
        else:
            if field.value is None:
                strSQL += "UPPER({fieldName}) {enclose}".format(fieldName=field.fieldName, enclose=self._enclose("", field.fieldType, field.whereOperator))
            else:
                strSQL += "UPPER({fieldName}) {enclose}".format(fieldName=field.fieldName, enclose=self._enclose(field.value.upper(), field.fieldType, field.whereOperator))

        strSQL += SQLBase.__getBracket(field.bracketType)
        return strSQL, logicalOperator

    @staticmethod
    def __getLogicalOperator(logicalOperator: LogicalOperator) -> str:
        if logicalOperator == LogicalOperator.AND:
            return "AND"
        elif logicalOperator == LogicalOperator.OR:
            return "OR"

    @staticmethod
    def __getBracket(bracketType: BracketType) -> str:
        if bracketType == BracketType.LeftBracket:
            return "("
        elif bracketType == BracketType.RightBracket:
            return ")"
        else:
            return ""

    def _enclose(self, value, fieldType: FieldType, whereOperator: WhereOperator) -> str:
        strEnclose = ""

        if value is None:
            value = ""

        if len(value) == 0 and fieldType == FieldType.Empty:
            if whereOperator == WhereOperator.IsNotNull or whereOperator == WhereOperator.NotEqual:
                strEnclose = " IS NOT NULL"
            else:
                strEnclose = " IS NULL"
        elif whereOperator == WhereOperator.IsNull or (fieldType == FieldType.Empty and whereOperator == WhereOperator.IsNull):
            strEnclose = " IS NULL"
        elif whereOperator == WhereOperator.IsNotNull or (fieldType == FieldType.Empty and whereOperator == WhereOperator.IsNotNull):
            strEnclose = " IS NOT NULL"
        elif whereOperator == WhereOperator.Like:
            strEnclose = f" LIKE '{value}'"
        elif whereOperator == WhereOperator.Contains:
            strEnclose = f" LIKE '%{value}%'"
        elif whereOperator == WhereOperator.BeginsWith:
            strEnclose = f" LIKE '%{value}'"
        elif whereOperator == WhereOperator.EndsWith:
            strEnclose = f" LIKE '%{value}'"
        elif whereOperator == WhereOperator.NotContains:
            strEnclose = f" NOT LIKE '%{value}%'"
        elif whereOperator == WhereOperator.NotBeginsWith:
            strEnclose = f" NOT LIKE '%{value}'"
        elif whereOperator == WhereOperator.NotEndsWith:
            strEnclose = f" NOT LIKE '{value}%'"
        elif whereOperator == WhereOperator.NotLike:
            strEnclose = f" NOT LIKE '{value}'"
        elif whereOperator == WhereOperator.In or (fieldType == FieldType.Empty and whereOperator == WhereOperator.In):
            strEnclose = f" IN {value}"
        elif whereOperator == WhereOperator.NotIn or (
                fieldType == FieldType.Empty and whereOperator == WhereOperator.NotIn):
            strEnclose = f" NOT IN {value}"
        else:
            strValue = self.__encloseValues(value, fieldType)

            if whereOperator == WhereOperator.Equal:
                strEnclose = f" = {strValue}"
            elif whereOperator == WhereOperator.NotEqual:
                strEnclose = f" <> {strValue}"
            elif whereOperator == WhereOperator.Greater:
                strEnclose = f" > {strValue}"
            elif whereOperator == WhereOperator.Greater_OR_Equal:
                strEnclose = f" >= {strValue}"
            elif whereOperator == WhereOperator.Less:
                strEnclose = f" < {strValue}"
            elif whereOperator == WhereOperator.Less_OR_Equal:
                strEnclose = f" <= {strValue}"

        return strEnclose

    def __encloseValues(self, value, fieldType: FieldType):
        strValue = value

        if fieldType == FieldType.Parameter:
            strValue = value.replace(",", ".")
        else:
            if fieldType == FieldType.Numeric:
                if value is None:
                    strValue = "0"
                else:
                    strValue = str(value)

                if isinstance(value, str) and value.isnumeric():
                    strValue = value.replace(",", ".")

            if fieldType == FieldType.Boolean:
                if value != "0":
                    strValue = True
                else:
                    strValue = False

            if fieldType == FieldType.Date:
                try:  # try cast date time
                    dt = Date.toDateTime(strValue)
                except Exception as e:
                    dt = Date.now()
                    print(e)

                strValue = dt

            if fieldType == FieldType.Text or fieldType == FieldType.Memo:
                strValue = "{val}".format(val=value.replace("'", "''"))
                strValue = f"'{strValue}'"

            if fieldType == FieldType.Decimal4 or fieldType == FieldType.Decimal18 or fieldType == FieldType.Currency:
                if value is None:
                    strValue = 0
                else:
                    strValue = float(value)

                if fieldType == FieldType.Currency:
                    strFormat = "%.2f"
                else:
                    strFormat = "%.4f"

                strValue = strFormat % strValue

        return strValue

    def _encloseSet(self, value, fieldType: FieldType) -> str:
        if value is None:
            strEnclose = "NULL"
        else:
            strValue = self.__encloseValues(value, fieldType)
            strEnclose = strValue

        return strEnclose


class SQLSelect(SQLBase):
    def __init__(self):
        super().__init__()
        self.__fields = []
        self.__orders = []
        self.__groups = []

    def AddField(self, fieldNames):
        if isinstance(fieldNames, str):
            values = fieldNames.split(",")
        else:
            if isinstance(fieldNames, (dict, list)):
                values = fieldNames
            else:
                raise Exception("fieldNames must be a string or a list")

        for f in values:
            self.__fields.append(SQLField(f.strip()))
        pass

    def AddJoin(self, tableName: str, joinType: JoinType = JoinType.Left):
        if len(tableName) == 0:
            pass

        self.setTableName(self._AddJoin(self.getTableName(), tableName, joinType))
        pass

    def AddOn(self, fieldName: str, value, fieldType=FieldType.Numeric, whereOperator=WhereOperator.Equal, logicalOperator=LogicalOperator.AND):
        self._AddOn(fieldName, value, fieldType, whereOperator, logicalOperator)
        pass

    def AddWhere(self, fieldName: str, value, fieldType=FieldType.Numeric, whereOperator=WhereOperator.Equal, logicalOperator=LogicalOperator.AND, bracketType=BracketType.NoBracket):
        self._AddWhere(fieldName, value, fieldType, whereOperator, logicalOperator, bracketType)
        pass

    def AddOrder(self, fieldName: str, orderBy=OrderByDirection.Asc):
        if len(fieldName) == 0:
            pass

        self.__orders.append(SQLField(fieldName + "ASC" if orderBy == OrderByDirection.Asc else "DESC"))
        pass

    def AddGroup(self, fieldName: str):
        if len(fieldName) == 0:
            pass

        self.__orders.append(SQLField(fieldName))
        pass

    def __getSelectFields(self) -> str:
        if len(self.__fields) == 0:
            return "*"
        else:
            return self._getFields(self.__fields)

    def __getOrderBys(self) -> str:
        if len(self.__orders) == 0:
            return ""
        else:
            return " ORDER BY {orders}".format(orders=self._getFields(self.__orders))

    def __getGroups(self) -> str:
        if len(self.__groups) == 0:
            return ""
        else:
            return " GROUP BY {groups}".format(groups=self._getFields(self.__groups))

    def SQL(self) -> str:
        if len(self.__fields) == 0:
            return ""

        strSQL = "SELECT {fields} FROM {tableName}{where}{groups}{orders}".format(tableName=self.getTableName(), fields=self.__getSelectFields(), where=self._getWheres(self.whereClauses), groups=self.__getGroups(), orders=self.__getOrderBys())
        return strSQL


class SQLInsert(SQLBase):
    def __init__(self):
        super().__init__()
        self.__fields = []

    def AddValue(self, fieldName: str, value, fieldType=FieldType.Numeric):
        if len(fieldName) == 0:
            pass

        self.__fields.append(SQLField(fieldName, value, fieldType))
        pass

    def SQL(self) -> str:
        if len(self.__fields) == 0:
            return ""

        columns = ""
        values = ""

        for f in self.__fields:
            columns += f.fieldName + ", "
            values += self._encloseSet(f.value, f.fieldType) + ", "

        columns = columns.strip()[:-1]
        values = values.strip()[:-1]

        strSQL = "INSERT INTO {tableName} ({fields}) VALUES ({values})".format(tableName=self.getTableName(), fields=columns, values=values)
        return strSQL


class SQLUpdate(SQLBase):
    def __init__(self):
        super().__init__()
        self.__fields = []

    def AddSet(self, fieldName: str, value, fieldType=FieldType.Numeric):
        if len(fieldName) == 0:
            pass

        self.__fields.append(SQLField(fieldName, value, fieldType))
        pass

    def AddWhere(self, fieldName: str, value, fieldType=FieldType.Numeric, whereOperator=WhereOperator.Equal, logicalOperator=LogicalOperator.AND, bracketType=BracketType.NoBracket):
        self._AddWhere(fieldName, value, fieldType, whereOperator, logicalOperator, bracketType)
        pass

    def SQL(self) -> str:
        if len(self.__fields) == 0:
            return ""

        strSQL = "UPDATE {tableName} {sets}{where}".format(tableName=self.getTableName(), sets=self._getSet(self.__fields), where=self._getWheres(self.whereClauses))
        return strSQL


class SQLDelete(SQLBase):

    def AddWhere(self, fieldName: str, value, fieldType=FieldType.Numeric, whereOperator=WhereOperator.Equal, logicalOperator=LogicalOperator.AND, bracketType=BracketType.NoBracket):
        self._AddWhere(fieldName, value, fieldType, whereOperator, logicalOperator, bracketType)
        pass

    def SQL(self) -> str:
        strSQL = "DELETE FROM {tableName}{where}".format(tableName=self.getTableName(), where=self._getWheres(self.whereClauses))
        return strSQL

