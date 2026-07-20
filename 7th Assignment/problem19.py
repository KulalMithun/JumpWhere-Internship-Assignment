data=[[10,20],[40],[30,56,25],[10,20],[33],[40]]
new=[]
for item in data:
    if item not in new:
        new.append(item)
print(new)
