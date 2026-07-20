items=[]
for _ in range(int(input())):
    items.append(input())
value=input()
for item in items:
    if item==value:
        items.remove(item)
        break
print(items)
