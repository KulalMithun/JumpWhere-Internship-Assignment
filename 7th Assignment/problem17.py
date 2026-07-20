x={'key1':1,'key2':3,'key3':2}
y={'key1':1,'key2':2}
for k,v in x.items():
    if k in y and y[k]==v:
        print(f"{k}: {v} is present in both x and y")
