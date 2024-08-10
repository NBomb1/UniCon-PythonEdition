def checkInteger(number: str) -> bool:
    """returns True if number is integer"""
    try:
        int(number)
        return True
    except ValueError:
        return False
