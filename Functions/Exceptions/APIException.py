class APIException(Exception):
    class ObjectIsNull(Exception):
        def __init__(self, *args, **kwargs):  # real signature unknown
            pass

    class ObjectIsNotNull(Exception):
        def __init__(self, *args, **kwargs):  # real signature unknown
            pass

    class WrongDataGiven(Exception):
        def __init__(self, *args, **kwargs):  # real signature unknown
            pass
