# ====================================================================
# QUANLY_DOAN.PY - HỆ THỐNG QUẢN LÝ XE VÀ LÁI XE
# ====================================================================
import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk 
from tkcalendar import DateEntry
import mysql.connector

# ==================== THIẾT LẬP KẾT NỐI CSDL ====================

def connect_to_database():
    """Thiết lập kết nối đến CSDL MySQL. Trả về đối tượng kết nối hoặc None nếu lỗi."""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Astella250205@", 
            database="qlxevalaixe"
        )
        print("--- Kết nối CSDL thành công ---")
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Lỗi CSDL", f"Không thể kết nối đến MySQL. Lỗi chi tiết: {err}")
        print(f"--- LỖI KẾT NỐI: {err} ---")
        return None

# ==================== HÀM CHUNG ====================

def center_window(win, w=1200, h=700):
    """Canh giữa cửa sổ ứng dụng."""
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f'{w}x{h}+{x}+{y}')

# ==================== CÁC CỬA SỔ CHỨC NĂNG ====================

# --- 1. Quản lý Xe Buýt (xebuyt) ---
def create_quanlyxebuyt_window(parent=None):
    root = tk.Toplevel(parent) if parent is not None else tk.Tk()
    root.title("Quản lý Xe Buýt")
    center_window(root, 1000, 600)
    root.resizable(False, False)
    
    tree = None 

    # ====== Tiêu đề ======
    lbl_title = tk.Label(root, text="QUẢN LÝ XE BUÝT", font=("Arial", 18, "bold"))
    lbl_title.pack(pady=10)
    
    # Định nghĩa các Entry và Combobox (Trước khi gọi các hàm CRUD/Load)
    entry_maxb = tk.Entry()
    entry_bienso = tk.Entry()
    entry_hangxe = tk.Entry()
    entry_soghe = tk.Entry()
    cbb_tt = ttk.Combobox()
    entry_namsx = tk.Entry()
    
    # ====== Frame nhập thông tin ======
    frame_info = tk.Frame(root)
    frame_info.pack(pady=5, padx=10, fill="x")
    
    tk.Label(frame_info, text="Mã xe buýt").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_maxb = tk.Entry(frame_info, width=15)
    entry_maxb.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame_info, text="Biển số xe").grid(row=0, column=2, padx=5, pady=5, sticky="w")
    entry_bienso = tk.Entry(frame_info, width=15)
    entry_bienso.grid(row=0, column=3, padx=5, pady=5, sticky="w")

    tk.Label(frame_info, text="Hãng xe").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entry_hangxe = tk.Entry(frame_info, width=15)
    entry_hangxe.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame_info, text="Số ghế").grid(row=1, column=2, padx=5, pady=5, sticky="w")
    entry_soghe = tk.Entry(frame_info, width=15)
    entry_soghe.grid(row=1, column=3, padx=5, pady=5, sticky="w")

    tk.Label(frame_info, text="Tình trạng").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    cbb_tt = ttk.Combobox(frame_info, values=[
        "available", "on_trip", "maintenance", "unavailable"
    ], width=20, state='readonly')
    cbb_tt.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame_info, text="Năm sản xuất").grid(row=2, column=2, padx=5, pady=5, sticky="w")
    entry_namsx = tk.Entry(frame_info, width=15)
    entry_namsx.grid(row=2, column=3, padx=5, pady=5, sticky="w")
    
    # ====== Chức năng CRUD & Load Data ======
    def clear_input():
        entry_maxb.delete(0, tk.END)
        entry_bienso.delete(0, tk.END)
        entry_hangxe.delete(0, tk.END)
        entry_soghe.delete(0, tk.END)
        cbb_tt.set("available")
        entry_namsx.delete(0, tk.END)
        entry_maxb.config(state=tk.NORMAL)

    def load_data():
        nonlocal tree # Chỉ định rõ đây là biến tree của hàm ngoài
        if tree is None: return
        for i in tree.get_children():
            tree.delete(i)
        conn = connect_to_database()
        if conn:
            cursor = conn.cursor()
            try:
                # LIST CỘT RÕ RÀNG để khớp với Treeview
                sql = "SELECT * FROM xebuyt" 
                cursor.execute(sql)
                for row in cursor.fetchall():
                    tree.insert("", tk.END, values=row)
            except mysql.connector.Error as err:
                 messagebox.showerror("Lỗi Tải Dữ liệu", f"Lỗi khi tải dữ liệu xe buýt: {err}", parent=root)
            finally:
                conn.close()

    def them_xe():
        maxb = entry_maxb.get()
        bienso = entry_bienso.get()
        hangxe = entry_hangxe.get()
        soghe = entry_soghe.get()
        tinhtrang = cbb_tt.get()
        namsx = entry_namsx.get()
        if not (maxb and bienso and hangxe and soghe and tinhtrang and namsx):
            messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin.", parent=root)
            return
        
        conn = connect_to_database()
        if conn:
            cursor = conn.cursor()
            try:
                sql = "INSERT INTO xebuyt (maxb, bienso, hangxe, soghe, tinhtrang, namsx) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (maxb, bienso, hangxe, soghe, tinhtrang, namsx))
                conn.commit()
                messagebox.showinfo("Thành Công","Thêm xe buýt thành công.", parent=root)
                load_data()
                clear_input()
            except mysql.connector.Error as err:
                messagebox.showerror("Lỗi", f"Lỗi khi thêm xe buýt: {err}", parent=root)
            finally:
                conn.close()

    def xoa_xe():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn xe buýt để xóa.", parent=root)
            return
        
        maxb = tree.item(selected_item)["values"][0]
        if not messagebox.askyesno("Xác nhận Xóa", f"Bạn có chắc muốn xóa xe buýt có Mã: {maxb}?", parent=root):
            return

        conn = connect_to_database()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM xebuyt WHERE maxb = %s", (maxb,))
                conn.commit()
                messagebox.showinfo("Thành Công", "Xóa xe buýt thành công.", parent=root)
                load_data()
                clear_input()
            except mysql.connector.Error as err:
                messagebox.showerror("Lỗi", f"Lỗi khi xóa xe buýt: {err}", parent=root)
            finally:
                conn.close()

    def select_item(event):         
        selected_item = tree.focus()
        if selected_item:
            values = tree.item(selected_item)["values"]
            entry_maxb.config(state=tk.NORMAL)
            clear_input()
            
            entry_maxb.insert(0, values[0])
            entry_bienso.insert(0, values[1])
            entry_hangxe.insert(0, values[2])
            entry_soghe.insert(0, values[3])
            cbb_tt.set(values[4])
            entry_namsx.insert(0, values[5])

            entry_maxb.config(state=tk.DISABLED)
            entry_bienso.config(state=tk.DISABLED)
            entry_hangxe.config(state=tk.DISABLED)
            entry_soghe.config(state=tk.DISABLED)
            cbb_tt.config(state=tk.DISABLED)
            entry_namsx.config(state=tk.DISABLED)
            
    def sua_xe():
        entry_maxb.config(state=tk.NORMAL)
        entry_bienso.config(state=tk.NORMAL)
        entry_hangxe.config(state=tk.NORMAL)
        entry_soghe.config(state=tk.NORMAL)
        cbb_tt.config(state=tk.NORMAL)
        entry_namsx.config(state=tk.NORMAL)

    def luu_xe():
        maxb=entry_maxb.get()
        bienso=entry_bienso.get()
        hangxe=entry_hangxe.get()
        soghe=entry_soghe.get()
        tinhtrang=cbb_tt.get()
        namsx=entry_namsx.get()
        
        if not (maxb and bienso and hangxe and soghe and tinhtrang and namsx):
            messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin.", parent=root)
            return

        conn=connect_to_database()
        if conn:
            cursor=conn.cursor()
            try:
                sql = "UPDATE xebuyt SET bienso=%s, hangxe=%s, soghe=%s, tinhtrang=%s, namsx=%s WHERE maxb=%s"
                cursor.execute(sql, (bienso, hangxe, soghe, tinhtrang, namsx, maxb))
                conn.commit()
                messagebox.showinfo("Thành Công","Cập nhật xe buýt thành công.", parent=root)
                load_data()
                clear_input()
            except mysql.connector.Error as err:
                messagebox.showerror("Lỗi", f"Lỗi khi cập nhật xe buýt: {err}", parent=root)
            finally:
                conn.close()
    
    # ====== Bảng danh sách xe buýt======
    lbl_ds = tk.Label(root, text="Danh sách xe buýt", font=("Arial", 10, "bold"))
    lbl_ds.pack(pady=5, anchor="w", padx=10)

    columns = ("Mã xe buýt", "Biển số xe", "Hãng xe", "Số ghế", "Tình Trạng", "Năm sản xuất")
    tree = ttk.Treeview(root, columns=columns, show="headings", height=10)
    
    tree.bind("<<TreeviewSelect>>", select_item)
    
    for col in columns:
        tree.heading(col, text=col.capitalize())

    tree.column("Mã xe buýt", width=80)
    tree.column("Biển số xe", width=100)
    tree.column("Hãng xe", width=100)
    tree.column("Số ghế", width=80)
    tree.column("Tình Trạng", width=100)
    tree.column("Năm sản xuất", width=100)

    tree.pack(padx=10, pady=5, fill="both")
    
    # ====== Frame nút ======
    frame_btn = tk.Frame(root)
    frame_btn.pack(pady=5)

    tk.Button(frame_btn, text="Thêm", width=8, command=them_xe).grid(row=0, column=0, padx=5)
    tk.Button(frame_btn, text="Lưu", width=8, command=luu_xe).grid(row=0, column=1, padx=5)
    tk.Button(frame_btn, text="Sửa (Tải lên)", width=10, command= sua_xe).grid(row=0, column=2, padx=5)
    tk.Button(frame_btn, text="Hủy", width=8, command=clear_input).grid(row=0, column=3, padx=5)
    tk.Button(frame_btn, text="Xóa", width=8, command=xoa_xe).grid(row=0, column=4, padx=5)
    tk.Button(frame_btn, text="Thoát", width=8, command=root.destroy).grid(row=0, column=5, padx=5)
    
    # ====== Tải dữ liệu ban đầu (Gọi sau khi Treeview được tạo) ======
    load_data()
    root.grab_set()
    root.wait_window()
    return root

