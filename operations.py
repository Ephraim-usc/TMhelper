import pandas as pd
import numpy as np
import os

def get_buyer(buyers, uid):
  buyers = pd.read_csv("buyers.csv")
  idx = np.where(buyers.loc[:, "uid"] == uid)[0] # find uid matches
  if idx.shape[0] > 1:
    print("Error: multiple matching")
  else:
    idx = idx[0] # get the unique match
  buyer = buyers.iloc[idx, :]
  return buyer

def get_product(products, uid):
  products = pd.read_csv("products.csv")
  idx = np.where(products.loc[:, "uid"] == uid)[0] # find uid matches
  if idx.shape[0] > 1:
    print("Error: multiple matching")
  else:
    idx = idx[0] # get the unique match
  product = products.iloc[idx, :]
  return product

def get_order(orders, uid):
  orders = pd.read_csv("orders.csv")
  idx = np.where(orders.loc[:, "uid"] == uid)[0] # find uid matches
  if idx.shape[0] > 1:
    print("Error: multiple matching")
  else:
    idx = idx[0] # get the unique match
  order = orders.iloc[idx, :]
  return order

def feed_gmails(str):
  columns = pd.Index(['uid', 'buyer', 'Gmail', 'Password', 'SupportGmail', 'SupportGmailPassword'])
  if os.path.isfile("gmails.csv"):
    gmails = pd.read_csv("gmails.csv", index_col=0)
  else:
    gmails = pd.DataFrame(columns = columns)
  
  strll = [tmp.split() for tmp in str.split('\n')]
  new = pd.DataFrame(strll, columns = columns[2:])
  
  uids = np.sort(list(set(range(gmails.shape[0] + new.shape[0])) - set(gmails.uid)))[:new.shape[0]]
  new["uid"] = uids; new["buyer"] = np.nan
  gmails = pd.concat([gmails, new])
  gmails.to_csv("gmails.csv")

def feed_addresses(str):
  columns = pd.Index(['uid', 'buyer', 'RecipientName', 'Address1', 'Address2', 'City', 'Zip', 'State', 'PhoneNumber'])
  if os.path.isfile("addresses.csv"):
    addresses = pd.read_csv("addresses.csv", index_col=0)
  else:
    addresses = pd.DataFrame(columns = columns)
  
  strll = [tmp.split('\t') for tmp in str.split('\n')]
  new = pd.DataFrame(strll, columns = columns[2:])
  
  uids = np.sort(list(set(range(addresses.shape[0] + new.shape[0])) - set(addresses.uid)))[:new.shape[0]]
  new["uid"] = uids; new["buyer"] = np.nan
  addresses = pd.concat([addresses, new])
  addresses.to_csv("addresses.csv")

def feed_bankcards(str):
  columns = pd.Index(['uid', 'buyer', 'BankNumber', 'BankCard', 'BankCardExpirationDate'])
  if os.path.isfile("bankcards.csv"):
    bankcards = pd.read_csv("bankcards.csv", index_col=0)
  else:
    bankcards = pd.DataFrame(columns = columns)
  
  strll = [tmp.split('\t') for tmp in str.split('\n')]
  new = pd.DataFrame(strll, columns = columns[2:])
  
  uids = np.sort(list(set(range(bankcards.shape[0] + new.shape[0])) - set(bankcards.uid)))[:new.shape[0]]
  new["uid"] = uids; new["buyer"] = np.nan
  bankcards = pd.concat([bankcards, new])
  bankcards.to_csv("bankcards.csv")

def new_buyer():
  gmails = pd.read_csv("gmails.csv", index_col=0); gmail = gmails.iloc[np.where(gmails.buyer != gmails.buyer)[0][0], :]
  addresses = pd.read_csv("addresses.csv", index_col=0); address = addresses.iloc[np.where(addresses.buyer != addresses.buyer)[0][0], :]
  bankcards = pd.read_csv("bankcards.csv", index_col=0); bankcard = bankcards.iloc[np.where(addresses.buyer != addresses.buyer)[0][0], :]
  return gmail, address, bankcard

#def new_buyer_submit():
