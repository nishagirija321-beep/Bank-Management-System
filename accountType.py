from transaction import Account
from tkinter import *
from tkinter import messagebox
from database import update_account

class savingAccount(Account):
    def __init__(self,root,holder_name,holder_id,interest_rate=0.04,pin='1234'):
        super().__init__(root,holder_name,holder_id,pin=pin)
        self.interest_rate = interest_rate

    def add_interest(self):
        interest = self._balance *self.interest_rate

        if interest > 0:
            self._balance += interest
            self.history.append(f"Interest Added: {interest:.2f} \t Total Balance: {self._balance}")
            update_account(self)

            messagebox.showinfo("Interest Added", f"Interest of ${interest:.2f} has been added.\nNew Balance: ${self._balance:.2f}")
        else:
            messagebox.showwarning("No Interest", "Balance is 0. No interest earned.")
        
class currentAccount(Account):
    def __init__(self,root,holder_name,holder_id,overdraft_money = 1000,pin='1234'):
            super().__init__(root,holder_name,holder_id,pin=pin)
            self.overdraft_money = overdraft_money

    def withdrawal_window(self):
        app = Toplevel(self.root)
        app.title("Overdraft Calculation")
        app.geometry("500x300")

        Label(app, text="Withdrawal Amount:", font="Helvetica 12 bold").grid(row=1, column=1, padx=10, pady=20)         

        amount_var = StringVar()
        
        amount_entry = Entry(app, textvariable=amount_var, font=("Helvetica", 12))
        amount_entry.grid(row=1, column=2, padx=10, pady=20)

        def process_withdraw():
            try:
                amount = float(amount_var.get())

                if amount <= 0:
                    messagebox.showerror("Error", "Amount must be greater than zero")
                    return
                
                if self._balance+self.overdraft_money >= amount:
                    self._balance -= amount
                    self.history.append(f"Withdrawn : {amount:.2f} \t Total Amount: {self._balance}")
                    update_account(self)
                    messagebox.showinfo("Success", f"Withdrew: ${amount:.2f}\nNew Balance: ${self._balance:.2f}")
                    app.destroy()
                    self.dashboard.deiconify()
                    self.dashboard.lift()
                    self.dashboard.focus_force()
                else:
                    messagebox.showerror("Error", f"Requested amount ${amount:.2f} exceeds your overdraft limit.")
            except ValueError:
                messagebox.showerror("Error","Please enter valid numeric amount")
        
        submit_btn = Button(app, text="Submit", font="Helvetica 10 bold", command=process_withdraw)
        submit_btn.grid(row=3, column=1, columnspan=2, pady=20)
        

    