# --- 2. Quản lý Lái xe (taixe) ---
def create_quanlytaixe_window(parent=None):
    root2 = tk.Toplevel(parent) if parent is not None else tk.Tk()
    root2.title("Quản lý Tài Xế")
    center_window(root2, 1000, 650)
    root2.resizable(False, False)

    tree = None
    
    # ====== Tiêu đề ======
    lbl_title = tk.Label(root2, text="QUẢN LÝ TÀI XẾ", font=("Arial", 18, "bold"))
    lbl_title.pack(pady=10)

    # ====== Frame nhập thông tin ======
    frame_info = tk.Frame(root2)
    frame_info.pack(pady=5, padx=10, fill="x")

    tk.Label(frame_info, text="Mã số").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_maso = tk.Entry(frame_info, width=15)
    entry_maso.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame_info, text="Số điện thoại").grid(row=0, column=2, padx=5, pady=5, sticky="w")
    entry_sdt = tk.Entry(frame_info, width=15)
    entry_sdt.grid(row=0, column=3, padx=5, pady=5, sticky="w")

    tk.Label(frame_info, text="Họ lót").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entry_holot = tk.Entry(frame_info, width=20)
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
    entry_banglai = tk.Entry(frame_info, width=15)
    entry_banglai.grid(row=0, column=5, padx=5, pady=5, sticky="w")

    # ====== Chức năng CRUD & Load Data ======
    def clear_input():
        entry_maso.delete(0, tk.END)
        entry_holot.delete(0, tk.END)
        entry_ten.delete(0, tk.END)
        gender_var.set("Nam")
        date_entry.set_date(datetime.date.today())
        entry_sdt.delete(0, tk.END)
        entry_banglai.delete(0, tk.END)
        entry_maso.config(state=tk.NORMAL)

    def load_data():
        nonlocal tree
        if tree is None: return
        for i in tree.get_children():
            tree.delete(i)
        conn = connect_to_database()
        if conn:
            cur = conn.cursor()
            try:
                sql = "SELECT * FROM taixe"
                cur.execute(sql)
                for row in cur.fetchall():
                    row_list = list(row)
                    if row_list[4]: 
                        row_list[4] = str(row_list[4]) # Chuyển đối tượng date thành str
                    
                    tree.insert("", tk.END, values=row_list)
            except mysql.connector.Error as err:
                 messagebox.showerror("Lỗi Tải Dữ liệu", f"Lỗi khi tải dữ liệu tài xế: {err}", parent=root2)
            finally:
                conn.close()

    def select_item(event):
        selected = tree.focus()
        if selected:
            values = tree.item(selected)["values"]
            entry_maso.config(state=tk.NORMAL)
            entry_holot.config(state=tk.NORMAL)
            entry_ten.config(state=tk.NORMAL)
            date_entry.config(state='normal')
            entry_sdt.config(state=tk.NORMAL)
            entry_banglai.config(state=tk.NORMAL)
            clear_input()
            
            entry_maso.insert(0, values[0])
            entry_holot.insert(0, values[1])
            entry_ten.insert(0, values[2])
            gender_var.set(values[3])
            date_entry.set_date(values[4])
            entry_sdt.insert(0, values[5])
            entry_banglai.insert(0, values[6])
            
            entry_maso.config(state=tk.DISABLED)
            entry_holot.config(state=tk.DISABLED)
            entry_ten.config(state=tk.DISABLED)
            date_entry.config(state='disabled')
            gender_var.trace_add('unset', lambda *args: None)  # Vô hiệu hóa thay đổi giá trị
            entry_sdt.config(state=tk.DISABLED)
            entry_banglai.config(state=tk.DISABLED)



    def them_tx():
        maso = entry_maso.get()
        holot = entry_holot.get()
        ten = entry_ten.get()
        phai = gender_var.get()
        ngaysinh = date_entry.get_date()
        sdt = entry_sdt.get()
        banglai = entry_banglai.get()

        if maso == "" or holot == "" or ten == "":
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin Họ tên và Mã số", parent=root2)
            return

        conn = connect_to_database()
        if conn:
            cur = conn.cursor()
            try:
                sql = "INSERT INTO taixe (maso, holot, ten, phai, ngaysinh, sdt, banglai) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cur.execute(sql, (maso, holot, ten, phai, ngaysinh, sdt, banglai))
                conn.commit()
                messagebox.showinfo("Thành Công", "Thêm tài xế thành công.", parent=root2)
                load_data()
                clear_input()
            except mysql.connector.Error as e:
                messagebox.showerror("Lỗi", f"Lỗi khi thêm tài xế: {e}", parent=root2)
            finally:
                conn.close()

    def xoa_tx():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Hãy chọn tài xế để xóa", parent=root2)
            return
        
        maso = tree.item(selected)["values"][0]
        if not messagebox.askyesno("Xác nhận Xóa", f"Bạn có chắc muốn xóa tài xế có Mã: {maso}?", parent=root2):
            return

        conn = connect_to_database()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("DELETE FROM taixe WHERE maso=%s", (maso,))
                conn.commit()
                messagebox.showinfo("Thành Công", "Xóa tài xế thành công.", parent=root2)
                load_data()
                clear_input()
            except mysql.connector.Error as e:
                messagebox.showerror("Lỗi", f"Lỗi khi xóa tài xế: {e}", parent=root2)
            finally:
                conn.close()
    def sua_tx():
        entry_maso.config(state=tk.NORMAL)
        entry_holot.config(state=tk.NORMAL)
        entry_ten.config(state=tk.NORMAL)
        date_entry.config(state='normal')
        entry_sdt.config(state=tk.NORMAL)
        entry_banglai.config(state=tk.NORMAL)

    def luu_tx():
        maso = entry_maso.get()
        holot = entry_holot.get()
        ten = entry_ten.get()
        phai = gender_var.get()
        ngaysinh = date_entry.get_date()
        sdt = entry_sdt.get()
        banglai = entry_banglai.get()

        if maso == "":
             messagebox.showwarning("Cảnh báo", "Vui lòng chọn tài xế cần sửa.", parent=root2)
             return

        conn = connect_to_database()
        if conn:
            cur = conn.cursor()
            try:
                sql = """UPDATE taixe SET holot=%s, ten=%s, phai=%s, ngaysinh=%s, 
                         sdt=%s, banglai=%s
                         WHERE maso=%s"""
                cur.execute(sql, (holot, ten, phai, ngaysinh, sdt, banglai, maso))
                conn.commit()
                messagebox.showinfo("Thành Công", "Cập nhật tài xế thành công.", parent=root2)
                load_data()
                clear_input()
            except mysql.connector.Error as e:
                messagebox.showerror("Lỗi", f"Lỗi khi cập nhật tài xế: {e}", parent=root2)
            finally:
                conn.close()
                
    # ====== Bảng danh sách tài xế ======
    lbl_ds = tk.Label(root2, text="Danh sách Tài xế", font=("Arial", 10, "bold"))
    lbl_ds.pack(pady=5, anchor="w", padx=10)

    columns = ("Mã tài xế", "Họ lót", "Tên", "Phái", "Ngày Sinh", "Số điện thoại", "Bằng lái")
    tree = ttk.Treeview(root2, columns=columns, show="headings", height=10)
    
    tree.bind("<<TreeviewSelect>>", select_item)

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

    # ====== Frame nút ======
    frame_btn = tk.Frame(root2)
    frame_btn.pack(pady=5)

    tk.Button(frame_btn, text="Thêm", width=8, command=them_tx).grid(row=0, column=0, padx=5)
    tk.Button(frame_btn, text="Lưu", width=8, command=luu_tx).grid(row=0, column=1, padx=5)
    tk.Button(frame_btn, text="Sửa (Tải lên)", width=10, command=sua_tx).grid(row=0, column=2, padx=5)
    tk.Button(frame_btn, text="Hủy", width=8, command=clear_input).grid(row=0, column=3, padx=5)
    tk.Button(frame_btn, text="Xóa", width=8, command=xoa_tx).grid(row=0, column=4, padx=5)
    tk.Button(frame_btn, text="Thoát", width=8, command=root2.destroy).grid(row=0, column=5, padx=5)

    # ====== Load dữ liệu ban đầu ======
    load_data()
    root2.grab_set()
    root2.wait_window()
    return root2

