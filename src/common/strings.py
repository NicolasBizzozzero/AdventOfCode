def insert_substring(original: str, substring: str, index: int) -> str:
    """
    Inserts a substring into a string at the specified index.

    Args:
    original (str): The original string.
    substring (str): The substring to insert.
    index (int): The index at which to insert the substring.

    Returns:
    str: The modified string with the substring inserted.
    """
    if index < 0 or index > len(original):
        raise ValueError("Index out of bounds.")

    return original[:index] + substring + original[index:]
