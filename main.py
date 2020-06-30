from tkinter import *
from tkinter import ttk

def calculate(*args):
  value = float(feet.get())
  meters.set((0.3048 * value * 10000.0 + 0.5)/10000.0)

feet = StringVar()
meters = StringVar()


root = Tk()
root.title("TMhelper")

mainframe = ttk.Frame(root, width=1000, height=600)
mainframe.grid_propagate(0)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

def login():
  return 0

def order():
  return 0

def review():
  return 0

ttk.Button(mainframe, text="Login", command=login).grid(column=0, row=0)
ttk.Button(mainframe, text="Order", command=order).grid(column=1, row=0)
ttk.Button(mainframe, text="Order", command=review).grid(column=2, row=0)



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
