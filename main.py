from tkinter import *
from tkinter import messagebox
from accountCreation import Bank
from details import AccountDetailsForm
from accountType import savingAccount, currentAccount
from Login import LoginSystem

# Helper function to clear out the current view before drawing a new page
def clear_frame():
    for widget in content_frame.winfo_children():
        widget.destroy()

# --- PAGE 1: THE MAIN MENU ---
def show_main_menu():
    clear_frame()
    
    Label(content_frame, text="=== Bank Management System ===", font="Helvetica 14 bold").pack(pady=20)
    
    # 1. Account Creation Button
    Button(content_frame, text="1. Create Account Window", font="Helvetica 12 bold", width=25, 
           command=show_personal_details).pack(pady=10)
    
    # 2. Login Button -> routes to the page where they select saving/current details
    Button(content_frame, text="2. Login To Account", font="Helvetica 12 bold", width=25, 
           command=show_input_page).pack(pady=10)
    
    # 3. Reset PIN Layout Button
    Button(content_frame, text="3. Reset PIN Layout", font="Helvetica 12 bold", width=25, 
           command=login_system.set_pin).pack(pady=10)
    
    # Exit App
    Button(content_frame, text="4. Exit System", font="Helvetica 12 bold", width=25, bg="red", fg="white",
           command=root.quit).pack(pady=15)

def show_personal_details():
    account_details_form.personal_details()

def show_input_page():
    clear_frame()
    
    Label(content_frame, text="=== Enter Account Details ===", font="Helvetica 14 bold").pack(pady=15)
    
    # To use grid inside the frame safely, we make a mini-subframe for the input form
    form_frame = Frame(content_frame)
    form_frame.pack(pady=10)
    
    Label(form_frame, text="Name:", font="Helvetica 12 bold").grid(row=0, column=0, sticky="w", padx=10, pady=10)
    name_var = StringVar()
    name_entry = Entry(form_frame, textvariable=name_var, font=("Helvetica", 12), width=25)
    name_entry.grid(row=0, column=1, padx=10, pady=10)

    Label(form_frame, text="Holder ID:", font="Helvetica 12 bold").grid(row=1, column=0, sticky="w", padx=10, pady=10)
    id_var = StringVar()
    id_entry = Entry(form_frame, textvariable=id_var, font=("Helvetica", 12), width=25)
    id_entry.grid(row=1, column=1, padx=10, pady=10)
    
    Label(form_frame, text="PIN:", font="Helvetica 12 bold").grid(row=2, column=0, sticky="w", padx=10, pady=10)
    pin_var = StringVar()
    pin_entry = Entry(form_frame, textvariable=pin_var, font=("Helvetica", 12), width=25)
    pin_entry.grid(row=2, column=1, padx=10, pady=10)
    
    # Navigation Buttons frame
    btn_frame = Frame(content_frame)
    btn_frame.pack(pady=15)
    
    # Button to log in as Savings
    Button(btn_frame, text="Login as Savings", font="Helvetica 10 bold", width=15, bg="lightblue",
           command=lambda: load_transaction_menu("savings", name_var, id_var, pin_var)).grid(row=0, column=0, padx=5)
           
    # Button to log in as Current
    Button(btn_frame, text="Login as Current", font="Helvetica 10 bold", width=15, bg="lightgreen",
           command=lambda: load_transaction_menu("current", name_var, id_var, pin_var)).grid(row=0, column=1, padx=5)
    
    # ↩️ BACK BUTTON: Returns directly to main menu
    Button(content_frame, text="← Back to Main Menu", font="Helvetica 11 bold", width=20,
           command=show_main_menu).pack(pady=10)

# --- PAGE 3: TRANSACTION MENU (DYNAMICS BASED ON ACCOUNT TYPE) ---
def load_transaction_menu(acc_type, name_var, id_var, pin_var):

    name = name_var.get().strip()
    raw_id = id_var.get().strip()
    raw_pin = pin_var.get().strip()

    if not name or not raw_id or not raw_pin:
        messagebox.showerror(
            "Error",
            "Please fill in all details before proceeding!"
        )
        return

    try:
        account_id = int(raw_id)
    except ValueError:
        messagebox.showerror(
            "Error",
            "Holder ID must be a valid number!"
        )
        return

    

    # Find the EXISTING account
    user_account = my_bank.get_account(account_id)

    if user_account is None:
        messagebox.showerror(
            "Login Failed",
            f"Account ID {account_id} does not exist."
        )
        return

    if not user_account.verify_pin(raw_pin):
        messagebox.showerror("Login Failed","Incorrect PIN")
        return
    
    # Check name
    if user_account.holder_name.lower() != name.lower():
        messagebox.showerror(
            "Login Failed",
            "Name does not match the account ID."
        )
        return

    # Check account type
    if acc_type == "savings":

        if not isinstance(user_account, savingAccount):
            messagebox.showerror(
                "Login Failed",
                "This is not a Savings Account."
            )
            return

    else:

        if not isinstance(user_account, currentAccount):
            messagebox.showerror(
                "Login Failed",
                "This is not a Current Account."
            )
            return

    # -------------------------------
    # NEW ACCOUNT DASHBOARD WINDOW
    # -------------------------------

    transaction_app = Toplevel(root)
    transaction_app.title("Account Dashboard")
    transaction_app.geometry("450x450")
    user_account.dashboard = transaction_app

    if acc_type == "savings":

        Label(
            transaction_app,
            text="=== Savings Account Menu ===",
            font="Helvetica 14 bold",
            fg="blue"
        ).pack(pady=15)

        Button(
            transaction_app,
            text="⭐ Add Interest",
            font="Helvetica 11 bold",
            width=22,
            command=user_account.add_interest
        ).pack(pady=5)

    else:

        Label(
            transaction_app,
            text="=== Current Account Menu ===",
            font="Helvetica 14 bold",
            fg="green"
        ).pack(pady=15)

    # Deposit
    Button(
        transaction_app,
        text="1. Deposit",
        font="Helvetica 12 bold",
        width=22,
        command=user_account.deposit_window
    ).pack(pady=5)

    # Withdraw
    Button(
        transaction_app,
        text="2. Withdraw",
        font="Helvetica 12 bold",
        width=22,
        command=user_account.withdrawal_window
    ).pack(pady=5)

    # Transfer
    Button(
        transaction_app,
        text="3. Transfer",
        font="Helvetica 12 bold",
        width=22,
        command=lambda: user_account.transfer_window(my_bank.accounts)
    ).pack(pady=5)

    # History
    Button(
        transaction_app,
        text="4. Transaction History",
        font="Helvetica 12 bold",
        width=22,
        command=user_account.history_window
    ).pack(pady=5)

    # Logout
    Button(
        transaction_app,
        text="Logout",
        font="Helvetica 11 bold",
        width=22,
        bg="orange",
        command=transaction_app.destroy
    ).pack(pady=15)
       
# --- MAIN APP RUNNER ---
if __name__ == "__main__":  
    root = Tk()
    root.title("Bank Management System")
    root.geometry("450x450") # Expanded slightly to safely fit grid fields nicely

    my_bank = Bank(root) 
    login_system = LoginSystem(root, my_bank) 

    def start_account_creation(profile_data):
        my_bank.account_creation(profile_data)

    account_details_form = AccountDetailsForm(root,on_complete = start_account_creation)

    # Central structural window frame where everything gets placed & cleared safely
    content_frame = Frame(root)
    content_frame.pack(fill="both", expand=True)

    show_main_menu()
    
    root.mainloop()
