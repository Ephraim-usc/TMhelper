import tkinter as tk
import tkinter.ttk as ttk
import datetime as dt
import pickle
import operations as op

root = tk.Tk()
root.geometry("1000x500")

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


class Report(Frame):
  def __init__(self, *args, **kwargs):
    Frame.__init__(self, *args, **kwargs)
    
    self.start_text = tk.Text(self)
    self.start_text.place(x = 50, y = 50, width = 200, height = 20)
    
    self.end_text = tk.Text(self)
    self.end_text.place(x = 280, y = 50, width = 200, height = 20)
    
    self.refresh_button = tk.Button(self, text = "Refresh", command = self.refresh)
    self.refresh_button.place(x = 570, y = 50, width = 80, height = 20)
    
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
    data = op.product_report(start, end)
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
    

reportframe = Report(root)
reportframe.place(x = 0, y = 30)
reportframe.init()








