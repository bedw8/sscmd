
class NotAcceptableError(Exception):
    def __init__(self, message):
        self.expression = 'Not Acceptable'
        self.message = message
        super().__init__(self.message)

class NotFoundError(Exception):
    def __init__(self, objecttype):
        self.expression = objecttype + ' not found'
        self.message = objecttype + ' not found'
        super().__init__(self.message)


class IncompleteQuestionnaireIdError(TypeError):
    def __init__(self):
        self.expression = 'Invalid questionnaire id'
        self.message = 'Both questionnaire guid and version number must be specified'
        super().__init__(self.message)


class UnauthorizedError(Exception):
    def __init__(self):
        self.expression = 'Unauthorized'
        self.message = 'Either username or password were not provided or wrong'
        super().__init__(self.message)


class ForbiddenError(Exception):
    def __init__(self):
        self.expression = 'Forbidden'
        self.message = 'User is not authorized to perform this action'
        super().__init__(self.message)

