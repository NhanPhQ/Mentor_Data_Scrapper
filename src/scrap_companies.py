# import ssi_fc_trading
from ssi_fc_data import fc_md_client, model
import config

class ScrapCompanies:

  def __init__(self):
    self._client = fc_md_client.MarketDataClient(config)

  def _get_data(self, market, page):
    req = model.securities(market, pageIndex=page, pageSize=config.batch_size)
    return self._client.securities(config, req)

  def _add_datalake(self, item):
    config.companies_collection.update_one(
      {"Market": item['Market'], "Symbol": item['Symbol']},
      {"$set":{**item}},
      upsert=True
    )
  
  def scrap(self, markets: list[str]):
    print("Start scraping companies by markets")
    for market in markets:
      print(f"Scraping companies by market: {market}")
      page = 1
      status = "Success"
      while status == "Success":
        response = self._get_data(market, page)
        
        page = page + 1
        status = response['status']
        if status != "Success":
          print(f"Failed to get data: {response['message']}")
          break

        data = response['data']  
        if data is not None and len(data) > 0:
          for item in data:
            self._add_datalake(item)
            
          print(f"Inserted {len(data)} data in {market}")


ScrapCompanies().scrap(config.markets)