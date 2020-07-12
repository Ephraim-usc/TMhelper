
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
from PIL import Image, ImageTk
import numpy as np
import os
import datetime as dt

import operations as op

'''
import requests
r = requests.get("https://raw.github.com/Ephraim-usc/TMhelper/master/operations.py")
with open("operations.py", "w", encoding="utf-8") as f:
  f.write(r.text)
'''

ACCOUNT = "public"

class TMhelper(tk.Tk):
  def __init__(self, *args, **kwargs):
    tk.Tk.__init__(self, *args, **kwargs)
    self.title('TMhelper')
    self.geometry("1000x500")
    
    self.menuframe = Menu(self)
    self.menuframe.place(x = 0, y = 0)
    
    self.reportframe = Report(self)
    self.reportframe.init()
    
    self.loginframe = Login(self)
    self.loginframe.place(x = 0, y = 30)
    
    self.feedframe = Feed(self)
    self.adminframe = Admin(self)
    self.checkframe = Check(self)
    self.buyerframe = Buyer(self)
    self.preorderframe = PreOrder(self)
    self.orderframe = Order(self)
    self.prereviewframe = PreReview(self)
    self.reviewframe = Review(self)
  
  def refresh(self):
    other_frames = [w for w in self.winfo_children() if w.winfo_y() > 0]
    for w in other_frames:
      w.place_forget()
    self.reportframe.place(x = 0, y = 30)

class Frame(tk.Frame):
  def __init__(self, parent, *args, **kwargs):
    tk.Frame.__init__(self, parent, *args, **kwargs)
    self.parent = parent
    self.configure(width = 1000, height = 470)
    self['bg'] = 'grey'
  
  def copy(self, event):
    self.parent.clipboard_clear()
    self.parent.clipboard_append(event.widget.get("1.0", "end-1c"))
  
  def clear(self):
    children = self.winfo_children()
    children_text = [w for w in children if type(w) == tk.Text]
    for w in children_text:
      if w['state'] == 'normal':
        w.delete("1.0", "end")
      if w['state'] == 'disabled':
        w.configure(state = 'normal')
        w.delete("1.0", "end")
        w.configure(state = 'disabled')
  
  def display(self, widget, string):
    if widget['state'] == 'normal':
      widget.delete("1.0", "end")
      widget.insert("1.0", str(string))
    if widget['state'] == 'disabled':
      widget.configure(state = "normal")
      widget.delete("1.0", "end")
      widget.insert("1.0", str(string))
      widget.configure(state = "disabled")
  
  def quit(self):
    self.place_forget()

class Menu(tk.Frame):
  feed = None
  phone = None
  
  def __init__(self, parent, *args, **kwargs):
    tk.Frame.__init__(self, parent, *args, **kwargs)
    self.parent = parent
    self.configure(width = 1000, height = 30)
    self['bg'] = 'grey'
    
    self.feed = tk.StringVar()
    self.phone = tk.StringVar()
    
    self.login_button = ttk.Button(self, text="Login", command = self.login_event)
    self.login_button.place(x = 0, y = 0, height = 30, width = 95)
    
    self.admin_button = ttk.Button(self, text="Admin", command = self.admin_event)
    self.admin_button.place(x = 100, y = 0, height = 30, width = 95)
    
    self.buyer_button = ttk.Button(self, text="Open Buyer", command = self.buyer_event)
    self.buyer_button.place(x = 200, y = 0, height = 30, width = 120)
    
    self.order_button = ttk.Button(self, text="Place Order", command = self.pre_order_event)
    self.order_button.place(x = 325, y = 0, height = 30, width = 120)
    
    self.review_button = ttk.Button(self, text="Leave Review", command = self.pre_review_event)
    self.review_button.place(x = 450, y = 0, height = 30, width = 120)
    
    self.feed_combobox = ttk.Combobox(self, textvariable = self.feed)
    self.feed_combobox['values'] = ['Import Data', 'Gmails', 'Addresses', 'BankCards', 'Reviews', 'Products']
    self.feed_combobox.current(0)
    self.feed_combobox.place(x = 720, y = 2, height = 40, width = 125)
    
    self.phone_combobox = ttk.Combobox(self, textvariable = self.phone)
    self.phone_combobox['values'] = ['Select Phone'] + next(os.walk('./phones'))[1]
    self.phone_combobox.current(0)
    self.phone_combobox.place(x = 850, y = 2, height = 40, width = 125)
    
    self.feed.trace("w", self.feed_write_event)
    self.phone.trace("w", self.phone_write_event)
  
  def login_event(self):
    self.parent.refresh()
    self.parent.loginframe.place(x = 0, y = 30)
  
  def admin_event(self):
    global ACCOUNT
    if ACCOUNT != "admin":
      messagebox.showinfo(title= "Error", message= "Accessible to admin only.")
      return None
    
    self.parent.refresh()
    self.parent.adminframe.place(x = 0, y = 30)
  
  def buyer_event(self):
    self.parent.refresh()
    self.parent.buyerframe.place(x = 0, y = 30)
  
  def pre_order_event(self):
    self.parent.refresh()
    self.parent.preorderframe.refresh()
    self.parent.preorderframe.place(x = 0, y = 30)
  
  def pre_review_event(self):
    self.parent.refresh()
    self.parent.prereviewframe.refresh()
    self.parent.prereviewframe.place(x = 0, y = 30)
  
  def feed_write_event(self, var, indx, mode):
    self.parent.refresh()
    if self.feed.get() == "Import Data":
      return None
    if self.phone.get() == "Select Phone" and self.feed.get() in ["Gmails", "Addresses", "BankCards"]:
      messagebox.showinfo(title= "Error", message= "You have to select a phone.")
      return None
    datatype = {"Gmails":op.gmail, "Addresses":op.address, "Reviews":op.review,
                "BankCards":op.bankcard, "Products":op.product}[self.feed.get()]
    self.parent.feedframe.datatype = datatype
    self.parent.feedframe.refresh()
    self.parent.feedframe.place(x = 0, y = 30)
  
  def phone_write_event(self, var, indx, mode):
    phone = self.phone.get()
    if phone == "Select Phone":
      return None
    op.gmail.filename = "./phones/" + phone + "/gmails.p"
    op.address.filename = "./phones/" + phone + "/addresses.p"
    op.bankcard.filename = "./phones/" + phone + "/bankcards.p"
    op.buyer.filename = "./phones/" + phone + "/buyers.p"
    op.order.filename = "./phones/" + phone + "/orders.p"
    self.parent.refresh()

