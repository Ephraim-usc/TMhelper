import pandas as pd
import numpy as np
import os
import pickle
import datetime as dt

class entry():
  attributes = ["uid", "alive", "working", "note"]
  required = []
  _initials = {"uid":None, "alive":False, "working":False, "note":None}
  
  def __init__(self, data): # to initialize an entry, input a list of its attributes
    self.dict = self._initials
    if len(data) != len(self.required): # 需要具体看每一个元素
      return
    received = dict(zip(self.required, data))
    self.dict = {**self.dict, **received}
    self.dict["alive"] = True
  
  def values(self):
    return list(self.dict.values())
  
  def str(self):
    zipped = zip(self.attributes, self.values())
    buffer = '\n'.join([attribute+"\t"+str(value) for attribute, value in zipped])
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
      entrylist = entryList.load(filename)
    else:
      entrylist = entryList([])
      entrylist.datatype = cls
    return entrylist

class gmail(entry):
  filename = "gmails.p"
  attributes = entry.attributes + ['buyers', 'Gmail', 'Password', 'SupportGmail', 'SupportGmailPassword']
  required = ['Gmail', 'Password', 'SupportGmail', 'SupportGmailPassword']
  _initials = {**entry._initials, 'buyers':None}
  
  def symbol(self):
    buffer = "<" + self.get("Gmail") + ">"
    return buffer


class address(entry):
  filename = "address.p"
  attributes = entry.attributes + ['buyers', 'RecipientName', 'Address1', 'Address2', 'City', 'Zip', 'State', 'PhoneNumber']
  required = ['RecipientName', 'Address1', 'Address2', 'City', 'Zip', 'State', 'PhoneNumber']
  _initials = {**entry._initials, 'buyers':None}
  
  def symbol(self):
    buffer = "<" + self.get("RecipientName") + ">"
    return buffer


class bankcard(entry):
  filename = "bankcards.p"
  attributes = entry.attributes + ['buyers', 'BankNumber', 'BankCard', 'BankCardExpirationDate']
  required = ['BankNumber', 'BankCard', 'BankCardExpirationDate']
  _initials = {**entry._initials, 'buyers':None}
  
  def symbol(self):
    buffer = "<" + self.get("BankCard") + ">"
    return buffer

class buyer(entry):
  filename = "buyers.p"
  attributes = entry.attributes + ['orders', 'creation_time', 'prime_time', 'gmail', 'bankcard', 'address']
  required = ['gmail', 'bankcard', 'address']
  _initials = {**entry._initials, 'orders':None, "creation_time":None}
  
  def __init__(self, data):
    super().__init__(data)
    self.set("creation_time", dt.datetime.now())
  
  def symbol(self):
    buffer = "<" + self.get("BankCard") + ">"
    return buffer

class entryList():
  datatype = entry
  values = []
  
  def __init__(self, el): # el is a list of entries
    if not el == []:
      self.datatype = type(el[0])
    self.values = el
  
  def get(self, attribute):
    buffer = [x.get(attribute) for x in self.values]
    return buffer
  
  def set(self, attribute, new):
    if len(new) != len(self.values):
      print("error!")
    for i in range(len(self.values)):
      self.values[i].set(attribute, new[i])
  
  def append(self, e):
    self.values = self.values + [e]
  
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
      if e.alive:
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


### special functionalities

def feed(datatype, string):
  current = datatype.all()
  new, remaining = entryList.from_string(datatype, string)
  maximum = len(current.values) + len(new.values)
  uids = np.sort(list(set(range(maximum)) - set(current.get("uid"))))[: len(new.values)]
  new.set("uid", uids)
  merged = entryList.merge(current, new)
  merged.write(datatype.filename)
  return remaining

def search(entrylist, string):
  buffer = []
  for e in entrylist.values:
    match = False
    for key, value in e.dict.items():
      if string in str(value): 
        match = True
        break
    if match == True:
      buffer.append((e, key))
  return buffer

def open_buyer():
  pass

