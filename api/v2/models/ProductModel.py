from api.v1.models.Product import Product

import json


class ProductModel(Product):
    def find_all(self):
        with open("seedv2.json", "r") as seed_file:
            data = json.load(seed_file)
            return data["products"]

    def get_percentage(self, discount_rate):
        return discount_rate * 100

    def get_price(self, discount_rate, original_price):
        discount_price = original_price * discount_rate
        return original_price - discount_price

    def get_feed(self, products):
        for product in products:
            original_price = product["original_price"]
            discount_rate = product["discount_rate"]

            product["discount"] = self.get_percentage(discount_rate)
            product["price"] = self.get_price(discount_rate, original_price)

        return products
