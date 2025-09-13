import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from decimal import Decimal
import sqlite3
import pyodbc

# 資料庫連線設定
server = 'DESKTOP-57P4JQ8\SQLSERVER2022'  # SQL Server 伺服器名稱
database = 'fruit_shop'  # 資料庫名稱

# 使用 Windows 認證連接到 Microsoft SQL Server
conn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                      f'SERVER={server};'
                      f'DATABASE={database};'
                      'Trusted_Connection=yes')

cursor = conn.cursor()

# 主視窗
root = tk.Tk()
root.title("水果行管理系統")
notebook = ttk.Notebook(root)
# ---------- 水果資訊頁面 ----------
def add_fruit():
    def submit_fruit():
        name = entry_name.get()
        category = entry_category.get()
        unit_price = entry_unit_price.get()
        stock_quantity = entry_stock_quantity.get()

        if name and category and unit_price and stock_quantity:
            try:
                cursor.execute("INSERT INTO Fruits (name, category, unit_price, stock_quantity) VALUES (?, ?, ?, ?)",
                               (name, category, float(unit_price), int(stock_quantity)))
                conn.commit()
                messagebox.showinfo("成功", "水果資訊新增成功！")
                entry_name.delete(0, tk.END)
                entry_category.delete(0, tk.END)
                entry_unit_price.delete(0, tk.END)
                entry_stock_quantity.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("錯誤", f"新增水果資訊時發生錯誤: {e}")
        else:
            messagebox.showwarning("警告", "所有欄位都必須填寫！")

    add_fruit_window = tk.Toplevel(root)
    add_fruit_window.title("新增水果資訊")

    tk.Label(add_fruit_window, text="水果名稱").pack()
    entry_name = tk.Entry(add_fruit_window)
    entry_name.pack()

    tk.Label(add_fruit_window, text="水果類型").pack()
    entry_category = tk.Entry(add_fruit_window)
    entry_category.pack()

    tk.Label(add_fruit_window, text="單價").pack()
    entry_unit_price = tk.Entry(add_fruit_window)
    entry_unit_price.pack()

    tk.Label(add_fruit_window, text="庫存數量").pack()
    entry_stock_quantity = tk.Entry(add_fruit_window)
    entry_stock_quantity.pack()

    tk.Button(add_fruit_window, text="提交", command=submit_fruit).pack()
    tk.Button(add_fruit_window, text="取消", command=add_fruit_window.destroy).pack()

def delete_fruit():
    def submit_Delete_Fruit():
        fruit_id = entry_fruit_id.get()

        if fruit_id:
            try:
                # 檢查是否有進貨記錄或銷售記錄
                cursor.execute("""
                    SELECT COUNT(*) FROM Purchases WHERE fruit_id = ?
                """, (fruit_id,))
                purchase_count = cursor.fetchone()[0]

                cursor.execute("""
                    SELECT COUNT(*) FROM Sales WHERE fruit_id = ?
                """, (fruit_id,))
                sales_count = cursor.fetchone()[0]

                if purchase_count > 0 or sales_count > 0:
                    messagebox.showwarning("警告", "該水果有相關進貨或銷售記錄，不能刪除！")
                else:
                    # 刪除水果記錄
                    cursor.execute("""
                        DELETE FROM Fruits WHERE fruit_id = ?
                    """, (fruit_id,))
                    conn.commit()
                    messagebox.showinfo("成功", "水果記錄已刪除！")
                    entry_fruit_id.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("錯誤", f"刪除水果記錄時發生錯誤: {e}")
        else:
            messagebox.showwarning("警告", "請輸入水果ID！")

    delete_fruit_window = tk.Toplevel(root)
    delete_fruit_window.title("刪除水果記錄")

    tk.Label(delete_fruit_window, text="水果ID").pack()
    entry_fruit_id = tk.Entry(delete_fruit_window)
    entry_fruit_id.pack()

    tk.Button(delete_fruit_window, text="刪除", command=submit_Delete_Fruit).pack()
    tk.Button(delete_fruit_window, text="取消", command=delete_fruit_window.destroy).pack()

