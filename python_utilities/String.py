import pandas as pd


class String(str):
    def printDataFrame(self, conn, n: int = 10):
        cur, con = conn.createCursor()
        cur.execute(self)
        data = cur.fetchall()
        df = pd.DataFrame(data).tail(n)
        print(df)
        con.close()
