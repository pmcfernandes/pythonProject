# pythonProject
Just for python learning. 

Created a small utility package with MSSQL support and SQLBuilder for learning proposal and jupyter Data Science.

Examples:
 
    from python_utilities import DataSet, Database

#### Create a connection

    conn = Database(host="localhost", username="sa", password="xpto", database="db")

#### Get data from database 

    data = conn.fetchCursor("SELECT * FROM MetaUser")

#### Convert to DataFrame

     d = DataSet \
        .createInstance(DataSet.createDataFrame(data=data, columns=None)) \
        .sliceColumns(["IDUser", "Username", "Email"]) \
        .top(10)

#### Add a row to DataFrame

    row = {"IDUser": 111, "Username": "xpto", "Email": "xxxx@gmail.com"}
    d.addRow(row)