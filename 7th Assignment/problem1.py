d={"a":3,"b":1,"c":2}
print(dict(sorted(d.items(), key=lambda x:x[1])))
print(dict(sorted(d.items(), key=lambda x:x[1], reverse=True)))
