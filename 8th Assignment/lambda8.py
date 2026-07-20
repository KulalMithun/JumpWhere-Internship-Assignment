validate=lambda s:len(s)>=10 and any(c.isupper() for c in s) and any(c.islower() for c in s) and any(c.isdigit() for c in s)
print('valid string' if validate('PaceWisd0m') else 'invalid string')
