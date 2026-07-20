import random

def load_words(filename):
    with open(filename) as f:
        return [line.strip() for line in f if line.strip()]

def choose_word(words):
    return random.choice(words).upper()

def play():
    words=load_words('words.txt')
    while True:
        secret=choose_word(words)
        guessed=set()
        tries=6
        print('Welcome to Hangman!')
        while tries>0:
            clue=' '.join(c if c in guessed else '_' for c in secret)
            print(clue)
            if all(c in guessed for c in secret):
                print('You win!')
                break
            letter=input('Guess your letter: ').upper()
            if letter in guessed:
                print('Already guessed')
                continue
            guessed.add(letter)
            if letter not in secret:
                tries-=1
                print('Incorrect!')
                print('You left with',tries,'chances to guess.')
        else:
            print('You lose. The word was',secret)
        if input('Play again? (y/n): ').lower()!='y':
            break

if __name__=='__main__':
    play()
