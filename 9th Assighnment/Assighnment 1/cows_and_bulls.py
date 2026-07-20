import random

def generate_number():
    digits='0123456789'
    return ''.join(random.sample(digits,4))

secret=generate_number()
guesses=0
print('Welcome to the Cows and Bulls Game!')
while True:
    guess=input('Enter a number: ')
    guesses+=1
    cows=sum(1 for i in range(4) if guess[i]==secret[i])
    bulls=sum(1 for c in guess if c in secret) - cows
    print(f"{cows} cows, {bulls} bulls")
    if guess==secret:
        print('You guessed it in',guesses,'tries')
        break
