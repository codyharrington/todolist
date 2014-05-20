__author__ = 'cody'

class AlreadyExistsException(Exception):
    pass

class NotFoundException(Exception):
    pass

class UnauthorisedException(Exception):
    pass

class AuthenticationFailureException(Exception):
    pass

class ForbiddenException(Exception):
    pass

class MalformedJSONException(Exception):
    pass

class ExpectedJSONObjectException(Exception):
    pass

class NoDataException(Exception):
    pass

class InsufficientFieldsException(Exception):
    pass

class InternalServerErrorException(Exception):
    pass