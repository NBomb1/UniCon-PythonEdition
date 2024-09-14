def checkInteger(number: any) -> bool:
    """returns True if number is integer"""
    try:
        int(number)
        return True
    except ValueError:
        return False
