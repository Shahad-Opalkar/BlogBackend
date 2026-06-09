class APIError(Exception):

    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code


class NotFoundError(APIError):

    def __init__(self, message="Resource not found"):
        super().__init__(message, 404)


class ForbiddenError(APIError):

    def __init__(self, message="Forbidden"):
        super().__init__(message, 403)


class BadRequestError(APIError):

    def __init__(self, message="Bad request"):
        super().__init__(message, 400)