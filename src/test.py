# import ssi_fc_trading
from ssi_fc_data import fc_md_client, model
import config

client = fc_md_client.MarketDataClient(config)

def md_get_stock_price():
  print(
      client.daily_stock_price(
          config,
          model.daily_stock_price('fpt', '15/10/2020', '25/10/2020', 2, 100,
                                  'hose')))

md_get_stock_price()