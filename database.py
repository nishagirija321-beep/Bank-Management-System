from pymongo import MongoClient

# connect to local mongodb server
client = MongoClient("mongodb://localhost:27017/")

# create a database and a collection
db = client["bank_management"]
accounts_collection = db["accounts"]

print("MongoDB connected successfully")

def update_account(account):
    accounts_collection.update_one(
        {"Holder_id" : account._holder_id},
        {
            "$set" : {
                "Balance" : account._balance,
                "History" : account.history
            }
        }
    )