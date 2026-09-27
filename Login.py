from tkinter import *
from tkinter import messagebox
from database import accounts_collection
from security import hash_pin

class LoginSystem:

    def __init__(self, root, bank_instance):
        self.root = root
        self.bank = bank_instance 

    def login_window(self):
        app = Toplevel(self.root)
        app.title("Login")
        app.geometry("450x250")

        # Account ID 
        Label(app, text="Account ID:", font="Helvetica 12 bold").grid(row=1, column=1, sticky="w", padx=10, pady=10)
        id_var = StringVar()
        id_entry = Entry(app, textvariable=id_var, font=("Helvetica", 12), width=25)
        id_entry.grid(row=1, column=2, sticky="w", padx=10, pady=10)

        # PIN Input (Masked with show="*")
        Label(app, text="PIN:", font="Helvetica 12 bold").grid(row=2, column=1, sticky="w", padx=10, pady=10)
        pin_var = StringVar()
        pin_entry = Entry(app, textvariable=pin_var, show="*", font=("Helvetica", 12), width=25)
        pin_entry.grid(row=2, column=2, sticky="w", padx=10, pady=10)

        def process_login():
            raw_id = id_var.get().strip()
            pin = pin_var.get().strip()

            if not raw_id or not pin:
                messagebox.showerror("Error", "All fields are required!")
                return

            try:
            
                account_id = int(raw_id) 
            except ValueError:
                messagebox.showerror("Error", "Account ID must be a valid number!")
                return

            user_account = self.bank.get_account(account_id)
            
            if user_account:

                if user_account.verify_pin(pin):
                    messagebox.showinfo("Success", f"WELCOME BACK, {user_account.holder_name.upper()}!")
                    app.destroy()  
                   
                else:
                    messagebox.showerror("Error", "Incorrect PIN. Login failed!")
            else:
                messagebox.showerror("Error", f"Account ID {account_id} not found in system.")

        # Row 3: Submit Login Button 
        submit_btn = Button(app, text="Login", font="Helvetica 10 bold",bg="red",fg="white", command=process_login, width=15)
        submit_btn.grid(row=3, column=1, columnspan=2, pady=20)

    def set_pin(self):
        app = Toplevel(self.root)
        app.title("Reset PIN")
        app.geometry("450x280")

        # Verify user identity by Account ID
        Label(app, text="Account ID:", font="Helvetica 12 bold").grid(row=1, column=1, sticky="w", padx=10, pady=10)
        id_var = StringVar()
        id_entry = Entry(app, textvariable=id_var, font=("Helvetica", 12), width=25)
        id_entry.grid(row=1, column=2, sticky="w", padx=10, pady=10)

        # New PIN Input
        Label(app, text="New 4-Digit PIN:", font="Helvetica 12 bold").grid(row=2, column=1, sticky="w", padx=10, pady=10)
        newpin_var = StringVar()
        newpin_entry = Entry(app, textvariable=newpin_var, show="*", font=("Helvetica", 12), width=25)
        newpin_entry.grid(row=2, column=2, sticky="w", padx=10, pady=10)

        # Confirm New PIN Input
        Label(app, text="Confirm PIN:", font="Helvetica 12 bold").grid(row=3, column=1, sticky="w", padx=10, pady=10)
        confirmpin_var = StringVar()
        confirmpin_entry = Entry(app, textvariable=confirmpin_var, show="*", font=("Helvetica", 12), width=25)
        confirmpin_entry.grid(row=3, column=2, sticky="w", padx=10, pady=10)

        def process_pin():
            raw_id = id_var.get().strip()
            new_pin = newpin_var.get().strip()
            confirm_pin = confirmpin_var.get().strip()

            if not raw_id:
                messagebox.showerror("Error","Please enter your account ID")
                return
            
            try:
                account_id = int(raw_id)
            except ValueError:
                messagebox.showerror("Error", "Account ID must be a valid number!")
                return

            user_account = self.bank.get_account(account_id)

            if not user_account:
                messagebox.showerror("Error", f"Account ID {account_id} does not exist.")
                return

            if len(new_pin) != 4 or not new_pin.isdigit():
                messagebox.showerror("Error", "PIN must be exactly 4 numeric digits.")
                return

            response = messagebox.askyesno("Confirm Action", "Are you sure you want to change the pin?")
            if response:
                if new_pin == confirm_pin:

                    hashed_pin = hash_pin(new_pin)
                    user_account._pin = hashed_pin
                    accounts_collection.update_one(
                        {"Holder_id" : user_account._holder_id},
                        {
                            "$set" : {
                                "Pin" : hashed_pin
                            }
                        }
                    )
                    
                    messagebox.showinfo("Success", "PIN updated successfully!")
                    app.destroy()
                else:
                    messagebox.showerror("Error", "PINs do not match. Reset failed.")

        # Submit Pin Button 
        submit_btn = Button(app, text="Reset PIN", font="Helvetica 10 bold", command=process_pin, width=15)
        submit_btn.grid(row=4, column=1, columnspan=2, pady=20)
