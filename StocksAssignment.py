import datetime


class StocksAssignment(object):

    __slots__ = ["trades", "exchange_table_data"]

    def __init__(self):
        self.trades = {}
        self.exchange_table_data = {
            "TEA": {
                "type": "Common",
                "last_dividend": 1,
                "fixed_dividend": None,
                "value": 100,
            },
            "POP": {
                "type": "Common",
                "last_dividend": 8,
                "fixed_dividend": None,
                "value": 100,
            },
            "ALE": {
                "type": "Common",
                "last_dividend": 23,
                "fixed_dividend": None,
                "value": 60,
            },
            "GIN": {
                "type": "Preferred",
                "last_dividend": 8,
                "fixed_dividend": 0.02,
                "value": 100,
            },
            "JOE": {
                "type": "Common",
                "last_dividend": 13,
                "fixed_dividend": None,
                "value": 250,
            },
        }

    def calculate_dividend(self, symbol, price):

        rule = self.exchange_table_data[symbol]

        if rule["type"] == "Common":
            dividend = rule["last_dividend"] / price
        else:
            dividend = rule["fixed_dividend"] * rule["value"] / price

        return dividend

    def calculate_pe_ratio(self, symbol, price):
        print(price / self.calculate_dividend(symbol=symbol, price=price))
        return price / self.calculate_dividend(symbol=symbol, price=price)

    def calculate_volume_weighted(self, symbol):

        last_five_minutes = int((datetime.datetime.now() - datetime.timedelta(minutes=5)).timestamp())
        total = 0
        quantities = 0
        for trade in self.trades.keys():
            if trade >= last_five_minutes and self.trades[trade]["symbol"] == symbol:
                total = self.trades[trade]["quantity"] * self.trades[trade]["price"]
                quantities += self.trades[trade]["quantity"]
        quantities = 1 if quantities == 0 else quantities
        return total / quantities

    def calculate_gbce(self):

        return sum([trade["price"] for trade in self.trades.values()])

    def add_record(self, symbol, quantity,price, buy=False):

        timestamp = datetime.datetime.now().timestamp()
        self.trades[int(timestamp)] = {
            "symbol": symbol,
            "action": "buy" if buy else "sell",
            "quantity": quantity,
            "price": price
        }

        print("Add with success! \n")

    def validate_symbol(self, symbol):

        if symbol not in self.exchange_table_data:
            raise ValueError("Symbol %s does not exist in table")

        return symbol

    def convert_to_float(self, value):

        try:
            value = float(value)
        except ValueError:
            raise ValueError("Value is not correct")

        return value



class UnitTests(object):

    __slots__ = ["quantity", "symbol", "price", "stocks"]

    def __init__(self, **kwargs):
        self.quantity = kwargs.get("quantity", 1)
        self.symbol = kwargs.get("symbol", "JOE")
        self.price = kwargs.get("quantity", 10)
        self.stocks = StocksAssignment()

    def test_calculate_dividend(self, expected=1.3):
        print("Running calculate_dividend(%s, %s) for Common -> Expected: %s" % (self.symbol, self.price, expected))
        assert self.stocks.calculate_dividend(self.symbol, self.price) == expected

    def test_calculate_dividend_fixed_dividend(self, expected=0.2):
        print("Running calculate_dividend('GIN', %s) for Preferred -> Expected: %s" % (self.price, expected))
        assert self.stocks.calculate_dividend("GIN", self.price) == expected

    def test_calculate_pe_ratio(self, expected=50):
        print("Running calculate_pe_ratio('GIN', %s) for Preferred -> Expected: %s" % (self.price, expected))
        assert self.stocks.calculate_pe_ratio("GIN", self.price) == expected

    def run_all_test(self):

        try:
            self.test_calculate_dividend()
            self.test_calculate_dividend_fixed_dividend()
            self.test_calculate_pe_ratio()

            print("Results tests -> OK")
        except AssertionError as err:
            print("Tests fail: %s" % err)

def userinput():

    print("---------------------------\n")
    print("1 - Calculate dividend\n")
    print("2 - Calculate P/E Ratio\n")
    print("3 - Record trade\n")
    print("4 - Calculate volume weighted stock for the past 5 minutes\n")
    print("5 - Calculate GBCE of all shares\n")
    print("6 - Run Unit Tests\n")
    print("---------------------------\n")


if __name__ == "__main__":
    running = True
    simplestocks = StocksAssignment()
    unit_tests = UnitTests()

    # Loop through the menu
    while running:
        userinput()
        option = input("Select option: \n")

        try:
            if option == "1" or option == "2" or option == "3" or option == "4":
                symbol = input("Select a symbol: ")
                symbol = simplestocks.validate_symbol(symbol)

            if option == "1" or option == "2":
                price = input("Select a price: ")
                price = simplestocks.convert_to_float(price)

            if option == "1":
                print("Dividend --> %s\n" % simplestocks.calculate_dividend(symbol=symbol, price=price))

            elif option == "2":
                print("P/E Ration --> %s\n" % simplestocks.calculate_pe_ratio(symbol=symbol, price=price))

            elif option == "3":
                quantity = input("Select a quantity: ")
                quantity = simplestocks.convert_to_float(quantity)
                buy = input("Is to buy? Yes(y) or No(n)")
                buy = True if buy == "y" else False
                price = input("Select a price: ")
                price = simplestocks.convert_to_float(price)
                simplestocks.add_record(symbol=symbol, quantity=quantity, price =price, buy=buy)

            elif option == "4":
                print("Volume --> %s\n" % simplestocks.calculate_volume_weighted(symbol=symbol))

            elif option == "5":
                print("GBCE of all shares --> %s\n" % simplestocks.calculate_gbce())

            elif option == "6":
                unit_tests.run_all_test()

            else:
                print("Invalid option\n")
        except (KeyError, ValueError, Exception) as error:
            print("Something went wrong. Error: %s", error)
