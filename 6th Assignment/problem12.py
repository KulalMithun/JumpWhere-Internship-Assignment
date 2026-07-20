held=int(input())
attended=int(input())
percentage=attended/held*100 if held else 0
print(percentage)
print('Allowed' if percentage>=75 else 'Not allowed')