class Login(Frame):
  image = None
  
  def __init__(self, parent, *args, **kwargs):
    Frame.__init__(self, parent, *args, **kwargs)
    
    self.img = ImageTk.PhotoImage(Image.open("images/cover.jpg").resize((300, 200)))
    self.image_label = tk.Label(self, image = self.img);
    self.image_label.place(x = 100, y = 120, width = 300, height = 200)
    
    self.username_text = tk.Text(self); 
    self.username_text.place(x = 550, y = 150, width = 300, height = 20)
    
    self.password_text = tk.Text(self); 
    self.password_text.place(x = 550, y = 200, width = 300, height = 20)
    
    tk.Label(self, text = "Username", bg = "grey").place(x = 460, y = 150, width = 70, height = 20)
    tk.Label(self, text = "Password", bg = "grey").place(x = 460, y = 200, width = 70, height = 20)
    
    self.login_button = tk.Button(self, text = "Log In", command = self.login)
    self.login_button.place(x = 750, y = 250, width = 100, height = 20)
    
    self.register_button = tk.Button(self, text = "Register", command = self.register)
    self.register_button.place(x = 750, y = 300, width = 100, height = 20)
  
  def login(self):
    username = self.username_text.get("1.0", "end-1c")
    password = self.password_text.get("1.0", "end-1c")
    
    if username == "":
      messagebox.showinfo(title= "Error", message= "Username cannot be empty.")
      return None
    if password == "":
      messagebox.showinfo(title= "Error", message= "Password cannot be empty.")
      return None
    
    if op.login(username, password) != True:
      messagebox.showinfo(title= "Error", message= "Username/Password incorrect.")
      return None
    
    global ACCOUNT
    ACCOUNT = username
    self.parent.refresh()
  
  def register(self):
    username = self.username_text.get("1.0", "end-1c")
    password = self.password_text.get("1.0", "end-1c")
    
    if username == "":
      messagebox.showinfo(title= "Error", message= "Username cannot be empty.")
      return None
    if password == "":
      messagebox.showinfo(title= "Error", message= "Password cannot be empty.")
      return None
    
    if op.register(username, password) == False:
      messagebox.showinfo(title= "Error", message= "Username exists.")
      return None
    
    self.login()

class Report(Frame):
  def __init__(self, *args, **kwargs):
    Frame.__init__(self, *args, **kwargs)
    
    tk.Label(self, text = "Homepage - Work Summary", bg = "grey", anchor = "w").place(x = 50, y = 30, width = 200, height = 20)
    
    self.start_text = tk.Text(self)
    self.start_text.place(x = 110, y = 60, width = 200, height = 20)
    
    self.end_text = tk.Text(self)
    self.end_text.place(x = 410, y = 60, width = 200, height = 20)
    
    self.account_text = tk.Text(self)
    self.account_text.place(x = 710, y = 60, width = 130, height = 20)
    
    tk.Label(self, text = "From", bg = "grey", anchor = "w").place(x = 50, y = 60, width = 50, height = 20)
    tk.Label(self, text = "To", bg = "grey", anchor = "w").place(x = 350, y = 60, width = 50, height = 20)
    tk.Label(self, text = "account", bg = "grey", anchor = "w").place(x = 650, y = 60, width = 50, height = 20)
    
    self.refresh_button = tk.Button(self, text = "Refresh", command = self.refresh)
    self.refresh_button.place(x = 870, y = 60, width = 80, height = 20)
    
    self.tree = ttk.Treeview(self)
    self.tree.place(x = 50, y = 100)
  
  def init(self):
    now = dt.datetime.now()
    now = now.replace(microsecond = 0)
    month_ago = now.replace(day = 1, hour = 0, minute = 0, second = 0, microsecond = 0)
    self.clear()
    self.display(self.start_text, str(month_ago))
    self.display(self.end_text, str(now))
    self.refresh()
  
  def refresh(self):
    start = self.start_text.get("1.0", "end-1c")
    end = self.end_text.get("1.0", "end-1c")
    start = dt.datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
    end = dt.datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
    account = self.account_text.get("1.0", "end-1c")
    data = op.product_report(start, end, account)
    cols = list(data.columns)
    
    self.tree.place_forget()
    self.tree = ttk.Treeview(self, height = 15)
    self.tree.place(x = 50, y = 100)
    
    self.tree["columns"] = cols
    self.tree.column("#0", width=0)
    
    widths = {"uid":50, "name":130, 'ASIN':90, 'Store':90, 'num_tasks':90, 
              'orders':70, 'reviews':70, 'reviews/orders':100, 'goal_reviews':100, 'reviews/goal_reviews':110}
    
    for i in cols:
      self.tree.column(i, width = widths[i], anchor = "w")
      self.tree.heading(i, text = i, anchor = 'w')
    
    for index, row in data.iterrows():
      self.tree.insert("",0,text=index,values=list(row))

