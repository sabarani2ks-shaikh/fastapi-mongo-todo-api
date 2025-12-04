import sqlite3

class TodoManager:
    # __init__ mein sirf database ka naam save karen
    def __init__(self, db_name):
        self.db_name = db_name

    # create_table function
    def create_table(self):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY, 
                        name TEXT NOT NULL
                    )
                """)
                conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")

    # add_task function
    def add_task(self, task_name):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                # Use parameterized query to prevent SQL injection
                cursor.execute("INSERT INTO tasks (name) VALUES(?)", (task_name,))
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Error adding task: {e}")
            return False

    # show_tasks function (Data ko return karegi, print nahi)
    def show_tasks(self):
        try:
            # Har bar naya aur fresh connection banayen
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                
                # id aur name retrieve karen
                cursor.execute("SELECT id, name FROM tasks")
                result = cursor.fetchall()
                
                # Data return karen (FastAPI isko JSON mein badal dega)
                return result if result else []
                
        except sqlite3.Error as e:
            print(f"Database Error in show_tasks: {e}")
            return []

    # delete_task function (Agar aapne ye banaya hai to ise bhi update karen)
    def delete_task(self, task_id):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                # task_id ko tuple mein dena zaroori hai
                cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
                conn.commit()
                return cursor.rowcount > 0 # Return True agar koi row delete hui
        except sqlite3.Error as e:
            print(f"Error deleting task: {e}")
            return False

# Zaroori: File ke end mein koi bhi user input ya loop wala code nahi hona chahiye (CLI code remove kar diya gaya hai).