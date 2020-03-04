class EvernoteMasterError(Exception):
    """ Base class for exceptions in this module. """
    def __init__(self, message):
        self.message = message


class NotFoundNotebookError(EvernoteMasterError):
    def __init__(self, name=None, guid=None, message=None):
        self.name = name
        self.guid = guid
        self.message = f'Notebook was not found. Name: {self.name}' if not message else ''

        EvernoteMasterError.__init__(self, self.message)
