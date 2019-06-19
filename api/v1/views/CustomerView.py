class CustomerView:
    def display(self, customer):
        return {
            "full_name": customer["full_name"],
            "email": customer["email"],
            "phone_number": customer["phone_number"],
            "billing_address": customer["billing_address"],
            "shipping_address": customer["shipping_address"]
        }

    def display_credentials(self, user):
        return {
            "_id": user["customer_id"],
            "email": user["email"],
            "password": user["password"]
        }
