class FingerError(Exception):
    """
    Custom error for palec' application.
    """
    def __init__(self, msg="invalid data dimension"):
        super().__init__()
        self.msg = msg

    def __repr__(self):
        return "!" + self.msg