class Feed(Frame):
  datatype = None
  
  def __init__(self, parent, *args, **kwargs):
    Frame.__init__(self, parent, *args, **kwargs)
    
    self.comment_label = tk.Label(self, text = "", bg = "grey", anchor = "w")
    self.comment_label.place(x = 30, y = 30, width = 700, height = 20)
    
    self.input_text = tk.Text(self)
    self.input_text.place(x = 30, y = 60, width = 700, height = 370)
    
    self.submit_button = ttk.Button(self, text="Submit", command = self.submit)
    self.submit_button.place(x = 850, y = 250, height = 30, width = 95)
    
    self.clear_button = ttk.Button(self, text="Clear", command = self.clear)
    self.clear_button.place(x = 850, y = 290, height = 30, width = 95)
    
    self.quit_button = ttk.Button(self, text="Quit", command = self.quit)
    self.quit_button.place(x = 850, y = 330, height = 30, width = 95)
  
  def refresh(self):
    self.clear()
    string_ = "    ".join(self.datatype.required)
    self.comment_label.configure(text = string_)
  
  def submit(self):
    string_ = self.input_text.get("1.0","end-1c")
    self.input_text.delete('1.0', "end")
    remaining = op.feed(self.datatype, string_)
    self.input_text.insert('1.0', remaining)

class Admin(Frame):
  results = []
  selected = None
  
  def __init__(self, parent, *args, **kwargs):
    Frame.__init__(self, parent, *args, **kwargs)
    
    self.search_text = tk.Text(self)
    self.search_text.place(x = 50, y = 50, width = 500, height = 25)
    
    self.search_combobox = ttk.Combobox(self)
    self.search_combobox.place(x = 560, y = 50, width = 100, height = 25)
    self.search_combobox['values'] = ['Accounts', 'Gmails', 'Addresses', 'BankCards', 'Buyers', 'Products', 'Orders', "Reviews"]
    self.search_combobox.current(0)
    
    self.search_button = ttk.Button(self, text = "Search", command = self.search)
    self.search_button.place(x = 670, y = 50, width = 100, height = 25)
    
    self.search_listbox = tk.Listbox(self)
    self.search_listbox.place(x = 50, y = 100, width = 700, height = 300)
    
    self.check_button = ttk.Button(self, text="Check", command = self.check)
    self.check_button.place(x = 850, y = 290, height = 30, width = 95)
    
    self.quit_button = ttk.Button(self, text="Quit", command = self.quit)
    self.quit_button.place(x = 850, y = 330, height = 30, width = 95)
  
  def search(self):
    string_ = self.search_text.get("1.0","end-1c")
    datatype = {"Gmails":op.gmail, "Addresses":op.address, "BankCards":op.bankcard, "Reviews":op.review, 
                "Buyers":op.buyer, "Products":op.product, "Orders":op.order, "Accounts":op.account}[self.search_combobox.get()]
    self.results = op.search(datatype, string_)
    self.search_listbox.delete(0, "end")
    for e, key in self.results:
      if key == "uid": value = e.uid
      else: value = e.get(key)
      self.search_listbox.insert("end", e.symbol() + "\t\t[" + str(key) + "] " + str(value))
  
  def check(self):
    self.selected = self.results[self.search_listbox.curselection()[0]][0]
    self.parent.checkframe.entry = self.selected
    self.parent.checkframe.refresh()
    self.parent.checkframe.place(x = 0, y = 30)

class Check(Frame):
  entry = None
  
  def __init__(self, parent, *args, **kwargs):
    Frame.__init__(self, parent, *args, **kwargs)
    
    self.info_text = tk.Text(self); 
    self.info_text.place(x = 50, y = 50, width = 650, height = 310)
    self.info_text.configure(tabs = "6c")
    
    self.commit_button = ttk.Button(self, text="Commit Change", command = self.commit)
    self.commit_button.place(x = 840, y = 290, height = 30, width = 105)
    
    self.quit_button = ttk.Button(self, text="Quit", command = self.quit)
    self.quit_button.place(x = 840, y = 330, height = 30, width = 105)
  
  def refresh(self):
    self.display(self.info_text, self.entry.str())
  
  def commit(self):
    string_ = self.info_text.get("1.0", "end-1c")
    op.commit(self.entry, string_)

