import pandas as pd

update = []
for i in range (1,5):
    dictinary = {str(i) : i}
    update.append(dictinary)
df = pd.DataFrame(update)
print(df)