def view_fruits():
    cursor.execute("SELECT * FROM Fruits")
    fruits = cursor.fetchall()

    view_fruits_window = tk.Toplevel(root)
    view_fruits_window.title("所有水果資訊")

    tk.Label(view_fruits_window, text="水果ID", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=10, pady=5)
    tk.Label(view_fruits_window, text="水果名稱", font=("Arial", 12, "bold")).grid(row=0, column=1, padx=10, pady=5)
    tk.Label(view_fruits_window, text="水果類型", font=("Arial", 12, "bold")).grid(row=0, column=2, padx=10, pady=5)
    tk.Label(view_fruits_window, text="單價", font=("Arial", 12, "bold")).grid(row=0, column=3, padx=10, pady=5)
    tk.Label(view_fruits_window, text="庫存數量", font=("Arial", 12, "bold")).grid(row=0, column=4, padx=10, pady=5)

    for index, fruit in enumerate(fruits, start=1):
        tk.Label(view_fruits_window, text=fruit[0]).grid(row=index, column=0, padx=10, pady=5)
        tk.Label(view_fruits_window, text=fruit[1]).grid(row=index, column=1, padx=10, pady=5)
        tk.Label(view_fruits_window, text=fruit[2]).grid(row=index, column=2, padx=10, pady=5)
        tk.Label(view_fruits_window, text=fruit[3]).grid(row=index, column=3, padx=10, pady=5)
        tk.Label(view_fruits_window, text=fruit[4]).grid(row=index, column=4, padx=10, pady=5)

    tk.Button(view_fruits_window, text="取消", command=view_fruits_window.destroy).grid(row=len(fruits)+1, column=0, columnspan=5, pady=10)

def add_suppliers():
    def submit_supplier():
        name = entry_supplier_name.get()
        phone = entry_phone.get()
        email = entry_email.get()
        address = entry_address.get()

        if name and phone and email and address:
            try:
                cursor.execute("INSERT INTO Suppliers (name, phone, email, address) VALUES (?, ?, ?, ?)",
                               (name, phone, email, address))
                conn.commit()
                messagebox.showinfo("成功", "供應商資訊新增成功！")
                entry_supplier_name.delete(0, tk.END)
                entry_phone.delete(0, tk.END)
                entry_email.delete(0, tk.END)
                entry_address.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("錯誤", f"新增供應商資訊時發生錯誤: {e}")
        else:
            messagebox.showwarning("警告", "所有欄位都必須填寫！")

    add_supplier_window = tk.Toplevel(root)
    add_supplier_window.title("新增供應商資訊")

    tk.Label(add_supplier_window, text="供應商名稱").pack()
    entry_supplier_name = tk.Entry(add_supplier_window)
    entry_supplier_name.pack()

    tk.Label(add_supplier_window, text="電話").pack()
    entry_phone = tk.Entry(add_supplier_window)
    entry_phone.pack()

    tk.Label(add_supplier_window, text="電子郵件").pack()
    entry_email = tk.Entry(add_supplier_window)
    entry_email.pack()

    tk.Label(add_supplier_window, text="地址").pack()
    entry_address = tk.Entry(add_supplier_window)
    entry_address.pack()

    tk.Button(add_supplier_window, text="提交", command=submit_supplier).pack()
    tk.Button(add_supplier_window, text="取消", command=add_supplier_window.destroy).pack()

def delete_supplier():
    def submit_Delete_Supplier():
        supplier_id = entry_supplier_id.get()

        if supplier_id:
            try:
                # 檢查是否有進貨記錄
                cursor.execute("""
                    SELECT COUNT(*) FROM Purchases WHERE supplier_id = ?
                """, (supplier_id,))
                purchase_count = cursor.fetchone()[0]

                if purchase_count > 0:
                    messagebox.showwarning("警告", "該供應商有相關進貨記錄，不能刪除！")
                else:
                    # 刪除供應商記錄
                    cursor.execute("""
                        DELETE FROM Suppliers WHERE supplier_id = ?
                    """, (supplier_id,))
                    conn.commit()
                    messagebox.showinfo("成功", "供應商記錄已刪除！")
                    entry_supplier_id.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("錯誤", f"刪除供應商記錄時發生錯誤: {e}")
        else:
            messagebox.showwarning("警告", "請輸入供應商ID！")

    delete_supplier_window = tk.Toplevel(root)
    delete_supplier_window.title("刪除供應商記錄")

    tk.Label(delete_supplier_window, text="供應商ID").pack()
    entry_supplier_id = tk.Entry(delete_supplier_window)
    entry_supplier_id.pack()

    tk.Button(delete_supplier_window, text="刪除", command=submit_Delete_Supplier).pack()
    tk.Button(delete_supplier_window, text="取消", command=delete_supplier_window.destroy).pack()

