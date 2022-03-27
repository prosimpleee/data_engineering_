# PySpark

This is a very powerful tool that I would like to use on a regular basis. 

It allows you to process more data than the RAM of the machine + can process data on several machines, yet Pandas does not have such an option.

## Create session:
```python
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
import datetime
spark = SparkSession.builder.getOrCreate()
```

## Read a file:
```python
spark \
  .read \
  .option('header', True) \
  .option('inferSchema', True)\              # get types
  .csv(f'path/file_name.csv') \              # path + file name
  .createOrReplaceTempView('business_sales') # create view
```

## Create a dataframe:
```python
df = spark.table('your_view')
```

## Projects:
**1. cars_prices.csv:** 
- I have processed a csv file related to the sale of cars. I selected the fields I needed and did the aggregation.
Click [here](https://github.com/prosimpleee/data_engineering_/blob/main/python_pyspark/cars_prices.ipynb) to go to cars_prices project. 

**2. business_sales.csv tasks:** 
- How much money each customer spent per month? 
- How many different items of goods he bought?
- What goods he bought most often?
Click [here](https://github.com/prosimpleee/data_engineering_/blob/main/python_pyspark/business_sales_pyspark.ipynb) to go to cars_prices project. 

**3. zara_products:**
- Find the dependence of the price on the presented colors.
Click [here](https://github.com/prosimpleee/data_engineering_/blob/main/python_pyspark/zara_products_color.ipynb) to go to cars_prices project. 

