from api.v1.common import get_response
from api.v1.models.Cart import Cart
from api.v1.views.CartView import CartView
from error.model import NotFoundError
from error.model import UnprocessableEntityError
from error.model import ResourceAlreadyExistError
from error.view import ErrorView

from flask import request
from flask_restful import Resource, reqparse

model = Cart()
view = CartView()
ErrorView = ErrorView()


class CartController(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('item_id',
                        type=str,
                        required=True,
                        help="This field cannot be blank")
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be blank")
    parser.add_argument('description',
                        type=str,
                        required=True,
                        help="This field cannot be blank")
    parser.add_argument('brand',
                        type=str,
                        required=True,
                        help="This field cannot be blank")
    parser.add_argument('model',
                        type=str,
                        required=True,
                        help="This field cannot be blank")
    parser.add_argument('warranty_period',
                        type=str,
                        required=True,
                        help="This field cannot be blank")
    parser.add_argument('warranty_type',
                        type=str,
                        required=True,
                        help="This field cannot be blank")
    parser.add_argument('quantity',
                        type=int,
                        required=True,
                        help="This field cannot be blank")
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be blank")
    parser.add_argument('original_price',
                        type=float,
                        required=True,
                        help="This field cannot be blank")
    parser.add_argument('discount_rate',
                        type=float,
                        required=True,
                        help="This field cannot be blank")
    parser.add_argument('sub_total',
                        type=float,
                        required=True,
                        help="This field cannot be blank")
    parser.add_argument('images',
                        type=str,
                        required=True,
                        action='append')

    def get(self, customer_id):
        cart = model.find_by_customer(customer_id)

        if cart:
            display = view.display_cart(cart)
            return get_response(display, 200)

        if cart is None:
            error = NotFoundError("Cart")
            display = ErrorView.display(error)
            return get_response(display, 404)

    def post(self, customer_id):
        cart = model.find_by_customer(customer_id)

        if cart is None or not cart:
            new_cart = Cart(customer_id, []).__dict__

            state = model.add(new_cart)

            if state:
                new_cart["sub_total"] = model.get_sub_total(new_cart)
                new_cart["number_of_items"] = model.count_all_items(new_cart)
                new_cart["tax_amount"] = 0
                new_cart["total"] = 0

                return get_response(new_cart, 201)

        if cart is not None:
            error = ResourceAlreadyExistError("Cart")
            display = ErrorView.display(error)
            return get_response(display, 409)

        error = UnprocessableEntityError()
        display = ErrorView.display(error)
        return get_response(display, 422)

    def put(self, customer_id):
        data = CartController.parser.parse_args()
        cart = model.find_by_customer(customer_id)

        if cart:
            item = model.add_item(cart, data)

            if item:
                cart["sub_total"] = model.get_sub_total(cart)
                cart["number_of_items"] = model.count_all_items(cart)
                cart["tax_amount"] = model.get_tax_amount(cart)
                cart["total"] = model.get_total(cart)

                display = view.display_cart(cart)
                return get_response(display, 200)

        if cart is None:
            error = NotFoundError("Cart")
            display = ErrorView.display(error)
            return get_response(display, 404)

        error = UnprocessableEntityError()
        display = ErrorView.display(error)
        return get_response(display, 422)


class ItemController(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('quantity',
                        type=int,
                        required=True,
                        help="This field cannot be blank")

    def put(self, customer_id, item_id):
        data = ItemController.parser.parse_args()

        cart = model.find_by_customer(customer_id)

        if cart:
            item = model.edit_item(cart, item_id, data)

            if item:
                cart["sub_total"] = model.get_sub_total(cart)
                cart["number_of_items"] = model.count_all_items(cart)
                cart["tax_amount"] = model.get_tax_amount(cart)
                cart["total"] = model.get_total(cart)

                display = view.display_cart(cart)
                return get_response(display, 200)

        if cart is None:
            error = NotFoundError("Cart")
            display = ErrorView.display(error)
            return get_response(display, 404)

        error = UnprocessableEntityError()
        display = ErrorView.display(error)
        return get_response(display, 422)

    def delete(self, customer_id, item_id):
        cart = model.find_by_customer(customer_id)

        if cart is not None:

            item = model.remove_item(cart, item_id)

            if item is not None:
                cart["sub_total"] = model.get_sub_total(cart)
                cart["number_of_items"] = model.count_all_items(cart)
                cart["tax_amount"] = model.get_tax_amount(cart)
                cart["total"] = model.get_total(cart)

                display = view.display_cart(cart)
                return get_response(display, 200)

        if cart is None:
            error = NotFoundError("Cart")
            display = ErrorView.display(error)
            return get_response(display, 404)

        error = UnprocessableEntityError()
        display = ErrorView.display(error),
        return get_response(display, 422)
