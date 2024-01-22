# importing Mongoclient from pymongo
from pymongo import MongoClient 

auth_type = 'Bearer'
consumerID = '65ec0bc1c62c4c4188135319559538c2'
consumerSecret = '30f8fc08616c4be99663dd82ca9cc1d0'

url = 'https://fc-data.ssi.com.vn/'
stream_url = 'https://fc-datahub.ssi.com.vn/'

markets = [
  "HNX",
  "HOSE",
  "Upcom"
]

mongo_uri = "mongodb+srv://sangdoan123:sangdoan29052005@cluster0.w6mw3mv.mongodb.net/?retryWrites=true&w=majority"
datalake_client = MongoClient(mongo_uri)
datalake_db = datalake_client["datalake"]
companies_collection = datalake_db["companies"]
stock_price_collection = datalake_db["stock_price"]
batch_size = 100
date_interval = 5