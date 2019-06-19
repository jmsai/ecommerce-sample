from api.v1.common import get_response
from api.v2.models.CartModel import CartModel
from api.v2.views.CartView import CartView
from api.v1.controllers.Cart import CartController as CartController_v1
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


class CartController(CartController_v1):
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
    parser.add_argument('reviews_count',
                        type=int,
                        required=True,
                        help="This field cannot be blank")
    parser.add_argument('rating',
                        type=float,
                        required=True,
                        help="This field cannot be blank")
    parser.add_argument('currency',
                        type=str,
                        required=True,
                        help="This field cannot be blank")

    def post(self, customer_id):
        cart = Cart.find_by_customer(customer_id)

        if cart is not None:
            error = ResourceAlreadyExistError("Cart")
            display = ErrorView.display(error)
            return get_response(display, 409)

        new_cart = CartModel(customer_id, []).__dict__

        state = Cart.add(new_cart)

        if state:
            new_cart["sub_total"] = Cart.get_sub_total(new_cart)
            new_cart["number_of_items"] = Cart.count_all_items(new_cart)
            new_cart["tax_amount"] = 0
            new_cart["total"] = 0

            return get_response(new_cart, 201)

    def put(self, customer_id):
        data = CartController.parser.parse_args()
        cart = Cart.find_by_customer(customer_id)

        if cart:
            item = Cart.add_item(cart, data)

            if item:
                cart["sub_total"] = Cart.get_sub_total(cart)
                cart["number_of_items"] = Cart.count_all_items(cart)
                cart["tax_amount"] = Cart.get_tax_amount(cart)
                cart["total"] = Cart.get_total(cart)

                display = CartView.display_cart(cart)
                return get_response(display, 200)

        if cart is None:
            error = NotFoundError("Cart")
            display = ErrorView.display(error)
            return get_response(display, 404)

        error = UnprocessableEntityError()
        display = ErrorView.display(error)
        return get_response(display, 422)
