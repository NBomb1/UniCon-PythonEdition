def checkYaml() -> bool:
    """
    This function checks if the 'yaml' module is installed in the current Python environment.

    Parameters:
    None

    Returns:
    bool: True if the 'yaml' module is installed, False otherwise.
    """
    try:
        import yaml
    except ModuleNotFoundError:
        return False
    return True


def checkPywin32() -> bool:
    try:
        import win32gui
    except ModuleNotFoundError:
        return False
    return True


def checkPyUAC() -> bool:
    try:
        import pyuac
    except ModuleNotFoundError:
        return False
    return True
