import tkinter as tk
from tkinter import messagebox
from tkinter import ttk 
from tkcalendar import DateEntry
import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Astella250205@",
        database="qlxevalaixe"
)

# ====== Hàm canh giữa cửa sổ ======
def center_window(win, w=1200, h=700):
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f'{w}x{h}+{x}+{y}')
# ====== Cửa sổ chính ======
root2 = tk.Tk()
root2.title("Quản lý Tài Xế")
center_window(root2, 1200, 700)
root2.resizable(False, False)
# ====== Tiêu đề ======
lbl_title = tk.Label(root2, text="QUẢN LÝ TÀI XẾ", font=("Arial", 18, "bold"))
lbl_title.pack(pady=10)

# ====== Frame nhập thông tin ======
frame_info = tk.Frame(root2)
frame_info.pack(pady=5, padx=10, fill="x")

tk.Label(frame_info, text="Mã số").grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_maso = tk.Entry(frame_info, width=10)
entry_maso.grid(row=0, column=1, padx=5, pady=5, sticky="w")

tk.Label(frame_info, text="Số điện thoại").grid(row=0, column=2, padx=5, pady=5, sticky="w")
entry_sdt = tk.Entry(frame_info, width=15)
entry_sdt.grid(row=0, column=3, padx=5, pady=5, sticky="w")

tk.Label(frame_info, text="Họ lót").grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_holot = tk.Entry(frame_info, width=25)
entry_holot.grid(row=1, column=1, padx=5, pady=5, sticky="w")

tk.Label(frame_info, text="Tên").grid(row=1, column=2, padx=5, pady=5, sticky="w")
entry_ten = tk.Entry(frame_info, width=15)
entry_ten.grid(row=1, column=3, padx=5, pady=5, sticky="w")

tk.Label(frame_info, text="Phái").grid(row=2, column=0, padx=5, pady=5, sticky="w")
gender_var = tk.StringVar(value="Nam")
tk.Radiobutton(frame_info, text="Nam", variable=gender_var, value="Nam").grid(row=2, column=1, pady=5, sticky="w")
tk.Radiobutton(frame_info, text="Nữ", variable=gender_var, value="Nữ").grid(row=2, column=1, padx=60, sticky="w")

tk.Label(frame_info, text="Ngày sinh").grid(row=2, column=2, padx=5, pady=5, sticky="w")
date_entry = DateEntry(frame_info, width=12, background="darkblue", 
                        foreground="white", date_pattern="yyyy-mm-dd")
date_entry.grid(row=2, column=3, padx=5, pady=5, sticky="w")

tk.Label(frame_info, text="Bằng lái").grid(row=0, column=4, padx=5, pady=5, sticky="w")
entry_banglai = tk.Entry(frame_info, width=25)
entry_banglai.grid(row=0, column=5, padx=5, pady=5, sticky="w")
# ====== Bảng danh sách tài xế ======
lbl_ds = tk.Label(root2, text="Danh sách Tài xế", font=("Arial", 10, "bold"))
lbl_ds.pack(pady=5, anchor="w", padx=10)

columns = ("Mã tài xế", "Họ lót", "Tên", "Phái", "Ngày Sinh", "Số điện thoại", "Bằng lái")
tree = ttk.Treeview(root2, columns=columns, show="headings", height=10)

for col in columns:
    tree.heading(col, text=col.capitalize())

tree.column("Mã tài xế", width=60, anchor="center")
tree.column("Họ lót", width=150)
tree.column("Tên", width=100)
tree.column("Phái", width=60, anchor="center")
tree.column("Ngày Sinh", width=100, anchor="center")
tree.column("Số điện thoại", width=150)
tree.column("Bằng lái", width=60)
tree.pack(padx=10, pady=5, fill="both")
def clear_input():
    entry_maso.delete(0, tk.END)
    entry_holot.delete(0, tk.END)
    entry_ten.delete(0, tk.END)
    gender_var.set("Nam")
    date_entry.set_date("2000-01-01")
    entry_sdt.delete(0, tk.END)
    entry_banglai.delete(0, tk.END)

def load_data():
    for i in tree.get_children():
        tree.delete(i)
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM taixe")
    for row in cur.fetchall():
        tree.insert("", tk.END, values=row)
    conn.close()

def them_tx():
    maso = entry_maso.get()
    holot = entry_holot.get()
    ten = entry_ten.get()
    phai = gender_var.get()
    ngaysinh = date_entry.get()
    sdt = entry_sdt.get()
    banglai = entry_banglai.get()

    if maso == "" or holot == "" or ten == "":
        messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin")
        return

    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO taixe VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (maso, holot, ten, phai, ngaysinh, sdt, banglai))

        conn.commit()
        load_data()
        clear_input()
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

    conn.close()

def xoa_tx():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Hãy chọn tài xế để xóa")
        return

    maso = tree.item(selected)["values"][0]
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM taixe WHERE maso=%s", (maso,))
    conn.commit()
    conn.close()
    load_data()

def sua_tx():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Hãy chọn tài xế để sửa")
        return
        
    values = tree.item(selected)["values"]
    entry_maso.delete(0, tk.END)
    entry_maso.insert(0, values[0])
    entry_holot.delete(0, tk.END)
    entry_holot.insert(0, values[1])
    entry_ten.delete(0, tk.END)
    entry_ten.insert(0, values[2])
    gender_var.set(values[3])
    date_entry.set_date(values[4])
    entry_sdt.delete(0, tk.END)
    entry_sdt.insert(0, values[5])
    entry_banglai.delete(0, tk.END)
    entry_banglai.insert(0, values[6])

def luu_tx():
    maso = entry_maso.get()
    holot = entry_holot.get()
    ten = entry_ten.get()
    phai = gender_var.get()
    ngaysinh = date_entry.get()
    sdt = entry_sdt.get()
    banglai = entry_banglai.get()
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""UPDATE taixe SET holot=%s, ten=%s, phai=%s, ngaysinh=%s, 
                   sdt=%s, banglai=%s
                   WHERE maso=%s""",
                (holot, ten, phai, ngaysinh, sdt, banglai, maso))

    conn.commit()
    conn.close()
    load_data()
    clear_input()
    # ====== Frame nút ======
frame_btn = tk.Frame(root2)
frame_btn.pack(pady=5)

tk.Button(frame_btn, text="Thêm", width=8, command=them_tx).grid(row=0, column=0, padx=5)
tk.Button(frame_btn, text="Lưu", width=8, command=luu_tx).grid(row=0, column=1, padx=5)
tk.Button(frame_btn, text="Sửa", width=8, command=sua_tx).grid(row=0, column=2, padx=5)
tk.Button(frame_btn, text="Hủy", width=8, command=clear_input).grid(row=0, column=3, padx=5)
tk.Button(frame_btn, text="Xóa", width=8, command=xoa_tx).grid(row=0, column=4, padx=5)
tk.Button(frame_btn, text="Thoát", width=8, command=root2.quit).grid(row=0, column=5, padx=5)

# ====== Load dữ liệu ban đầu ======
load_data()
root2.mainloop()