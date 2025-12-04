# mongo_manager.py

from pymongo import MongoClient
from bson.objectid import ObjectId # MongoDB ki khas ID ko handle karta hai

class MongoTodoManager:
    # connection_string ab __init__ mein bahar se aayega
    def __init__(self, connection_string, db_name="todo_db"):
        
        try:
            # 1. Connection string ko use karte hue client banayen
            self.client = MongoClient(connection_string,serverSelectionTimeoutMS=5000)
        
            # Connection check karne ke liye ping
            self.client.admin.command('ping') 
            print(f"MongoDB Connected to DB: {db_name}")

            # 2. Database aur Collection select karen
            self.db = self.client[db_name]
            self.collection = self.db['tasks']
       
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            raise e
        
    # Task add karna (CRUD: Create)
    def add_task(self, task_name):
        task_data = {"name": task_name, "completed": False}
        result = self.collection.insert_one(task_data)
        # Inserted ID ko string mein badal kar wapas bhejte hain
        return str(result.inserted_id) 

    # Sabhi tasks dikhana (CRUD: Read)
    def show_tasks(self):
        # Database se sabhi documents nikalen
        tasks = list(self.collection.find({}))
        
        # FastAPI/JSON mein ObjectId nahi chalta, is liye string mein badlen
        for task in tasks:
            task['_id'] = str(task['_id']) 
        return tasks
    #update task
    def update_task(self, task_id,new_data):
        #id ko string sy mangdb k obj m badalna
        obj_id=ObjectId(task_id)
        #only update fields presnt in new data
        result = self.collection.update_one({"_id":obj_id},{"$set":new_data}
                                            )
        #agar doc mil jaye tu true return kary
        return result.modified_count>0
    # Task ko delete karna (CRUD: Delete)
    def delete_task(self, task_id):
        # ID ko string se MongoDB ki khas ObjectId mein badalna zaroori hai
        obj_id = ObjectId(task_id)
        
        # Task ko ID ki buniyad par delete karen
        result = self.collection.delete_one({"_id": obj_id})
        
        # Agar document delete ho jaye to True return karen
        return result.deleted_count > 0