from api.v1.common import get_response
from api.v1.models.Order import Order
from api.v1.views.OrderView import OrderView
from error.model import NotFoundError
from error.model import BadRequestError
from error.model import UnprocessableEntityError
from error.model import ResourceAlreadyExistError
from error.view import ErrorView

from flask import request
from flask_restful import Resource, reqparse

model = Order()
view = OrderView()
ErrorView = ErrorView()


class OrderController(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('customer_name',
                        type=str,
                        required=True,
                        help="This field cannot be blank")
    parser.add_argument('phone_number',
                        type=str,
                        required=True,
                        help="This field cannot be blank")
    parser.add_argument('shipping_address',
                        type=dict,
                        required=True,
                        help="This field cannot be blank",
                        action='append')
    parser.add_argument('billing_address',
                        type=dict,
                        required=True,
                        help="This field cannot be blank",
                        action='append')
    parser.add_argument('delivery_date',
                        type=str,
                        required=True,
                        help="This field cannot be blank")
    parser.add_argument('payment_date',
                        type=str,
                        required=True,
                        help="This field cannot be blank")
    parser.add_argument('payment_method',
                        type=str,
                        required=True,
                        help="This field cannot be blank")
    parser.add_argument('shipping_fee',
                        type=float,
                        required=True,
                        help="This field cannot be blank")
    parser.add_argument('tax_rate',
                        type=float,
                        required=True,
                        help="This field cannot be blank")
    parser.add_argument('items',
                        type=dict,
                        required=True,
                        action='append')

    def get(self, customer_id):
        orders = model.find_by_customer(customer_id)

        if orders is not None:
            display = view.display_list(orders)
            return get_response(display, 200)

        if orders is None:
            error = NotFoundError("Results")
            display = ErrorView.display(error)
            return get_response(display, 404)

    def post(self, customer_id):
        data = OrderController.parser.parse_args()

        new_order = Order(
                            data["customer_name"],
                            data["phone_number"],
                            data["shipping_address"],
                            data["billing_address"],
                            data["delivery_date"],
                            data["payment_method"],
                            data["payment_date"],
                            data["shipping_fee"],
                            data["tax_rate"],
                            data["items"],
                            customer_id
                        ).__dict__

        state = model.add(new_order)

        if state is not None:
            new_order["sub_total"] = model.get_sub_total(new_order)
            new_order["tax_amount"] = model.get_tax_amount(new_order)
            new_order["number_of_items"] = model.count_all_items(new_order)
            new_order["total"] = model.get_total(new_order)

            display = view.display_details(new_order)
            return get_response(display, 201)

        if state is None:
            error = UnprocessableEntityError()
            display = ErrorView.display(error)
            return get_response(display, 422)


class OrderDetailsController(Resource):
    def get(self, customer_id, order_id):
        order = model.find_by(order_id)

        if order is not None:
            display = view.display_details(order)
            return get_response(display, 200)

        if order is None:
            error = NotFoundError("Order Number")
            display = ErrorView.display(error)
            return get_response(display, 404)

    def put(self, customer_id, order_id):
        data = request.get_json()
        orders = model.find_all()
        order = model.edit(orders, order_id, data)

        if order is not None:
            display = view.display_details(order)
            return get_response(display, 200)

        if not order:
            error = NotFoundError("Order Number")
            display = ErrorView.display(error)
            return get_response(display, 404)

        if order is None:
            error = UnprocessableEntityError()
            display = ErrorView.display(error)
            return get_response(display, 422)
