from tkinter import *
from tkinter import ttk

def login_event():
  return 0

def buyer_event():
  return 0

def order_event():
  return 0

def review_event():
  return 0

def feed_event(var, indx, mode):
  if feed.get() == "Import Data":
    inputbox.grid_remove()
    inputbutton.grid_remove()
  else:
    inputbox.grid(row=1, column = 0, columnspan = 5)
    inputbutton.grid(row=1, column = 5, sticky = (S,E))

def submit_event():
  print(inputbox.get("1.0","end-1c"))
  inputbox.delete('1.0', END)
  feed.set("Import Data")

root = Tk()
root.title("TMhelper")

mainframe = ttk.Frame(root, width=800, height=600)
mainframe.grid_propagate(0)
mainframe.grid(column=0, row=0)

ttk.Button(mainframe, text="Login", command=login_event).grid(column=0, row=0)
ttk.Button(mainframe, text="Buyer", command=buyer_event).grid(column=1, row=0)
ttk.Button(mainframe, text="Order", command=order_event).grid(column=2, row=0)
ttk.Button(mainframe, text="Review", command=review_event).grid(column=3, row=0)

inputbox = Text(mainframe)
inputbutton = ttk.Button(mainframe, text="Submit", command=submit_event)

feed = StringVar()
feed.trace("w", feed_event)
drop1 = ttk.Combobox(mainframe, textvariable = feed)
drop1['values'] = ['Import Data', 'Gmails', 'Addresses', 'BankCards', 'Reviews']
drop1.current(0)
drop1.grid(column=4, row=0)

phone = StringVar()
drop2 = ttk.Combobox(mainframe, textvariable = phone)
drop2['values'] = ['Select Phone', 'iphone1', 'iphone2', 'android']
drop2.current(0)
drop2.grid(column=5, row=0)

root.mainloop()









def calculate(*args):
  value = float(feet.get())
  meters.set((0.3048 * value * 10000.0 + 0.5)/10000.0)

feet = StringVar()
meters = StringVar()

feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)
feet_entry.grid(column=2, row=1)

ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))
ttk.Button(mainframe, text="Calculate", command=calculate).grid(column=3, row=3, sticky=W)

ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

feet_entry.focus()
root.bind('<Return>', calculate)

root.mainloop()
