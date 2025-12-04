# main.py
from fastapi import FastAPI, HTTPException
# Mongo Manager Class ko import karen
from mongo_manager import MongoTodoManager 

from pydantic import BaseModel # POST request mein data validation ke liye


# main.py mein Pydantic models ke niche ye shamil karen
class TaskUpdate(BaseModel):
    # Ye fields optional hain taaki aap sirf name ya sirf completed badal saken
    name: str | None = None
    completed: bool | None = None

# --- FastAPI Setup ---
app = FastAPI()

# 4. PUT Endpoint: Task ko update karna (CRUD: Update)
@app.put("/tasks/{task_id}")
def update_existing_task(task_id: str, task: TaskUpdate):
    if not mongo_manager:
        return {"error": "Database connection is not active"}, 500
    try:
       # from bson.objectid import objectId
        from bson import objectId
        objectId(task_id)
    except Exception:
        HTTPException(status_code=404, detail="task id format invalid")
        
    # Pydantic model se sirf woh data nikalen jo user ne bheja hai (non-None values)
    update_data = task.model_dump(exclude_none=True) 

    if not update_data:
        return {"message": "No data provided to update"}, 400

    success = mongo_manager.update_task(task_id, update_data)
    
    if success:
        return {"message": "Task updated successfully"}
    else:
        HTTPException(status_code=404, detail="task not found")
# 5. DELETE Endpoint: Task ko delete karna (CRUD: Delete)
@app.delete("/tasks/{task_id}")
def delete_task_by_id(task_id: str):
    if not mongo_manager:
        raise   
    HTTPException(status_code=500, detail="Database connection is not active")
    
    
    # ID Validation (jaisa pehle update mein dala tha)
    try:
        from bson import ObjectId
        ObjectId(task_id) 
    except Exception:
         HTTPException(status_code=400, detail="task id invalid")
    
    success = mongo_manager.delete_task(task_id)
    
    if success:
        return {"message": "Task deleted successfully"}
    else:
         # Agar ID sahi ho lekin MongoDB mein woh task na mile
        raise
    HTTPException(status_code=404, detail="task not found")
    
# --- MongoDB Setup ---
# Localhost string istemal karen (Aapke local server ke liye)
# Ye default port hai jab aap MongoDB Community Server install karti hain
LOCAL_MONGO_URI = "mongodb://localhost:27017/" 

# MongoDB Manager ka instance banayen (todo_db database use hoga)
# Agar connection mein error ho to yahan aayega
try:
    mongo_manager = MongoTodoManager(connection_string=LOCAL_MONGO_URI, db_name="todo_db")
except Exception as e:
    print(f"MongoDB Connection Failed: {e}")
    # Agar connection fail ho to app ko roken
    mongo_manager = None

# Pydantic Model: Naye task ke data structure ko define karta hai
class Task(BaseModel):
    name: str

# 1. Root Endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to Sabarani's MongoDB API (FastAPI)"}

# 2. GET Endpoint: Sabhi tasks ko dekhna
@app.get("/tasks")
def get_all_tasks():
    if not mongo_manager:
        return {"error": "Database connection is not active"}, 500
    
    # MongoManager se tasks mangwayen
    tasks_data = mongo_manager.show_tasks()
    
    # Ye tasks JSON format mein return honge
    return {"tasks": tasks_data} 

# 3. POST Endpoint: Naya task add karna (CRUD: Create)
@app.post("/tasks")
def add_new_task(task: Task):
    if not mongo_manager:
        return {"error": "Database connection is not active"}, 500
        
    inserted_id = mongo_manager.add_task(task.name)
    
    return {"message": "Task added successfully", "id": inserted_id, "name": task.name}

# NOTE: Is file ko terminal mein aise chalaen: uvicorn main:app --reload