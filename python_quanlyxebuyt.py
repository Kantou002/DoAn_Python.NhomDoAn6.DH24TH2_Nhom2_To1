import tkinter as tk
from tkinter import messagebox
from tkinter import ttk 
from tkcalendar import DateEntry
import mysql.connector

def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Astella250205@",
        database="qlxevalaixe"
)
# ====== Hàm canh giữa cửa sổ ======
def center_window(win, w=700, h=500):
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f'{w}x{h}+{x}+{y}')
# ====== Cửa sổ chính ======
root = tk.Tk()
root.title("Quản lý Xe Buýt")
center_window(root, 700, 500)
root.resizable(False, False)
# ====== Tiêu đề ======
lbl_title = tk.Label(root, text="QUẢN LÝ XE BUÝT", font=("Arial", 18, "bold"))
lbl_title.pack(pady=10)
# ====== Frame nhập thông tin ======
frame_info = tk.Frame(root)
frame_info.pack(pady=5, padx=10, fill="x")
tk.Label(frame_info, text="Mã xe buýt").grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_maxb = tk.Entry(frame_info, width=10)
entry_maxb.grid(row=0, column=1, padx=5, pady=5, sticky="w")

tk.Label(frame_info, text="Biển số xe").grid(row=0, column=2, padx=5, pady=5, sticky="w")
entry_bienso = tk.Entry(frame_info, width=10)
entry_bienso.grid(row=0, column=3, padx=5, pady=5, sticky="w")

tk.Label(frame_info, text="Hãng xe").grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_hangxe = tk.Entry(frame_info, width=10)
entry_hangxe.grid(row=1, column=1, padx=5, pady=5, sticky="w")

tk.Label(frame_info, text="Số ghế").grid(row=1, column=2, padx=5, pady=5, sticky="w")
entry_soghe = tk.Entry(frame_info, width=10)
entry_soghe.grid(row=1, column=3, padx=5, pady=5, sticky="w")

tk.Label(frame_info, text="Tình trạng").grid(row=2, column=0, padx=5, pady=5, sticky="w")
cbb_tt = ttk.Combobox(frame_info, values=[
    "Available","On Route","Maintance","Unavailable"
], width=20)
cbb_tt.grid(row=2, column=1, padx=5, pady=5, sticky="w")

tk.Label(frame_info, text="Năm sản xuất").grid(row=2, column=2, padx=5, pady=5, sticky="w")
entry_namsx = tk.Entry(frame_info, width=10)
entry_namsx.grid(row=2, column=3, padx=5, pady=5, sticky="w")
# ====== Bảng danh sách xe buýt======
lbl_ds = tk.Label(root, text="Danh sách xe buýt", font=("Arial", 10, "bold"))
lbl_ds.pack(pady=5, anchor="w", padx=10)

columns = ("Mã xe buýt", "Biển số xe", "Hãng xe", "Số ghế", "Tình Trạng", "Năm sản xuất")
tree = ttk.Treeview(root, columns=columns, show="headings", height=10)
for col in columns:
    tree.heading(col, text=col.capitalize())

tree.column("Mã xe buýt", width=80)
tree.column("Biển số xe", width=100)
tree.column("Hãng xe", width=100)
tree.column("Số ghế", width=80)
tree.column("Tình Trạng", width=100)
tree.column("Năm sản xuất", width=100)

tree.pack(padx=10, pady=5, fill="both")
# ====== Chức năng CRUD ======
def clear_input():
    entry_maxb.delete(0, tk.END)
    entry_bienso.delete(0, tk.END)
    entry_hangxe.delete(0, tk.END)
    entry_soghe.delete(0, tk.END)
    cbb_tt.set("")
    entry_namsx.delete(0, tk.END)

def load_data():
    for i in tree.get_children():
        tree.delete(i)
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM xebuyt")
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)
    conn.close()