class Buyer(Frame):
  gm = None
  ad = None
  bc = None
  br = None
  
  def __init__(self, parent, *args, **kwargs):
    Frame.__init__(self, parent, *args, **kwargs)
    
    self.gmail_text = tk.Text(self, state = "disabled"); 
    self.gmail_text.place(x = 150, y = 50, width = 250, height = 20)
    self.gmail_text.bind("<Button-1>", self.copy)
    
    self.gmail_password_text = tk.Text(self); 
    self.gmail_password_text.place(x = 150, y = 90, width = 250, height = 20)
    self.gmail_password_text.bind("<Button-1>", self.copy)
    
    self.name_text = tk.Text(self); 
    self.name_text.place(x = 150, y = 130, width = 250, height = 20)
    self.name_text.bind("<Button-1>", self.copy)
    
    self.address_text = tk.Text(self, state = "disabled"); 
    self.address_text.place(x = 150, y = 170, width = 250, height = 20)
    self.address_text.bind("<Button-1>", self.copy)
    
    self.city_text = tk.Text(self, state = "disabled"); 
    self.city_text.place(x = 150, y = 210, width = 100, height = 20)
    self.city_text.bind("<Button-1>", self.copy)
    
    self.state_text = tk.Text(self, state = "disabled"); 
    self.state_text.place(x = 300, y = 210, width = 100, height = 20)
    self.state_text.bind("<Button-1>", self.copy)
    
    self.zip_text = tk.Text(self, state = "disabled"); 
    self.zip_text.place(x = 150, y = 250, width = 100, height = 20)
    self.zip_text.bind("<Button-1>", self.copy)
    
    self.phone_text = tk.Text(self, state = "disabled"); 
    self.phone_text.place(x = 300, y = 250, width = 100, height = 20)
    self.phone_text.bind("<Button-1>", self.copy)
    
    self.bankcard_text = tk.Text(self, state = "disabled"); 
    self.bankcard_text.place(x = 150, y = 290, width = 250, height = 20)
    self.bankcard_text.bind("<Button-1>", self.copy)
    
    self.expiration_text = tk.Text(self, state = "disabled"); 
    self.expiration_text.place(x = 150, y = 330, width = 250, height = 20)
    self.expiration_text.bind("<Button-1>", self.copy)
    
    tk.Label(self, text = "Gmail", bg = "grey").place(x = 50, y = 50, width = 100, height = 20)
    tk.Label(self, text = "Gmail Password", bg = "grey").place(x = 50, y = 90, width = 100, height = 20)
    tk.Label(self, text = "Name", bg = "grey").place(x = 50, y = 130, width = 100, height = 20)
    tk.Label(self, text = "Address", bg = "grey").place(x = 50, y = 170, width = 100, height = 20)
    tk.Label(self, text = "City / State", bg = "grey").place(x = 50, y = 210, width = 100, height = 20)
    tk.Label(self, text = "Zip / Phone", bg = "grey").place(x = 50, y = 250, width = 100, height = 20)
    tk.Label(self, text = "Bank Card", bg = "grey").place(x = 50, y = 290, width = 100, height = 20)
    tk.Label(self, text = "Expiration", bg = "grey").place(x = 50, y = 330, width = 100, height = 20)
    
    self.password_text = tk.Text(self, state = "disabled"); 
    self.password_text.place(x = 540, y = 170, width = 200, height = 20)
    self.password_text.bind("<Button-1>", self.copy)
    
    self.uid_text = tk.Text(self, state = "disabled"); 
    self.uid_text.place(x = 540, y = 210, width = 200, height = 20)
    self.uid_text.bind("<Button-1>", self.copy)
    
    tk.Label(self, text = "Password", bg = "grey").place(x = 440, y = 170, width = 100, height = 20)
    tk.Label(self, text = "UID", bg = "grey").place(x = 440, y = 210, width = 100, height = 20)
    
    self.new_button = ttk.Button(self, text="New", command = self.new)
    self.new_button.place(x = 850, y = 210, height = 30, width = 95)
    
    self.submit_button = ttk.Button(self, text="Submit", command = self.submit)
    self.submit_button.place(x = 850, y = 250, height = 30, width = 95)
    
    self.skip_button = ttk.Button(self, text="Skip", command = self.skip)
    self.skip_button.place(x = 850, y = 290, height = 30, width = 95)
    
    self.quit_button = ttk.Button(self, text="Quit", command = self.quit)
    self.quit_button.place(x = 850, y = 330, height = 30, width = 95)
  
  def refresh(self):
    self.clear()
  
  def new(self):
    if self.br != None: return None
    
    self.gm, self.ad, self.bc, self.br = op.open_buyer()
    if self.br == None:
      messagebox.showinfo(title= "Error", message= "No available gmail/address/bankcard.")
      return None
    
    self.display(self.gmail_text, self.gm.get("Gmail"))
    self.display(self.gmail_password_text, self.gm.get("Password"))
    self.display(self.name_text, self.ad.get("RecipientName"))
    self.display(self.address_text, self.ad.get("Address1"))
    self.display(self.city_text, self.ad.get("City"))
    self.display(self.state_text, self.ad.get("State"))
    self.display(self.zip_text, self.ad.get("Zip"))
    self.display(self.phone_text, self.ad.get("PhoneNumber"))
    self.display(self.bankcard_text, self.bc.get("BankCard"))
    self.display(self.expiration_text, self.bc.get("BankCardExpirationDate"))
    
    pwd = self.br.get("AmazonPassword")
    self.display(self.password_text, pwd)
    self.display(self.uid_text, "B" + str(self.br.uid))
  
  def submit(self):
    if self.br == None: return None
    
    new_password = self.gmail_password_text.get("1.0", "end-1c")
    op.commit(self.gm, "Password\t" + new_password)
    
    new_name = self.name_text.get("1.0", "end-1c")
    op.commit(self.ad, "RecipientName\t" + new_name)
    
    global ACCOUNT
    op.open_buyer_confirm(self.gm, self.ad, self.bc, self.br, ACCOUNT)
    self.gm = None
    self.ad = None
    self.bc = None
    self.br = None
    self.clear()
  
  def skip(self):
    if self.br == None: return None
    op.open_buyer_abort(self.gm, self.ad, self.bc, self.br)
    self.gm = None
    self.ad = None
    self.bc = None
    self.br = None
    self.clear()

