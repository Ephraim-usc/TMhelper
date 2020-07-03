import pandas as pd
import numpy as np
import os
import pickle
import datetime as dt

class entry():
  uid = None
  filename = None
  
  attributes = ['alive', 'working', 'note']
  required = []
  
  def __init__(self, data):
    self.dict = dict.fromkeys(self.attributes, None)
    if len(data) != len(self.required):
      return
    received = dict(zip(self.required, data))
    self.dict = {**self.dict, **received}
    self.dict['alive'] = True
  
  def values(self):
    return list(self.dict.values())
  
  def str(self):
    buffer = 'uid\t' + str(self.uid) + '\n'
    buffer += '\n'.join([key+"\t"+str(value) for key, value in self.dict.items()])
    return buffer
  
  def get(self, attribute):
    buffer = self.dict[attribute]
    return buffer
  
  def set(self, attribute, new):
    self.dict[attribute] = new
  
  @classmethod
  def all(cls):
    filename = cls.filename
    if os.path.isfile(filename):
      el = entryList.load(filename)
    else:
      el = entryList([])
      el.datatype = cls
    return el
  
  @classmethod
  def query(cls, uid):
    el = cls.all()
    return el.query(uid)
  
  def submit(self):
    all = self.all()
    if self.uid == None:
      maximum = len(all.values) + 1
      uids = [e.uid for e in all.values]
      uid = np.sort(list(set(range(maximum)) - set(uids)))[0]
      self.uid = uid
    all.delete(self.uid)
    all.append(self)
    all.write(self.filename)

class entryList():
  datatype = entry
  values = []
  
  def __init__(self, el):
    if not el == []:
      self.datatype = type(el[0])
    self.values = el
  
  def query(self, uid):
    for e in self.values:
      if e.uid == uid:
        return e
  
  def append(self, e):
    self.values.append(e)
  
  def _delete(self, index):
    del self.values[index]
  
  def delete(self, uid):
    for i in range(len(self.values) - 1, -1, -1):
      if self.values[i].uid == uid:
        self._delete(i)
  
  def write(self, filename):
    with open(filename, "wb") as f:
      pickle.dump(self, f)
  
  @staticmethod
  def load(filename):
    with open(filename, "rb") as f:
      buffer = pickle.load(f)
    return buffer
  
  @staticmethod
  def from_string(datatype, string):
    string.replace("\r\n", "\n")
    stringll = [tmp.split('\t') for tmp in string.split('\n')]
    buffer = []
    remaining = []
    for stringl in stringll:
      e = datatype(stringl)
      if e.get("alive"):
        buffer.append(e)
      else:
        remaining.append('\t'.join(stringl))
    buffer = entryList(buffer)
    remaining = '\n'.join(remaining)
    return buffer, remaining
  
  @staticmethod
  def merge(x, y):
    buffer = entryList([])
    buffer.datatype = x.datatype
    for e in x.values:
      buffer.append(e)
    for e in y.values:
      buffer.append(e)
    return buffer

class gmail(entry):
  filename = "gmails.p"
  buyers = set()
  
  attributes = entry.attributes + ['Gmail', 'Password', 'SupportGmail', 'SupportGmailPassword']
  required = entry.required + ['Gmail', 'Password', 'SupportGmail', 'SupportGmailPassword']
  
  def __init__(self, data):
    entry.__init__(self, data)
    self.buyers = set()
  
  def symbol(self):
    buffer = "<" + str(self.get("Gmail")) + "|" + str(self.uid) + ">"
    return buffer
  
  def str(self):
    buffer = entry.str(self)
    buffer += '\nbuyers\t['
    buffer += ','.join([str(buyer.query(b).symbol()) for b in self.buyers])
    buffer += ']'
    return buffer

class address(entry):
  filename = "addresses.p"
  buyers = set()
  
  attributes = entry.attributes + ['RecipientName', 'Address1', 'Address2', 
                                   'City', 'Zip', 'State', 'PhoneNumber']
  required = entry.required + ['RecipientName', 'Address1', 'Address2', 
                               'City', 'Zip', 'State', 'PhoneNumber']
  
  def __init__(self, data):
    entry.__init__(self, data)
    self.buyers = set()
  
  def symbol(self):
    buffer = "<" + str(self.get("RecipientName")) + "|" + str(self.uid) + ">"
    return buffer
  
  def str(self):
    buffer = entry.str(self)
    buffer += '\nbuyers\t['
    buffer += ','.join([str(buyer.query(b).symbol()) for b in self.buyers])
    buffer += ']'
    return buffer

