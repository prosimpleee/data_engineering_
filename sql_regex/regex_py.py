import re

all_products = ['ProductNumber: 21404523', 'ProductNumber: 34534253', 'ProductNumber: 2355235',
                'ProductNumber: 65785856', 'ProductNumber: 9886743', 'ProductNumber: 867685',
                'ProductNumber: 96792353', 'ProductNumber: 36463643', 'ProductNumber: 45758458']

products_num = [re.findall("[0-9]+", i) for i in all_products]
print(products_num)

# Return:
# [['21404523'], ['34534253'], ['2355235'],
# ['65785856'], ['9886743'], ['867685'],
# ['96792353'], ['36463643'], ['45758458']]
