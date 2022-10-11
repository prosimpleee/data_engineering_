# 1. Parsing a file where the column contains an array. 

The data in the array is separated by a comma. We need to use regular expressions.

**Example below:**

- Audiences Column has array: {[1, 312], [2, 175], [3, 364], ..} # (PARAGRAPH 1)

**Solution:**

```python
import csv
import re
import pandas as pd

with open('your_file.csv', 'r') as csv_file:
    csvReader = csv.DictReader(csv_file)
    data = []
    for rows in csvReader:
        s = re.sub("[^0-9,]", " ", rows['audiences']).strip().split(' , ')
        d = [x.split(',') for x in s]
        for k in d:
            data.append({
                'event_id': rows['event_id'],
                'content_id': rows['content_id'],
                'date_update': rows['date_of_transmission'],
                'phone_code': rows['db2_station_code'],
                'start_time':rows['start_time'],
                'end_time' : rows['end_time'],
                'country_code': k[0],
                'target_size' : k[1]})
    df = pd.DataFrame(data)
    df.to_csv('name_new_file.csv', index=False)
```   
**[Click here: parse_reg_exp.py](https://github.com/prosimpleee/data_engineering_/blob/main/python_scripts/parse_reg_exp.py)**


# 2. Data generation (every 1-minute for 31 days)

With the help of a Snowflake, we pull out the necessary data, on the basis of which we will generate data.

In 1-minute we generate 10 records & Audiences in Array: [{'1': 49}, {'2': 121}, {'3': 851}, ….]

**Solution:**

```python
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
                                  FROM STATIONS_DATA;""")

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
```

**Result:**
![image](https://user-images.githubusercontent.com/55916170/195146491-d8be1404-98e4-4db6-a1b2-111880a60a9e.png)

**[Click here: generation_data.py](https://github.com/prosimpleee/data_engineering_/blob/main/python_scripts/generation_data.py)**
