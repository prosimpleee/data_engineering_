**Designing Fact Tables:**
- Business facts (events) -> become tables (example: Orders).
- Facts are the subject of business analysis.
- One fact - one table.
In my example, fact Orders: one row is one product order. I could add another fact table that would describe the buyer's general order.

**Dimension Table Design:**
- Dim tables attributes will become criteria for (group, filter, sort) in reports.
- Dim Tables should not grow at the same rate as fact tables.
- Data granulation for analysis (star or snowflake schemas).
- Slowly Changing Dimension (If the buyer moved to another city, then we will add a new CustomerKey and there will be a new person in the report).
The full version scheme and part version scheme show of the object data model, business area - "Orders".
![part_version_scheme](https://user-images.githubusercontent.com/55916170/157976059-431ce4a6-fe35-4179-9fe5-50132db6eaa7.png)
![full_version_scheme](https://user-images.githubusercontent.com/55916170/157976079-a0df365e-88f7-4b29-8ea3-058612068a34.png)
