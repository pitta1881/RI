from itertools import zip_longest

miarray = [11,2123,456,789,7897]
miarray2 = [456,89,561,12358]

for valor1, valor2 in zip_longest(miarray, miarray2, fillvalue=''):
    print(valor1, valor2)