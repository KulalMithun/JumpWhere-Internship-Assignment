from collections import Counter

# 1
def length_of_string(s):
    return len(s)


# 2
def char_frequency(s):
    return dict(Counter(s))


# 3
def first_last_two_chars(s):
    if len(s) < 2:
        return ""
    return s[:2] + s[-2:]


# 4
def replace_first_char_occurrences(s):
    if not s:
        return s
    first = s[0]
    rest = s[1:]
    return first + rest.replace(first, '$')


# 5
def swap_first_two_chars(a, b):
    if len(a) < 2 or len(b) < 2:
        return f"{a} {b}"
    return b[:2] + a[2:] + " " + a[:2] + b[2:]


# 6
def verbing(s):
    if len(s) < 3:
        return s
    if s.endswith('ing'):
        return s + 'ly'
    return s + 'ing'


# 7
def not_poor_wrong(s):
    not_index = s.find('not')
    poor_index = s.find('poor')
    if not_index != -1 and poor_index != -1 and poor_index < not_index:
        return s[:not_index] + 'good' + s[poor_index + 4:]
    return s


# 8
def longest_word_length(words):
    if not words:
        return 0
    return max(len(word) for word in words)


# 9
def remove_nth_char(s, n):
    if n < 0 or n >= len(s):
        return s
    return s[:n] + s[n+1:]


# 10
def unique_sorted_words(comma_separated):
    words = [word.strip() for word in comma_separated.split(',') if word.strip()]
    unique = sorted(set(words), key=lambda x: (x.lower(), x))
    return ', '.join(unique)


# 11
def reverse_if_multiple_of_four(s):
    return s[::-1] if len(s) % 4 == 0 else s


# 12
def uppercase_if_two_in_first_four_wrong(s):
    count = sum(1 for c in s[:4] if c.isupper())
    if count >= 3:
        return s.upper()
    return s


# 13
def starts_with(s, prefix):
    return s.startswith(prefix)


# 14
def format_two_decimals(value):
    return f"{value:.2f}"


# 15
def repeated_character_counts(s):
    counts = Counter(s)
    repeated = [(char, count) for char, count in counts.items() if count > 1]
    ordered = []
    seen = set()
    for ch in s:
        if ch in counts and counts[ch] > 1 and ch not in seen:
            ordered.append((ch, counts[ch]))
            seen.add(ch)
    return ordered


# 16
def index_of_char(s, ch):
    return s.find(ch)


# 17
def string_to_list(s):
    return list(s)


# 18
def swap_comma_dot(s):
    return s.replace('.', '<dot>').replace(',', '.').replace('<dot>', ',')


# 19
def smallest_largest_words(s):
    words = [word for word in s.split() if word]
    if not words:
        return None, None
    smallest = min(words, key=len)
    largest = max(words, key=len)
    return smallest, largest


# 20
def remove_consecutive_duplicates(s):
    if not s:
        return s
    result = [s[0]]
    for char in s[1:]:
        if char != result[-1]:
            result.append(char)
    return ''.join(result)

if __name__ == '__main__':
    print('1:', length_of_string('hello'))
    print('2:', char_frequency('google.com'))
    print('3a:', first_last_two_chars('thisisniceone'))
    print('3b:', first_last_two_chars('ab'))
    print('3c:', repr(first_last_two_chars('f')))
    print('4:', replace_first_char_occurrences('restart'))
    print('5:', swap_first_two_chars('abc', 'xyz'))
    print('6a:', verbing('abc'))
    print('6b:', verbing('string'))
    print('7a:', not_poor_wrong('The lyrics is not that poor!'))
    print('7b:', not_poor_wrong('The lyrics is poor!'))
    print('8:', longest_word_length(['hello', 'world', 'python']))
    print('9:', remove_nth_char('hello', 1))
    print('10:', unique_sorted_words('red, white, black, red, green, black'))
    print('11a:', reverse_if_multiple_of_four('abcd'))
    print('11b:', reverse_if_multiple_of_four('abc'))
    print('12a:', uppercase_if_two_in_first_four_wrong('ABcd'))
    print('12b:', uppercase_if_two_in_first_four_wrong('AbCd'))
    print('13:', starts_with('hello world', 'he'))
    print('14:', format_two_decimals(3.1415926))
    print('15:', repeated_character_counts('thequickbrownfoxjumpsoverthelazydog'))
    print('16:', index_of_char('hello', 'e'))
    print('17:', string_to_list('hello'))
    print('18:', swap_comma_dot('32.054,23'))
    print('19:', smallest_largest_words('The quick brown fox jumps over the lazy dog'))
    print('20:', remove_consecutive_duplicates('aabbccddeeeff'))
