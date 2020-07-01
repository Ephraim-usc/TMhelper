import tkinter as tk
import tkinter.ttk as ttk

### root

root = tk.Tk()
root.geometry("800x500")

menuframe = ttk.Frame(root, width = 800, height = 30)
menuframe.place(x = 0, y = 0)

ttk.Button(menuframe, text="Login").place(x = 0, y = 0, height = 30, width = 95)
ttk.Button(menuframe, text="Admin").place(x = 100, y = 0, height = 30, width = 95)

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
  str = feed_text.get("1.0","end-1c")
  feed_text.delete('1.0', tk.END)
  if feed.get() == "Gmails":
    feed_gmails(str)
  elif feed.get() == "Addresses":
    feed_addresses(str)
  elif feed.get() == "BankCards":
    feed_bankcards(str)

def feed_clear_event():
  feed_text.delete('1.0', tk.END)

def feed_quit_event():
  feed.set("Import Data")

feedframe.place(x = 0, y = 30)

ttk.Button(feedframe, text="Submit", command=feed_submit_event).place(x = 650, y = 250, height = 30, width = 95)
ttk.Button(feedframe, text="Clear", command=feed_clear_event).place(x = 650, y = 290, height = 30, width = 95)
ttk.Button(feedframe, text="Quit", command=feed_quit_event).place(x = 650, y = 330, height = 30, width = 95)

def feed_event(var, indx, mode):
  buyerframe.place_forget()
  
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
buyerframe.place(x = 0, y = 30)

gmail_text = tk.Text(buyerframe); gmail_text.place(x = 10, y = 10, width = 500, height = 120)
address_text = tk.Text(buyerframe); address_text.place(x = 10, y = 140, width = 500, height = 150)
bankcard_text = tk.Text(buyerframe); bankcard_text.place(x = 10, y = 300, width = 500, height = 120)

def buyer_event(event):
  buyerframe.place(x = 0, y = 30)
  gmail, address, bankcard = new_buyer()
  gmail_text.delete(1.0,"end"); gmail_text.insert(1.0, str(gmail[2:])); 
  address_text.delete(1.0,"end"); address_text.insert(1.0, str(address[2:]))
  bankcard_text.delete(1.0,"end"); bankcard_text.insert(1.0, str(bankcard[2:]))

  #address_label.configure(text = address)
  #bankcard_label.configure(text = bankcard)

buyer_button.bind('<Button-1>', buyer_event)


91104-4618

#root.mainloop()

