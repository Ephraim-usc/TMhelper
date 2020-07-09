
import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import datetime as dt
import numpy as np

import requests
r = requests.get("https://raw.github.com/Ephraim-usc/TMhelper/master/operations.py")
with open("operations.py", "w", encoding="utf-8") as f:
  f.write(r.text)

import operations as op



class TMhelper(tk.Tk):
  def __init__(self, *args, **kwargs):
    tk.Tk.__init__(self, *args, **kwargs)
    self.title('TMhelper')
    self.geometry("800x500")
    
    self.menuframe = Menu(self)
    self.feedframe = Feed(self)
    self.adminframe = Admin(self)
    self.buyerframe = Buyer(self)
    self.preorderframe = PreOrder(self)
    self.orderframe = Order(self)
    self.prereviewframe = PreReview(self)
    self.reviewframe = Review(self)
    self.checkframe = Check(self)
  
  def refresh(self):
    other_frames = [w for w in self.winfo_children() if w.winfo_y() > 0]
    for w in other_frames: w.place_forget()

class Menu(tk.Frame):
  feed = None
  phone = None
  
  def __init__(self, parent, *args, **kwargs):
    tk.Frame.__init__(self, parent, *args, **kwargs)
    self.parent = parent
    self.configure(width = 800, height = 30)
    self.place(x= 0, y = 0)
    self['bg'] = 'grey'
    
    self.feed = tk.StringVar()
    self.phone = tk.StringVar()
    
    self.login_button = ttk.Button(self, text="Login")
    self.login_button.place(x = 0, y = 0, height = 30, width = 95)
    
    self.admin_button = ttk.Button(self, text="Admin", command = self.admin_event)
    self.admin_button.place(x = 100, y = 0, height = 30, width = 95)
    
    self.buyer_button = ttk.Button(self, text="Buyer", command = self.buyer_event)
    self.buyer_button.place(x = 200, y = 0, height = 30, width = 95)
    
    self.order_button = ttk.Button(self, text="Order", command = self.pre_order_event)
    self.order_button.place(x = 300, y = 0, height = 30, width = 95)
    
    self.review_button = ttk.Button(self, text="Review", command = self.pre_review_event)
    self.review_button.place(x = 400, y = 0, height = 30, width = 95)
    
    self.feed_combobox = ttk.Combobox(self, textvariable = self.feed)
    self.feed_combobox['values'] = ['Import Data', 'Gmails', 'Addresses', 'BankCards', 'Reviews', 'Products']
    self.feed_combobox.current(0)
    self.feed_combobox.place(x = 500, y = 2, height = 40, width = 145)
    
    self.phone_combobox = ttk.Combobox(self, textvariable = self.phone)
    self.phone_combobox['values'] = ['Select Phone', 'iphone1', 'iphone2', 'android']
    self.phone_combobox.current(0)
    self.phone_combobox.place(x = 650, y = 2, height = 40, width = 145)
    
    self.feed.trace("w", self.feed_write_event)
  
  def login_event(self):
    self.parent.refresh()
    self.parent.loginframe.place(x = 0, y = 30)
  
  def admin_event(self):
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
    if self.feed.get() != "Import Data":
      self.parent.feedframe.place(x = 0, y = 30)


class Feed(tk.Frame):
  def __init__(self, parent, *args, **kwargs):
    tk.Frame.__init__(self, parent, *args, **kwargs)
    self.parent = parent
    self.configure(width = 800, height = 470)
    self['bg'] = 'grey'
    
    self.input_text = tk.Text(self)
    self.input_text.place(x = 30, y = 30, width = 600, height = 400)
    
    self.submit_button = ttk.Button(self, text="Submit", command = self.submit)
    self.submit_button.place(x = 650, y = 250, height = 30, width = 95)
    
    self.clear_button = ttk.Button(self, text="Clear", command = self.clear)
    self.clear_button.place(x = 650, y = 290, height = 30, width = 95)
    
    self.quit_button = ttk.Button(self, text="Quit", command = self.quit)
    self.quit_button.place(x = 650, y = 330, height = 30, width = 95)
  
  def submit(self):
    string_ = self.input_text.get("1.0","end-1c")
    self.input_text.delete('1.0', tk.END)
    datatype = {"Gmails":op.gmail, "Addresses":op.address, "Reviews":op.review,
                "BankCards":op.bankcard, "Products":op.product}[self.parent.menuframe.feed.get()]
    remaining = op.feed(datatype, string_)
    self.input_text.insert('1.0', remaining)
  
  def clear(self):
    self.input_text.delete('1.0', tk.END)
  
  def quit(self):
    self.place_forget()

