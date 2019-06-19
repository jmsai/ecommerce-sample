from api.v1.common import Common

import bcrypt
from validate_email import validate_email

customers = []
Common = Common()


class Customer:
    def __init__(self, email='', password='', first_name='',
                 middle_name='', last_name='', phone_number='',
                 billing_address='', shipping_address=''):
        self.customer_id = Common.generate_id()
        self.email = email
        self.password = password
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.billing_address = billing_address
        self.shipping_address = shipping_address
        self.middle_initial = ''
        self.full_name = ''

    def hash(self, _password):
        return bcrypt.hashpw(_password.encode(), bcrypt.gensalt(8))

    def is_password_valid(self, _password, password):
        hashed = self.hash(_password)

        if bcrypt.checkpw(password.encode(), hashed):
            return True

        return False

    def is_email_valid(self, _email):
        email = validate_email(_email)

        if email:
            return True

        return False

    def find_all(self):
            return customers

    def find_by(self, _id):
        customers = self.find_all()
        if customers:
            customer = Common.filter_result('customer_id', _id, customers)
            return next(customer, None)
        return None

    def find_by_email(self, _email):
        customers = self.find_all()
        if customers:
            customer = Common.filter_result('email', _email, customers)
            return next(customer, None)
        return None

    def add(self, new_customer):
        if new_customer:
            customers.append(new_customer)
            return new_customer

        return None

    def get_middle_initial(self, customer):
        if customer:
            return '{}.'.format(customer["middle_name"][0])

        return None

    def get_full_name(self, customer):
        if customer:
            first_name = customer["first_name"]
            middle_initial = customer["middle_initial"]
            last_name = customer["last_name"]
            return '{} {} {}'.format(first_name, middle_initial, last_name)

        return None

    def get_address(self, street, city,
                    state, zip_code, country):
        return {
            "street": street,
            "city": city,
            "state": state,
            "zip_code": zip_code,
            "country": country
        }
