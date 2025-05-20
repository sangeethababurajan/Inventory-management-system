from tkinter import *
from tkinter import messagebox
import sqlite3


class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - Inventory Management System")
        self.root.geometry("400x300+500+200")
        self.root.config(bg="white")
        self.root.resizable(False, False)

        # Title
        title = Label(self.root, text="Login", font=("times new roman", 30, "bold"), bg="white", fg="#010c48")
        title.pack(side=TOP, pady=20)

        # User ID Label and Entry
        lbl_user = Label(self.root, text="User ID", font=("times new roman", 15), bg="white")
        lbl_user.place(x=50, y=100)
        self.txt_user = Entry(self.root, font=("times new roman", 15), bg="#ececec")
        self.txt_user.place(x=150, y=100, width=200)

        # Password Label and Entry
        lbl_pass = Label(self.root, text="Password", font=("times new roman", 15), bg="white")
        lbl_pass.place(x=50, y=150)
        self.txt_pass = Entry(self.root, font=("times new roman", 15), show="*", bg="#ececec")
        self.txt_pass.place(x=150, y=150, width=200)

        # Login Button
        btn_login = Button(self.root, text="Login", command=self.login, font=("times new roman", 15, "bold"),
                           bg="#4caf50", fg="white", cursor="hand2")
        btn_login.place(x=150, y=200, width=100)

    def login(self):
        # Fetch user input
        user_id = self.txt_user.get()
        password = self.txt_pass.get()

        # Check credentials in the database
        con = sqlite3.connect('ims.db')  # Replace 'ims.db' with your database path if needed
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM users WHERE user_id=? AND password=?", (user_id, password))
            user = cur.fetchone()
            if user:
                messagebox.showinfo("Success", "Login Successful!", parent=self.root)
                self.root.destroy()  # Close login window
                self.open_dashboard()  # Open main application
            else:
                messagebox.showerror("Error", "Invalid User ID or Password!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def open_dashboard(self):
        from dashboard import IMS 
        root = Tk()
        IMS(root)
        root.mainloop()


if __name__ == "__main__":
    root = Tk()
    LoginPage(root)
    root.mainloop()