class Admin(tk.Frame):
  results = []
  selected = None
  
  def __init__(self, parent, *args, **kwargs):
    tk.Frame.__init__(self, parent, *args, **kwargs)
    self.parent = parent
    self.configure(width = 800, height = 470)
    self['bg'] = 'grey'
    
    self.search_text = tk.Text(self); 
    self.search_text.place(x = 50, y = 50, width = 400, height = 25)
    
    self.search_combobox = ttk.Combobox(self)
    self.search_combobox.place(x = 460, y = 50, width = 100, height = 30)
    self.search_combobox['values'] = ['Gmails', 'Addresses', 'BankCards', 'Buyers', 'Products', 'Orders', "Reviews"]
    self.search_combobox.current(0)
    
    self.search_button = ttk.Button(self, text = "Search", command = self.search)
    self.search_button.place(x = 570, y = 48, width = 100, height = 30)
    
    self.search_listbox = tk.Listbox(self)
    self.search_listbox.place(x = 50, y = 100, width = 600, height = 300)
    
    self.check_button = ttk.Button(self, text="Check", command = self.check)
    self.check_button.place(x = 650, y = 290, height = 30, width = 95)
    
    self.quit_button = ttk.Button(self, text="Quit", command = self.quit)
    self.quit_button.place(x = 650, y = 330, height = 30, width = 95)
  
  def search(self):
    string_ = self.search_text.get("1.0","end-1c")
    datatype = {"Gmails":op.gmail, "Addresses":op.address, "BankCards":op.bankcard, "Reviews":op.review, 
                "Buyers":op.buyer, "Products":op.product, "Orders":op.order}[self.search_combobox.get()]
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
  
  def quit(self):
    self.place_forget()