def view_suppliers():
    cursor.execute("SELECT * FROM Suppliers")
    suppliers = cursor.fetchall()


    view_suppliers_window = tk.Toplevel(root)
    view_suppliers_window.title("所有供應商資訊")

    # 顯示欄位名稱
    tk.Label(view_suppliers_window, text="供應商ID", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=10, pady=5)
    tk.Label(view_suppliers_window, text="供應商名稱", font=("Arial", 12, "bold")).grid(row=0, column=1, padx=10, pady=5)
    tk.Label(view_suppliers_window, text="電話", font=("Arial", 12, "bold")).grid(row=0, column=2, padx=10, pady=5)
    tk.Label(view_suppliers_window, text="電子郵件", font=("Arial", 12, "bold")).grid(row=0, column=3, padx=10, pady=5)
    tk.Label(view_suppliers_window, text="地址", font=("Arial", 12, "bold")).grid(row=0, column=4, padx=10, pady=5)

    # 顯示供應商資料
    for index, supplier in enumerate(suppliers, start=1):
        tk.Label(view_suppliers_window, text=supplier[0]).grid(row=index, column=0, padx=10, pady=5)
        tk.Label(view_suppliers_window, text=supplier[1]).grid(row=index, column=1, padx=10, pady=5)
        tk.Label(view_suppliers_window, text=supplier[2]).grid(row=index, column=2, padx=10, pady=5)
        tk.Label(view_suppliers_window, text=supplier[3]).grid(row=index, column=3, padx=10, pady=5)
        tk.Label(view_suppliers_window, text=supplier[4]).grid(row=index, column=4, padx=10, pady=5)

    # 取消按鈕
    tk.Button(view_suppliers_window, text="取消", command=view_suppliers_window.destroy).grid(row=len(suppliers)+1, column=0, columnspan=5, pady=10)

def add_Purchases():
    def submit_Purchases():
        # 取得使用者輸入的資料
        fruit_id = entry_fruit_id.get()
        supplier_id = entry_supplier_id.get()
        quantity = entry_quantity.get()
        purchase_date = entry_purchase_date.get()
        total_cost = entry_total_cost.get()
        
        # 檢查資料是否完整
        if fruit_id and supplier_id and quantity and purchase_date and total_cost:
            try:
                # 插入進貨記錄資料
                cursor.execute("""
                    INSERT INTO Purchases (fruit_id, supplier_id, quantity, purchase_date, total_cost)
                    VALUES (?, ?, ?, ?, ?)
                """, (fruit_id, supplier_id, quantity, purchase_date, total_cost))
                conn.commit()

                # 更新水果的庫存數量
                cursor.execute("""
                    UPDATE Fruits
                    SET stock_quantity = stock_quantity + ?
                    WHERE fruit_id = ?
                """, (quantity, fruit_id))
                conn.commit()

                messagebox.showinfo("成功", "進貨記錄新增成功，庫存已更新！")
                
                # 清空輸入框
                entry_fruit_id.delete(0, tk.END)
                entry_supplier_id.delete(0, tk.END)
                entry_quantity.delete(0, tk.END)
                entry_purchase_date.delete(0, tk.END)
                entry_total_cost.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("錯誤", f"新增進貨記錄時發生錯誤: {e}")
        else:
            messagebox.showwarning("警告", "所有欄位都必須填寫！")
    
    add_purchase_window = tk.Toplevel(root)
    add_purchase_window.title("新增進貨記錄")

    tk.Label(add_purchase_window, text="水果ID").pack()
    entry_fruit_id = tk.Entry(add_purchase_window)
    entry_fruit_id.pack()

    tk.Label(add_purchase_window, text="供應商ID").pack()
    entry_supplier_id = tk.Entry(add_purchase_window)
    entry_supplier_id.pack()

    tk.Label(add_purchase_window, text="進貨數量").pack()
    entry_quantity = tk.Entry(add_purchase_window)
    entry_quantity.pack()

    tk.Label(add_purchase_window, text="進貨日期 (YYYY-MM-DD)").pack()
    entry_purchase_date = tk.Entry(add_purchase_window)
    entry_purchase_date.pack()

    tk.Label(add_purchase_window, text="總成本").pack()
    entry_total_cost = tk.Entry(add_purchase_window)
    entry_total_cost.pack()

    tk.Button(add_purchase_window, text="提交", command=submit_Purchases).pack()
    tk.Button(add_purchase_window, text="取消", command=add_purchase_window.destroy).pack()