class PreOrder(Frame):
  def __init__(self, parent, *args, **kwargs):
    Frame.__init__(self, parent, *args, **kwargs)
    
    self.scale1 = tk.Scale(self, orient = "horizontal", length = 500)
    self.scale1.place(x = 150, y = 50)
    
    self.scale2 = tk.Scale(self, orient = "horizontal", length = 500)
    self.scale2.place(x = 150, y = 100)
    
    self.scale3 = tk.Scale(self, orient = "horizontal", length = 500)
    self.scale3.place(x = 150, y = 150)
    
    self.scale4 = tk.Scale(self, orient = "horizontal", length = 500)
    self.scale4.place(x = 150, y = 200)
    
    self.scale5 = tk.Scale(self, orient = "horizontal", length = 500)
    self.scale5.place(x = 150, y = 250)
    
    self.scale6 = tk.Scale(self, orient = "horizontal", length = 500)
    self.scale6.place(x = 150, y = 300)
    
    tk.Label(self, text = "Other", bg = "grey").place(x = 50, y = 60, width = 100, height = 20)
    tk.Label(self, text = "PP01", bg = "grey").place(x = 50, y = 110, width = 100, height = 20)
    tk.Label(self, text = "PP02", bg = "grey").place(x = 50, y = 160, width = 100, height = 20)
    tk.Label(self, text = "PP03", bg = "grey").place(x = 50, y = 210, width = 100, height = 20)
    tk.Label(self, text = "Other2", bg = "grey").place(x = 50, y = 260, width = 100, height = 20)
    tk.Label(self, text = "PP04", bg = "grey").place(x = 50, y = 310, width = 100, height = 20)
    
    self.max1_label = tk.Label(self, text = "0", bg = "grey")
    self.max1_label.place(x = 660, y = 60, width = 60, height = 20)
    
    self.max2_label = tk.Label(self, text = "0", bg = "grey")
    self.max2_label.place(x = 660, y = 110, width = 60, height = 20)
    
    self.max3_label = tk.Label(self, text = "0", bg = "grey")
    self.max3_label.place(x = 660, y = 160, width = 60, height = 20)
    
    self.max4_label = tk.Label(self, text = "0", bg = "grey")
    self.max4_label.place(x = 660, y = 210, width = 60, height = 20)
    
    self.max5_label = tk.Label(self, text = "0", bg = "grey")
    self.max5_label.place(x = 660, y = 260, width = 60, height = 20)
    
    self.max6_label = tk.Label(self, text = "0", bg = "grey")
    self.max6_label.place(x = 660, y = 310, width = 60, height = 20)
   
    self.start_button = ttk.Button(self, text="Start Working", command = self.start)
    self.start_button.place(x = 850, y = 280, height = 30, width = 95)
    
    self.quit_button = ttk.Button(self, text="Quit", command = self.quit)
    self.quit_button.place(x = 850, y = 330, height = 30, width = 95)
  
  def refresh(self):
    self.o1, self.o2, self.o3, self.o4, self.o5, self.o6 = op.orderable_buyers()
    self.scale1.configure(to = len(self.o1))
    self.scale2.configure(to = len(self.o2))
    self.scale3.configure(to = len(self.o3))
    self.scale4.configure(to = len(self.o4))
    self.scale5.configure(to = len(self.o5))
    self.scale6.configure(to = len(self.o6))
    
    self.max1_label.configure(text = str(len(self.o1)))
    self.max2_label.configure(text = str(len(self.o2)))
    self.max3_label.configure(text = str(len(self.o3)))
    self.max4_label.configure(text = str(len(self.o4)))
    self.max5_label.configure(text = str(len(self.o5)))
    self.max6_label.configure(text = str(len(self.o6)))
  
  def start(self):
    buyers = []
    buyers += list(np.random.choice(self.o1, self.scale1.get(), replace = False))
    buyers += list(np.random.choice(self.o2, self.scale2.get(), replace = False))
    buyers += list(np.random.choice(self.o3, self.scale3.get(), replace = False))
    buyers += list(np.random.choice(self.o4, self.scale4.get(), replace = False))
    buyers += list(np.random.choice(self.o5, self.scale5.get(), replace = False))
    buyers += list(np.random.choice(self.o6, self.scale6.get(), replace = False))
    
    if buyers == []: return None
    self.parent.refresh()
    self.parent.orderframe.place(x = 0, y = 30)
    self.parent.orderframe.buyers = buyers
    self.parent.orderframe.init()

