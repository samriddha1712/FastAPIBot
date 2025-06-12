from pymongo import MongoClient
import os
import datetime
import uuid

class Database:
    def __init__(self):
        try:
            connection_string = os.getenv("MONGODB_URI")
            self.client = MongoClient(
                connection_string,
                serverSelectionTimeoutMS=10000,
                connectTimeoutMS=20000,
                socketTimeoutMS=30000,
                retryWrites=True,
                retryReads=True,
                w="majority",
                maxIdleTimeMS=120000,
                maxPoolSize=20
            )
            self.client.admin.command('ping', socketTimeoutMS=5000)
            self.db = self.client[os.getenv("DB_NAME", "complaint_system")]
            self.complaints = self.db.complaints
        except Exception as e:
            print(f"MongoDB Connection Error: {str(e)}")
            raise

    def create_complaint(self, name, phone_number, email, complaint_details):
        complaint_id = str(uuid.uuid4())[:8].upper()
        complaint = {
            "complaint_id": complaint_id,
            "name": name,
            "phone_number": phone_number,
            "email": email,
            "complaint_details": complaint_details,
            "created_at": datetime.datetime.now()
        }
        self.complaints.insert_one(complaint)
        return complaint_id

    def get_complaint(self, complaint_id):
        result = self.complaints.find_one({"complaint_id": complaint_id})
        if not result:
            result = self.complaints.find_one({"complaint_id": {"$regex": f"^{complaint_id}$", "$options": "i"}})
        return result
