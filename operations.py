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
  _initials = {"alive":False, "working":False, "note":None}
  
  def __init__(self, data):
    self.dict = self._initials
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
  _initials = {**entry._initials, 'Gmail':None, 'Password':None, 
               'SupportGmail':None, 'SupportGmailPassword':None}
  
  def symbol(self):
    buffer = "<" + str(self.get("Gmail")) + "|" + str(self.uid) + ">"
    return buffer
  
  def str(self):
    buffer = entry.str(self)
    buffer += '\nbuyers\t['
    for b in self.buyers:
      buffer += b.symbol()
    buffer += ']'
    return buffer

class address(entry):
  filename = "addresses.p"
  buyers = set()
  
  attributes = entry.attributes + ['RecipientName', 'Address1', 'Address2', 
                                   'City', 'Zip', 'State', 'PhoneNumber']
  required = entry.required + ['RecipientName', 'Address1', 'Address2', 
                               'City', 'Zip', 'State', 'PhoneNumber']
  _initials = {**entry._initials, 'RecipientName':None, 'Address1':None, 'Address2':None, 
               'City':None, 'Zip':None, 'State':None, 'PhoneNumber':None}
  
  def symbol(self):
    buffer = "<" + str(self.get("RecipientName")) + "|" + str(self.uid) + ">"
    return buffer
  
  def str(self):
    buffer = entry.str(self)
    buffer += '\nbuyers\t['
    for b in self.buyers:
      buffer += b.symbol()
    buffer += ']'
    return buffer

class bankcard(entry):
  filename = "bankcards.p"
  buyers = set()
  
  attributes = entry.attributes + ['BankNumber', 'BankCard', 'BankCardExpirationDate']
  required = entry.required + ['BankNumber', 'BankCard', 'BankCardExpirationDate']
  _initials = {**entry._initials, 'BankNumber':None, 'BankCard':None, 'BankCardExpirationDate':None}
  
  def symbol(self):
    buffer = "<" + str(self.get("BankCard")) + "|" + str(self.uid) + ">"
    return buffer
  
  def str(self):
    buffer = entry.str(self)
    buffer += '\nbuyers\t['
    for b in self.buyers:
      buffer += b.symbol()
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
  _initials = {**entry._initials, 'creation_time':None, 'prime_time':None}
  
  def __init__(self, gm, ad, bc):
    entry.__init__(self, [])
    self.set("creation_time", dt.datetime.now())
    self.gmail = gm
    self.address = ad
    self.bankcard = bc
    gm.buyers.add(self)
    ad.buyers.add(self)
    bc.buyers.add(self)
  
  def str(self):
    buffer = entry.str(self)
    buffer += '\n' + "gmail\t" + self.gmail.symbol()
    buffer += '\n' + "address\t" + self.address.symbol()
    buffer += '\n' + "bankcard\t" + self.bankcard.symbol()
    return buffer
  
  def symbol(self):
      buffer = "<" + str(self.address.get("RecipientName")) + "|" + str(self.uid) + ">"
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

def open_buyer_confirm(newbuyer):
  gm = newbuyer.gmail
  ad = newbuyer.address
  bc = newbuyer.bankcard
  gm.set("working", False); gm.submit()
  ad.set("working", False); ad.submit()
  bc.set("working", False); bc.submit()
  newbuyer.submit()