class Order(Frame):
  buyers = []
  products = []
  tmp = None
  img = None
  
  def __init__(self, parent, *args, **kwargs):
    Frame.__init__(self, parent, *args, **kwargs)
    
    self.uid_text = tk.Text(self); 
    self.uid_text.place(x = 150, y = 50, width = 250, height = 20)
    self.uid_text.bind("<Button-1>", self.copy)
    
    self.password_text = tk.Text(self); 
    self.password_text.place(x = 150, y = 80, width = 250, height = 20)
    self.password_text.bind("<Button-1>", self.copy)
    
    self.gmail_text = tk.Text(self); 
    self.gmail_text.place(x = 150, y = 110, width = 250, height = 20)
    self.gmail_text.bind("<Button-1>", self.copy)
    
    self.gmail_password_text = tk.Text(self); 
    self.gmail_password_text.place(x = 150, y = 140, width = 250, height = 20)
    self.gmail_password_text.bind("<Button-1>", self.copy)
    
    self.name_text = tk.Text(self); 
    self.name_text.place(x = 150, y = 170, width = 250, height = 20)
    self.name_text.bind("<Button-1>", self.copy)
    
    self.address_text = tk.Text(self); 
    self.address_text.place(x = 150, y = 200, width = 250, height = 20)
    self.address_text.bind("<Button-1>", self.copy)
    
    self.city_text = tk.Text(self); 
    self.city_text.place(x = 150, y = 230, width = 100, height = 20)
    self.city_text.bind("<Button-1>", self.copy)
    
    self.state_text = tk.Text(self); 
    self.state_text.place(x = 300, y = 230, width = 100, height = 20)
    self.state_text.bind("<Button-1>", self.copy)
    
    self.zip_text = tk.Text(self); 
    self.zip_text.place(x = 150, y = 260, width = 100, height = 20)
    self.zip_text.bind("<Button-1>", self.copy)
    
    self.phone_text = tk.Text(self); 
    self.phone_text.place(x = 300, y = 260, width = 100, height = 20)
    self.phone_text.bind("<Button-1>", self.copy)
    
    self.bankcard_text = tk.Text(self); 
    self.bankcard_text.place(x = 150, y = 290, width = 250, height = 20)
    self.bankcard_text.bind("<Button-1>", self.copy)
    
    self.expiration_text = tk.Text(self); 
    self.expiration_text.place(x = 150, y = 320, width = 250, height = 20)
    self.expiration_text.bind("<Button-1>", self.copy)
    
    tk.Label(self, text = "UID", bg = "grey").place(x = 50, y = 50, width = 100, height = 20)
    tk.Label(self, text = "Password", bg = "grey").place(x = 50, y = 80, width = 100, height = 20)
    tk.Label(self, text = "Gmail", bg = "grey").place(x = 50, y = 110, width = 100, height = 20)
    tk.Label(self, text = "Gmail Password", bg = "grey").place(x = 50, y = 140, width = 100, height = 20)
    tk.Label(self, text = "Name", bg = "grey").place(x = 50, y = 170, width = 100, height = 20)
    tk.Label(self, text = "Address", bg = "grey").place(x = 50, y = 200, width = 100, height = 20)
    tk.Label(self, text = "City / State", bg = "grey").place(x = 50, y = 230, width = 100, height = 20)
    tk.Label(self, text = "Zip / Phone", bg = "grey").place(x = 50, y = 260, width = 100, height = 20)
    tk.Label(self, text = "Bank Card", bg = "grey").place(x = 50, y = 290, width = 100, height = 20)
    tk.Label(self, text = "Expiration", bg = "grey").place(x = 50, y = 320, width = 100, height = 20)
    
    self.keyword_text = tk.Text(self); 
    self.keyword_text.place(x = 530, y = 230, width = 180, height = 20)
    self.keyword_text.bind("<Button-1>", self.copy)
    
    self.store_text = tk.Text(self); 
    self.store_text.place(x = 530, y = 260, width = 180, height = 20)
    self.store_text.bind("<Button-1>", self.copy)
    
    self.product_name_text = tk.Text(self); 
    self.product_name_text.place(x = 530, y = 290, width = 180, height = 20)
    self.product_name_text.bind("<Button-1>", self.copy)
    
    self.asin_text = tk.Text(self); 
    self.asin_text.place(x = 530, y = 320, width = 180, height = 20)
    self.asin_text.bind("<Button-1>", self.copy)
    
    tk.Label(self, text = "Key Word", bg = "grey").place(x = 430, y = 230, width = 100, height = 20)
    tk.Label(self, text = "Store", bg = "grey").place(x = 430, y = 260, width = 100, height = 20)
    tk.Label(self, text = "Product", bg = "grey").place(x = 430, y = 290, width = 100, height = 20)
    tk.Label(self, text = "ASIN", bg = "grey").place(x = 430, y = 320, width = 100, height = 20)
    
    self.progressbar = ttk.Progressbar(self, length = 900)
    self.progressbar.configure(maximum = len(self.buyers), value = 0)
    self.progressbar.place(x = 50, y = 10)
    
    self.tmp = tk.StringVar()
    self.product_combobox = ttk.Combobox(self, textvariable = self.tmp);
    self.product_combobox.place(x = 430, y = 50, width = 280)
    self.tmp.trace("w", self.show_product)
    
    self.ordernumber_entry = tk.Entry(self); 
    self.ordernumber_entry.place(x = 50, y = 370, width = 300)
    self.ordernumber_entry.bind("<Button-1>", self.input)
    
    self.cost_entry = tk.Entry(self); 
    self.cost_entry.place(x = 360, y = 370, width = 100)
    self.cost_entry.bind("<Button-1>", self.input)
    
    self.img = tk.PhotoImage()
    self.image_label = tk.Label(self, image = self.img);
    self.image_label.place(x = 530, y = 80, width = 140, height = 140)
    
    self.submit_button = ttk.Button(self, text="Submit", command = self.submit)
    self.submit_button.place(x = 850, y = 230, height = 30, width = 95)
    
    self.skip_button = ttk.Button(self, text="Skip", command = self.skip)
    self.skip_button.place(x = 850, y = 270, height = 30, width = 95)
    
    self.quit_button = ttk.Button(self, text="Quit", command = self.quit)
    self.quit_button.place(x = 850, y = 310, height = 30, width = 95)
  
  def init(self):
    self.progressbar.configure(maximum = len(self.buyers), value = 0)
    self.show_buyer()
  
  def show_buyer(self):
    br = self.buyers[self.progressbar['value']]
    
    self.display(self.uid_text, "B" + str(br.uid))
    self.display(self.password_text, br.get("AmazonPassword"))
    self.display(self.gmail_text, op.gmail.query(br.gmail).get("Gmail"))
    self.display(self.gmail_password_text, op.gmail.query(br.gmail).get("Password"))
    self.display(self.name_text, op.address.query(br.address).get("RecipientName"))
    self.display(self.address_text, op.address.query(br.address).get("Address1"))
    self.display(self.city_text, op.address.query(br.address).get("City"))
    self.display(self.state_text, op.address.query(br.address).get("State"))
    self.display(self.zip_text, op.address.query(br.address).get("Zip"))
    self.display(self.phone_text, op.address.query(br.address).get("PhoneNumber"))
    self.display(self.bankcard_text, op.bankcard.query(br.bankcard).get("BankCard"))
    self.display(self.expiration_text, op.bankcard.query(br.bankcard).get("BankCardExpirationDate"))
    
    self.products = op.orderable_products(br)
    self.product_combobox['values'] = [x.symbol() for x in self.products]
    if self.products != []:
      self.product_combobox.current(0)
    
    self.ordernumber_entry.configure(fg = "grey")
    self.ordernumber_entry.delete(0, "end")
    self.ordernumber_entry.insert("end", "Order Number")
    
    self.cost_entry.configure(fg = "grey")
    self.cost_entry.delete(0, "end")
    self.cost_entry.insert("end", "Cost")
  
  def show_product(self, var, indx, mode):
    pd = self.products[self.product_combobox.current()]
    
    self.display(self.keyword_text, pd.get("keyword"))
    self.display(self.store_text, pd.get("Store"))
    self.display(self.product_name_text, pd.get("name"))
    self.display(self.asin_text, pd.get("ASIN"))
    
    self.image_label.configure(image = tk.PhotoImage())
    if pd.get("image") != None:
      self.img = ImageTk.PhotoImage(Image.open("images/" + pd.get("image")).resize((140, 140)))
      self.image_label.configure(image = self.img)
  
  def input(self, event):
    event.widget.configure(fg = "black")
    event.widget.delete(0, "end")
  
  def submit(self):
    br = self.buyers[self.progressbar['value']]
    pd = self.products[self.product_combobox.current()]
    ordernumber = self.ordernumber_entry.get() # other orders do not have ordernumber !!
    cost = self.cost_entry.get()
    
    if (self.ordernumber_entry.get() in ["", "Order Number"] or 
        self.cost_entry.get() in ["", "Cost"]) and pd.uid != -1: 
      messagebox.showinfo(title= "Error", message= "Make sure Order Number and Cost are typed in.")
      return None
    
    if (self.cost_entry.get() in ["", "Cost"]) and pd.uid == -1: 
      messagebox.showinfo(title= "Error", message= "Make sure Cost is typed in.")
      return None
    
    global ACCOUNT
    op.buy(br, pd, ordernumber, cost, ACCOUNT)
    self.skip()
  
  def skip(self):
    self.progressbar['value'] += 1
    if self.progressbar['value'] == self.progressbar['maximum']:
      self.quit()
    else:
      self.show_buyer()