class Buyer(tk.Frame):
  gm = None
  ad = None
  bc = None
  br = None
  
  def __init__(self, parent, *args, **kwargs):
    tk.Frame.__init__(self, parent, *args, **kwargs)
    self.parent = parent
    self.configure(width = 800, height = 470)
    self['bg'] = 'grey'
    
    self.gmail_text = tk.Text(self); 
    self.gmail_text.place(x = 150, y = 50, width = 250, height = 20)
    self.gmail_text.bind("<Button-1>", self.copy)
    
    self.gmail_password_text = tk.Text(self); 
    self.gmail_password_text.place(x = 150, y = 90, width = 250, height = 20)
    self.gmail_password_text.bind("<Button-1>", self.copy)
    
    self.name_text = tk.Text(self); 
    self.name_text.place(x = 150, y = 130, width = 250, height = 20)
    self.name_text.bind("<Button-1>", self.copy)
    
    self.address_text = tk.Text(self); 
    self.address_text.place(x = 150, y = 170, width = 250, height = 20)
    self.address_text.bind("<Button-1>", self.copy)
    
    self.city_text = tk.Text(self); 
    self.city_text.place(x = 150, y = 210, width = 100, height = 20)
    self.city_text.bind("<Button-1>", self.copy)
    
    self.state_text = tk.Text(self); 
    self.state_text.place(x = 300, y = 210, width = 100, height = 20)
    self.state_text.bind("<Button-1>", self.copy)
    
    self.zip_text = tk.Text(self); 
    self.zip_text.place(x = 150, y = 250, width = 100, height = 20)
    self.zip_text.bind("<Button-1>", self.copy)
    
    self.phone_text = tk.Text(self); 
    self.phone_text.place(x = 300, y = 250, width = 100, height = 20)
    self.phone_text.bind("<Button-1>", self.copy)
    
    self.bankcard_text = tk.Text(self); 
    self.bankcard_text.place(x = 150, y = 290, width = 250, height = 20)
    self.bankcard_text.bind("<Button-1>", self.copy)
    
    self.expiration_text = tk.Text(self); 
    self.expiration_text.place(x = 150, y = 330, width = 250, height = 20)
    self.expiration_text.bind("<Button-1>", self.copy)
    
    self.password_text = tk.Text(self); 
    self.password_text.place(x = 540, y = 50, width = 200, height = 20)
    self.password_text.bind("<Button-1>", self.copy)
    
    self.uid_text = tk.Text(self); 
    self.uid_text.place(x = 540, y = 90, width = 200, height = 20)
    self.uid_text.bind("<Button-1>", self.copy)
    
    tk.Label(self, text = "Gmail", bg = "grey").place(x = 50, y = 50, width = 100, height = 20)
    tk.Label(self, text = "Gmail Password", bg = "grey").place(x = 50, y = 90, width = 100, height = 20)
    tk.Label(self, text = "Name", bg = "grey").place(x = 50, y = 130, width = 100, height = 20)
    tk.Label(self, text = "Address", bg = "grey").place(x = 50, y = 170, width = 100, height = 20)
    tk.Label(self, text = "City / State", bg = "grey").place(x = 50, y = 210, width = 100, height = 20)
    tk.Label(self, text = "Zip / Phone", bg = "grey").place(x = 50, y = 250, width = 100, height = 20)
    tk.Label(self, text = "Bank Card", bg = "grey").place(x = 50, y = 290, width = 100, height = 20)
    tk.Label(self, text = "Expiration", bg = "grey").place(x = 50, y = 330, width = 100, height = 20)
    
    tk.Label(self, text = "Password", bg = "grey").place(x = 440, y = 50, width = 100, height = 20)
    tk.Label(self, text = "UID", bg = "grey").place(x = 440, y = 90, width = 100, height = 20)
    
    self.submit_button = ttk.Button(self, text="New", command = self.new)
    self.submit_button.place(x = 650, y = 210, height = 30, width = 95)
    
    self.submit_button = ttk.Button(self, text="Submit", command = self.submit)
    self.submit_button.place(x = 650, y = 250, height = 30, width = 95)
    
    self.skip_button = ttk.Button(self, text="Skip", command = self.skip)
    self.skip_button.place(x = 650, y = 290, height = 30, width = 95)
    
    self.quit_button = ttk.Button(self, text="Quit", command = self.quit)
    self.quit_button.place(x = 650, y = 330, height = 30, width = 95)
  
  def refresh(self):
    self.gmail_text.configure(state = "normal"); self.gmail_text.delete("1.0", "end") 
    self.gmail_password_text.configure(state = "normal"); self.gmail_password_text.delete("1.0", "end")
    self.name_text.configure(state = "normal"); self.name_text.delete("1.0", "end")
    self.address_text.configure(state = "normal"); self.address_text.delete("1.0", "end")
    self.city_text.configure(state = "normal"); self.city_text.delete("1.0", "end")
    self.state_text.configure(state = "normal"); self.state_text.delete("1.0", "end")
    self.zip_text.configure(state = "normal"); self.zip_text.delete("1.0", "end")
    self.phone_text.configure(state = "normal"); self.phone_text.delete("1.0", "end")
    self.bankcard_text.configure(state = "normal"); self.bankcard_text.delete("1.0", "end")
    self.expiration_text.configure(state = "normal"); self.expiration_text.delete("1.0", "end")
    self.password_text.configure(state = "normal"); self.password_text.delete("1.0", "end")
    self.uid_text.configure(state = "normal"); self.uid_text.delete("1.0", "end")
  
  def copy(self, event):
    self.parent.clipboard_clear()
    self.parent.clipboard_append(event.widget.get("1.0", "end-1c"))
  
  def display(self, widget, string):
    widget.configure(state = "normal")
    widget.delete("1.0", "end")
    widget.insert("1.0", string)
    widget.configure(state = "disabled")
  
  def new(self):
    if self.br != None: return None
    
    self.gm, self.ad, self.bc, self.br = op.open_buyer()
    
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
    op.open_buyer_confirm(self.gm, self.ad, self.bc, self.br)
    self.gm = None
    self.ad = None
    self.bc = None
    self.br = None
    self.refresh()
  
  def skip(self):
    if self.br == None: return None
    op.open_buyer_abort(self.gm, self.ad, self.bc, self.br)
    self.gm = None
    self.ad = None
    self.bc = None
    self.br = None
    self.refresh()
  
  def quit(self):
    self.place_forget()

