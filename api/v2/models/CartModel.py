from api.v2.common import Common
from api.v1.models.Cart import Cart

Common = Common()


class CartModel(Cart):
    def __init__(self, customer_id='', items=''):
        super().__init__(customer_id, items)
        self._id = Common.generate_id()
