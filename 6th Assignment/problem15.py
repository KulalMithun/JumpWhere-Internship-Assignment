nums=[]
while True:
    value=input()
    if value.lower()=='q':
        break
    nums.append(int(value))
if nums:
    product=1
    for n in nums:
        product*=n
    print(sum(nums)/len(nums))
    print(product)
else:
    print(0)
    print(0)
