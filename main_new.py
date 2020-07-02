import tkinter as tk
import tkinter.ttk as ttk

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

class Menu(tk.Frame):
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
    
    self.admin_button = ttk.Button(self, text="Admin")
    self.admin_button.place(x = 100, y = 0, height = 30, width = 95)
    
    self.buyer_button = ttk.Button(self, text="Buyer")
    self.buyer_button.place(x = 200, y = 0, height = 30, width = 95)
    
    self.order_button = ttk.Button(self, text="Order")
    self.order_button.place(x = 300, y = 0, height = 30, width = 95)
    
    self.review_button = ttk.Button(self, text="Review")
    self.review_button.place(x = 400, y = 0, height = 30, width = 95)
    
    self.feed_combobox = ttk.Combobox(self, textvariable = self.feed)
    self.feed_combobox['values'] = ['Import Data', 'Gmails', 'Addresses', 'BankCards', 'Reviews']
    self.feed_combobox.current(0)
    self.feed_combobox.place(x = 500, y = 2, height = 40, width = 145)
    
    self.phone_combobox = ttk.Combobox(self, textvariable = self.phone)
    self.phone_combobox['values'] = ['Select Phone', 'iphone1', 'iphone2', 'android']
    self.phone_combobox.current(0)
    self.phone_combobox.place(x = 650, y = 2, height = 40, width = 145)
    
    self.feed.trace("w", self.feed_write_event)
    
  def feed_write_event(self, var, indx, mode):
    parent = self.parent
    other_frames = [w for w in parent.winfo_children() if w.winfo_y() > 0]
    for w in other_frames: w.place_forget()
    
    if self.feed.get() == "Import Data":
      parent.feedframe.place_forget()
    else:
      parent.feedframe.place(x = 0, y = 30)


class Feed(tk.Frame):
  def __init__(self, parent, *args, **kwargs):
    tk.Frame.__init__(self, parent, *args, **kwargs)
    self.parent = parent
    self.configure(width = 800, height = 470)
    self['bg'] = 'light blue'
    
    self.input_text = tk.Text(self)
    self.input_text.place(x = 30, y = 30, width = 600, height = 400)
    
    self.submit_button = ttk.Button(self, text="Submit")
    self.submit_button.place(x = 650, y = 250, height = 30, width = 95)
    
    self.clear_button = ttk.Button(self, text="Clear")
    self.clear_button.place(x = 650, y = 290, height = 30, width = 95)
    
    self.quit_button = ttk.Button(self, text="Quit", command = self.quit)
    self.quit_button.place(x = 650, y = 330, height = 30, width = 95)
  
  def quit(self):
    self.place_forget()
    

class Admin(tk.Frame):
  def __init__(self, parent, *args, **kwargs):
    tk.Frame.__init__(self, parent, *args, **kwargs)
    self.parent = parent
    self.configure(width = 800, height = 470)
    self['bg'] = 'light green'
    
    self.search_text = tk.Text(self); 
    self.search_text.place(x = 50, y = 50, width = 400, height = 25)
    
    self.search_combobox = ttk.Combobox(self)
    self.search_combobox.place(x = 460, y = 50, width = 100, height = 30)
    self.search_combobox['values'] = ['Gmails', 'Addresses', 'BankCards']
    self.search_combobox.current(0)
    
    self.search_button = ttk.Button(self, text = "Search")
    self.search_button.place(x = 570, y = 48, width = 100, height = 30)
    
    self.search_listbox = tk.Listbox(self)
    self.search_listbox.place(x = 50, y = 100, width = 600, height = 300)
    
    self.quit_button = ttk.Button(self, text="Quit", command = self.quit)
    self.quit_button.place(x = 650, y = 330, height = 30, width = 95)
  
  def quit(self):
    self.place_forget()

class Buyer(tk.Frame):
  def __init__(self, parent, *args, **kwargs):
    tk.Frame.__init__(self, parent, *args, **kwargs)
    self.parent = parent
    self.configure(width = 800, height = 470)
    self['bg'] = 'light yellow'
    
    self.attributes_text = tk.Text(self); 
    self.attributes_text.place(x = 50, y = 50, width = 150, height = 300)
    self.attributes_text.configure(state = "disabled")
    
    self.values_text = tk.Text(self); 
    self.values_text.place(x = 210, y = 50, width = 150, height = 300)
    self.values_text.configure(state = "disabled")
    
    self.quit_button = ttk.Button(self, text="Quit", command = self.quit)
    self.quit_button.place(x = 650, y = 330, height = 30, width = 95)
  
  def quit(self):
    self.place_forget()


tmhelper = TMhelper()
