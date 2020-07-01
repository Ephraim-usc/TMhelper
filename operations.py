import pandas as pd
import numpy as np

orders = pd.read_csv("orders.csv")

def get_buyer(buyers, uid):
  idx = np.where(buyers.loc[:, "uid"] == uid)[0] # find uid matches
  if idx.shape[0] > 1:
    print("Error: multiple matching")
  else:
    idx = idx[0] # get the unique match
  buyer = buyers.iloc[idx, :]
  return buyer

def get_product(products, uid):
  idx = np.where(products.loc[:, "uid"] == uid)[0] # find uid matches
  if idx.shape[0] > 1:
    print("Error: multiple matching")
  else:
    idx = idx[0] # get the unique match
  product = products.iloc[idx, :]
  return product

def get_order(orders, uid):
  idx = np.where(orders.loc[:, "uid"] == uid)[0] # find uid matches
  if idx.shape[0] > 1:
    print("Error: multiple matching")
  else:
    idx = idx[0] # get the unique match
  order = orders.iloc[idx, :]
  return order

def feed_gmail(str):
  gmails = pd.read_csv("gmails.csv")
  strll = [tmp.split() for tmp in str.split('\n')]
  new = pd.DataFrame(strll, columns = gmails.columns)
  gmails = pd.concat([gmails, new])
  gmails.to_csv("gmails.csv")

def feed_address(str):
  addresses = pd.read_csv("addresses.csv")
  strll = [tmp.split('\t') for tmp in str.split('\n')]
  new = pd.DataFrame(strll, columns = addresses.columns)
  addresses = pd.concat([addresses, new])
  addresses.to_csv("addresses.csv")

def feed_bankcards(str):
  bankcards = pd.read_csv("bankcards.csv")
  strll = [tmp.split('\t') for tmp in str.split('\n')]
  new = pd.DataFrame(strll, columns = bankcards.columns)
  bankcards = pd.concat([bankcards, new])
  bankcards.to_csv("bankcards.csv")
  
  
