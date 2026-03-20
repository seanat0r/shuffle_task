import os
import mysql, mysql.connector
from dotenv import load_dotenv

class Database:
    def __init__(self):
        load_dotenv()
        self.create_database()
        self.load_databas()
        
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
    
    def get_all_entries(self, energy_level):
        mycursor = self.mydb.cursor()
        
        sql = """
        SELECT *
        FROM tasks
        WHERE %s
        """
        
    def get_random_task(self, energy_level):
        if not energy_level:
            return print(f"No ${energy_level} set")
        if (energy_level != 'fun' or energy_level != 'low' or energy_level != 'medium' or energy_level != 'high'):
            return print(f"enegry_level has wrong value!")
        get_array = self.get_all_entries(energy_level)
        
        
        
        
        
if __name__ == "__main__":
    db = Database()
    print("connection should exists")
    