import uuid
import json
from datetime import datetime as Date
from flask import Response


class Common:
    def filter_result(self, key, to_find, table):
        return filter(lambda data: data[key] == to_find, table)

    def generate_id(self):
        return str(uuid.uuid4().fields[-1])[:8]

    def generate_tracking_number(self):
        return str(uuid.uuid4().fields[-1])[:12]

    def get_currency(self, value):
        return "Php {:,.2f}".format(value)

    def get_whole_number(self, number):
        return int(number)

    def get_discount(self, rate):
        percentage = self.get_whole_number(rate)
        return "-{}%".format(percentage)

    def get_tax(self, rate):
        percentage = self.get_whole_number(rate)
        return "{}%".format(percentage)

    def set_date(self, date):
        return date.strftime("%a %d %b %Y")

    def get_date(self, str):
        date_object = Date.strptime(str, "%Y-%m-%d %H:%M:%S.%f")
        return self.set_date(date_object)


def get_response(obj, status):
    data = json.dumps(obj)
    return Response(data, status, mimetype='application/json')