class PreOrder(tk.Frame):
  def __init__(self, parent, *args, **kwargs):
    tk.Frame.__init__(self, parent, *args, **kwargs)
    self.parent = parent
    self.configure(width = 800, height = 470)
    self['bg'] = 'grey'
    
    self.scale1 = tk.Scale(self, orient = "horizontal", length = 400)
    self.scale1.place(x = 150, y = 50)
    
    self.scale2 = tk.Scale(self, orient = "horizontal", length = 400)
    self.scale2.place(x = 150, y = 100)
    
    self.scale3 = tk.Scale(self, orient = "horizontal", length = 400)
    self.scale3.place(x = 150, y = 150)
    
    self.scale4 = tk.Scale(self, orient = "horizontal", length = 400)
    self.scale4.place(x = 150, y = 200)
    
    self.scale5 = tk.Scale(self, orient = "horizontal", length = 400)
    self.scale5.place(x = 150, y = 250)
    
    self.scale6 = tk.Scale(self, orient = "horizontal", length = 400)
    self.scale6.place(x = 150, y = 300)
    
    tk.Label(self, text = "Other", bg = "grey").place(x = 50, y = 60, width = 100, height = 20)
    tk.Label(self, text = "PP01", bg = "grey").place(x = 50, y = 110, width = 100, height = 20)
    tk.Label(self, text = "PP02", bg = "grey").place(x = 50, y = 160, width = 100, height = 20)
    tk.Label(self, text = "PP03", bg = "grey").place(x = 50, y = 210, width = 100, height = 20)
    tk.Label(self, text = "Other2", bg = "grey").place(x = 50, y = 260, width = 100, height = 20)
    tk.Label(self, text = "PP04", bg = "grey").place(x = 50, y = 310, width = 100, height = 20)
    
    self.max1_label = tk.Label(self, text = "0", bg = "grey")
    self.max1_label.place(x = 560, y = 60, width = 60, height = 20)
    
    self.max2_label = tk.Label(self, text = "0", bg = "grey")
    self.max2_label.place(x = 560, y = 110, width = 60, height = 20)
    
    self.max3_label = tk.Label(self, text = "0", bg = "grey")
    self.max3_label.place(x = 560, y = 160, width = 60, height = 20)
    
    self.max4_label = tk.Label(self, text = "0", bg = "grey")
    self.max4_label.place(x = 560, y = 210, width = 60, height = 20)
    
    self.max5_label = tk.Label(self, text = "0", bg = "grey")
    self.max5_label.place(x = 560, y = 260, width = 60, height = 20)
    
    self.max6_label = tk.Label(self, text = "0", bg = "grey")
    self.max6_label.place(x = 560, y = 310, width = 60, height = 20)
   
    self.start_button = ttk.Button(self, text="Start Working", command = self.start)
    self.start_button.place(x = 650, y = 280, height = 30, width = 95)
    
    self.quit_button = ttk.Button(self, text="Quit", command = self.quit)
    self.quit_button.place(x = 650, y = 330, height = 30, width = 95)
  
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
  
  def quit(self):
    self.place_forget()

