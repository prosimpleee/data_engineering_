from sqlalchemy import create_engine
import psycopg2
import pandas as pd


POSTGRES_USER = 'USER'
POSTGRES_PASS = 'PASSWORD'
POSTGRES_HOST = 'AZURE_HOST'
POSTGRES_PORT = 5432
POSTGRES_DB = 'postgres'


print('Connect to DB')
conn = psycopg2.connect(user=POSTGRES_USER, database=POSTGRES_DB, password=POSTGRES_PASS, host=POSTGRES_HOST, port=POSTGRES_PORT)
if conn.cursor():
    cur = conn.cursor()
    print('psycopg2 connected')
engine = create_engine(f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASS}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}')
print('sqlalchemy connected')

sql_drop = '''
DROP TABLE IF EXISTS Linkedin;
'''
cur.execute(sql_drop)
conn.commit()

sql = '''
CREATE TABLE IF NOT EXISTS Linkedin (
    id int primary key,
    name varchar(50)
);
'''

cur.execute(sql)
conn.commit()

sql_insert = f"INSERT INTO Linkedin VALUES (1, 'Dmitry');"
cur.execute(sql_insert)
conn.commit()


sql_select = f"SELECT * FROM Linkedin;"
routing_df = pd.read_sql(sql_select, engine)
df = pd.DataFrame(routing_df)
print(df)
