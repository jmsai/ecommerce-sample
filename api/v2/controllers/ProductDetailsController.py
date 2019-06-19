from api.v1.common import get_response
from api.v2.models.ProductModel import ProductModel
from api.v2.views.ProductView import ProductView
from error.model import NotFoundError
from error.model import BadRequestError
from error.model import UnprocessableEntityError
from error.model import ResourceAlreadyExistError
from error.view import ErrorView

from flask import request
from flask_restful import Resource

Product = ProductModel()
ProductView = ProductView()
ErrorView = ErrorView()


class ProductDetailsController(Resource):
    def get(self, _id):
        products = Product.find_all()

        if products is None:
            error = NotFoundError("Results")
            display = ErrorView.display(error)
            return get_response(display, 404)

        product = Product.find_by(products, _id)

        if product is None:
            error = NotFoundError("Product")
            display = ErrorView.display(error)
            return get_response(display, 404)

        discount_rate = product["discount_rate"]
        product["discount"] = Product.get_percentage(discount_rate)
        original_price = product["original_price"]
        product["price"] = Product.get_price(discount_rate, original_price)

        display = ProductView.display_details(product)
        return get_response(display, 200)
