import tkinter as tk
import tkinter.ttk as ttk
import datetime as dt

root = tk.Tk()
root.geometry("800x500")

class Report(tk.Frame):
  def __init__(self, *args, **kwargs):
    tk.Frame.__init__(self, *args, **kwargs)
    self.configure(width = 800, height = 470)
    self.place(x = 0, y = 30)
    
    self.start_text = tk.Text(self)
    self.start_text.place(x = 50, y = 50, width = 200, height = 20)
    
    self.end_text = tk.Text(self)
    self.end_text.place(x = 280, y = 50, width = 200, height = 20)
    
    self.refresh_button = tk.Button(self, text = "Refresh", command = self.refresh)
    self.refresh_button.place(x = 570, y = 50, width = 80, height = 20)
    
  def refresh(self):
      start = self.start_text.get("1.0", "end-1c")
      end = self.end_text.get("1.0", "end-1c")
      start = dt.datetime.strptime(start, "%Y-%m-%d")
      print(start)

reportframe = Report(root)








now = dt.datetime.now(); now = now - dt.timedelta(microseconds = now.microsecond)
dt.datetime.strptime("2018-3-12", "%Y-%m-%d")


