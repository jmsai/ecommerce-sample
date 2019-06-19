from api.v1.common import Common as Common_v1


class Common(Common_v1):
    def get_tax(self, rate):
        percentage = self.get_whole_number(rate * 100)
        return "{}%".format(percentage)

    def get_discount(self, rate):
        percentage = self.get_whole_number(rate)
        return "{}% off".format(percentage)

    def get_currency(self, currency, value):
        return '{0} {1:.2f}'.format(currency, value)
