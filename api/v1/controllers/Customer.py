from api.v1.common import get_response
from api.v1.models.Customer import Customer
from api.v1.views.CustomerView import CustomerView
from error.model import NotFoundError
from error.model import BadRequestError
from error.model import UnprocessableEntityError
from error.model import ResourceAlreadyExistError
from error.view import ErrorView

from flask import request
from flask_restful import Resource, reqparse

model = Customer()
view = CustomerView()
ErrorView = ErrorView()


class CustomerController(Resource):
    def get(self, _id):
            customer = model.find_by(_id)

            if customer is not None:
                customer["middle_initial"] = model.get_middle_initial(customer)
                customer["full_name"] = model.get_full_name(customer)

                display = view.display(customer)
                return get_response(display, 200)

            if customer is None:
                display = ErrorView.display(NotFoundError("Customer"))
                return get_response(display, 404)


class SignupController(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="Email is required")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="Password is required")
    parser.add_argument('first_name',
                        type=str,
                        required=True,
                        help="This field cannot be blank")
    parser.add_argument('middle_name',
                        type=str)
    parser.add_argument('last_name',
                        type=str,
                        required=True,
                        help="This field cannot be blank")

    def post(self):
        data = SignupController.parser.parse_args()

        valid_email = model.is_email_valid(data["email"])

        if valid_email:
            customer = model.find_by_email(data["email"])

            if customer is not None:
                error = ResourceAlreadyExistError("User")
                display = ErrorView.display(error)
                return get_response(display, 409)

            new_customer = Customer(
                                    data["email"],
                                    data["password"],
                                    data["first_name"],
                                    data["middle_name"],
                                    data["last_name"]
                                    ).__dict__

            state = model.add(new_customer)

            if state is not None:
                display = view.display_credentials(new_customer)
                return get_response(display, 201)

        error = UnprocessableEntityError()
        display = ErrorView.display(error)
        return get_response(display, 422)


class LoginController(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="Email is required")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="Password is required")

    def post(self):
        data = LoginController.parser.parse_args()

        customer = model.find_by_email(data["email"])

        if customer is not None:
            input_password = data["password"]
            password = customer['password']

            valid_password = model.is_password_valid(input_password, password)

            if valid_password:
                display = view.display_credentials(customer)
                return get_response(display, 200)

        if customer is None or not valid_password:
            error = BadRequestError("Login failed",
                                    "Invalid email/password")
            display = ErrorView.display(error)
            return get_response(display, 400)

        error = UnprocessableEntityError()
        display = ErrorView.display(error)
        get_response(display, error)
