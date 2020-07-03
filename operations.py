import pandas as pd
import numpy as np
import os
import pickle
import datetime as dt

class entry():
  uid = None
  
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

class gmail(entry):
  filename = "gmails.p"
  buyer = None
  
  attributes = entry.attributes + ['Gmail', 'Password', 'SupportGmail', 'SupportGmailPassword']
  required = entry.required + ['Gmail', 'Password', 'SupportGmail', 'SupportGmailPassword']
  _initials = {**entry._initials, 'Gmail':None, 'Password':None, 
               'SupportGmail':None, 'SupportGmailPassword':None}
  
  def symbol(self):
    buffer = "<" + str(self.get("Gmail")) + "|" + str(self.uid) + ">"
    return buffer

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
  def merge(x, y):
    buffer = entryList([])
    buffer.datatype = x.datatype
    for e in x.values:
      buffer.append(e)
    for e in y.values:
      buffer.append(e)
    return buffer