class bankcard(entry):
  filename = "bankcards.p"
  buyers = set()
  
  attributes = entry.attributes + ['BankNumber', 'BankCard', 'BankCardExpirationDate']
  required = entry.required + ['BankNumber', 'BankCard', 'BankCardExpirationDate']
  
  def __init__(self, data):
    entry.__init__(self, data)
    self.buyers = set()
  
  def symbol(self):
    buffer = "<" + str(self.get("BankCard")) + "|" + str(self.uid) + ">"
    return buffer
  
  def str(self):
    buffer = entry.str(self)
    buffer += '\nbuyers\t['
    buffer += ','.join([str(buyer.query(b).symbol()) for b in self.buyers])
    buffer += ']'
    return buffer

class buyer(entry):
  filename = "buyers.p"
  gmail = None
  address = None
  bankcard = None
  orders = set()
  
  attributes = entry.attributes + ['creation_time', 'prime_time']
  required = entry.required
  
  def __init__(self, data):
    entry.__init__(self, data)
    self.set("creation_time", dt.datetime.now())
    self.orders = set()
  
  def bind(self, gm, ad, bc):
    self.gmail = gm.uid
    self.address = ad.uid
    self.bankcard = bc.uid
    gm.buyers.add(self.uid)
    ad.buyers.add(self.uid)
    bc.buyers.add(self.uid)
  
  def str(self):
    buffer = entry.str(self)
    buffer += '\n' + "gmail\t" + str(gmail.query(self.gmail).symbol())
    buffer += '\n' + "address\t" + str(address.query(self.address).symbol())
    buffer += '\n' + "bankcard\t" + str(bankcard.query(self.bankcard).symbol())
    return buffer
  
  def symbol(self):
    ad = address.query(self.address)
    buffer = "<" + str(ad.get("RecipientName")) + "|" + str(self.uid) + ">"
    return buffer

class product(entry):
  filename = "products.p"
  orders = set()
  
  attributes = entry.attributes + ['ASIN', 'name', 'Store', 'Brand', 'keyword', 'Price', 'link', 'image']
  required = entry.required + ['ASIN', 'name', 'Store']
  
  def __init__(self, data):
    entry.__init__(self, data)
    self.set("creation_time", dt.datetime.now())
    self.orders = set()
  
  def symbol(self):
    buffer = "<" + str(self.get("name")) + "|" + str(self.uid) + ">"
    return buffer
  
  def str(self):
    buffer = entry.str(self)
    buffer += '\norders\t['
    buffer += ','.join([str(order.query(b).symbol()) for b in self.orders])
    buffer += ']'
    return buffer

class order(entry):
  filename = "orders.p"
  product = None
  
  attributes = entry.attributes + ['OrderID', 'OrderTime', 'Cost', 'DeliveryTime', 'Delivered']
  required = entry.required + ['OrderID', 'Cost']
  
  def __init__(self, data, product):
    entry.__init__(self, data)
    self.set("OrderTime", dt.datetime.now())
    self.set("Delivered", False)
    self.product = product
  
  def symbol(self):
    buffer = "<" + str(self.get("OrderID")) + "|" + str(self.uid) + ">"
    return buffer
  
  def str(self):
    buffer = entry.str(self)
    buffer += '\nproduct\t' + self.product.symbol()
    return buffer

    
### special functionalities

def feed(datatype, string):
  el, remaining = entryList.from_string(datatype, string)
  for e in el.values:
    e.submit()
  return remaining

def search(datatype, string):
  el = datatype.all()
  buffer = []
  for e in el.values:
    match = False
    if string in str(e.uid):
      match = True
      key = "uid"
    else:
      for key, value in e.dict.items():
        if string in str(value): 
          match = True
          break
    if match == True:
      buffer.append((e, key))
  return buffer

def open_buyer():
  available_gmails = [e for e in gmail.all().values if e.get("alive") and e.get("working")==False and e.buyers==set() ]
  gm = np.random.choice(available_gmails); gm.set("working", True)
  
  available_addresses = [e for e in address.all().values if e.get("alive") and e.get("working")==False and e.buyers==set() ]
  ad = np.random.choice(available_addresses); ad.set("working", True)
  
  available_bankcards = [e for e in bankcard.all().values if e.get("alive") and e.get("working")==False and e.buyers==set() ]
  bc = np.random.choice(available_bankcards); bc.set("working", True)
  
  return gm, ad, bc

def open_buyer_confirm(gm, ad, bc):
  newbuyer = buyer([])
  newbuyer.submit()
  newbuyer.bind(gm, ad, bc)
  gm.set("working", False); gm.submit()
  ad.set("working", False); ad.submit()
  bc.set("working", False); bc.submit()
  newbuyer.submit()
