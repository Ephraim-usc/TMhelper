import pandas as pd
import numpy as np
import os

'''
def get_buyer(buyers, uid):
  buyers = pd.read_csv("buyers.csv")
  idx = np.where(buyers.loc[:, "uid"] == uid)[0] # find uid matches
  if idx.shape[0] > 1:
    print("Error: multiple matching")
  else:
    idx = idx[0] # get the unique match
  buyer = buyers.iloc[idx, :]
  return buyer

'''

### lookup table for all datatypes
gmail_columns = ['uid', 'buyer', 'Gmail', 'Password', 'SupportGmail', 'SupportGmailPassword']
gmail_filename = "gmails.csv"
gmail_str = lambda x: "<" + x["Gmail"] + ">"
gmail_lkt = {"columns":gmail_columns, "filename":gmail_filename, "str_method":gmail_str}

address_columns = ['uid', 'buyer', 'RecipientName', 'Address1', 'Address2', 'City', 'Zip', 'State', 'PhoneNumber']
address_filename = "addresses.csv"
address_lkt = {"columns":address_columns, "filename":address_filename}

bankcard_columns = ['uid', 'buyer', 'BankNumber', 'BankCard', 'BankCardExpirationDate']
bankcard_filename = "bankcards.csv"
bankcard_str = lambda x: "<" + x["BankCard"] + ">"
bankcard_lkt = {"columns":bankcard_columns, "filename":bankcard_filename, "str_method":bankcard_str}

lkt = {"gmail":gmail_lkt, "address":address_lkt, "bankcard":bankcard_lkt}

###
def feed(datatype, string):
  filename = lkt[datatype]["filename"]
  columns = lkt[datatype]["columns"]
  if os.path.isfile(filename):
    current = pd.read_csv(filename, index_col=0, dtype = str)
  else:
    current = pd.DataFrame(columns = columns)
  
  new = pd.DataFrame([tmp.split('\t') for tmp in string.split('\n')], 
                     columns = list(set(columns) - set(["uid", "buyer"])))
  total_nrow = current.shape[0] + new.shape[0]
  current_uids = np.array(current.uid).astype(int)
  uids = np.sort(list(set(range(total_nrow)) - set(current_uids)))[:new.shape[0]]
  new["uid"] = uids; new["buyer"] = np.nan
  merged = pd.concat([current, new])
  merged.to_csv(filename)

def new_buyer():
  gmails = pd.read_csv("gmails.csv", index_col=0, dtype = str); gmail = gmails.iloc[np.where(gmails.buyer != gmails.buyer)[0][0], :]
  addresses = pd.read_csv("addresses.csv", index_col=0, dtype = str); address = addresses.iloc[np.where(addresses.buyer != addresses.buyer)[0][0], :]
  bankcards = pd.read_csv("bankcards.csv", index_col=0, dtype = str); bankcard = bankcards.iloc[np.where(addresses.buyer != addresses.buyer)[0][0], :]
  return gmail, address, bankcard



#def new_buyer_submit():

def search(datatype, string):
  filename = lkt[datatype]["filename"]
  data = pd.read_csv(filename, index_col=0, dtype= str)
  str_method = lkt[datatype]["str_method"]
  
  buffer = []
  for i in range(data.shape[0]):
    entry = data.iloc[i, :]
    match = False
    for j in range(entry.shape[0]):
      if not isinstance(entry[j], str):
        continue
      if string in entry[j]:
        match = True
    if match == True:
      buffer.append(str_method(entry))
  
  return(buffer)

