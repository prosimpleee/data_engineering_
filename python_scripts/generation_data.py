import datetime
import random
import pandas as pd
import snowflake.connector

# Gets the version
ctx = snowflake.connector.connect(
    user='snowflake_user',
    password='snowflake_password',
    account='snowflake_account',
    database='our_db',
    schema='our_schema',
    role='our_role',
    warehouse='snowflake_warehouse'
)
cs = ctx.cursor()

activity = ['act1', 'act2', 'act3']
station_codes = []
content_codes = []
category_code = [i for i in range(1, 11)]
audience_size = [i for i in range(1000)]

try:
    query_station = cs.execute("""SELECT DISTINCT STATION_CODE
                                  FROM STATIONS_DATA""")

    for station in query_station:
        station_codes.append(*station)

    query_content = cs.execute("""SELECT DISTINCT CONTENT_CODE
                                FROM CONTENT_DATA;""")

    for content in query_content:
        content_codes.append(*content)
finally:
    cs.close()
ctx.close()


generate_data = []

# From 01.09.2022 to 31.09.2022
for day_calendar in range(1, 32):
    start_time = datetime.datetime.strptime(f'{day_calendar}/09/22 00:00:00', '%d/%m/%y %H:%M:%S')
    date = start_time.date()
    while start_time != datetime.datetime.strptime(f'{day_calendar}/09/22 23:59:00', '%d/%m/%y %H:%M:%S'):
        start_time += datetime.timedelta(minutes=1)
        # Here we select the amount of data in 1-minute
        for rng in range(1, 11):
            generate_data.append({
                    'ACTIVITY': random.choice(activity),
                    'CONTENT_CODE': random.choice(content_codes),
                    'STATION_CODE': random.choice(station_codes),
                    'DATE_OF_TRANSMISSION': date,
                    'START_DATE_TIME': start_time,
                    'ARRAY_AUDIENCE': [{str(i): random.choice(audience_size)} for i in category_code]
            })

df = pd.DataFrame(generate_data)
df.to_csv('generation_data_w_array.csv', index=False)