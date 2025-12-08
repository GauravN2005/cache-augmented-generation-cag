def is_valid_output(text: str) -> bool:
    """
    Simple validation:
    - Output must not be empty
    - Output should be readable English
    """
    if text is None:
        return False
    if len(text.strip()) < 3:
        return False
    if "�" in text:  # broken text
        return False
    return True
