# import ssi_fc_trading
from ssi_fc_data import fc_md_client, model
import config
from datetime import datetime, timedelta


class ScrapStockPrices:

  def __init__(self):
    self._client = fc_md_client.MarketDataClient(config)
    self._end_date = datetime.now()
    self._start_date = self._end_date - timedelta(days=config.date_interval)
    self._start_date = self._start_date.strftime("%d/%m/%Y")
    self._end_date = self._end_date.strftime("%d/%m/%Y")

  def _get_data(self, symbol, market, page):
    req = model.daily_stock_price(symbol=symbol, market=market, fromDate=self._start_date, toDate=self._end_date, pageIndex=page, pageSize=config.batch_size)
    return self._client.daily_stock_price(config, req)

  def _add_datalake(self, item):
    config.stock_price_collection.update_one(
      {"TradingDate": item['TradingDate'], "Symbol": item["Symbol"]},
      {"$set":{**item}},
      upsert=True
    )

  def scrap(self, limit=5):
    companies = config.companies_collection.find({})
    symbols = [ (c['Symbol'], c['Market']) for c in companies ][0:limit]
    print("Start scraping stock price by symbols: ", symbols)
    print("From date: ", self._start_date)
    print("To date: ", self._end_date)
    for symbol in symbols:
      print(f"Scraping stock price by symbols: {symbol}")
      page = 1
      status = "Success"
      while status == "Success":
        response = self._get_data(symbol[0], symbol[1], page)

        page = page + 1
        status = response['status']
        if status != "Success":
          print(f"Failed to get data: {response['message']}")
          break

        data = response['data']  
        if data is not None and len(data) > 0:
          for item in data:
            self._add_datalake(item)

          print(f"Inserted {len(data)} data in {symbol}")


ScrapStockPrices().scrap()