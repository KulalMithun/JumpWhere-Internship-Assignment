d={"a":1,"b":2,"c":1}
seen={}
for k,v in d.items():
    if v not in seen:
        seen[v]=k
print({seen[v]:v for v in seen})
