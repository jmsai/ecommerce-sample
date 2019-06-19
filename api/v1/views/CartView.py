from api.v1.common import Common

Common = Common()


class CartView:
    def display_cart(self, cart):
        itemData = list()
        items = cart["items"]

        for item in items:
            sub_total = Common.get_currency(item["sub_total"])
            price = Common.get_currency(item["price"])
            original_price = Common.get_currency(item["original_price"])
            discount = Common.get_discount(item["discount_rate"])
            quantity = Common.get_whole_number(item["quantity"])

            data = {
                "item_id": item["item_id"],
                "name": item["name"],
                "description": item["description"],
                "brand": item["brand"],
                "model": item["model"],
                "warranty_period": item["warranty_period"],
                "warranty_type": item["warranty_type"],
                "images": item["images"],
                "quantity": quantity,
                "original_price": original_price,
                "discount": discount,
                "price": price,
                "sub_total": sub_total
            }

            itemData.append(data)

        tax_rate = Common.get_tax(cart["tax_rate"] * 100)
        tax_amount = Common.get_currency(cart["tax_amount"])
        total = Common.get_currency(cart["total"])
        sub_total = Common.get_currency(cart["sub_total"])
        number_of_items = Common.get_whole_number(cart["number_of_items"])
        shipping_fee = Common.get_currency(cart["shipping_fee"])

        response = {
            "items_count": len(items),
            "items": itemData,
            "order_summary": {
                "sub_total": sub_total,
                "number_of_items": number_of_items,
                "shipping_fee": shipping_fee,
                "tax_rate": tax_rate,
                "tax_amount": tax_amount,
                "total": total
            }
        }

        return response
