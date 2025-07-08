import sqlite3
import functools
from datetime import datetime


#### decorator to log SQL queries

def log_queries(func):


    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        if 'query' in kwargs:
            query = kwargs['query']
        # Method 2: If query is the first positional argument
        elif args:
            query = args[0]
        else:
            query = "No query found"

        # Log the SQL query with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [LOG] Executing SQL Query: {query}")


        result = func(*args, **kwargs)


        completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{completion_time}] [LOG] Query executed successfully")

        return result

    return wrapper


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


#
if __name__ == "__main__":
    # This will create a simple test database if it doesn't exist
    def setup_test_db():
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE
            )
        ''')
        # Insert some test data
        cursor.execute("INSERT OR IGNORE INTO users (name, email) VALUES ('John Doe', 'john@example.com')")
        cursor.execute("INSERT OR IGNORE INTO users (name, email) VALUES ('Jane Smith', 'jane@example.com')")
        conn.commit()
        conn.close()



    setup_test_db()

    #### fetch users while logging the query
    users = fetch_all_users(query="SELECT * FROM users")
    print(f"Retrieved {len(users)} users: {users}")