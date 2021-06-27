def string_only_contains(str, charset):
    for char in str:
        if char not in charset:
            return False
    return True
