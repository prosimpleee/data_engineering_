
# How to connect to PgAdmin in Docker?

Consider connecting 2 docker containers

**1. Create Network**

```docker
docker network create pg-network(name_of_network)
```

**2. Connecting to Postgres**

```docker
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v c://Users/dmitr/git/data-engineering-zoomcamp/week_1_basics_n_setup/2_docker_sql/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \ 
  --network=pg-network \ 
  --name pg-database \
  postgres:13
```

**3. Put the data into PostgresDB (using Python)**

```python
engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')
df = pd.read_parquet('yellow_tripdata_2021-01.parquet', engine='pyarrow')
pd.io.sql.get_schema(df, name = 'yellow_taxi_data', con = engine)
df.to_sql(name="yellow_taxi_data", con=engine, if_exists="replace")
```
**4. Connecting to PgAdmin**

```docker
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  --network=pg-network \
  --name pgadmin dpage/pgadmin4
```

**5. Logging** 

Logging into to PgAdmin 
![Logging](https://user-images.githubusercontent.com/55916170/181265341-3a8dc817-f332-4f3b-8b22-f6ef7fe0f634.png)

**6. Create a connection**

![image](https://user-images.githubusercontent.com/55916170/181265984-3344a392-3ccd-4c96-8f4b-b8314d506b20.png)

## 7. Success!!!

![image](https://user-images.githubusercontent.com/55916170/181266778-b2e16c84-7bd0-4291-8725-600d2b19da04.png)

**Connection with docker-compose**

```docker
docker-compose up
```

**[Click here: docker-compose file](https://github.com/prosimpleee/data_engineering_/blob/main/data-engineering-zoomcamp/week_1_basics_n_setup/docker-compose.yaml)**







