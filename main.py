import tkinter as tk
import tkinter.ttk as ttk

import operations as op

### root

root = tk.Tk()
root.title('TMhelper')
root.geometry("800x500")

menuframe = ttk.Frame(root, width = 800, height = 30)
menuframe.place(x = 0, y = 0)

ttk.Button(menuframe, text="Login").place(x = 0, y = 0, height = 30, width = 95)

admin_button = ttk.Button(menuframe, text="Admin")
admin_button.place(x = 100, y = 0, height = 30, width = 95)

buyer_button = ttk.Button(menuframe, text="Buyer")
buyer_button.place(x = 200, y = 0, height = 30, width = 95)

ttk.Button(menuframe, text="Order").place(x = 300, y = 0, height = 30, width = 95)
ttk.Button(menuframe, text="Review").place(x = 400, y = 0, height = 30, width = 95)

mainframe = ttk.Frame(root, width = 800, height = 470)
mainframe.place(x = 0, y = 30)


### feed

feed = tk.StringVar()
feed_combobox = ttk.Combobox(menuframe, textvariable = feed)
feed_combobox['values'] = ['Import Data', 'Gmails', 'Addresses', 'BankCards', 'Reviews']
feed_combobox.current(0)
feed_combobox.place(x = 500, y = 2, height = 40, width = 145)

feedframe = ttk.Frame(root, width = 800, height = 470)
feed_text = tk.Text(feedframe)
feed_text.place(x = 30, y = 30, width = 600, height = 400)

def feed_submit_event():
  string = feed_text.get("1.0","end-1c")
  feed_text.delete('1.0', tk.END)
  datatype = {"Gmails":op.gmail, "Addresses":op.address, "BankCards":op.bankcard}[feed.get()]
  op.feed(datatype, string)

def feed_clear_event():
  feed_text.delete('1.0', tk.END)

def feed_quit_event():
  feed.set("Import Data")

ttk.Button(feedframe, text="Submit", command=feed_submit_event).place(x = 650, y = 250, height = 30, width = 95)
ttk.Button(feedframe, text="Clear", command=feed_clear_event).place(x = 650, y = 290, height = 30, width = 95)
ttk.Button(feedframe, text="Quit", command=feed_quit_event).place(x = 650, y = 330, height = 30, width = 95)

def feed_event(var, indx, mode):
  other_frames = [w for w in root.winfo_children() if w.winfo_y() > 0]
  for w in other_frames: w.place_forget()
  
  if feed.get() == "Import Data":
    feedframe.place_forget()
  else:
    feedframe.place(x = 0, y = 30)

feed.trace("w", feed_event)

### phone

phone = tk.StringVar()
phone_combobox = ttk.Combobox(menuframe, textvariable = phone)
phone_combobox['values'] = ['Select Phone', 'iphone1', 'iphone2', 'android']
phone_combobox.current(0)
phone_combobox.place(x = 650, y = 2, height = 40, width = 145)

### buyer

buyerframe = ttk.Frame(root, width = 800, height = 470)

gmail_text = tk.Text(buyerframe); gmail_text.place(x = 10, y = 10, width = 500, height = 120)
address_text = tk.Text(buyerframe); address_text.place(x = 10, y = 140, width = 500, height = 150)
bankcard_text = tk.Text(buyerframe); bankcard_text.place(x = 10, y = 300, width = 500, height = 120)

def buyer_event(event):
  other_frames = [w for w in root.winfo_children() if w.winfo_y() > 0]
  for w in other_frames: w.place_forget()
  buyerframe.place(x = 0, y = 30)
  
  #gmail, address, bankcard = op.new_buyer()
  gmail_text.delete(1.0,"end"); gmail_text.insert(1.0, str(gmail[2:])); 
  address_text.delete(1.0,"end"); address_text.insert(1.0, str(address[2:]))
  bankcard_text.delete(1.0,"end"); bankcard_text.insert(1.0, str(bankcard[2:]))

  address_label.configure(text = address)
  bankcard_label.configure(text = bankcard)

buyer_button.bind('<Button-1>', buyer_event)

def buyer_submit_event():
  pass

ttk.Button(buyerframe, text="Submit", command=feed_submit_event).place(x = 660, y = 330, width = 100, height = 30)

### admin

adminframe = ttk.Frame(root, width = 800, height = 470)

def admin_event(event):
  other_frames = [w for w in root.winfo_children() if w.winfo_y() > 0]
  for w in other_frames: w.place_forget()
  adminframe.place(x = 0, y = 30)

admin_button.bind('<Button-1>', admin_event)

search_text = tk.Text(adminframe); search_text.place(x = 50, y = 50, width = 400, height = 25)
search_combobox = ttk.Combobox(adminframe); search_combobox.place(x = 460, y = 50, width = 100, height = 30)
search_combobox['values'] = ['Gmails', 'Addresses', 'BankCards']
search_combobox.current(0)
search_button = ttk.Button(adminframe, text = "Search"); search_button.place(x = 570, y = 48, width = 100, height = 30)
search_listbox = tk.Listbox(adminframe); search_listbox.place(x = 50, y = 100, width = 600, height = 300)

objects = []
def search_event(event):
  global objects
  string = search_text.get("1.0","end-1c")
  datatype = {"Gmails":"gmail", "Addresses":"address", "BankCards":"bankcard"}[search_combobox.get()]
  #displays, objects = op.search(datatype, string)
  search_listbox.delete(0, tk.END)
  for display in displays:
    search_listbox.insert("end", display)

search_button.bind('<Button-1>', search_event)

### check
checkframe = ttk.Frame(root, width = 800, height = 470)
check_text = tk.Text(checkframe); check_text.place(x = 50, y = 100, width = 600, height = 300)
check_text.configure(state='disabled')

def check_event():
  o = objects[search_listbox.curselection()[0]]
  check_text.configure(state='normal')
  check_text.delete('1.0', tk.END)
  check_text.insert("end", str(o))
  check_text.configure(state='disabled')
  checkframe.place(x = 0, y = 30)

check_button = ttk.Button(adminframe, text = "Check", command = check_event); check_button.place(x = 660, y = 330, width = 100, height = 30)

def quit_check_event():
  checkframe.place_forget()

quit_check_button = ttk.Button(checkframe, text = "Quit", command = quit_check_event); quit_check_button.place(x = 660, y = 330, width = 100, height = 30)

### 




#root.mainloop()

