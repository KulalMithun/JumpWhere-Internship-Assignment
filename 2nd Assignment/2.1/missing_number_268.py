def missing_number(a):
    n=len(a)
    total=n*(n+1)//2
    return total-sum(a)
if __name__=='__main__':
    print(missing_number([3,0,1]))