# --- 3. Phân công Chuyến đi (phancong) ---
def create_phancong_window(parent):
    """Tạo cửa sổ phân công chuyến đi."""
    root = tk.Toplevel(parent)
    root.title("Phân công Chuyến đi")
    center_window(root, 1100, 650)
    root.resizable(False, False)

    tree = None

    # ====== GIAO DIỆN PHÂN CÔNG ======
    lbl_title = tk.Label(root, text="PHÂN CÔNG CHUYẾN ĐI", font=("Arial", 18, "bold"))
    lbl_title.pack(pady=10)

    
    # --- Helper Functions ---
    def fetch_available_vehicles():
        conn = connect_to_database()
        if conn:
            cursor = conn.cursor()
            # Vì bảng taixe không có tinhtrang, tạm thời tất cả xe đều sẵn sàng
            cursor.execute("SELECT maxb FROM xebuyt") 
            vehicles = [row[0] for row in cursor.fetchall()]
            conn.close()
            return vehicles
        return []

    def fetch_available_drivers():
        conn = connect_to_database()
        if conn:
            cursor = conn.cursor()
            # Vì bảng taixe không có tinhtrang, tạm thời tất cả tài xế đều sẵn sàng
            cursor.execute("SELECT maso, holot, ten FROM taixe")
            drivers = [f"{row[0]} - {row[1]} {row[2]}" for row in cursor.fetchall()]
            conn.close()
            return drivers
        return []

    def populate_comboboxes():
        # Lấy dữ liệu sẵn sàng
        available_vehicles = fetch_available_vehicles()
        available_drivers = fetch_available_drivers()
        
        cbb_maxb['values'] = available_vehicles
        cbb_maso['values'] = available_drivers
        
        # Thiết lập giá trị mặc định cho Combobox
        if available_vehicles:
            cbb_maxb.current(0)
        else:
            cbb_maxb.set("--- Không có xe sẵn sàng ---")
        
        if available_drivers:
            cbb_maso.current(0)
        else:
            cbb_maso.set("--- Không có tài xế sẵn sàng ---")
            
    # ====== Tải dữ liệu Phân công ======
    def load_data():
        nonlocal tree
        if tree is None: return
        for i in tree.get_children():
            tree.delete(i)
        conn = connect_to_database()
        if conn:
            cursor = conn.cursor()
            try:
                # SELECT 8 cột (Đã sửa id_pc -> mapc, gioketthuc -> gioden)
                sql = """
                SELECT
                    pc.mapc,            
                    pc.ngayphancong,    
                    pc.maxb,            
                    tx.holot,           
                    tx.ten,             
                    pc.diadiemden,      
                    pc.giodi,          
                    pc.gioden,         
                    pc.trangthaichuyen  
                FROM phancong pc
                JOIN xebuyt xb ON pc.maxb = xb.maxb
                JOIN taixe tx ON pc.maso = tx.maso
                ORDER BY pc.ngayphancong DESC, pc.giodi DESC
                """
                cursor.execute(sql)
                for row in cursor.fetchall():
                    row_list = list(row)
                    
                    driver_name = f"{row_list[3]} {row_list[4]}"
                    
                    # Chuyển đổi đối tượng datetime/time/date sang chuỗi (str)
                    ngaypc = str(row_list[1]) 
                    giodi = str(row_list[6]) if row_list[6] else ""
                    gioden = str(row_list[7]) if row_list[7] else ""
                    
                    # Đổi giá trị CSDL thành hiển thị tiếng Việt
                    trangthai_vn = row_list[8].replace('Đã đi', 'Đang hoạt động').replace('Chưa đi', 'Dự kiến')

                    # Chèn dữ liệu vào Treeview
                    tree.insert("", tk.END, values=(
                        row_list[0], # mapc
                        ngaypc,
                        row_list[2], # bienso
                        driver_name,
                        row_list[5], # diadiemden
                        giodi,
                        gioden,
                        trangthai_vn 
                    ))
            except mysql.connector.Error as err:
                 messagebox.showerror("Lỗi Tải Dữ liệu", f"Lỗi khi tải dữ liệu phân công: {err}", parent=root)
            finally:
                conn.close()

    # ====== phân công chuyến đi ======
    def phan_cong():
        selected_maxb = cbb_maxb.get()
        selected_maso_info = cbb_maso.get()
        ngaypc = date_ngaypc.get_date()
        diadiemden = entry_diadiemden.get()
        giodi = entry_giodi.get()
        gioden = entry_gioden.get()
        trangthai = 'Đã đi' # Mặc định là Đã đi khi tạo
        
        maso = selected_maso_info.split(' - ')[0] if ' - ' in selected_maso_info else None

        if not (selected_maxb and maso and ngaypc and diadiemden and giodi):
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn Xe, Tài xế và điền các thông tin bắt buộc.", parent=root)
            return

        conn = connect_to_database()
        if conn:
            cursor = conn.cursor()
            try:
                # 1. Chèn vào bảng phancong
                sql_insert = "INSERT INTO phancong (maxb, maso, ngayphancong, diadiemden, giodi, gioden, trangthaichuyen) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql_insert, (selected_maxb, maso, ngaypc, diadiemden, giodi, gioden if gioden else None, trangthai))
                
                # 2. Cập nhật trạng thái của Xe (không cập nhật tài xế vì không có cột tinhtrang)
                cursor.execute("UPDATE xebuyt SET tinhtrang='on_trip' WHERE maxb=%s", (selected_maxb,))
                # Ghi chú: Nếu có cột tinhtrang trong taixe, lệnh ở đây sẽ là: UPDATE taixe SET tinhtrang='on_trip' WHERE maso=%s

                conn.commit()
                messagebox.showinfo("Thành Công", "Phân công chuyến đi thành công.", parent=root)
                load_data()
                populate_comboboxes()
            except mysql.connector.Error as err:
                messagebox.showerror("Lỗi", f"Lỗi khi phân công: {err}", parent=root)
            finally:
                conn.close() 

    # ====== Kết thúc chuyến đi ======
    def ket_thuc_chuyen():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn chuyến đi để kết thúc.", parent=root)
            return

        values = tree.item(selected_item)["values"]
        mapc = values[0] 
        bienso = values[2]
        trangthai_hien_tai = values[7].replace('Đang hoạt động', 'Đã đi') # Quay về giá trị SQL
        
        if trangthai_hien_tai == 'completed' or trangthai_hien_tai == 'Đã hoàn thành':
            messagebox.showinfo("Thông báo", "Chuyến đi này đã hoàn thành rồi.", parent=root)
            return
        
        conn = connect_to_database()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT maxb FROM phancong WHERE mapc = %s", (mapc,)) 
            result = cursor.fetchone()
            if not result:
                 messagebox.showerror("Lỗi", "Không tìm thấy thông tin phân công.", parent=root)
                 conn.close()
                 return

            maxb_pc = result[0]

            try:
                # 1. Cập nhật trạng thái phancong và Giờ kết thúc thực tế
                sql_update_pc = "UPDATE phancong SET trangthaichuyen='Đã hoàn thành', gioden=%s WHERE mapc=%s" 
                current_time = datetime.datetime.now().strftime('%H:%M:%S')
                cursor.execute(sql_update_pc, (current_time, mapc))
                
                # 2. Cập nhật trạng thái Xe thành 'available'
                cursor.execute("UPDATE xebuyt SET tinhtrang='available' WHERE maxb=%s", (maxb_pc,))

                conn.commit()
                messagebox.showinfo("Thành Công", f"Chuyến đi của xe {bienso} đã kết thúc và Xe đã sẵn sàng.", parent=root)
                load_data()
                populate_comboboxes()
            except mysql.connector.Error as err:
                messagebox.showerror("Lỗi", f"Lỗi khi kết thúc chuyến: {err}", )
            finally:
                conn.close()
    def xoa_chuyen():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Hãy chọn chuyến đi để xóa", parent=root)
            return
        mapc = tree.item(selected)["values"][0]
        if not messagebox.askyesno("Xác nhận Xóa", f"Bạn có chắc muốn xóa chuyến đi Mã PC: {mapc}?", parent=root):
            return
        conn = connect_to_database()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("DELETE FROM phancong WHERE mapc=%s", (mapc,))
                conn.commit()
                messagebox.showinfo("Thành Công", "Xóa chuyến đi thành công.", parent=root)
                load_data()
            except mysql.connector.Error as e:
                messagebox.showerror("Lỗi", f"Lỗi khi xóa chuyến đi: {e}", parent=root)
            finally:
                conn.close()
        
    # --- Frame nhập thông tin ---
    frame_info = tk.Frame(root)
    frame_info.pack(pady=5, padx=10, fill="x")
    
    cbb_maxb = ttk.Combobox(frame_info, width=25, state='readonly')
    cbb_maso = ttk.Combobox(frame_info, width=25, state='readonly')
    date_ngaypc = DateEntry(frame_info, width=23, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
    entry_diadiemden = tk.Entry(frame_info, width=27)
    entry_giodi = tk.Entry(frame_info, width=27)
    entry_gioden = tk.Entry(frame_info, width=27)
    cbb_trangthaichuyen = ttk.Combobox(frame_info, values=["Chưa đi", "Đã đi", "Đã hoàn thành", "Đã hủy"], width=25, state='readonly')
    cbb_trangthaichuyen.set("Đã đi") # Mặc định là Đã đi

    tk.Label(frame_info, text="Chọn Xe (Available)").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    cbb_maxb.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame_info, text="Chọn Tài xế").grid(row=0, column=2, padx=5, pady=5, sticky="w")
    cbb_maso.grid(row=0, column=3, padx=5, pady=5, sticky="w")

    tk.Label(frame_info, text="Ngày phân công").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    date_ngaypc.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame_info, text="Địa điểm đến").grid(row=1, column=2, padx=5, pady=5, sticky="w")
    entry_diadiemden.grid(row=1, column=3, padx=5, pady=5, sticky="w")
    
    tk.Label(frame_info, text="Giờ đi (HH:MM:SS)").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    entry_giodi.grid(row=2, column=1, padx=5, pady=5, sticky="w")
    entry_giodi.insert(0, datetime.datetime.now().strftime('%H:%M:%S'))

    tk.Label(frame_info, text="Giờ đến (Dự kiến)").grid(row=2, column=2, padx=5, pady=5, sticky="w")
    entry_gioden.grid(row=2, column=3, padx=5, pady=5, sticky="w")
    
    tk.Label(frame_info, text="Trạng thái chuyến").grid(row=3, column=0, padx=5, pady=5, sticky="w")
    cbb_trangthaichuyen.grid(row=3, column=1, padx=5, pady=5, sticky="w")
    
    # --- Frame nút ---
    frame_btn = tk.Frame(root)
    frame_btn.pack(pady=10)

    tk.Button(frame_btn, text="PHÂN CÔNG MỚI", width=18, command=phan_cong, bg="#4CAF50", fg="white").grid(row=0, column=0, padx=10)
    tk.Button(frame_btn, text="KẾT THÚC CHUYẾN", width=18, command=ket_thuc_chuyen, bg="#FF9800", fg="white").grid(row=0, column=1, padx=10)
    tk.Button(frame_btn, text="XÓA CHUYẾN", width=18, command=xoa_chuyen, bg="#F44336", fg="white").grid(row=0, column=2, padx=10)
    tk.Button(frame_btn, text="Đóng", width=10, command=root.destroy).grid(row=0, column=3, padx=10)
    
    # --- Bảng danh sách phân công ---
    lbl_ds = tk.Label(root, text="Lịch sử Phân công Chuyến đi", font=("Arial", 10, "bold"))
    lbl_ds.pack(pady=5, anchor="w", padx=10)

    columns = ("mapc", "ngayphancong", "bienso", "taixe", "diadiemden", "giodi", "gioden", "trangthaichuyen")
    tree = ttk.Treeview(root, columns=columns, show="headings", height=15)
    
    # Định nghĩa tiêu đề
    headings = {"mapc": "Mã PC", "ngayphancong": "Ngày PC", "bienso": "Biển số", "taixe": "Tài xế", 
                "diadiemden": "Địa điểm đến", "giodi": "Giờ đi", "gioden": "Giờ đến", "trangthaichuyen": "Trạng thái"}
    for col in columns:
        tree.heading(col, text=headings[col])

    # Định nghĩa kích thước cột
    tree.column("mapc", width=80, anchor="center")
    tree.column("ngayphancong", width=100)
    tree.column("bienso", width=100)
    tree.column("taixe", width=120)
    tree.column("diadiemden", width=150)
    tree.column("giodi", width=100, anchor="center")
    tree.column("gioden", width=100, anchor="center")
    tree.column("trangthaichuyen", width=120, anchor="center")

    tree.pack(padx=10, pady=5, fill="both", expand=True)

    # Tải dữ liệu ban đầu
    populate_comboboxes()
    load_data()
    root.grab_set()
    root.wait_window()
    return root


