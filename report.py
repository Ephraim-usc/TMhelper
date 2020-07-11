import tkinter as tk
import tkinter.ttk as ttk
import datetime as dt

root = tk.Tk()
root.geometry("800x500")

frame = tk.Frame(root)
frame.configure(width = 800, height = 470)
frame.place(x = 0, y = 30)

start_text = tk.Text(frame)
start_text.place(x = 50, y = 50, width = 200, height = 20)

start_text = tk.Text(frame)
start_text.place(x = 260, y = 50, width = 200, height = 20)

refresh_button = tk.Button(frame)
refresh_button.place(x = 570, y = 50, width = 50, height = 20)

now = dt.datetime.now(); now = now - dt.timedelta(microseconds = now.microsecond)
dt.datetime.strptime("2018-3-12", "%Y-%m-%d")
