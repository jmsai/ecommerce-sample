from api.v2.common import Common

Common = Common()


class CartView:
    def display_cart(self, cart):
        itemData = list()
        items = cart["items"]

        for item in items:
            reviews_count = Common.get_whole_number(item["reviews_count"])
            quantity = Common.get_whole_number(item["quantity"])
            discount = Common.get_discount(item["discount_rate"])
            sub_total = Common.get_currency('Php', item["sub_total"])
            original_price = Common.get_currency('Php', item["original_price"])
            price = Common.get_currency('Php', item["price"])

            data = {
                "name": item["name"],
                "description": item["description"],
                "brand": item["brand"],
                "images": item["images"],
                "rating": item["rating"],
                "reviews_count": reviews_count,
                "quantity": quantity,
                "original_price": original_price,
                "discount": discount,
                "price": price,
                "sub_total": sub_total
            }

            itemData.append(data)

        number_of_items = Common.get_whole_number(cart["number_of_items"])
        tax_rate = Common.get_tax(cart["tax_rate"])
        tax_amount = Common.get_currency("Php", cart["tax_amount"])
        total = Common.get_currency("Php", cart["total"])
        sub_total = Common.get_currency("Php", cart["sub_total"])
        shipping_fee = Common.get_currency("Php", cart["shipping_fee"])

        response = {
            "items_count": len(items),
            "items": itemData,
            "order_summary": {
                "number_of_items": number_of_items,
                "sub_total": sub_total,
                "shipping_fee": shipping_fee,
                "tax_rate": tax_rate,
                "tax_amount": tax_amount,
                "total": total
            }
        }

        return response
