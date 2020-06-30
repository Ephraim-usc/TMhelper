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
