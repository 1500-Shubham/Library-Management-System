## Throw an exception when and only when function preconditions (assumptions about arguments) are broken.

class ValidationError(Exception):
    pass

class ObjectAlreadyExist(Exception):
    pass

class LanguageExists(Exception):
    ''''''
    def __init__(self, message, *args, **kwargs):
        self.code = 404 # Precondition Failed
        self.message = "Language Already Exist, Enter New Language"
        Exception.__init__(self, *args, **kwargs)

class NothingToParse(Exception):
    ''''''
    def __init__(self, message, *args, **kwargs):
        self.code = 415 # Precondition Failed
        self.message = message
        Exception.__init__(self, *args, **kwargs)
