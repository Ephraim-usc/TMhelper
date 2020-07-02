import tkinter as tk
import tkinter.ttk as ttk

import operations as op



class Menu(tk.Frame):
  def __init__(self, parent, *args, **kwargs):
    tk.Frame.__init__(self, parent, *args, **kwargs)
    self.parent = parent
    self.configure(width = 800, height = 30)
    self['bg'] = 'grey'
    
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
    
    global feed
    self.feed_combobox = ttk.Combobox(self, textvariable = feed)
    self.feed_combobox['values'] = ['Import Data', 'Gmails', 'Addresses', 'BankCards', 'Reviews']
    self.feed_combobox.current(0)
    self.feed_combobox.place(x = 500, y = 2, height = 40, width = 145)
    
    global phone
    self.phone_combobox = ttk.Combobox(self, textvariable = phone)
    self.phone_combobox['values'] = ['Select Phone', 'iphone1', 'iphone2', 'android']
    self.phone_combobox.current(0)
    self.phone_combobox.place(x = 650, y = 2, height = 40, width = 145)


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
    
    self.quit_button = ttk.Button(self, text="Quit")
    self.quit_button.place(x = 650, y = 330, height = 30, width = 95)

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


root = tk.Tk()
root.title('TMhelper')
root.geometry("800x500")

feed = tk.StringVar()
phone = tk.StringVar()

menuframe = Menu(root); menuframe.place(x = 0, y = 0)
feedframe = Feed(root); feedframe.place(x = 0, y = 30)
adminframe = Admin(root); adminframe.place(x = 0, y = 30)

def feed_event(var, indx, mode):
  other_frames = [w for w in root.winfo_children() if w.winfo_y() > 0]
  for w in other_frames: w.place_forget()
  
  if feed.get() == "Import Data":
    feedframe.place_forget()
  else:
    feedframe.place(x = 0, y = 30)

feed.trace("w", feed_event)

