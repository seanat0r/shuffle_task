import os
from src import config
import mysql, mysql.connector
from dotenv import load_dotenv

class Database:
    def __init__(self):
        load_dotenv()
        self.create_database()
        self.load_database()
        
    def create_database(self):
        create_db = mysql.connector.connect(
            host = os.getenv("DB_HOST"),
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD"),
        )
        
        mycursor = create_db.cursor()
        
        sql_string_create_database = """
            CREATE DATABASE IF NOT EXISTS shuffle_task
            DEFAULT CHARACTER SET = 'utf8mb4';
        """
        
        sql_string_use_database = """
            USE shuffle_task;
        """
        
        sql_string_create_table = """
            CREATE TABLE IF NOT EXISTS tasks (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                duration INT NOT NULL DEFAULT 0,
                is_favorite BOOLEAN NOT NULL DEFAULT FALSE,
                description TEXT,
                energy_level ENUM('fun', 'low', 'medium', 'high') NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """
        
        mycursor.execute(sql_string_create_database)
        mycursor.execute(sql_string_use_database)
        mycursor.execute(sql_string_create_table)
        
        create_db.commit()
        
        mycursor.close()
        create_db.close()
        
    def load_database(self):
        self.mydb = mysql.connector.connect(
            host = os.getenv("DB_HOST"),
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD"),
            database = os.getenv("DB_DATABASE")
        )
    
    def get_random_task(self, energy_level):
        if not energy_level:
            print(f"No ${energy_level} set")
            return None
        if energy_level not in config.VALID_LEVELS:
            print(f"enegry_level has wrong value!")
            return None
        
        mycursor = self.mydb.cursor(dictionary=True)
        
        sql = """
        SELECT *
        FROM tasks
        WHERE energy_level = %s
        ORDER BY RAND()
        LIMIT 1
        """
        
        val = energy_level
        mycursor.execute(sql, (val,))
        
        result = mycursor.fetchone()
        
        mycursor.close()
        return result
    
    def add_task(self, task_obj):
        title = task_obj.title
        duration = task_obj.duration
        is_favorite = task_obj.is_favorite
        description = task_obj.description
        energy_level = task_obj.energy_level
        
        if title is None:
            print(f"title canno't be null: {title}")
            return
        
        if energy_level not in config.VALID_LEVELS and energy_level is not None:
            print(f"energy_level canno't be other than: None, fun, low, medium and high; {energy_level}")
            return
        
        mycursor = self.mydb.cursor()
        
        val = (title, duration, is_favorite, description, energy_level)

        sql = """
            INSERT INTO tasks(title, duration, is_favorite, description, energy_level)
            VALUES (%s, %s, %s, %s, %s);
            """
        try:
            mycursor.execute(sql, val)
            self.mydb.commit()
            print (f"Task: {title} was successfully created.")
        except mysql.connector.Error as err:
            print(f"error: {err}")
        finally:
            mycursor.close()
        
    def delete_task(self, task_current, delete_isTrue):
        task_id = task_current.id
        title = task_current.title

        if not delete_isTrue:
            print(f"No authorization: {delete_isTrue}")
            return

        if task_id is None or title is None:
            print(f"ID or/ and title cannot be none: id: {task_id}; title: {title}")
            return

        mycursor = self.mydb.cursor()

        val = (task_id, title)
        sql = """
        DELETE FROM tasks WHERE id = %s AND title = %s;
        """

        try:
            mycursor.execute(sql, val)
            self.mydb.commit()

            if mycursor.rowcount > 0:
                print(f"Task {task_id}, {title} was successfully deleted!")
            else:
                print(f"No match found: No task deleted with ID {task_id} and title {title}")
        except mysql.connector.Error as err:
            print(f"error: {err}")
        finally:
            mycursor.close()    