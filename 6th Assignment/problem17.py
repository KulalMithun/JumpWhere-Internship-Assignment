evens=[i for i in range(1,101) if i%2==0]
odds=[i for i in range(1,101) if i%2!=0]
primes=[]
for i in range(2,101):
    for j in range(2,int(i**0.5)+1):
        if i%j==0:
            break
    else:
        primes.append(i)
print(evens)
print(odds)
print(primes)
