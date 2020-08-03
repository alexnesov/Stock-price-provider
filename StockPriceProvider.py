import pandas as pd
from bs4 import BeautifulSoup
import requests
import logging

csvfile = pd.read_csv('Stock_indices_NASDAQ.csv') # we assume that the csv is in the same directory as the script
list_of_symbols = csvfile['Symbol']

# change this parameter to select how many stocks you want to DL for the sake of the exercise 
n_first_stocks = 15


class PricesProvider:
    def __init__(self, list_of_symbols):
        self.list_of_symbols = list_of_symbols[:n_first_stocks]
        self.stocks = []
        self.urls = []

    def get_urls(self):                                                          #1
        for i in self.list_of_symbols:
            g = "https://finance.yahoo.com/quote/{i}?p={i}&.tsrc=fin-srch".format(i=i)
            self.urls.append(g)

    def get_prices(self):                                                         #2
        for (ticker, b) in zip(enumerate(self.list_of_symbols), self.urls):
            try:
                print(f"Starting a new HTTPS connection for {ticker[1]}")
                print(b)
                request = requests.get(f"{b}")
                content = request.content
                soup = BeautifulSoup(content, "html.parser")
                element = str(soup.find("span", {"class": "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"}))

                # We could use regex to find the price, but this method is more elegant in my opinion to find the price
                # in the "element" string
                string_start = '>'
                string_end = '</span>'
                price = float(element[element.find(string_start)+len(string_start):element.rfind(string_end)])

                stock = {
                'ticker': ticker,
                'price': price
                 }
                self.stocks.append(stock)
                print(f"Downloading the quote for: '{ticker[1]}' from yahoofinance.com")
                print(f"{ticker[0]} - Price for {ticker[1]} is : {price}$")
                logging.debug(f"Downloading the quote for: '{ticker[1]}' from yahoofinance.com")
            except:
                print(f"The following ticker: {ticker[1]} wasn't  found on YF")
                print("Trying next ticker...")
                logging.debug(f"The following ticker: {ticker[1]} wasn't  found on YF")


if __name__ == "__main__":
    nasdaq = PricesProvider(list_of_symbols)
    nasdaq.get_urls()
    nasdaq.urls
    nasdaq.get_prices()

    df = pd.DataFrame.from_dict(nasdaq.stocks)
    rows = df.ticker
    df.ticker = [x[1] for x in rows]



