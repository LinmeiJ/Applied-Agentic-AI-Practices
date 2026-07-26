from solution import is_palindrome

# Typical palindromes
assert is_palindrome("racecar") is True
assert is_palindrome("abba") is True

# Mixed case and punctuation (common palindrome definitions ignore non-alphanumeric and case)
assert is_palindrome("A man, a plan, a canal: Panama") is True
assert is_palindrome("No 'x' in Nixon") is True
assert is_palindrome("Able was I ere I saw Elba") is True

# Empty and whitespace-only strings
assert is_palindrome("") is True
assert is_palindrome("   ") is True

# Punctuation-only (reduces to empty if non-alphanumerics are ignored)
assert is_palindrome(".,!!") is True

# Single characters
assert is_palindrome("x") is True
assert is_palindrome("Z") is True

# Numeric examples
assert is_palindrome("12321") is True
assert is_palindrome("1,2,3,2,1") is True
assert is_palindrome("1231") is False

# Non-palindromes
assert is_palindrome("hello") is False
assert is_palindrome("abca") is False

# Long palindrome (performance & correctness on long input)
long_pal = "a" * 10000 + "b" + "a" * 10000
assert is_palindrome(long_pal) is True

# Long with mixed characters and punctuation interspersed (should still be palindrome if cleaned)
base = "Able was I ere I saw Elba"
long_mixed = (base + "!!! ") * 200  # repeated phrase with punctuation
assert is_palindrome(long_mixed) is True