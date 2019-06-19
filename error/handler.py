from api.v1.common import get_response
from error.model import NotFoundError
from error.model import InternalServerError
from error.model import AccessDeniedError
from error.model import UnauthorizedError
from error.view import ErrorView

ErrorView = ErrorView()


def handle_page_not_found(e):
    view = ErrorView.display(NotFoundError("Page"))
    return get_response(view, 404)


def handle_internal_server_error(e):
    view = ErrorView.display(InternalServerError())
    return get_response(view, 500)


def handle_access_denied_error(e):
    view = ErrorView.display(AccessDeniedError())
    return get_response(view, 401)


def handle_unauthorized_error(e):
    view = ErrorView.display(UnauthorizedError())
    return get_response(view, 403)
