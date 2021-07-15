import re


def test_data(pattern, test_string):
    result = re.match(pattern, test_string)
    if result:
        return True
    else:
        return False
