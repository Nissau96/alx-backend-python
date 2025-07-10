import sqlite3
import functools

def with_db_connection(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = None # Initialize conn to None
        try:
            conn = sqlite3.connect('users.db')

            result = func(conn, *args, **kwargs)
            return result
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            raise # Re-raise the exception after printing
        finally:
            if conn:
                conn.close() # Close the connection
    return wrapper

@with_db_connection
def get_user_by_id(conn, user_id):
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

#### Database Setup
def setup_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        );
    ''')
    cursor.execute("INSERT OR IGNORE INTO users (id, name, email) VALUES (1, 'Alice', 'alice@example.com')")
    cursor.execute("INSERT OR IGNORE INTO users (id, name, email) VALUES (2, 'Bob', 'bob@example.com')")
    cursor.execute("INSERT OR IGNORE INTO users (id, name, email) VALUES (3, 'Charlie', 'charlie@example.com')")
    conn.commit()
    conn.close()

# Call setup_database to ensure your database is ready
setup_database()

#### Fetch user by ID with automatic connection handling
print("Fetching user with ID 1:")
user = get_user_by_id(user_id=1)
if user:
    print(f"User found: {user}")
else:
    print("User not found.")

print("\nFetching user with ID 5 (should not exist):")
user_non_existent = get_user_by_id(user_id=5)
if user_non_existent:
    print(f"User found: {user_non_existent}")
else:
    print("User not found.")