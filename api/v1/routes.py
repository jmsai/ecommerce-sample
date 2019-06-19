from api.v1.controllers.Customer import SignupController
from api.v1.controllers.Customer import LoginController
from api.v1.controllers.Customer import CustomerController
from api.v1.controllers.Product import ProductController
from api.v1.controllers.Product import ProductDetailsController
from api.v1.controllers.Cart import CartController
from api.v1.controllers.Cart import ItemController
from api.v1.controllers.Order import OrderController
from api.v1.controllers.Order import OrderDetailsController

from flask import Blueprint
from flask_restful import Api

api_v1 = Blueprint('api_v1', __name__)
api = Api(api_v1)

CUSTOMERS_ROUTE = '/customers'
PRODUCTS_ROUTE = '/products'
CARTS_ROUTE = f'{CUSTOMERS_ROUTE}/<customer_id>/items'
ORDERS_ROUTE = f'{CUSTOMERS_ROUTE}/<customer_id>/orders'

# Customer Routes
api.add_resource(SignupController, '/signup')
api.add_resource(LoginController, '/login')
api.add_resource(CustomerController, f'{CUSTOMERS_ROUTE}/<_id>')

# Product Routes
api.add_resource(ProductController, '/', f'{PRODUCTS_ROUTE}')
api.add_resource(ProductDetailsController, f'{PRODUCTS_ROUTE}/<_id>')

# Cart Routes
api.add_resource(CartController, f'{CARTS_ROUTE}')
api.add_resource(ItemController, f'{CARTS_ROUTE}/<item_id>')

# Order Routes
api.add_resource(OrderController, f'{ORDERS_ROUTE}')
api.add_resource(OrderDetailsController, f'{ORDERS_ROUTE}/<order_id>')
