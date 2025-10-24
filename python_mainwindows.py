import tkinter as tk
from tkinter import messagebox
from tkinter import ttk 
from tkcalendar import DateEntry
import mysql.connector
from python_quanlytaixe import create_quanlytaixe_window
from python_quanlyxebuyt import create_quanlyxebuyt_window

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Astella250205@",
        database="qlxevalaixe"
)

# ====== Hàm canh giữa cửa sổ ======
def center_window(win, w=800, h=600):
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f'{w}x{h}+{x}+{y}')
# ====== Cửa sổ chính ======
main = tk.Tk()
main.title("Quản lý Xe và Lái Xe")
center_window(main, 800, 600)
main.resizable(False, False)
# create the Toplevel after main exists
root=create_quanlyxebuyt_window(main)
root2=create_quanlytaixe_window(main)
# hide it so main shows first
root.withdraw()
root2.withdraw()
# ====== Tiêu đề ======
lbl_title = tk.Label(main, text="QUẢN LÝ XE VÀ LÁI XE", font=("Arial", 18, "bold"))
lbl_title.pack(pady=10)
# ====== Nút mở cửa sổ Quản lý Tài Xế ======
def open_quanlyxebuyt():
    root.deiconify()
    root.lift()
    root.focus_force()

def open_quanlytaixe():
    root2.deiconify()
    root2.lift()
    root2.focus_force()

btn_quanlyxebuyt = tk.Button(main, text="Quản lý Xe Buýt", font=("Arial", 14), command=open_quanlyxebuyt)
btn_quanlyxebuyt.pack(pady=20)

btn_quanlytaixe = tk.Button(main, text="Quản lý Tài Xế", font=("Arial", 14), command=open_quanlytaixe)
btn_quanlytaixe.pack(pady=20)


main.mainloop()



