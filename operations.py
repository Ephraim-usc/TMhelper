import numpy as np
import os
import pickle
import datetime as dt
import re
import string
import random
import pandas

TIME_INTERVAL_1 = dt.timedelta(days = 2)
TIME_INTERVAL_2 = dt.timedelta(days = 3)
TIME_INTERVAL_3 = dt.timedelta(days = 3)
TIME_INTERVAL_4 = dt.timedelta(days = 7)

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
    self.dict['working'] = False
  
  def values(self):
    return list(self.dict.values())
  
  def str(self):
    buffer = 'uid\t' + str(self.uid) + '\n'
    buffer += '\n'.join([key+"\t"+str(value) for key, value in self.dict.items()])
    return buffer
  
  def get(self, attribute):
    buffer = self.dict.get(attribute, None)
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
  
  @classmethod
  def delete(cls, uid): # only used on entries without reference !!
    el = cls.all()
    el.delete(uid)
    el.write(cls.filename)
  
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
  buyers = []
  
  attributes = entry.attributes + ['Gmail', 'Password', 'SupportGmail', 'SupportGmailPassword']
  required = entry.required + ['Gmail', 'Password', 'SupportGmail', 'SupportGmailPassword']
  
  def __init__(self, data):
    entry.__init__(self, data)
    self.buyers = []
  
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
  buyers = []
  
  attributes = entry.attributes + ['RecipientName', 'Address1', 'Address2', 
                                   'City', 'Zip', 'State', 'PhoneNumber']
  required = entry.required + ['RecipientName', 'Address1', 'Address2', 
                               'City', 'Zip', 'State', 'PhoneNumber']
  
  def __init__(self, data):
    entry.__init__(self, data)
    self.buyers = []
  
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
  buyers = []
  
  attributes = entry.attributes + ['BankNumber', 'BankCard', 'BankCardExpirationDate']
  required = entry.required + ['BankNumber', 'BankCard', 'BankCardExpirationDate']
  
  def __init__(self, data):
    entry.__init__(self, data)
    self.buyers = []
  
  def symbol(self):
    buffer = "<" + str(self.get("BankCard")) + "|" + str(self.uid) + ">"
    return buffer
  
  def str(self):
    buffer = entry.str(self)
    buffer += '\nbuyers\t['
    buffer += ','.join([str(buyer.query(i).symbol()) for i in self.buyers])
    buffer += ']'
    return buffer

class buyer(entry):
  filename = "buyers.p"
  gmail = None
  address = None
  bankcard = None
  orders = []
  
  attributes = entry.attributes + ['creation_time', 'prime_time', 'AmazonPassword']
  required = entry.required + ['AmazonPassword']
  
  def __init__(self, data):
    entry.__init__(self, data)
    self.set("creation_time", dt.datetime.now())
    self.orders = []
  
  def bind(self, gm, ad, bc):
    self.gmail = gm.uid
    self.address = ad.uid
    self.bankcard = bc.uid
    gm.buyers.append(self.uid)
    ad.buyers.append(self.uid)
    bc.buyers.append(self.uid)
  
  def str(self):
    buffer = entry.str(self)
    if self.get("alive") == False: return buffer
    buffer += '\n' + "gmail\t" + str(gmail.query(self.gmail).symbol())
    buffer += '\n' + "address\t" + str(address.query(self.address).symbol())
    buffer += '\n' + "bankcard\t" + str(bankcard.query(self.bankcard).symbol())
    buffer += '\n' + "orders\t[" + ','.join([str(order.query(i).symbol()) for i in self.orders]) + ']'
    return buffer
  
  def symbol(self):
    if self.get("alive") == False:
      return "<" + "temporary" + "|" + str(self.uid) + ">"
    buffer = "<" + str(address.query(self.address).get("RecipientName")) + "|" + str(self.uid) + ">"
    return buffer
  
  def num_orders(self):
    buffer = len(self.orders)
    return buffer
  
  def latest_order_time(self):
    times = [order.query(i).get("OrderTime") for i in self.orders]
    return max(times)
  
  def latest_order(self):
    latest = self.latest_order_time()
    for i in self.orders:
      od = order.query(i)
      if od.get("OrderTime") == latest:
        return od
  
  def able_to_order(self): # store instead of uid; first 2 orders should be reviewable products
    if self.get("alive") == False: return False
    
    global TIME_INTERVAL_1
    global TIME_INTERVAL_2
    num = self.num_orders()
    current = dt.datetime.now()
    buffer = False
    if num == 0:
      if current > self.get("creation_time") + TIME_INTERVAL_1:
        buffer = True
    elif num == 1:
      od = self.latest_order()
      if current > self.latest_order_time() + TIME_INTERVAL_1:
        buffer = True
      if od.get("EstimatedDeliveryTime") != None and current > od.get("EstimatedDeliveryTime"):
        buffer = True
      if od.get("DeliveryTime") != None:
        buffer = True
    elif num in [2,3,4,5]:
      if current > self.latest_order_time() + TIME_INTERVAL_2:
        buffer = True
    return buffer
      

