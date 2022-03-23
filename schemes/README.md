# DWH Logic Design

## Designing Fact Tables:
- Business facts (events) -> become tables (example: Orders).
- Facts are the subject of business analysis.
- One fact - one table.
In my example, fact Orders: one row is one product order. I could add another fact table that would describe the buyer's general order.

## Dimension Table Design: ##
- Dim tables attributes will become criteria for (group, filter, sort) in reports.
- Dim Tables should not grow at the same rate as fact tables.
- Data granulation for analysis (star or snowflake schemas).
- Slowly Changing Dimension (If the buyer moved to another city, then we will add a new CustomerKey and there will be a new person in the report).
The full version scheme and part version scheme show of the object data model, business area - "Orders".

