mixed=[1,'two',3.0,4,'five',6.7]
ints=[x for x in mixed if isinstance(x,int) and not isinstance(x,bool)]
strings=[x for x in mixed if isinstance(x,str)]
floats=[x for x in mixed if isinstance(x,float)]
print(ints)
print(strings)
print(floats)