class Order(tk.Frame):
  buyers = []
  products = []
  tmp = None
  img = None
  
  def __init__(self, parent, *args, **kwargs):
    tk.Frame.__init__(self, parent, *args, **kwargs)
    self.parent = parent
    self.configure(width = 800, height = 470)
    self['bg'] = 'grey'
    
    self.buyer_text = tk.Text(self); 
    self.buyer_text.place(x = 50, y = 100, width = 250, height = 300)
    
    self.tmp = tk.StringVar()
    self.product_combobox = ttk.Combobox(self, textvariable = self.tmp);
    self.product_combobox.place(x = 310, y = 100, width = 250)
    self.tmp.trace("w", self.show_product)
    
    self.product_text = tk.Text(self); 
    self.product_text.place(x = 310, y = 150, width = 250, height = 250)
    
    self.ordernumber_text = tk.Text(self); 
    self.ordernumber_text.place(x = 50, y = 410, width = 300, height = 30)
    
    self.cost_text = tk.Text(self); 
    self.cost_text.place(x = 360, y = 410, width = 100, height = 30)
    
    self.progressbar = ttk.Progressbar(self, length = 510)
    self.progressbar.configure(maximum = len(self.buyers), value = 0)
    self.progressbar.place(x = 50, y = 50)
    
    self.img = tk.PhotoImage()
    self.image_label = tk.Label(self, image = self.img);
    self.image_label.place(x = 600, y = 50, width = 150, height = 150)
    
    self.submit_button = ttk.Button(self, text="Submit", command = self.submit)
    self.submit_button.place(x = 650, y = 250, height = 30, width = 95)
    
    self.skip_button = ttk.Button(self, text="Skip", command = self.skip)
    self.skip_button.place(x = 650, y = 290, height = 30, width = 95)
    
    self.quit_button = ttk.Button(self, text="Quit", command = self.quit)
    self.quit_button.place(x = 650, y = 330, height = 30, width = 95)
  
  def init(self):
    self.progressbar.configure(maximum = len(self.buyers), value = 0)
    self.show_buyer()
  
  def show_buyer(self):
    br = self.buyers[self.progressbar['value']]
    self.buyer_text.delete("1.0", "end")
    self.buyer_text.insert("1.0", br.str())
    self.products = op.orderable_products(br)
    self.product_combobox['values'] = [x.symbol() for x in self.products]
    self.product_combobox.current(0)
  
  def show_product(self, var, indx, mode):
    pd = self.products[self.product_combobox.current()]
    self.product_text.delete("1.0", "end")
    self.product_text.insert("1.0", pd.str())
    
    self.image_label.configure(image = tk.PhotoImage())
    if pd.get("image") != None:
      self.img = ImageTk.PhotoImage(Image.open(pd.get("image")).resize((150, 150)))
      self.image_label.configure(image = self.img)
  
  def submit(self):
    br = self.buyers[self.progressbar['value']]
    pd = self.products[self.product_combobox.current()]
    ordernumber = self.ordernumber_text.get("1.0", "end-1c")
    cost = self.cost_text.get("1.0", "end-1c")
    op.buy(br, pd, ordernumber, cost)
    self.skip()
  
  def skip(self):
    self.progressbar['value'] += 1
    if self.progressbar['value'] == self.progressbar['maximum']:
      self.quit()
    else:
      self.show_buyer()
  
  def quit(self):
    self.place_forget()

