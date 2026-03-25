import pytest
from src.config import VALID_LEVELS
from src.database import Database

@pytest.fixture
def db_instance():
    db = Database()
    yield db
    
    cursor = db.mydb.cursor()
    cursor.execute("DELETE FROM tasks WHERE title LIKE '%Test%' OR title = 'Delete Me'")
    db.mydb.commit()
    cursor.close()

class Test_Database:
    def test_connection(self, db_instance):
        assert db_instance.mydb is not None
        assert db_instance.mydb.is_connected()
        
    def test_add_task(self, db_instance):
        class TaskMock:
            title = 'Test Task'
            duration = 10
            is_favorite = False
            description = 'Test'
            energy_level = 'low'
            
        test_task = TaskMock()
        
        db_instance.add_task(test_task)
        
        cursor = db_instance.mydb.cursor(dictionary=True)
        sql = """
        SELECT *
        FROM tasks
        WHERE title = %s
        """
        cursor.execute(sql, (test_task.title,))
        
        result = cursor.fetchone()
        
        assert result is not None
        assert result['title'] == 'Test Task'
        assert result['energy_level'] == 'low'
        
        cursor.close()
    def test_delete_task(self, db_instance):
        task_title = "Delete Me"
        cursor = db_instance.mydb.cursor()
        cursor.execute("INSERT INTO tasks (title, energy_level) VALUES (%s, %s)", (task_title, "fun"))
        db_instance.mydb.commit()
        task_id = cursor.lastrowid
        cursor.close()
        
        class Task_to_delete:
            id = task_id
            title = task_title
        
        new_task = Task_to_delete()

        db_instance.delete_task(new_task, True)

        cursor = db_instance.mydb.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
        result = cursor.fetchone()
        
        assert result is None
        cursor.close()
        
    def test_get_random_task(self, db_instance):
        class TaskMock:
            title = 'Zufalls-Test'
            duration = 5
            is_favorite = False
            description = 'Test'
            energy_level = 'low'
    
        db_instance.add_task(TaskMock())
        result = db_instance.get_random_task('low')
        
        assert result is not None
        assert result['energy_level'] == 'low'
        assert 'title' in result