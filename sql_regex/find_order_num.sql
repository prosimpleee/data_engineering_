-- PostgreSQL
-- Search from (#), any number (\d), \d any quantity (+) 

WITH CTE AS (
SELECT 'Holaquetal#4702665' as order1, 
       'Randal Runolfsson #7480358897 Wayne Jast' as order2,
       '#Jae Jacobs #4384715554 #Elvina Osinski DC' as order3,
       'Deckow #8385923183 #Mac Morar Esq. 8385923183' as order4,
       'Ambrose Koepp #3817501344 Melba Harber	3817501344' as order5,
       'Schoen D  #Milagro D""Amore #4594280029 #Sammy Goyette 	4594280029' as order6
FROM regex) 

SELECT substring(order1 from '#(\d+)') as OrderID_1,
       substring(order2 from '#(\d+)') as OrderID_2,
       substring(order3 from '#(\d+)') as OrderID_3,
       substring(order4 from '#(\d+)') as OrderID_4,
       substring(order5 from '#(\d+)') as OrderID_5, 
       substring(order5 from '#(\d+)') as OrderID_6
FROM CTE

-- We have: 4702665 (order1), 7480358897(order2), 4384715554(order3), 8385923183(order4), 3817501344(order5), 4594280029(order6)
