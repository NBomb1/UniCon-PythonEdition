class FileTransfer(Exception):
    class NoConnectionException(Exception):
        def __init__(self, *args, **kwargs):  # real signature unknown
            pass

    class ReceiverError(Exception):
        def __init__(self, *args, **kwargs):  # real signature unknown
            pass

    class ModuleDoesNotExistsException(Exception):
        def __init__(self, *args, **kwargs):  # real signature unknown
            pass