class product(entry):
  filename = "products.p"
  orders = []
  
  attributes = entry.attributes + ['ASIN', 'name', 'Store', 'Brand', 'keyword', 'Price', 'link', 'image', 'num_tasks', 'num_daily_reviews', "goal_reviews"]
  required = entry.required + ['ASIN', 'name', 'Store']
  
  def __init__(self, data):
    entry.__init__(self, data)
    self.orders = []
    self.set("num_tasks", 0)
    self.set("num_daily_reviews", 2)
    self.set("goal_reviews", 0)
    if self.get("ASIN") != None:
      self.set("image", self.get("ASIN") + ".jpg")
  
  def symbol(self):
    buffer = "<" + str(self.get("name")) + "|" + str(self.uid) + ">"
    return buffer
  
  def str(self):
    buffer = entry.str(self)
    buffer += '\norders\t['
    buffer += ','.join([str(order.query(b).symbol()) for b in self.orders])
    buffer += ']'
    return buffer
  
  def num_orders_today(self):
    today = dt.datetime.combine(dt.date.today(), dt.datetime.min.time())
    buffer = 0
    for i in self.orders:
      if order.query(i).get("OrderTime") > today:
        buffer += 1
    return buffer
  
  @classmethod
  def query(cls, uid):
    if uid == -1:
      global OTHER
      return OTHER
    else:
      el = cls.all()
      return el.query(uid)

class order(entry):
  filename = "orders.p"
  buyer = None
  product = None
  review = None
  
  attributes = entry.attributes + ['rank', 'OrderID', 'OrderTime', 'Cost', 'EstimatedDeliveryTime', 'DeliveryTime']
  required = entry.required + ['OrderID', 'Cost']
  
  def __init__(self, data):
    entry.__init__(self, data)
    self.set("OrderTime", dt.datetime.now())
  
  def place(self, br, pdt):
    self.buyer = br.uid
    self.product = pdt.uid
    br.orders.append(self.uid)
    pdt.orders.append(self.uid)
    pdt.set("num_tasks", pdt.get("num_tasks") - 1)
    self.set("rank", len(br.orders))
  
  def leave_review(self, rv):
    self.review = rv
    rv.order = self.uid
    rv.set("Time", dt.datetime.now())
  
  def symbol(self):
    buffer = "<" + str(self.get("OrderID")) + "|" + str(self.uid) + ">"
    return buffer
  
  def str(self):
    buffer = entry.str(self)
    buffer += '\nbuyer\t' + buyer.query(self.buyer).symbol()
    buffer += '\nproduct\t' + product.query(self.product).symbol()
    if self.review != None:
      buffer += '\nreview\t' + review.query(self.review).symbol()
    else:
      buffer += '\nreview\t' + "None"
    return buffer
  
  def able_to_review(self):
    pd = product.query(self.product)
    if pd.uid == -1:
      return False
    if pd.get("num_daily_reviews") == 0:
      return False
    if self.review != None:
      return False
    
    global TIME_INTERVAL_3
    global TIME_INTERVAL_4
    
    br = buyer.query(self.buyer)
    num = br.num_orders()
    current = dt.datetime.now()
    if self.get("rank") == 2 and num >= 4:
      fourthorder = order.query(br.orders[3])
      if current > fourthorder.get("OrderTime") + TIME_INTERVAL_3:
        return True
    if self.get("rank") == 3:
      secondorder = order.query(br.orders[1])
      sr = secondorder.review
      if sr != None and current > sr.get("Time") + TIME_INTERVAL_4:
        return True
    return False

class review(entry):
  filename = "reviews.p"
  order = None
  
  attributes = entry.attributes + ['ASIN', 'Title', 'Content', 'Time']
  required = entry.required + ['ASIN', 'Title', 'Content']
  
  def symbol(self):
    return "<" + str(self.get("Content")) + "|" + str(self.uid) + ">"

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
  available_gmails = [e for e in gmail.all().values if e.get("alive") and e.get("working")==False and e.buyers==[] ]
  available_addresses = [e for e in address.all().values if e.get("alive") and e.get("working")==False and e.buyers==[] ]
  available_bankcards = [e for e in bankcard.all().values if e.get("alive") and e.get("working")==False and e.buyers==[] ]
  
  if (available_gmails == [] or available_addresses == [] or available_bankcards == []):
    return None, None, None, None
  
  gm = np.random.choice(available_gmails); gm.set("working", True)
  ad = np.random.choice(available_addresses); ad.set("working", True)
  bc = np.random.choice(available_bankcards); bc.set("working", True)
  
  pwd = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))
  br = buyer([pwd]); br.set("alive", False); br.submit()
  
  return gm, ad, bc, br