class PreReview(Frame):
  products = []
  orders_ = {}
  selection = {}
  tmp = None
  img = None
  
  def __init__(self, parent, *args, **kwargs):
    Frame.__init__(self, parent, *args, **kwargs)
    
    self.listbox = tk.Listbox(self)
    self.listbox.place(x = 470, y = 50, height = 330, width = 230)
    
    self.tmp = tk.StringVar()
    self.combobox = ttk.Combobox(self, textvariable = self.tmp)
    self.combobox.place(x = 50, y = 50, width = 300)
    self.tmp.trace("w", self.max_num)
    
    self.img = tk.PhotoImage()
    self.image_label = tk.Label(self, image = self.img);
    self.image_label.place(x = 125, y = 110, width = 150, height = 150)
    
    self.scale = tk.Scale(self, length = 300, orient = "horizontal")
    self.scale.place(x = 50, y = 300)
    
    self.max_label = tk.Label(self, text = "0", bg = "grey")
    self.max_label.place(x = 360, y = 310, width = 60, height = 20)
    
    self.add_button = ttk.Button(self, text="Add", command = self.add)
    self.add_button.place(x = 50, y = 350, height = 30, width = 95)
    
    self.start_button = ttk.Button(self, text="Start Working", command = self.start)
    self.start_button.place(x = 850, y = 280, height = 30, width = 95)
    
    self.quit_button = ttk.Button(self, text="Quit", command = self.quit)
    self.quit_button.place(x = 850, y = 330, height = 30, width = 95)
    
    self.selection = {}
  
  def refresh(self):
    self.orders_ = op.reviewable_orders()
    if self.orders_ == {}:
      return None
    self.products = [op.product.query(i) for i in self.orders_.keys()]
    self.combobox['values'] = [pd.symbol() for pd in self.products]
    self.combobox.current(0)
    self.selection = {key:0 for key in self.orders_}
    self.listbox.delete("0", "end")
  
  def max_num(self, var, indx, mode):
    pd = self.products[self.combobox.current()]
    self.scale.configure(to = min(pd.get("num_daily_reviews"), len(self.orders_[pd.uid])))
    self.max_label.configure(text = str(min(pd.get("num_daily_reviews"), len(self.orders_[pd.uid]))))
    
    self.image_label.configure(image = tk.PhotoImage())
    if pd.get("image") != None:
      self.img = ImageTk.PhotoImage(Image.open("images/" + pd.get("image")).resize((140, 140)))
      self.image_label.configure(image = self.img)
  
  def show_selection(self):
    self.listbox.delete("0", "end")
    for key, value in self.selection.items():
      if value == 0:
        continue
      self.listbox.insert("end", op.product.query(key).symbol() + " * " + str(value))
  
  def add(self):
    pd = self.products[self.combobox.current()]
    num = self.scale.get()
    self.selection[pd.uid] += num
    limit = int(self.scale['to'])
    if self.selection[pd.uid] > limit:
      self.selection[pd.uid] = limit
    self.show_selection()
  
  def start(self):
    buffer = []
    for key, value in self.selection.items():
      if value == 0:
        continue
      ods = list(np.random.choice(self.orders_[key], value, replace = False))
      buffer += ods
    if buffer == []: return None
    self.parent.refresh()
    self.parent.reviewframe.orders = buffer
    self.parent.reviewframe.place(x = 0, y = 30)
    self.parent.reviewframe.init()

