class HTTPError:
    def __init__(self, title, message, code):
        self.title = title
        self.message = message
        self.code = code


class ClientError(HTTPError):
    def __init__(self, message, code):
        super().__init__("Client Error", message, code)


class ServerError(HTTPError):
    def __init__(self, message, code):
        super().__init__("Server Error", message, code)


class BadRequestError(HTTPError):
    def __init__(self, title, message):
        super().__init__("{} 400".format(title), message, 400)


class UnauthorizedError(HTTPError):
    def __init__(self):
        super().__init__("Unauthorized 401",
                         "Authentication is required for access", 401)


class AccessDeniedError(HTTPError):
    def __init__(self):
        super().__init__("Forbidden 403",
                         "Access is denied with given request", 403)


class NotFoundError(HTTPError):
    def __init__(self, resource):
        super().__init__("Not Found 404",
                         "{} not found".format(resource), 404)


class ResourceAlreadyExistError(HTTPError):
    def __init__(self, resource):
        super().__init__("Conflict 409",
                         "{} already exist".format(resource), 409)


class UnprocessableEntityError(HTTPError):
    def __init__(self):
        super().__init__("Unprocessable Entity",
                         "Failed to perform action due to request error", 422)


class InternalServerError(HTTPError):
    def __init__(self):
        super().__init__("Server currently unavailable",
                         "Request cannot be fulfilled at this moment", 500)
