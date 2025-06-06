import math
x=int(input())
b = 1
fact = 1
if x > 1:
    while x>=b:
        fact=fact * b
        b = b + 1
    print(fact)
else:
    print(b)