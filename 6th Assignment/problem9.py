quantity=int(input())
unit_cost=100
total=quantity*unit_cost
if total>1000:
    total*=0.9
print(total)
