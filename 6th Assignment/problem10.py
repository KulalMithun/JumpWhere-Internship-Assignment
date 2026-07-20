salary=float(input())
years=int(input())
bonus=salary*0.05 if years>5 else 0
print(bonus)
