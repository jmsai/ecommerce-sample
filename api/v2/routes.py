from api.v2.controllers.SignupController import SignupController
from api.v2.controllers.LoginController import LoginController
from api.v2.controllers.CustomerController import CustomerController
from api.v2.controllers.ProductController import ProductController
from api.v2.controllers.ProductDetailsController import ProductDetailsController
from api.v2.controllers.CartController import CartController
from api.v2.controllers.ItemController import ItemController
from api.v2.controllers.OrderController import OrderController
from api.v2.controllers.OrderDetailsController import OrderDetailsController

from flask import Blueprint
from flask_restful import Api
from os import path
import sys

sys.path.append(path.join(path.dirname(__file__), '..'))

api_v2 = Blueprint('api_v2', __name__)
api = Api(api_v2)

CUSTOMERS_ROUTE = '/customers'
PRODUCTS_ROUTE = '/products'
CARTS_ROUTE = f'{CUSTOMERS_ROUTE}/<customer_id>/carts'
ITEMS_ROUTE = f'{CARTS_ROUTE}/<cart_id>/items'
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
api.add_resource(ItemController, f'{ITEMS_ROUTE}/<item_id>')

# Order Routes
api.add_resource(OrderController, f'{ORDERS_ROUTE}')
api.add_resource(OrderDetailsController, f'{ORDERS_ROUTE}/<order_id>')
