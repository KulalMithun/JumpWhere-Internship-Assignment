words=['red','black','white','green','orange']
search='ack'
print(list(filter(lambda w:search in w,words)))
search='abc'
print(list(filter(lambda w:search in w,words)))