def delete_Purchases():
    def submit_Delete():
        purchase_id = entry_purchase_id.get()
        
        if purchase_id:
            try:
                # 查找該進貨記錄的水果ID和進貨數量
                cursor.execute("""
                    SELECT fruit_id, quantity FROM Purchases WHERE purchase_id = ?
                """, (purchase_id,))
                purchase = cursor.fetchone()

                if purchase:
                    fruit_id = purchase[0]
                    quantity = purchase[1]

                    # 刪除進貨記錄
                    cursor.execute("""
                        DELETE FROM Purchases WHERE purchase_id = ?
                    """, (purchase_id,))
                    conn.commit()

                    # 更新水果庫存，減少刪除的進貨數量
                    cursor.execute("""
                        UPDATE Fruits
                        SET stock_quantity = stock_quantity - ?
                        WHERE fruit_id = ?
                    """, (quantity, fruit_id))
                    conn.commit()

                    messagebox.showinfo("成功", "進貨記錄已刪除，庫存已更新！")
                    entry_purchase_id.delete(0, tk.END)
                else:
                    messagebox.showwarning("警告", "找不到該進貨記錄！")
            except Exception as e:
                messagebox.showerror("錯誤", f"刪除進貨記錄時發生錯誤: {e}")
        else:
            messagebox.showwarning("警告", "請輸入進貨記錄ID！")
    
    delete_purchase_window = tk.Toplevel(root)
    delete_purchase_window.title("刪除進貨記錄")

    tk.Label(delete_purchase_window, text="進貨記錄ID").pack()
    entry_purchase_id = tk.Entry(delete_purchase_window)
    entry_purchase_id.pack()

    tk.Button(delete_purchase_window, text="刪除", command=submit_Delete).pack()
    tk.Button(delete_purchase_window, text="取消", command=delete_purchase_window.destroy).pack()

def view_Purchases():
    cursor.execute("SELECT * FROM Purchases")
    purchases = cursor.fetchall()

    view_purchases_window = tk.Toplevel(root)
    view_purchases_window.title("所有進貨記錄")

    # 顯示欄位名稱
    tk.Label(view_purchases_window, text="進貨ID", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=10, pady=5)
    tk.Label(view_purchases_window, text="水果ID", font=("Arial", 12, "bold")).grid(row=0, column=1, padx=10, pady=5)
    tk.Label(view_purchases_window, text="供應商ID", font=("Arial", 12, "bold")).grid(row=0, column=2, padx=10, pady=5)
    tk.Label(view_purchases_window, text="進貨數量", font=("Arial", 12, "bold")).grid(row=0, column=3, padx=10, pady=5)
    tk.Label(view_purchases_window, text="進貨日期", font=("Arial", 12, "bold")).grid(row=0, column=4, padx=10, pady=5)
    tk.Label(view_purchases_window, text="總成本", font=("Arial", 12, "bold")).grid(row=0, column=5, padx=10, pady=5)

    # 顯示進貨記錄資料
    for index, purchase in enumerate(purchases, start=1):
        tk.Label(view_purchases_window, text=purchase[0]).grid(row=index, column=0, padx=10, pady=5)
        tk.Label(view_purchases_window, text=purchase[1]).grid(row=index, column=1, padx=10, pady=5)
        tk.Label(view_purchases_window, text=purchase[2]).grid(row=index, column=2, padx=10, pady=5)
        tk.Label(view_purchases_window, text=purchase[3]).grid(row=index, column=3, padx=10, pady=5)
        tk.Label(view_purchases_window, text=purchase[4]).grid(row=index, column=4, padx=10, pady=5)
        tk.Label(view_purchases_window, text=purchase[5]).grid(row=index, column=5, padx=10, pady=5)

    # 取消按鈕
    tk.Button(view_purchases_window, text="取消", command=view_purchases_window.destroy).grid(row=len(purchases)+1, column=0, columnspan=6, pady=10)

