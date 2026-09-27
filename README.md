# Banking Management System

```
A Python-based Banking Management System built as an educational project to practice Python, Object-Oriented Programming, GUI development, database integration, and basic security.
```

## Features

```
- Create Savings and Current accounts
- Personal and contact information management
- Account ID and PIN-based login
- Secure PIN hashing
- PIN reset
- Deposit money
- Withdraw money
- Transfer money between accounts
- Transaction history
- Savings account interest calculation
- Current account overdraft facility
- Input validation and error handling
- Persistent data storage using MongoDB
- Tkinter-based graphical user interface
```

## Technologies Used

```
- Python
- Tkinter
- MongoDB
- PyMongo
- Tkcalendar
- hashlib
```

## Project Structure

```text
Banking Management System/
│
├── main.py
├── accountCreation.py
├── accountType.py
├── transaction.py
├── Login.py
├── details.py
├── database.py
├── security.py
├── requirements.txt
├── .gitignore
└── README.md

```

##How to Run

1. Clone the repository

```
git clone <https://github.com/nishagirija321-beep/Bank-Management-System>
```

2. Open the project folder

```
-cd Bank Management
```

3. Install the required packages

```
-pip install -r requirements.txt
```

4. Make sure MongoDB is running

```
-The application uses a local MongoDB database named:
bank_management
The application automatically uses the accounts collection.
```

5. Run the application

```
-python main.py
```

##Database

```
The application stores account information in MongoDB, including:
-Account ID
-Account holder name
-Hashed PIN
-Account type
-Balance
-Transaction history
-Personal information
-Contact information
-Interest rate for Savings accounts
-Overdraft limit for Current accounts
```

##Security

```
PINs are not stored as plain text. The application uses Python's hashlib library to create a SHA-256 hash of the PIN before storing it in MongoDB.
```

```
Note: This is an educational project and is not intended for production banking use. Real banking applications require additional security measures, encryption, auditing, authorization, and secure infrastructure.

```

##Learning Outcomes

Through this project, I practiced:

```
-Python Object-Oriented Programming
-Inheritance
-Modular programming
-Exception handling
-GUI development with Tkinter
-MongoDB database integration
-CRUD operations
-Input validation
-Authentication
-Basic security practices
-Designing and maintaining a multi-file Python application

```

##Future Improvements

```
-Possible future improvements include:
-Automated unit testing
-More structured transaction records
-Stronger authentication
-Role-based access
-Improved database security
-Deployment using a cloud database
```