def them_xe():
    maxb = entry_maxb.get()
    bienso = entry_bienso.get()
    hangxe = entry_hangxe.get()
    soghe = entry_soghe.get()
    tinhtrang = cbb_tt.get()
    namsx = entry_namsx.get()
    if not (maxb and bienso and hangxe and soghe and tinhtrang and namsx):
        messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin.")
        return
    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO xebuyt (maxb, bienso, hangxe, soghe, tinhtrang, namsx) VALUES (%s, %s, %s, %s, %s, %s)",
                       (maxb, bienso, hangxe, soghe, tinhtrang, namsx))
        conn.commit()
        messagebox.showinfo("Thành Công","Thêm xe buýt thành công.")
        load_data()
        clear_input()
    except mysql.connector.Error as err:
        messagebox.showerror("Lỗi", f"Lỗi khi thêm xe buýt: {err}")
    finally:
        conn.close()
def xoa_xe():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn xe buýt để xóa.")
        return
    maxb = tree.item(selected_item)["values"][0]
    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM xebuyt WHERE maxb = %s", (maxb,))
        conn.commit()
        messagebox.showinfo("Xóa xe buýt thành công.")
        load_data()
        clear_input()
    except mysql.connector.Error as err:
        messagebox.showerror("Lỗi", f"Lỗi khi xóa xe buýt: {err}")
    finally:
        conn.close()
    load_data()
def sua_xe():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn xe buýt để sửa.")
        return
    maxb = entry_maxb.get()
    bienso = entry_bienso.get()
    hangxe = entry_hangxe.get()
    soghe = entry_soghe.get()
    tinhtrang = cbb_tt.get()
    namsx = entry_namsx.get()
    if not (maxb and bienso and hangxe and soghe and tinhtrang and namsx):
        messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin.")
        return
    values = tree.item(selected_item)["values"]
    entry_maxb.delete(0, tk.END)
    entry_maxb.insert(0, values[0])
    entry_bienso.delete(0, tk.END)
    entry_bienso.insert(0, values[1])
    entry_hangxe.delete(0, tk.END)
    entry_hangxe.insert(0, values[2])
    entry_soghe.delete(0, tk.END)
    entry_soghe.insert(0, values[3])
    cbb_tt.set(values[4])
    entry_namsx.delete(0, tk.END)
    entry_namsx.insert(0, values[5])
def luu_xe():
    maxb=entry_maxb.get()
    bienso=entry_bienso.get()
    hangxe=entry_hangxe.get()
    soghe=entry_soghe.get()
    tinhtrang=cbb_tt.get()
    namsx=entry_namsx.get()
    conn=connect_to_database()
    cursor=conn.cursor()
    cursor.execute("UPDATE xebuyt SET bienso=%s, hangxe=%s, soghe=%s, tinhtrang=%s, namsx=%s WHERE maxb=%s",
                   (bienso, hangxe, soghe, tinhtrang, namsx, maxb))
    conn.commit()
    conn.close()
    load_data()
    clear_input()
# ====== Frame nút ======
frame_btn = tk.Frame(root)
frame_btn.pack(pady=5)

tk.Button(frame_btn, text="Thêm", width=8, command=them_xe).grid(row=0, column=0, padx=5)
tk.Button(frame_btn, text="Lưu", width=8, command=luu_xe).grid(row=0, column=1, padx=5)
tk.Button(frame_btn, text="Sửa", width=8, command=sua_xe).grid(row=0, column=2, padx=5)
tk.Button(frame_btn, text="Hủy", width=8, command=clear_input).grid(row=0, column=3, padx=5)
tk.Button(frame_btn, text="Xóa", width=8, command=xoa_xe).grid(row=0, column=4, padx=5)
tk.Button(frame_btn, text="Thoát", width=8, command=root.quit).grid(row=0, column=5, padx=5)
# ====== Tải dữ liệu ban đầu ======
load_data()
root.mainloop()