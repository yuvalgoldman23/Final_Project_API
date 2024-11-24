

def is_one_or_zero(value):
    return value in {1, 0, True, False, "1", "0"}
def is_only_numbers_or_letters(value):
    if isinstance(value, int):
        return True
    if isinstance(value, str):  # Ensure the input is a string
        return value.isalnum()  # Checks if the string is alphanumeric (letters and/or numbers)
    return False