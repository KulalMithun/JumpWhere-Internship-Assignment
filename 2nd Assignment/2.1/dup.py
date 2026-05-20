def contains_duplicate(a):
    return len(a)!=len(set(a))
if __name__=='__main__':
    print(contains_duplicate([1,1,1,2,2,54,5,3,6]))
