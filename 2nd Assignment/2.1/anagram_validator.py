from collections import Counter
def check_anagrams(s1, s2):
    if len(s1) != len(s2):
        return False
    return Counter(s1) == Counter(s2)
if __name__ == "__main__":
    print(check_anagrams("listen", "silent"))
    print(check_anagrams("hello", "world"))
