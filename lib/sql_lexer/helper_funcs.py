def tuple_remove(tuple_data, element):
    tuple_data = list(tuple_data)
    tuple_data.remove(element)
    return tuple(tuple_data)


def is_float(numeric_str):
    for char in numeric_str:
        if char not in "1234567890.":
            return False
    return True


def is_int_or_float(numeric_str: str):
    return numeric_str.isnumeric() or is_float(numeric_str)