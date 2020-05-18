class FingerError(Exception):
    """
    Custom error for palec' application.
    """
    def __init__(self, msg="invalid data dimension"):
        self.__super__()
        self.msg = msg

    def __repr__(self):
        return "!" + self.msg
