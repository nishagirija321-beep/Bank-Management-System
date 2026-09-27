from accountType import savingAccount, currentAccount
from tkinter import *
from tkinter import messagebox
from database import accounts_collection
from security import hash_pin

class Bank:
    def __init__(self, root,pin = '1234'):
        self.root = root
        self.accounts = {}
        self.next_id = 1001
        self._pin = pin
        self.load_accounts()

    def account_creation(self,profile_data = None):
        app = Toplevel(self.root)
        app.title("Account Creation")
        app.geometry("500x300")

        # Row 1: Name Label and Entry
        Label(app, text="Name:", font="Helvetica 12 bold").grid(row=1, column=1, sticky="w", padx=10, pady=10)
        name_var = StringVar()
        name_entry = Entry(app, textvariable=name_var, font=("Helvetica", 12), width=32)
        name_entry.grid(row=1, column=2, sticky="w", padx=10, pady=10)
        
        # Row 2: Account Type Label and Entry
        Label(app, text="Account Type (savings/current):", font="Helvetica 12 bold").grid(row=2, column=1, sticky="w", padx=10, pady=10)
        account_var = StringVar()
        account_entry = Entry(app, textvariable=account_var, font=("Helvetica", 12), width=32)
        account_entry.grid(row=2, column=2, sticky="w", padx=10, pady=10)

        # Choose 4-Digit Security PIN
        Label(app, text="Set 4-Digit PIN:", font="Helvetica 12 bold").grid(row=3, column=1, sticky="w", padx=10, pady=10)
        pin_var = StringVar()
        Entry(app, textvariable=pin_var, show="*", font=("Helvetica", 12), width=32).grid(row=3, column=2, padx=10, pady=10)


        def process_creation():
            try:
                holder_id = self.next_id
                name = name_var.get().strip()
                account = account_var.get().strip().lower() # Standardise input string
                pin = pin_var.get().strip()

                if not name :
                    messagebox.showerror("Error", "Name cannot be empty")
                    return
                
                if not pin:
                    messagebox.showerror("Error", "PIN cannot be empty")
                    return

                if len(pin) != 4 or not pin.isdigit():
                    messagebox.showerror("Error", "PIN must be exactly 4 numeric digits!")
                    return

                hashed_pin = hash_pin(pin)
                if account == "savings":
                    new_account = savingAccount(self.root, name, holder_id, pin=hashed_pin)
                elif account == "current":
                    new_account = currentAccount(self.root, name, holder_id, pin=hashed_pin) 
                else:
                    messagebox.showerror("Error", "Invalid account type. Please enter 'savings' or 'current'.")
                    return

                new_account.profile_data = profile_data or {
                    "Personal Information": {},
                    "Contact Information" : {}
                }
                self.accounts[holder_id] = new_account

                account_document = ({
                    "Holder_id" : holder_id,
                    "Holder_name" : name,
                    "Pin" : hash_pin(pin),
                    "Account-Type" : type(new_account).__name__,
                    "Balance" : 0.0,
                    "History" : [],
                    "Profile-Data" : profile_data or {
                        "Personal Information" : {},
                        "Contact information" : {}
                    }
                })
                if isinstance(new_account,savingAccount):
                    account_document["Interest Rate"] = new_account.interest_rate
                
                if isinstance(new_account,currentAccount):
                    account_document["Overdraft Money"] = new_account.overdraft_money

                accounts_collection.insert_one(account_document)
                
                new_account.bank = self
                self.next_id += 1  
                
                print(f"Account created successfully! Name: {name}, ID: {holder_id}")
                messagebox.showinfo("Success", f"Account for {name} created successfully!\nYour Account ID is: {holder_id}")
                app.destroy() # Automatically close window on success
                
            except Exception as e:
                messagebox.showerror("Error", f"Account creation failed: {e}")
                print("Account creation failed")

        # Submit Button 
        submit_btn = Button(app, text="Create Account", font="Helvetica 10 bold", command=process_creation)
        submit_btn.grid(row=4, column=1, columnspan=2, pady=20)

    def get_account(self, holder_id):
        return self.accounts.get(holder_id, None)

    def load_accounts(self):
        try:
            data = accounts_collection.find()

            for info in data:
                holder_id = int(info["Holder_id"])
                holder_name = info["Holder_name"]
                pin = info.get("Pin","1234")
                
                account_type = info.get("Account-Type")
                if account_type == "savingAccount":
                    interest_rate = info.get("Interest Rate",0.04)
                    account = savingAccount(self.root,holder_name, holder_id, interest_rate = interest_rate, pin = pin)

                elif account_type == "currentAccount":
                    overdraft_money = info.get("Overdraft Money",1000)   
                    account = currentAccount(self.root, holder_name, holder_id, overdraft_money = overdraft_money, pin = pin)

                else:
                    continue

                account._balance = info.get("Balance",0.0)
                account.history = info.get("History",[])
                account.profile_data = info.get("Profile-Data" , {
                    "Personal Information" : {},
                    "Contact Information" : {}
                })

                self.accounts[holder_id] = account
                account.bank = self

            if self.accounts:
                self.next_id = max(self.accounts.keys())+1

        except Exception as e:
            messagebox.showerror("Database Error",f" Could not load saved accounts:\n{e}")

