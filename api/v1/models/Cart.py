from api.v1.common import Common

carts = []
Common = Common()


class Cart:
    def __init__(self, customer_id='', items=''):
        self.customer_id = customer_id
        self.items = items
        self.tax_rate = 0.04
        self.shipping_fee = 50.00
        self.sub_total = 0.00
        self.number_of_items = 0
        self.tax_amount = 0
        self.total = 0

    def add(self, new_cart):
        if new_cart:
            carts.append(new_cart)
            return new_cart

        return None

    def find_all(self):
        return carts

    def find_by_customer(self, customer_id):
        carts = self.find_all()
        customer = Common.filter_result('customer_id', customer_id, carts)
        return next(customer, None)

    def find_by_item(self, item_id, cart):
        item = Common.filter_result('item_id', item_id, cart["items"])
        return next(item, None)

    def add_item(self, cart, data):
        items = cart['items']
        for item in items:
            if item['item_id'] == data['item_id']:
                item['quantity'] += data['quantity']

                if item['quantity'] == 1:
                    item['sub_total'] = item['price']

                item['sub_total'] = item['price'] * item['quantity']
                return cart
        items.append(data)
        return cart

    def edit_item(self, cart, item_id, data):
        item = self.find_by_item(item_id, cart)

        if item:
            if item['quantity'] < 1:
                return self.remove_item(cart, item_id)

            item['quantity'] += data['quantity']
            item["number_of_items"] = self.count_all_items(cart)

            return cart

        return None

    def remove_item(self, cart, item_id):
        item = self.find_by_item(item_id, cart)

        if item:
            cart["items"].remove(item)
            cart["sub_total"] = 0.00
            cart["number_of_items"] = 0
            cart["tax_amount"] = 0.00
            cart["total"] = 0.00
            return cart

        return None

    def count_all_items(self, cart):
        if cart:
            for item in cart["items"]:
                cart["number_of_items"] += item["quantity"]
            return cart["number_of_items"]

        return None

    def get_sub_total(self, cart):
        if cart:
            for item in cart["items"]:
                cart["sub_total"] += item["sub_total"]
            return cart["sub_total"]

        return None

    def get_tax_amount(self, cart):
        if cart:
            return cart["sub_total"] * cart["tax_rate"]
        return None

    def get_total(self, cart):
        if cart:
            sub_total = cart["sub_total"]
            return sub_total + cart["shipping_fee"] + cart["tax_amount"]

        return None