class Review(Frame):
  orders = []
  review = None
  
  def __init__(self, parent, *args, **kwargs):
    Frame.__init__(self, parent, *args, **kwargs)
    
    self.uid_text = tk.Text(self); 
    self.uid_text.place(x = 150, y = 100, width = 280, height = 20)
    self.uid_text.bind("<Button-1>", self.copy)
    
    self.password_text = tk.Text(self); 
    self.password_text.place(x = 150, y = 130, width = 280, height = 20)
    self.password_text.bind("<Button-1>", self.copy)
    
    self.gmail_text = tk.Text(self); 
    self.gmail_text.place(x = 150, y = 160, width = 280, height = 20)
    self.gmail_text.bind("<Button-1>", self.copy)
    
    self.gmail_password_text = tk.Text(self); 
    self.gmail_password_text.place(x = 150, y = 190, width = 280, height = 20)
    self.gmail_password_text.bind("<Button-1>", self.copy)
    
    tk.Label(self, text = "UID", bg = "grey").place(x = 50, y = 100, width = 100, height = 20)
    tk.Label(self, text = "Password", bg = "grey").place(x = 50, y = 130, width = 100, height = 20)
    tk.Label(self, text = "Gmail", bg = "grey").place(x = 50, y = 160, width = 100, height = 20)
    tk.Label(self, text = "Gmail Password", bg = "grey").place(x = 50, y = 190, width = 100, height = 20)
    
    self.title_text = tk.Text(self); 
    self.title_text.place(x = 150, y = 250, width = 280, height = 20)
    self.title_text.bind("<Button-1>", self.copy)
    
    self.content_text = tk.Text(self);
    self.content_text.place(x = 150, y = 280, width = 280, height = 100)
    self.content_text.bind("<Button-1>", self.copy)
    
    tk.Label(self, text = "Title", bg = "grey").place(x = 50, y = 250, width = 100, height = 20)
    tk.Label(self, text = "Content", bg = "grey").place(x = 50, y = 280, width = 100, height = 20)
    
    self.progressbar = ttk.Progressbar(self, length = 660)
    self.progressbar.configure(maximum = 100, value = 0)
    self.progressbar.place(x = 50, y = 50)
    
    self.img = tk.PhotoImage()
    self.image_label = tk.Label(self, image = self.img);
    self.image_label.place(x = 500, y = 100, width = 210, height = 210)
    
    self.submit_button = ttk.Button(self, text="Submit", command = self.submit)
    self.submit_button.place(x = 850, y = 250, height = 30, width = 95)
    
    self.skip_button = ttk.Button(self, text="Skip", command = self.skip)
    self.skip_button.place(x = 850, y = 290, height = 30, width = 95)
    
    self.quit_button = ttk.Button(self, text="Quit", command = self.quit)
    self.quit_button.place(x = 850, y = 330, height = 30, width = 95)
  
  def init(self):
    self.progressbar.configure(maximum = len(self.orders), value = 0)
    if self.orders == []:
      return
    self.show_order()
    self.show_review()
  
  def show_order(self):
    od = self.orders[self.progressbar['value']]
    br = op.buyer.query(od.buyer)
    pd = op.product.query(od.product)
    
    self.display(self.uid_text, "B" + str(br.uid))
    self.display(self.password_text, br.get("AmazonPassword"))
    self.display(self.gmail_text, op.gmail.query(br.gmail).get("Gmail"))
    self.display(self.gmail_password_text, op.gmail.query(br.gmail).get("Password"))
    
    self.image_label.configure(image = tk.PhotoImage())
    if pd.get("image") != None:
      self.img = ImageTk.PhotoImage(Image.open("images/" + pd.get("image")).resize((210, 210)))
      self.image_label.configure(image = self.img)
  
  def show_review(self):
    order = self.orders[self.progressbar['value']]
    pd = op.product.query(order.product)
    rvs = op.suitable_reviews(pd)
    self.review = list(np.random.choice(rvs, 1))[0]
    self.title_text.delete("1.0", "end")
    self.content_text.delete("1.0", "end")
    self.title_text.insert("end", self.review.get("Title"))
    self.content_text.insert("end", self.review.get("Content"))
  
  def submit(self):
    title = self.title_text.get("1.0", "end-1c")
    content = self.content_text.get("1.0", "end-1c")
    string_ = "Title\t" + title + "\nContent\t" + content
    od = self.orders[self.progressbar['value']]
    
    op.submit_review(od, self.review, string_)
    self.skip()
  
  def skip(self):
    self.progressbar['value'] += 1
    if self.progressbar['value'] == self.progressbar['maximum']:
      self.quit()
    else:
      self.show_order()
      self.show_review()

if __name__ == '__main__':
  abspath = os.path.abspath(__file__)
  dname = os.path.dirname(abspath)
  os.chdir(dname)
  
  tmhelper = TMhelper()
  tmhelper.mainloop()