def add_Customers():
    def submit_add_customer():
        name = entry_name.get()
        phone = entry_phone.get()
        email = entry_email.get()
        address = entry_address.get()

        if name and phone and email and address:
            try:
                # 插入顧客資料
                cursor.execute("""
                    INSERT INTO Customers (name, phone, email, address)
                    VALUES (?, ?, ?, ?)
                """, (name, phone, email, address))
                conn.commit()
                messagebox.showinfo("成功", "顧客資料新增成功！")
                # 清空輸入框
                entry_name.delete(0, tk.END)
                entry_phone.delete(0, tk.END)
                entry_email.delete(0, tk.END)
                entry_address.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("錯誤", f"新增顧客資料時發生錯誤: {e}")
        else:
            messagebox.showwarning("警告", "所有欄位都必須填寫！")

    # 新增顧客視窗
    add_customer_window = tk.Toplevel(root)
    add_customer_window.title("新增顧客資料")

    tk.Label(add_customer_window, text="顧客姓名").pack()
    entry_name = tk.Entry(add_customer_window)
    entry_name.pack()

    tk.Label(add_customer_window, text="顧客電話").pack()
    entry_phone = tk.Entry(add_customer_window)
    entry_phone.pack()

    tk.Label(add_customer_window, text="顧客電子郵件").pack()
    entry_email = tk.Entry(add_customer_window)
    entry_email.pack()

    tk.Label(add_customer_window, text="顧客地址").pack()
    entry_address = tk.Entry(add_customer_window)
    entry_address.pack()

    tk.Button(add_customer_window, text="提交", command=submit_add_customer).pack()
    tk.Button(add_customer_window, text="取消", command=add_customer_window.destroy).pack()

def delete_Customers():
    def submit_delete_customer():
        customer_id = entry_customer_id.get()

        if customer_id:
            try:
                # 檢查顧客是否有銷售記錄
                cursor.execute("""
                    SELECT COUNT(*) FROM Sales WHERE customer_id = ?
                """, (customer_id,))
                sales_count = cursor.fetchone()[0]

                if sales_count > 0:
                    messagebox.showwarning("警告", "該顧客有相關銷售記錄，不能刪除！")
                else:
                    # 刪除顧客記錄
                    cursor.execute("""
                        DELETE FROM Customers WHERE customer_id = ?
                    """, (customer_id,))
                    conn.commit()
                    messagebox.showinfo("成功", "顧客資料已刪除！")
                    entry_customer_id.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("錯誤", f"刪除顧客資料時發生錯誤: {e}")
        else:
            messagebox.showwarning("警告", "請輸入顧客ID！")

    # 刪除顧客視窗
    delete_customer_window = tk.Toplevel(root)
    delete_customer_window.title("刪除顧客資料")

    tk.Label(delete_customer_window, text="顧客ID").pack()
    entry_customer_id = tk.Entry(delete_customer_window)
    entry_customer_id.pack()

    tk.Button(delete_customer_window, text="刪除", command=submit_delete_customer).pack()
    tk.Button(delete_customer_window, text="取消", command=delete_customer_window.destroy).pack()

def view_Customers():
    cursor.execute("SELECT * FROM Customers")
    customers = cursor.fetchall()

    view_customers_window = tk.Toplevel(root)
    view_customers_window.title("所有顧客資料")

    # 顯示欄位名稱
    tk.Label(view_customers_window, text="顧客ID", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=10, pady=5)
    tk.Label(view_customers_window, text="顧客姓名", font=("Arial", 12, "bold")).grid(row=0, column=1, padx=10, pady=5)
    tk.Label(view_customers_window, text="顧客電話", font=("Arial", 12, "bold")).grid(row=0, column=2, padx=10, pady=5)
    tk.Label(view_customers_window, text="顧客電子郵件", font=("Arial", 12, "bold")).grid(row=0, column=3, padx=10, pady=5)
    tk.Label(view_customers_window, text="顧客地址", font=("Arial", 12, "bold")).grid(row=0, column=4, padx=10, pady=5)

    # 顯示顧客資料
    for index, customer in enumerate(customers, start=1):
        tk.Label(view_customers_window, text=customer[0]).grid(row=index, column=0, padx=10, pady=5)
        tk.Label(view_customers_window, text=customer[1]).grid(row=index, column=1, padx=10, pady=5)
        tk.Label(view_customers_window, text=customer[2]).grid(row=index, column=2, padx=10, pady=5)
        tk.Label(view_customers_window, text=customer[3]).grid(row=index, column=3, padx=10, pady=5)
        tk.Label(view_customers_window, text=customer[4]).grid(row=index, column=4, padx=10, pady=5)

    # 取消按鈕
    tk.Button(view_customers_window, text="取消", command=view_customers_window.destroy).grid(row=len(customers)+1, column=0, columnspan=5, pady=10)

