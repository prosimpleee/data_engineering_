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
                'content_id': rows['barb_content_id'],
                'date_update': rows['date_of_transmission'],
                'phone_code': rows['db2_station_code'],
                'start_time':rows['start_time'],
                'end_time' : rows['end_time'],
                'country_code': k[0],
                'target_size' : k[1]})
    df = pd.DataFrame(data)
    df.to_csv('name_new_file.csv', index=False)
