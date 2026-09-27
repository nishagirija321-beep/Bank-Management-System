from tkinter import *
from tkinter import messagebox
from database import update_account
from security import verify_pin

class Account:
    def __init__(self,root,holder_name,holder_id,pin='1234'):
        self.holder_name = holder_name
        self._holder_id = holder_id
        self._balance = 0.0
        self.history = []
        self.root = root
        self._pin = pin

    def verify_pin(self,pin):
        return verify_pin(pin,self._pin)

    def deposit_window(self,default_amount=None):
        app = Toplevel(self.dashboard)
        app.title("Deposit Funds")
        app.geometry("500x300")

        Label(app, text="Deposit Amount:", font="Helvetica 12 bold").grid(row=1, column=1, padx=10, pady=20)
                
        amount_var = StringVar()

        if default_amount is not None:
            amount_var.set(f"{default_amount:.2f}")

        amount_entry = Entry(app, textvariable=amount_var, font=("Helvetica", 12))
        amount_entry.grid(row=1, column=2, padx=10, pady=20)

        def process_deposit():
            try:
                amount = float(amount_var.get())
                if amount>0:
                    self._balance+=amount
                    self.history.append(f"Deposited: {amount:.2f} \t Total Amount: {self._balance:.2f}")
                    update_account(self)
                    messagebox.showinfo("Success", f"${amount:.2f} deposited successfully!\nNew Balance: ${self._balance:.2f}")
                    app.destroy() # Close the pop-up window
                    self.dashboard.deiconify()
                    self.dashboard.lift()
                    self.dashboard.focus_force()
                else:
                    messagebox.showerror("Error","Amount must be greater than zero")
            except ValueError:
                messagebox.showerror("Error","Please enter valid amount")

        submit_btn = Button(app, text="Submit", font="Helvetica 10 bold",bg="purple",fg="white",width=25,command=process_deposit)
        submit_btn.grid(row=2, column=1, columnspan=2, pady=10)

    def withdrawal_window(self):
        app = Toplevel(self.dashboard)
        app.title("Withdraw Funds")
        app.geometry("500x300")
        
        Label(app, text="Withdrawal Amount:", font="Helvetica 12 bold").grid(row=1, column=1, padx=10, pady=20)
                        
        amount_var = StringVar()
        amount_entry = Entry(app, textvariable=amount_var, font=("Helvetica", 12))
        amount_entry.grid(row=1, column=2, padx=10, pady=20)

        def process_withdrawal():
            try:
                amount = float(amount_var.get())
                if amount>0 and self._balance>=amount:
                    self._balance-=amount

                    self.history.append(f"Withdrawn: {amount:.2f} \t Total Amount: {self._balance}")
                    update_account(self)

                    messagebox.showinfo("Success", f"${amount:.2f} withdrawn successfully!\nNew Balance: ${self._balance:.2f}")
                    app.destroy() 
                    self.dashboard.deiconify()
                    self.dashboard.lift()
                    self.dashboard.focus_force()
                else:
                    messagebox.showerror("Error","Insufficient or invalid amount")
            except ValueError:
                messagebox.showerror("Error","Please enter valid amount")

        submit_btn = Button(app, text="Submit", font="Helvetica 10 bold",bg="light green",fg="white",width=25, command=process_withdrawal)
        submit_btn.grid(row=2, column=1, columnspan=2, pady=10)

    def transfer_window(self, accounts):
    # Pass your accounts dictionary/database into this method to check receiver IDs
        app = Toplevel(self.dashboard)
        app.title("Transfer Funds")
        app.geometry("500x300")
            
        # Row 1: Receiver Details
        Label(app, text="Receiver Account ID:", font="Helvetica 12 bold").grid(row=1, column=1, padx=10, pady=15, sticky="w")
        receiver_var = StringVar()
        receiver_entry = Entry(app, textvariable=receiver_var, font=("Helvetica", 12))
        receiver_entry.grid(row=1, column=2, padx=10, pady=15)
    
        Label(app, text="Transfer Amount:", font="Helvetica 12 bold").grid(row=2, column=1, padx=10, pady=15, sticky="w")
        amount_var = StringVar()
        amount_entry = Entry(app, textvariable=amount_var, font=("Helvetica", 12))
        amount_entry.grid(row=2, column=2, padx=10, pady=15)

        def process_transfer():
            try:
                receiver = int(receiver_var.get())
                amount = float(amount_var.get())
            
                if amount <= 0:
                    messagebox.showerror("Invalid Amount", "Please enter an amount greater than zero.")
                    return

                # Check if target user exists in our accounts storage dictionary
                if receiver not in accounts:
                    messagebox.showerror("Error", "Receiver account not found.")
                    return

                if receiver == self._holder_id:
                    messagebox.showerror("Invalid Transfer","You cannot transfer money to your own account.")
                    return
            
                if self._balance >= amount:
                    response = messagebox.askyesno("Confirm Action", "Are you sure you want to proceed?")

                    if response:
                        self._balance -= amount
                        accounts[receiver]._balance += amount

                    # Update history streams
                        self.history.append(f"Transferred ${amount:.2f} to {accounts[receiver].holder_name}'s ID {receiver} \t Total Amount: {self._balance}")
                        accounts[receiver].history.append(f"Received ${amount:.2f} from {self.holder_name} \t Total Amount: {accounts[receiver]._balance}")
                        update_account(self)
                        update_account(accounts[receiver])

                        messagebox.showinfo("Success", f"${amount:.2f} transferred successfully to Account {receiver}!")
                        app.destroy()
                        self.dashboard.deiconify()
                        self.dashboard.lift()
                        self.dashboard.focus_force()
                else:
                    messagebox.showerror("Balance Error", "Insufficient balance to execute this transfer.")
            except ValueError:
                messagebox.showerror("Input Error", "Please enter a valid Receiver ID and Amount.")

        submit_btn = Button(app, text="Submit", font="Helvetica 10 bold",bg="pink",fg="white",width=25 ,command=process_transfer)
        submit_btn.grid(row=3, column=1, columnspan=2, pady=20)

    def history_window(self):
        app = Toplevel(self.dashboard)
        app.title(f"{self.holder_name}'s Transaction Ledger")
        app.geometry("450x400")

        title_lbl = Label(app, text="=== Transaction History ===", font="Helvetica 14 bold", fg="navy")
        title_lbl.pack(pady=15)

        if not self.history:
            messagebox.showinfo("No Records", "No transactions found for this account yet.")
            app.destroy()
            self.dashboard.deiconify()
            self.dashboard.lift()
            self.dashboard.focus_force()
            return

    # Frame wrapper to contain our ledger history log neatly
        frame = Frame(app)
        frame.pack(fill="both", expand=True, padx=20, pady=10)

    # Use a Listbox to render each individual transaction record cleanly onto the GUI screen
        history_listbox = Listbox(frame, font=("Courier", 10), width=50, height=15)
        history_listbox.pack(side="left", fill="both", expand=True)

    # Add a clean scrollbar to scroll through long transaction chains smoothly
        scrollbar = Scrollbar(frame, orient="vertical", command=history_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        history_listbox.config(yscrollcommand=scrollbar.set)

        for index, record in enumerate(self.history):
            history_listbox.insert(END, f"{index + 1}. {record}")