def add_Sales():
    def submit_add_sales():
        fruit_id = entry_fruit_id.get()  # 水果 ID
        quantity = entry_quantity.get()  # 銷售數量
        sale_date = entry_sale_date.get()  # 銷售日期
        customer_id = entry_customer_id.get()  # 顧客 ID

        # 確保水果 ID 存在
        cursor.execute("SELECT * FROM Fruits WHERE fruit_id = ?", (fruit_id,))
        fruit = cursor.fetchone()

        # 確保顧客 ID 存在
        cursor.execute("SELECT * FROM Customers WHERE customer_id = ?", (customer_id,))
        customer = cursor.fetchone()

        if not fruit:
            messagebox.showwarning("錯誤", "指定的水果 ID 不存在！")
            return
        
        if not customer:
            messagebox.showwarning("錯誤", "指定的顧客 ID 不存在！")
            return

        # 確認庫存足夠
        current_stock = fruit[4]  # 取得庫存數量
        if current_stock < int(quantity):
            messagebox.showwarning("錯誤", "庫存不足，無法完成銷售！")
            return

        try:
            # 計算總價
            unit_price = fruit[3]  # 水果單價
            total_price = unit_price * int(quantity)

            # 新增銷售記錄
            cursor.execute("""
                INSERT INTO Sales (fruit_id, quantity, sale_date, total_price, customer_id)
                VALUES (?, ?, ?, ?, ?)
            """, (fruit_id, quantity, sale_date, total_price, customer_id))

            # 更新庫存數量：減少銷售數量
            cursor.execute("UPDATE Fruits SET stock_quantity = stock_quantity - ? WHERE fruit_id = ?", 
                           (quantity, fruit_id))

            # 提交變更
            conn.commit()

            # 顯示成功訊息
            messagebox.showinfo("成功", f"銷售記錄已成功新增！")

        except Exception as e:
            messagebox.showerror("錯誤", f"發生錯誤: {str(e)}")

    # 顯示新增銷售的界面
    add_sales_window = tk.Toplevel(root)
    add_sales_window.title("新增銷售記錄")

    # 水果 ID
    tk.Label(add_sales_window, text="水果 ID").pack()
    entry_fruit_id = tk.Entry(add_sales_window)
    entry_fruit_id.pack()

    # 銷售數量
    tk.Label(add_sales_window, text="銷售數量").pack()
    entry_quantity = tk.Entry(add_sales_window)
    entry_quantity.pack()

    # 銷售日期
    tk.Label(add_sales_window, text="銷售日期 (YYYY-MM-DD)").pack()
    entry_sale_date = tk.Entry(add_sales_window)
    entry_sale_date.pack()

    # 顧客 ID
    tk.Label(add_sales_window, text="顧客 ID").pack()
    entry_customer_id = tk.Entry(add_sales_window)
    entry_customer_id.pack()

    # 提交按鈕
    tk.Button(add_sales_window, text="提交", command=submit_add_sales).pack()

    # 取消按鈕
    tk.Button(add_sales_window, text="取消", command=add_sales_window.destroy).pack()

