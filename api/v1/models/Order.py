from api.v1.common import Common

from datetime import datetime as Date

orders = []
Common = Common()


class Order:
    def __init__(self, customer_name='', phone_number='', shipping_address='',
                 billing_address='', delivery_date='', payment_method='',
                 payment_date='', shipping_fee='', tax_rate='',
                 items='', customer_id=''):
        self.order_id = Common.generate_id()
        self.transaction_date = Common.set_date(Date.today())
        self.customer_name = customer_name
        self.phone_number = phone_number
        self.shipping_address = shipping_address
        self.billing_address = billing_address
        self.tracking_id = Common.generate_tracking_number()
        self.delivery_status = "Pending"
        self.delivery_date = delivery_date
        self.payment_date = payment_date
        self.payment_status = "Pending"
        self.payment_method = payment_method
        self.shipping_fee = shipping_fee
        self.tax_rate = tax_rate
        self.items = items
        self.customer_id = customer_id
        self.sub_total = 0.00
        self.number_of_items = 0

    def find_all(self):
        return orders

    def find_by_customer(self, _id):
        orders = self.find_all()
        customer_orders = Common.filter_result('customer_id', _id, orders)
        return list(customer_orders)

    def search_by(self, customer_id, order_id):
        customer_orders = self.find_by_customer(customer_id)
        order = Common.filter_result('order_id', order_id, customer_orders)
        return next(order, None)

    def find_by(self, _id):
        orders = self.find_all()
        order = Common.filter_result('order_id', _id, orders)
        return next(order, None)

    def add(self, new_order):
        if new_order:
            orders.append(new_order)
            return new_order

        return None

    def edit(self, orders, order_id, data):
        if orders is not None or orders:
            order = self.find_by(order_id)

            if order is not None:
                order.update(data)

            return order

        return None

    def count_all_items(self, order):
        if order is not None:
            for item in order["items"]:
                order["number_of_items"] += item["quantity"]
            return order["number_of_items"]

        return None

    def get_sub_total(self, order):
        if order is not None:
            for item in order["items"]:
                order["sub_total"] += (item["price"] * item["quantity"])
            return order['sub_total']

        return None

    def get_tax_amount(self, order):
        if order is not None:
            return order["sub_total"] * order["tax_rate"]

        return None

    def get_total(self, order):
        if order is not None:
            sub_total = order["sub_total"]
            return sub_total + order["shipping_fee"] + order["tax_amount"]

        return None
