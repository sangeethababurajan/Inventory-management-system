from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import time
import sqlite3
import os
from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import salesClass
from billing import billClass


class IMS:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+110+80")
        self.root.title("Inventory Management System |")
        self.root.resizable(False, False)
        self.root.config(bg="#f7f7f7")  # Light pastel background

        # -------- Title ---------
        self.icon_title = PhotoImage(file="C:\\Users\\Sangeetha\\Downloads\\Inventory-Management-System-main\\Inventory-Management-System-main\\images\\logo1.png")
        title = Label(self.root, text="Inventory Management System", image=self.icon_title, compound=LEFT,
                      font=("Helvetica", 35, "bold"), bg="#fbe0e0", fg="black", anchor="w", padx=20)
        title.place(x=0, y=0, relwidth=1, height=70)

        # -------- Logout Button --------
        btn_logout = Button(self.root, text="Logout", font=("Helvetica", 15, "bold"), bg="#e53935", fg="white",
                            cursor="hand2").place(x=1150, y=10, height=50, width=150)

        # -------- Clock --------
        self.lbl_clock = Label(self.root,
                               text="Welcome to Inventory Management System\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS",
                               font=("Helvetica", 15), bg="#e5d4ef", fg="black")
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

        # -------- Left Menu --------
        self.MenuLogo = Image.open("C:\\Users\\Sangeetha\\Downloads\\Inventory-Management-System-main\\Inventory-Management-System-main\\images\\menu_im.png")
        self.MenuLogo = self.MenuLogo.resize((180, 180), Image.Resampling.LANCZOS)
        self.MenuLogo = ImageTk.PhotoImage(self.MenuLogo)

        LeftMenu = Frame(self.root, bd=2, relief=RIDGE, bg="#f1f8e9")  # Soft pastel green
        LeftMenu.place(x=0, y=102, width=200, height=565)

        lbl_menuLogo = Label(LeftMenu, image=self.MenuLogo, bg="#f1f8e9")
        lbl_menuLogo.pack(side=TOP, fill=X)

        lbl_menu = Label(LeftMenu, text="Menu", font=("Helvetica", 20, "bold"), bg="#fbe0e0", fg="black")
        lbl_menu.pack(side=TOP, fill=X)

        self.icon_side = PhotoImage(file="C:\\Users\\Sangeetha\\Downloads\\Inventory-Management-System-main\\Inventory-Management-System-main\\images\\side.png")

        menu_items = [("Employee", self.employee), ("Supplier", self.supplier),
                      ("Category", self.category), ("Products", self.product),
                      ("Sales", self.sales), ("Billing", self.billing), ("Exit", root.quit)]

        for text, command in menu_items:
            Button(LeftMenu, text=text, command=command, image=self.icon_side, compound=LEFT, padx=10,
                   anchor="w", font=("Helvetica", 15, "bold"), bg="#ffffff", bd=2, cursor="hand2").pack(side=TOP, fill=X)

        # -------- Dashboard Content --------
        colors = ["#90caf9", "#f48fb1", "#80cbc4", "#b0bec5", "#ffe082"]  # Pastel tones
        labels = [("Total Employee\n{ 0 }", 300, 120), ("Total Supplier\n{ 0 }", 650, 120),
                  ("Total Category\n{ 0 }", 1000, 120), ("Total Product\n{ 0 }", 300, 300),
                  ("Total Sales\n{ 0 }", 650, 300)]

        self.stat_labels = []
        for i, (text, x, y) in enumerate(labels):
            lbl = Label(self.root, text=text, bd=5, relief=RIDGE, bg=colors[i], fg="black",
                        font=("Helvetica", 20, "bold"))
            lbl.place(x=x, y=y, height=150, width=300)
            self.stat_labels.append(lbl)

        # -------- Footer --------
        lbl_footer = Label(self.root,
                           text="IMS-Inventory Management System\n 2024 All Rights Reserved",
                           font=("Helvetica", 12), bg="#fbe0e0", fg="black")
        lbl_footer.pack(side=BOTTOM, fill=X)

        self.update_content()

    # -------- Functions --------
    def employee(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = employeeClass(self.new_win)

    def supplier(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = supplierClass(self.new_win)

    def category(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = categoryClass(self.new_win)

    def product(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = productClass(self.new_win)

    def sales(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = salesClass(self.new_win)

    def billing(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = billClass(self.new_win)

    def update_content(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("select * from product")
            product = cur.fetchall()
            self.stat_labels[3].config(text=f"Total Product\n[ {str(len(product))} ]")

            cur.execute("select * from category")
            category = cur.fetchall()
            self.stat_labels[2].config(text=f"Total Category\n[ {str(len(category))} ]")

            cur.execute("select * from employee")
            employee = cur.fetchall()
            self.stat_labels[0].config(text=f"Total Employee\n[ {str(len(employee))} ]")

            cur.execute("select * from supplier")
            supplier = cur.fetchall()
            self.stat_labels[1].config(text=f"Total Supplier\n[ {str(len(supplier))} ]")

            # Ensure 'bills' directory exists
            if not os.path.exists("bills"):
                os.makedirs("bills")
            bill = len(os.listdir("bills"))
            self.stat_labels[4].config(text=f"Total Sales\n[ {str(bill)} ]")

            time_ = time.strftime("%I:%M:%S")
            date_ = time.strftime("%d-%m-%Y")
            self.lbl_clock.config(
                text=f"Welcome to Inventory Management System\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
            self.lbl_clock.after(200, self.update_content)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = IMS(root)
    root.mainloop()