def delete_Sales():
    def submit_delete_sales():
        sale_id = entry_delete_sale_id.get()  # 要刪除的銷售編號

        # 確保銷售 ID 存在
        cursor.execute("SELECT * FROM Sales WHERE sale_id = ?", (sale_id,))
        sale = cursor.fetchone()

        if not sale:
            messagebox.showwarning("錯誤", "指定的銷售 ID 不存在！")
            return

        fruit_id = sale[1]  # 取得該銷售記錄中的水果 ID
        quantity = sale[2]  # 取得該銷售記錄中的銷售數量

        try:
            # 刪除銷售記錄
            cursor.execute("DELETE FROM Sales WHERE sale_id = ?", (sale_id,))
            
            # 恢復庫存數量
            cursor.execute("UPDATE Fruits SET stock_quantity = stock_quantity + ? WHERE fruit_id = ?", 
                           (quantity, fruit_id))

            # 提交變更
            conn.commit()

            # 顯示成功訊息
            messagebox.showinfo("成功", f"銷售編號 {sale_id} 的記錄已成功刪除！")

        except Exception as e:
            messagebox.showerror("錯誤", f"發生錯誤: {str(e)}")

    # 顯示刪除銷售的界面
    delete_sales_window = tk.Toplevel(root)
    delete_sales_window.title("刪除銷售記錄")

    # 銷售 ID
    tk.Label(delete_sales_window, text="銷售編號").pack()
    entry_delete_sale_id = tk.Entry(delete_sales_window)
    entry_delete_sale_id.pack()

    # 提交按鈕
    tk.Button(delete_sales_window, text="提交", command=submit_delete_sales).pack()

    # 取消按鈕
    tk.Button(delete_sales_window, text="取消", command=delete_sales_window.destroy).pack()

def view_Sales():
    cursor.execute("""
        SELECT S.sale_id, F.name AS fruit_name, S.quantity, S.sale_date, S.total_price, S.customer_id, C.name AS customer_name
        FROM Sales S
        JOIN Fruits F ON S.fruit_id = F.fruit_id
        JOIN Customers C ON S.customer_id = C.customer_id
    """)
    sales = cursor.fetchall()

    view_sales_window = tk.Toplevel(root)
    view_sales_window.title("所有銷售資料")

    # 顯示欄位名稱
    tk.Label(view_sales_window, text="銷售ID", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=10, pady=5)
    tk.Label(view_sales_window, text="水果名稱", font=("Arial", 12, "bold")).grid(row=0, column=1, padx=10, pady=5)
    tk.Label(view_sales_window, text="銷售數量", font=("Arial", 12, "bold")).grid(row=0, column=2, padx=10, pady=5)
    tk.Label(view_sales_window, text="銷售日期", font=("Arial", 12, "bold")).grid(row=0, column=3, padx=10, pady=5)
    tk.Label(view_sales_window, text="總價格", font=("Arial", 12, "bold")).grid(row=0, column=4, padx=10, pady=5)
    tk.Label(view_sales_window, text="顧客ID", font=("Arial", 12, "bold")).grid(row=0, column=5, padx=10, pady=5)
    tk.Label(view_sales_window, text="顧客名稱", font=("Arial", 12, "bold")).grid(row=0, column=6, padx=10, pady=5)

    # 顯示銷售資料
    for index, sale in enumerate(sales, start=1):
        tk.Label(view_sales_window, text=sale[0]).grid(row=index, column=0, padx=10, pady=5)
        tk.Label(view_sales_window, text=sale[1]).grid(row=index, column=1, padx=10, pady=5)
        tk.Label(view_sales_window, text=sale[2]).grid(row=index, column=2, padx=10, pady=5)
        tk.Label(view_sales_window, text=sale[3]).grid(row=index, column=3, padx=10, pady=5)
        tk.Label(view_sales_window, text=sale[4]).grid(row=index, column=4, padx=10, pady=5)
        tk.Label(view_sales_window, text=sale[5]).grid(row=index, column=5, padx=10, pady=5)
        tk.Label(view_sales_window, text=sale[6]).grid(row=index, column=6, padx=10, pady=5)

    # 取消按鈕
    tk.Button(view_sales_window, text="取消", command=view_sales_window.destroy).grid(row=len(sales)+1, column=0, columnspan=7, pady=10)

