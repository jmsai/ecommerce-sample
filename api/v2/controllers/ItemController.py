from api.v1.common import get_response
from api.v2.models.CartModel import CartModel
from api.v2.views.CartView import CartView
from error.model import NotFoundError
from error.model import BadRequestError
from error.model import UnprocessableEntityError
from error.model import ResourceAlreadyExistError
from error.view import ErrorView

from flask import request
from flask_restful import Resource, reqparse

Cart = CartModel()
CartView = CartView()
ErrorView = ErrorView()


class ItemController(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('quantity',
                        type=int,
                        required=True,
                        help="This field cannot be blank")

    def put(self, cart_id, customer_id, item_id):
        data = ItemController.parser.parse_args()
        cart = Cart.find_by_customer(customer_id)

        if cart:
            cart["sub_total"] = Cart.get_sub_total(cart)
            cart["number_of_items"] = Cart.count_all_items(cart)
            cart["tax_amount"] = Cart.get_tax_amount(cart)
            cart["total"] = Cart.get_total(cart)

            item = Cart.edit_item(cart, item_id, data)

            if item:
                display = CartView.display_cart(cart)
                return get_response(display, 200)

        if cart is None:
            error = NotFoundError("Cart")
            display = ErrorView.display(error)
            return get_response(display, 404)

        error = UnprocessableEntityError()
        display = ErrorView.display(error)
        return get_response(display, 422)

    def delete(self, cart_id, customer_id, item_id):
        cart = Cart.find_by_customer(customer_id)

        if cart:

            cart["sub_total"] = Cart.get_sub_total(cart)
            cart["number_of_items"] = Cart.count_all_items(cart)
            cart["tax_amount"] = Cart.get_tax_amount(cart)
            cart["total"] = Cart.get_total(cart)

            item = Cart.remove_item(cart, item_id)

            if item:
                display = CartView.display_cart(cart)
                return get_response(display, 200)

        if cart is None:
            error = NotFoundError("Cart")
            display = ErrorView.display(error)
            return get_response(display, 404)

        error = UnprocessableEntityError()
        display = ErrorView.display(error)
        return get_response(display, 422)
