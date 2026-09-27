from tkinter import *
from tkcalendar import DateEntry 
from tkinter import messagebox
import re

class AccountDetailsForm:
    def __init__(self, root,on_complete = None):
        self.root = root
        self.on_complete = on_complete
        self.profile_data = {
            "Personal Information": {},
            "Contact Information": {}
        }

    def personal_details(self):

        app = Toplevel(self.root)
        app.title("Personal Information")
        app.geometry("550x550")

        # Name 
        Label(app, text="Name:", font="Helvetica 12 bold").grid(row=1, column=1, sticky="w", padx=10, pady=10)
        name = StringVar()
        Entry(app, textvariable=name, font=("Helvetica", 12), width=25).grid(row=1, column=2, sticky="w", padx=10, pady=10)

        # Age
        Label(app, text="Age:", font="Helvetica 12 bold").grid(row=2, column=1, sticky="w", padx=10, pady=10)
        age = StringVar()
        Entry(app, textvariable=age, font=("Helvetica", 12), width=25).grid(row=2, column=2, sticky="w", padx=10, pady=10)

        # Date of Birth
        Label(app, text="Date of Birth:", font="Helvetica 12 bold").grid(row=3, column=1, sticky="w", padx=10, pady=10)
        dob_entry = DateEntry(app, width=22, font=("Helvetica", 12), date_pattern='dd/mm/yyyy')
        dob_entry.grid(row=3, column=2, sticky="w", padx=10, pady=10)

        # Father/Spouse Name
        Label(app, text="Father / Spouse Name:", font="Helvetica 12 bold").grid(row=4, column=1, sticky="w", padx=10, pady=10)
        parent = StringVar()
        Entry(app, textvariable=parent, font=("Helvetica", 12), width=25).grid(row=4, column=2, sticky="w", padx=10, pady=10)

        # Nationality
        Label(app, text="Nationality:", font="Helvetica 12 bold").grid(row=5, column=1, sticky="w", padx=10, pady=10)
        national = StringVar()
        Entry(app, textvariable=national, font=("Helvetica", 12), width=25).grid(row=5, column=2, sticky="w", padx=10, pady=10)

        # Gender Selection
        text_var = StringVar(value="Male")
        Label(app, text="Gender:", font="Helvetica 12 bold").grid(row=6, column=1, sticky="nw", padx=10, pady=10)
        gender_frame = Frame(app)
        gender_frame.grid(row=6, column=2, sticky="w", padx=10, pady=5)
        for ch in ["Male", "Female", "Other"]:
            Radiobutton(gender_frame, text=ch, variable=text_var, value=ch, font=("Helvetica", 11)).pack(anchor="w")

        # Marital Status
        marital_val = StringVar(value="Unmarried")
        Label(app, text="Marital Status:", font="Helvetica 12 bold").grid(row=7, column=1, sticky="nw", padx=10, pady=10)
        marital_frame = Frame(app)
        marital_frame.grid(row=7, column=2, sticky="w", padx=10, pady=5)
        for ch in ["Married", "Unmarried"]:
            Radiobutton(marital_frame, text=ch, variable=marital_val, value=ch, font=("Helvetica", 11)).pack(anchor="w")

        def collect_info():

            try:
                age_value = int(age.get())
                if age_value <= 0:
                    messagebox.showerror("Invalid Age","Age must be greater than zero")
                    return
            except ValueError:
                messagebox.showerror("Invalid Age","Please enter a valid age.")
                return

            name_value = name.get().strip()
            if name_value == "":
                messagebox.showerror("Invalid Name","Please enter your name.")
                return

            if age_value <= 0 or age_value > 120:
                messagebox.showerror("Invalid Age","Please enter valid age between 1 and 120.")
                return
            
            # Save the structural dataset directly onto your persistent account object reference
            self.profile_data["Personal Information"] = { 
                "Name": name_value,
                "Age": age_value,
                "Date of Birth": dob_entry.get(),
                "Father/Spouse Name": parent.get().strip(),
                "Nationality": national.get().strip(),
                "Gender": text_var.get(),
                "Marital Status": marital_val.get()
            }
            messagebox.showinfo("Success", "Personal Info saved to your profile record!")
            app.destroy() 

            # automatically opens contact details
            self.contact_details()

        # Action Submit Button
        Button(app, text="Save Personal Details", font="Helvetica 12 bold", command=collect_info).grid(row=8, column=2, pady=20)

    def contact_details(self):
        app = Toplevel(self.root)
        app.title("Contact Information")
        app.geometry("500x400")

        # Address Field
        Label(app, text="Address:", font="Helvetica 12 bold").grid(row=1, column=1, sticky="nw", padx=10, pady=10)
        your_address = Text(app, font=("Helvetica", 12), height=4, width=25)
        your_address.grid(row=1, column=2, sticky="w", padx=10, pady=10)

        # Contact Number
        Label(app, text="Contact Number:", font="Helvetica 12 bold").grid(row=2, column=1, sticky="w", padx=10, pady=10)
        number = StringVar()
        Entry(app, textvariable=number, font=("Helvetica", 12), width=25).grid(row=2, column=2, sticky="w", padx=10, pady=10)

        # Email ID Form
        Label(app, text="Email ID:", font="Helvetica 12 bold").grid(row=3, column=1, sticky="w", padx=10, pady=10)
        email = StringVar()
        Entry(app, textvariable=email, font=("Helvetica", 12), width=25).grid(row=3, column=2, sticky="w", padx=10, pady=10)

        def contact_info():
            email_text = email.get().strip()
            email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        
            if not re.match(email_pattern, email_text):
                messagebox.showerror("Invalid Input", "Please enter a valid Email ID (e.g., example@domain.com)")
                return
            
            # Extract texts securely
            address_text = your_address.get("1.0", "end-1c").strip()
            number_text = number.get().strip()

            if not number_text.isdigit() or len(number_text) != 10:
                messagebox.showerror("Invalid Number","Please enter a valid 10-digit contact number")
                return

            if address_text == " ":
                messagebox.showerror("Invalid Address","Please enter valid address" )
                return

            # Append the data package safely onto the runtime account profile dictionary map
            self.profile_data["Contact Information"] = {
                "address": address_text,
                "number": number_text,
                "email": email_text
            }

            messagebox.showinfo("Success", "Contact details updated successfully!")
            app.destroy() 

            # allow account creation
            if self.on_complete:
                self.on_complete(self.profile_data)

        # Submit Button
        Button(app, text="Save Contact Details", font="Helvetica 12 bold", command=contact_info).grid(row=4, column=2, pady=20)
