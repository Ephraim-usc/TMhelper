import tkinter as tk
import tkinter.ttk as ttk

root = tk.Tk()
root.geometry("800x500")

frame = tk.Frame(root)
frame.configure(width = 800, height = 470)
frame.place(x = 0, y = 30)

start_text = tk.Text(frame)
start_text.place(x = 50, y = 50, width = 200)
