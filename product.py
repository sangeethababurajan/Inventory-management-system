from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class productClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+320+220")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")
        self.root.resizable(False, False)
        self.root.focus_force()

        # ----------- Variables -------------
        self.var_cat = StringVar()
        self.cat_list = []
        self.sup_list = []
        self.fetch_cat_sup()
        self.var_pid = StringVar()
        self.var_sup = StringVar()
        self.var_name = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_status = StringVar()
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        # ----------- Product Management Frame -------------
        product_Frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        product_Frame.place(x=10, y=10, width=450, height=480)

        title = Label(product_Frame, text="Manage Product Details", font=("goudy old style", 18), bg="#0f4d7d", fg="white").pack(side=TOP, fill=X)
        
        lbl_category = Label(product_Frame, text="Category", font=("goudy old style", 18), bg="white").place(x=30, y=60)
        lbl_supplier = Label(product_Frame, text="Supplier", font=("goudy old style", 18), bg="white").place(x=30, y=110)
        lbl_product_name = Label(product_Frame, text="Name", font=("goudy old style", 18), bg="white").place(x=30, y=160)
        lbl_price = Label(product_Frame, text="Price", font=("goudy old style", 18), bg="white").place(x=30, y=210)
        lbl_qty = Label(product_Frame, text="Quantity", font=("goudy old style", 18), bg="white").place(x=30, y=260)
        lbl_status = Label(product_Frame, text="Status", font=("goudy old style", 18), bg="white").place(x=30, y=310)

        cmb_cat = ttk.Combobox(product_Frame, textvariable=self.var_cat, values=self.cat_list, state='readonly', justify=CENTER, font=("goudy old style", 15))
        cmb_cat.place(x=150, y=60, width=200)
        cmb_cat.current(0)

        cmb_sup = ttk.Combobox(product_Frame, textvariable=self.var_sup, values=self.sup_list, state='readonly', justify=CENTER, font=("goudy old style", 15))
        cmb_sup.place(x=150, y=110, width=200)
        cmb_sup.current(0)

        txt_name = Entry(product_Frame, textvariable=self.var_name, font=("goudy old style", 15), bg="lightyellow").place(x=150, y=160, width=200)
        txt_price = Entry(product_Frame, textvariable=self.var_price, font=("goudy old style", 15), bg="lightyellow").place(x=150, y=210, width=200)
        txt_qty = Entry(product_Frame, textvariable=self.var_qty, font=("goudy old style", 15), bg="lightyellow").place(x=150, y=260, width=200)

        cmb_status = ttk.Combobox(product_Frame, textvariable=self.var_status, values=("Active", "Inactive"), state='readonly', justify=CENTER, font=("goudy old style", 15))
        cmb_status.place(x=150, y=310, width=200)
        cmb_status.current(0)

        btn_add = Button(product_Frame, text="Save", command=self.add, font=("goudy old style", 15), bg="#90caf9", fg="white", cursor="hand2").place(x=10, y=400, width=100, height=40)
        btn_update = Button(product_Frame, text="Update", command=self.update, font=("goudy old style", 15), bg="#f48fb1", fg="white", cursor="hand2").place(x=120, y=400, width=100, height=40)
        btn_delete = Button(product_Frame, text="Delete", command=self.delete, font=("goudy old style", 15), bg="#80cbc4", fg="white", cursor="hand2").place(x=230, y=400, width=100, height=40)
        btn_clear = Button(product_Frame, text="Clear", command=self.clear, font=("goudy old style", 15), bg="#b0bec5", fg="white", cursor="hand2").place(x=340, y=400, width=100, height=40)

        # Add graph button
        btn_graph = Button(product_Frame, text="View Stock Graph", command=self.open_graph_window, font=("goudy old style", 15), bg="#ff9800", fg="white", cursor="hand2").place(x=150, y=350, width=200, height=40)

        # ----------- Search Frame -------------
        SearchFrame = LabelFrame(self.root, text="Search Product", font=("goudy old style", 12, "bold"), bd=2, relief=RIDGE, bg="white")
        SearchFrame.place(x=480, y=10, width=600, height=80)

        cmb_search = ttk.Combobox(SearchFrame, textvariable=self.var_searchby, values=("Select", "Category", "Supplier", "Name"), state='readonly', justify=CENTER, font=("goudy old style", 15))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        txt_search = Entry(SearchFrame, textvariable=self.var_searchtxt, font=("goudy old style", 15), bg="lightyellow").place(x=200, y=10)
        btn_search = Button(SearchFrame, text="Search", command=self.search, font=("goudy old style", 15), bg="#4caf50", fg="white", cursor="hand2").place(x=410, y=9, width=150, height=30)

        # ----------- Product Details -------------
        product_frame = Frame(self.root, bd=3, relief=RIDGE)
        product_frame.place(x=480, y=100, width=600, height=390)

        scrolly = Scrollbar(product_frame, orient=VERTICAL)
        scrollx = Scrollbar(product_frame, orient=HORIZONTAL)

        self.ProductTable = ttk.Treeview(product_frame, columns=("pid", "Category", "Supplier", "name", "price", "qty", "status"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.ProductTable.xview)
        scrolly.config(command=self.ProductTable.yview)
        self.ProductTable.heading("pid", text="P ID")
        self.ProductTable.heading("Category", text="Category")
        self.ProductTable.heading("Supplier", text="Supplier")
        self.ProductTable.heading("name", text="Name")
        self.ProductTable.heading("price", text="Price")
        self.ProductTable.heading("qty", text="Quantity")
        self.ProductTable.heading("status", text="Status")
        self.ProductTable["show"] = "headings"
        self.ProductTable.column("pid", width=90)
        self.ProductTable.column("Category", width=100)
        self.ProductTable.column("Supplier", width=100)
        self.ProductTable.column("name", width=100)
        self.ProductTable.column("price", width=100)
        self.ProductTable.column("qty", width=100)
        self.ProductTable.column("status", width=100)
        self.ProductTable.pack(fill=BOTH, expand=1)
        self.ProductTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()
        self.fetch_cat_sup()

    def fetch_cat_sup(self):
        self.cat_list.append("Empty")
        self.sup_list.append("Empty")
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("select name from category")
            cat = cur.fetchall()
            if len(cat) > 0:
                del self.cat_list[:]
                self.cat_list.append("Select")
                for i in cat:
                    self.cat_list.append(i[0])
            cur.execute("select name from supplier")
            sup = cur.fetchall()
            if len(sup) > 0:
                del self.sup_list[:]
                self.sup_list.append("Select")
                for i in sup:
                    self.sup_list.append(i[0])
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")

    def open_graph_window(self):
        graph_window = Toplevel(self.root)
        graph_window.title("Stock Graph")
        graph_window.geometry("500x400")

        lbl_select = Label(graph_window, text="Select Category", font=("goudy old style", 18), bg="white").pack(pady=20)
        cmb_category = ttk.Combobox(graph_window, values=self.cat_list, state='readonly', justify=CENTER, font=("goudy old style", 15))
        cmb_category.pack()

        def show_graph():
            category = cmb_category.get()
            if category == "Select":
                messagebox.showerror("Error", "Please select a category", parent=graph_window)
            else:
                self.plot_graph(category)

        btn_show = Button(graph_window, text="Show Graph", command=show_graph, font=("goudy old style", 15), bg="#4caf50", fg="white", cursor="hand2").pack(pady=20)

    def plot_graph(self, category):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT name, qty FROM product WHERE category=?", (category,))
            data = cur.fetchall()
            if not data:
                messagebox.showinfo("Info", "No data found for the selected category")
                return

            names = [x[0] for x in data]
            quantities = [int(x[1]) for x in data]  # Ensure quantities are integers

        # Plotting the graph
            plt.figure(figsize=(8, 5))
            plt.bar(names, quantities, color='blue')

        # Adding labels and title
            plt.xlabel('Product Names')
            plt.ylabel('Quantity')
            plt.title(f'Stock Graph for Category: {category}')
            plt.xticks(rotation=45)

        # Set the y-axis range and ticks
            max_qty = max(quantities)
            step = max(1, max_qty // 10)  # Dynamically decide step size for clarity
            plt.ylim(0, max_qty + step)  # Ensure the y-axis starts at 0 and extends slightly beyond the max value
            plt.yticks(range(0, max_qty + step, step))  # Define ticks with a consistent step size

            plt.tight_layout()
            plt.show()

        except ValueError as ve:
            messagebox.showerror("Error", f"Invalid quantity data: {str(ve)}")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")


    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_cat.get()=="Select" or self.var_cat.get()=="Empty" or self.var_sup=="Select" or self.var_sup=="Empty":
                messagebox.showerror("Error","All fields are required",parent=self.root)
            else:
                cur.execute("Select * from product where name=?",(self.var_name.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Product already present",parent=self.root)
                else:
                    cur.execute("insert into product(Category,Supplier,name,price,qty,status) values(?,?,?,?,?,?)",(
                        self.var_cat.get(),
                        self.var_sup.get(),
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_qty.get(),
                        self.var_status.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Product Added Successfully",parent=self.root)
                    self.clear()
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select * from product")
            rows=cur.fetchall()
            self.ProductTable.delete(*self.ProductTable.get_children())
            for row in rows:
                self.ProductTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def get_data(self,ev):
        f=self.ProductTable.focus()
        content=(self.ProductTable.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_cat.set(row[1])
        self.var_sup.set(row[2])
        self.var_name.set(row[3])
        self.var_price.set(row[4])
        self.var_qty.set(row[5])
        self.var_status.set(row[6])

    def update(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error","Please select product from list",parent=self.root)
            else:
                cur.execute("Select * from product where pid=?",(self.var_pid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Product",parent=self.root)
                else:
                    cur.execute("update product set Category=?,Supplier=?,name=?,price=?,qty=?,status=? where pid=?",(
                        self.var_cat.get(),
                        self.var_sup.get(),
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_qty.get(),
                        self.var_status.get(),
                        self.var_pid.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Product Updated Successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error","Select Product from the list",parent=self.root)
            else:
                cur.execute("Select * from product where pid=?",(self.var_pid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Product",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op==True:
                        cur.execute("delete from product where pid=?",(self.var_pid.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Product Deleted Successfully",parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def clear(self):
        self.var_cat.set("Select")
        self.var_sup.set("Select")
        self.var_name.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.var_status.set("Active")
        self.var_pid.set("")
        self.var_searchby.set("Select")
        self.var_searchtxt.set("")
        self.show()

    
    def search(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_searchby.get()=="Select":
                messagebox.showerror("Error","Select Search By option",parent=self.root)
            elif self.var_searchtxt.get()=="":
                messagebox.showerror("Error","Search input should be required",parent=self.root)
            else:
                cur.execute("select * from product where "+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.ProductTable.delete(*self.ProductTable.get_children())
                    for row in rows:
                        self.ProductTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record found!!!",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

if __name__=="__main__":
    root=Tk()
    obj=productClass(root)
    root.mainloop()