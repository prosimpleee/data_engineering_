import pandas
from sqlalchemy.engine import URL
from sqlalchemy import create_engine

driver = '{SQL Server}'
server = 'SQL Server Name'
database = 'Database Name'
login = 'Login Name'
password = 'Password'


def connection_mssql(driver, server, database, login, password):
    connection_str = 'Driver=' + driver + ';' \
                     'Server=' + server + ';' \
                     'Database=' + database + ';' \
                     'UID=' + login + ';' \
                     'PWD=' + password
    connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_str})
    engine = create_engine(connection_url)
    return engine


connection_mssql(driver, server, database, login, password)


def sql_query_mssql():
    sql_query = pandas.read_sql_query('''select top 10 * from Schema.YourTable''',
                                      connection_mssql(driver, server, database, login, password))
    query_df = pandas.DataFrame(sql_query)
    print(query_df)


sql_query_mssql()
