s=input().strip()
pairs={')':'(','}':'{',']':'['}
stack=[]
for ch in s:
    if ch in '([{':
        stack.append(ch)
    elif ch in pairs:
        if not stack or stack.pop()!=pairs[ch]:
            print(False)
            break
else:
    print(not stack)