def open_buyer_confirm(gm, ad, bc, br):
  br.bind(gm, ad, bc)
  gm.set("working", False); gm.submit()
  ad.set("working", False); ad.submit()
  bc.set("working", False); bc.submit()
  br.set("alive", True)
  br.submit()

def open_buyer_abort(gm, ad, bc, br):
  gm.set("working", False); gm.submit()
  ad.set("working", False); ad.submit()
  bc.set("working", False); bc.submit()
  buyer.delete(br.uid)

def buy(br, pdt, order_id, cost):
  od = order([order_id, cost])
  od.submit()
  od.place(br, pdt)
  br.submit()
  pdt.submit()
  od.submit()
  
def orderable_buyers():
  buffer = []
  for br in buyer.all().values:
    if br.able_to_order():
      buffer.append(br)
  o1, o2, o3, o4, o5, o6 = [], [], [], [], [], []
  for br in buffer:
    num = br.num_orders()
    if num == 0:
      o1.append(br)
    if num == 1:
      o2.append(br)
    if num == 2:
      o3.append(br)
    if num == 3:
      o4.append(br)
    if num == 4:
      o5.append(br)
    if num == 5:
      o6.append(br)
  return o1, o2, o3, o4, o5, o6

OTHER = product([None, None, None])
OTHER.str = lambda : "other item"
OTHER.symbol = lambda : "<other>"
OTHER.submit = lambda : None
OTHER.uid = -1

def orderable_products(br):
  num = br.num_orders()
  if num in [0, 4]:
    return [OTHER]
  pds = product.all().values
  ordered = br.orders
  stores = [product.query(order.query(od).product).get("Store") for od in ordered]
  buffer = []
  for pd in pds:
    if pd.get("num_tasks") > 0 and pd.get("Store") not in stores:
      buffer.append(pd)
  if num in [2, 3]:
    buffer = [pd for pd in buffer if pd.get("num_daily_reviews") > 0]
  return buffer

def reviewable_orders():
  ods = []
  for od in order.all().values:
    if od.able_to_review():
      ods.append(od)
  
  pds_uid = list(set([od.product for od in ods]))
  buffer = {x:[] for x in pds_uid}
  for od in ods:
    buffer[od.product].append(od)
  
  return buffer
  
def suitable_reviews(pd):
  rvs = review.all().values
  asin = pd.get("ASIN")
  buffer = []
  for rv in rvs:
    if rv.order != None:
      continue
    if rv.get("ASIN") == asin:
      buffer.append(rv)
  
  return buffer

def submit_review(pd, rv, string_):
  commit(rv, string_)
  pd.leave_review(rv)
  pd.submit()
  rv.submit()

def commit(e, string):
  stringll = [stringl.split('\t') for stringl in string.split('\n')]
  for key, value in stringll:
    if not key in e.attributes:
      continue
    if re.search("^True$|^False$", value) is not None:
      value = bool(value)
    elif re.search('^[0-9]+\.*[0-9]*$', value) is not None:  # dt.time!!!
      value = float(value)
    elif re.search('^None$', value) is not None:
      value = None
    e.set(key, value)
  e.submit()

def product_report(start, end):
  pds = product.all().values
  buffer = pandas.DataFrame(columns=['uid', 'ASIN', 'Store', 'num_tasks', 'orders', 'reviews', 'reviews/orders', 'goal_reviews', 'reviews/goal_reviews'])
  
  for pd in pds:
    ods = [i for i in pd.orders if 
           (order.query(i).get("OrderTime") > start and order.query(i).get("OrderTime") < end)]
    rv_ods = [i for i in pd.orders if 
              (order.query(i).review != None and order.query(i).review.get("Time") > start and order.query(i).review.get("Time") < end)]
    
    buffer_ = []
    buffer_.append(str(pd.uid))
    buffer_.append(str(pd.get("ASIN")))
    buffer_.append(str(pd.get("Store")))
    buffer_.append(str(pd.get("num_tasks")))
    buffer_.append(str(len(ods)))
    buffer_.append(str(len(rv_ods)))
    if ods != []:
      buffer_.append(str(len(rv_ods)/len(ods)))
    else:
      buffer_.append("NA")
    buffer_.append(str(pd.get("goal_reviews")))
    if pd.get("goal_reviews") not in [0, None]:
      buffer_.append(str(len(rv_ods)/pd.get("goal_reviews")))
    else:
      buffer_.append("NA")
    
    buffer.loc[buffer.shape[0]] = buffer_
  
  return buffer
  

    






