from api.v2.common import Common

Common = Common()


class ProductView:
    def display_list(self, products):
        response = list()

        for product in products:
            currency = product["currency"]
            original_price = product["original_price"]
            orig_price = Common.get_currency(currency, original_price)
            discount = Common.get_discount(product["discount"])
            reviews_count = Common.get_whole_number(product["reviews_count"])
            price = Common.get_currency(currency, product["price"])

            data = {
                "id": product["product_id"],
                "name": product["name"],
                "rating": product['rating'],
                "reviews_count": reviews_count,
                "original_price": orig_price,
                "discount": discount,
                "price": price
            }

            response.append(data)

        return response

    def display_details(self, product):
        currency = product["currency"]
        orig_price = Common.get_currency(currency, product["original_price"])
        discount = Common.get_discount(product["discount"])
        reviews_count = Common.get_whole_number(product["reviews_count"])
        price = Common.get_currency(currency, product["price"])

        return {
            "name": product["name"],
            "description": product["description"],
            "product_type": product["product_type"],
            "brand": product["brand"],
            "images": product["images"],
            "rating": product['rating'],
            "reviews_count": reviews_count,
            "original_price": orig_price,
            "discount": discount,
            "price": price
        }
