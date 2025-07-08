import sqlite3
import functools


#### decorator to log SQL queries

def log_queries(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the query from function arguments
        # Method 1: If query is passed as keyword argument
        if 'query' in kwargs:
            query = kwargs['query']
        # Method 2: If query is the first positional argument
        elif args:
            query = args[0]
        else:
            query = "No query found"

        # Log the SQL query
        print(f"[LOG] Executing SQL Query: {query}")

        # Execute the original function
        result = func(*args, **kwargs)

        # Optionally log completion
        print(f"[LOG] Query executed successfully")

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


# Test the decorator
if __name__ == "__main__":

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

        cursor.execute("INSERT OR IGNORE INTO users (name, email) VALUES ('John Doe', 'john@example.com')")
        cursor.execute("INSERT OR IGNORE INTO users (name, email) VALUES ('Jane Smith', 'jane@example.com')")
        conn.commit()
        conn.close()



    setup_test_db()

    #### fetch users while logging the query
    users = fetch_all_users(query="SELECT * FROM users")
    print(f"Retrieved {len(users)} users: {users}")