def view_sales_and_purchases():
    # SQL 查询：合并 Sales 和 Purchases 表的数据
    query = """
    SELECT
        COALESCE(S.sale_date, P.purchase_date) AS date,  -- 合并销售日期和进货日期
        SUM(DISTINCT S.total_price) AS total_income,              -- 计算销售总收入
        SUM(DISTINCT P.total_cost) AS total_expense              -- 计算进货总成本
    FROM
        Sales S
    FULL OUTER JOIN Purchases P 
        ON S.sale_date = P.purchase_date                -- 按日期匹配销售和进货
    GROUP BY
        COALESCE(S.sale_date, P.purchase_date)          -- 按日期分组
    ORDER BY
        date;                                           -- 按日期排序
    """


        # 执行 SQL 查询
    cursor.execute(query)
    results = cursor.fetchall()

        # 创建一个新窗口来显示查询结果
    view_window = tk.Toplevel(root)
    view_window.title("Sales and Purchases Overview")

        # 添加标签显示列头
    tk.Label(view_window, text="日期", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=10, pady=5)
    tk.Label(view_window, text="總收入", font=("Arial", 12, "bold")).grid(row=0, column=1, padx=10, pady=5)
    tk.Label(view_window, text="總支出", font=("Arial", 12, "bold")).grid(row=0, column=2, padx=10, pady=5)

        # 显示查询结果
    for index, row in enumerate(results, start=1):
            date = row[0]  # 日期
            total_income = row[1] if row[1] is not None else 0  # 销售收入
            total_expense = row[2] if row[2] is not None else 0  # 进货成本

            # 显示每行数据
            tk.Label(view_window, text=date).grid(row=index, column=0, padx=10, pady=5)
            tk.Label(view_window, text=f"{total_income:,.2f}").grid(row=index, column=1, padx=10, pady=5)
            tk.Label(view_window, text=f"{total_expense:,.2f}").grid(row=index, column=2, padx=10, pady=5)

        # 取消按钮
    tk.Button(view_window, text="取消", command=view_window.destroy).grid(row=len(results)+1, column=0, columnspan=3, pady=10)

fruit_tab = ttk.Frame(notebook)
supplier_tab = ttk.Frame(notebook)
purchase_tab = ttk.Frame(notebook)
customer_tab = ttk.Frame(notebook)
sales_tab = ttk.Frame(notebook)
finance_tab = ttk.Frame(notebook)

notebook.add(fruit_tab, text="水果管理")
notebook.add(supplier_tab, text="供應商管理")
notebook.add(purchase_tab, text="進貨管理")
notebook.add(customer_tab, text="顧客管理")
notebook.add(sales_tab, text="銷售管理")
notebook.add(finance_tab, text="財務管理")

notebook.pack(expand=True, fill="both")

# 在每個標籤頁中放置按鈕或功能
tk.Button(fruit_tab, text="新增水果資訊", command=add_fruit).pack(pady=10)
tk.Button(fruit_tab, text="刪除水果資訊", command=delete_fruit).pack(pady=10)
tk.Button(fruit_tab, text="查詢所有水果資訊", command=view_fruits).pack(pady=10)

tk.Button(supplier_tab, text="新增供應商資訊", command=add_suppliers).pack(pady=10)
tk.Button(supplier_tab, text="刪除供應商資訊", command=delete_supplier).pack(pady=10)
tk.Button(supplier_tab, text="查詢所有供應商資訊", command=view_suppliers).pack(pady=10)

tk.Button(purchase_tab, text="新增進貨資訊", command=add_Purchases).pack(pady=10)
tk.Button(purchase_tab, text="刪除進貨資訊", command=delete_Purchases).pack(pady=10)
tk.Button(purchase_tab, text="查詢所有進貨資訊", command=view_Purchases).pack(pady=10)

tk.Button(customer_tab, text="新增顧客資訊", command=add_Customers).pack(pady=10)
tk.Button(customer_tab, text="刪除顧客資訊", command=delete_Customers).pack(pady=10)
tk.Button(customer_tab, text="查詢所有顧客資訊", command=view_Customers).pack(pady=10)

tk.Button(sales_tab, text="新增銷售資訊", command=add_Sales).pack(pady=10)
tk.Button(sales_tab, text="刪除銷售資訊", command=delete_Sales).pack(pady=10)
tk.Button(sales_tab, text="查詢所有銷售資訊", command=view_Sales).pack(pady=10)

tk.Button(finance_tab, text="查詢單日財務資訊", command=view_sales_and_purchases).pack(pady=10)

# 運行主視窗
root.mainloop()

# 關閉資料庫連接
conn.close()