class PreReview(tk.Frame):
  products = []
  orders_ = {}
  selection = {}
  tmp = None
  
  def __init__(self, parent, *args, **kwargs):
    tk.Frame.__init__(self, parent, *args, **kwargs)
    self.parent = parent
    self.configure(width = 800, height = 470)
    self['bg'] = 'grey'
    
    self.listbox = tk.Listbox(self)
    self.listbox.place(x = 470, y = 50, height = 200, width = 230)
    
    self.tmp = tk.StringVar()
    self.combobox = ttk.Combobox(self, textvariable = self.tmp)
    self.combobox.place(x = 50, y = 50, width = 300)
    
    self.scale = tk.Scale(self, length = 300, orient = "horizontal")
    self.scale.place(x = 50, y = 100)
    
    self.start_button = ttk.Button(self, text="Add", command = self.add)
    self.start_button.place(x = 50, y = 150, height = 30, width = 95)
    
    self.start_button = ttk.Button(self, text="Start Working", command = self.start)
    self.start_button.place(x = 650, y = 280, height = 30, width = 95)
    
    self.quit_button = ttk.Button(self, text="Quit", command = self.quit)
    self.quit_button.place(x = 650, y = 330, height = 30, width = 95)
    
    self.selection = {}
    self.tmp.trace("w", self.max_num)
  
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
    pass
  
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
    pass
  
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
  
  def quit(self):
    self.place_forget()

class Review(tk.Frame):
  orders = []
  review = None
  
  def __init__(self, parent, *args, **kwargs):
    tk.Frame.__init__(self, parent, *args, **kwargs)
    self.parent = parent
    self.configure(width = 800, height = 470)
    self['bg'] = 'grey'
    
    self.order_text = tk.Text(self); 
    self.order_text.place(x = 50, y = 100, width = 250, height = 300)
    
    self.title_text = tk.Text(self); 
    self.title_text.place(x = 310, y = 100, width = 250, height = 30)
    
    self.content_text = tk.Text(self); 
    self.content_text.place(x = 310, y = 150, width = 250, height = 250)
    
    self.progressbar = ttk.Progressbar(self, length = 510)
    self.progressbar.configure(maximum = 100, value = 0)
    self.progressbar.place(x = 50, y = 50)
    
    self.image_label = tk.Label(self);
    self.image_label.place(x = 600, y = 50, width = 150, height = 150)
    
    self.submit_button = ttk.Button(self, text="Submit", command = self.submit)
    self.submit_button.place(x = 650, y = 250, height = 30, width = 95)
    
    self.skip_button = ttk.Button(self, text="Skip", command = self.skip)
    self.skip_button.place(x = 650, y = 290, height = 30, width = 95)
    
    self.quit_button = ttk.Button(self, text="Quit", command = self.quit)
    self.quit_button.place(x = 650, y = 330, height = 30, width = 95)
  
  def init(self):
    self.progressbar.configure(maximum = len(self.orders), value = 0)
    if self.orders == []:
      return
    self.show_order()
    self.show_review()
  
  def show_order(self):
    order = self.orders[self.progressbar['value']]
    self.order_text.delete("1.0", "end")
    self.order_text.insert("end", order.str())
  
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
    order = self.orders[self.progressbar['value']]
    op.submit_review(order, self.review)
    self.skip()
  
  def skip(self):
    self.progressbar['value'] += 1
    if self.progressbar['value'] == self.progressbar['maximum']:
      self.quit()
    else:
      self.show_order()
      self.show_review()
  
  def quit(self):
    self.place_forget()

class Check(tk.Frame):
  entry = None
  
  def __init__(self, parent, *args, **kwargs):
    tk.Frame.__init__(self, parent, *args, **kwargs)
    self.parent = parent
    self.configure(width = 800, height = 470)
    self['bg'] = 'grey'
    
    self.info_text = tk.Text(self); 
    self.info_text.place(x = 50, y = 50, width = 500, height = 300)
    self.info_text.configure(tabs = "5c")
    
    self.quit_button = ttk.Button(self, text="Commit Change", command = self.commit)
    self.quit_button.place(x = 650, y = 290, height = 30, width = 95)
    
    self.quit_button = ttk.Button(self, text="Quit", command = self.quit)
    self.quit_button.place(x = 650, y = 330, height = 30, width = 95)
  
  def refresh(self):
    self.info_text.delete("1.0", "end")
    self.info_text.insert("1.0", self.entry.str())
  
  def commit(self):
    string_ = self.info_text.get("1.0", "end-1c")
    op.commit(self.entry, string_)
  
  def quit(self):
    self.place_forget()

tmhelper = TMhelper()
#tmhelper.mainloop()