# ==============================================
# ==================== MENU CHÍNH ==============
# ==============================================

def create_main_menu():
    """Tạo cửa sổ Menu Chính (root)."""
    # Khởi tạo cửa sổ chính
    root = tk.Tk()
    root.title("HỆ THỐNG QUẢN LÝ ĐỒ ÁN")
    center_window(root, 600, 400)
    root.resizable(False, False)

    # Kiểm tra kết nối CSDL trước khi mở menu
    if not connect_to_database():
        root.destroy()
        return

    lbl_title = tk.Label(root, text="MENU QUẢN LÝ", font=("Arial", 20, "bold"), fg="#1976D2")
    lbl_title.pack(pady=20)

    # Frame chứa các nút chức năng
    frame_menu = tk.Frame(root)
    frame_menu.pack(pady=10)

    # Sử dụng command=lambda để truyền root làm parent cho cửa sổ con
    tk.Button(frame_menu, text="1. Quản lý Xe Buýt", width=25, height=2, command=lambda: create_quanlyxebuyt_window(root), 
              bg="#E3F2FD", fg="#1976D2", relief=tk.RAISED, bd=3).pack(pady=5)
    tk.Button(frame_menu, text="2. Quản lý Lái Xe", width=25, height=2, command=lambda: create_quanlytaixe_window(root), 
              bg="#E8F5E9", fg="#388E3C", relief=tk.RAISED, bd=3).pack(pady=5)
    tk.Button(frame_menu, text="3. Phân công Chuyến đi", width=25, height=2, command=lambda: create_phancong_window(root), 
              bg="#FFFDE7", fg="#FBC02D", relief=tk.RAISED, bd=3).pack(pady=5)
    
    tk.Button(root, text="Thoát Ứng dụng", width=25, command=root.quit, bg="#F43636", fg="white").pack(pady=20)

    root.mainloop()

# ==================== KHỐI CHẠY CHÍNH ====================
if __name__ == "__main__":
    create_main_menu()