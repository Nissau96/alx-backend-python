import sqlite3
import functools


def with_db_connection(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        try:
            conn = sqlite3.connect('users.db')
            # Pass the connection as the first argument to the decorated function
            result = func(conn, *args, **kwargs)
            return result
        except sqlite3.Error as e:
            print(f"Database connection or operation error: {e}")
            raise
        finally:
            if conn:
                conn.close()
    return wrapper

# --- New transactional decorator ---
def transactional(func):

    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            print("Transaction committed successfully.")
            return result
        except Exception as e: # Catch any exception
            if conn:
                conn.rollback() # Rollback changes if an error occurs
                print(f"Transaction rolled back due to error: {e}")
            else:
                print(f"Error occurred, but no connection to rollback: {e}")
            raise
    return wrapper

# --- Database Setup  ---
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

# --- Helper to view user data (for verifying changes) ---
@with_db_connection
def get_user_email(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    return result[0] if result else None

# --- Decorated function for updating email ---
@with_db_connection # This decorator provides the 'conn'
@transactional      # This decorator manages the transaction using the 'conn'
def update_user_email(conn, user_id, new_email):

    cursor = conn.cursor()
    print(f"Attempting to update user ID {user_id} email to {new_email}...")
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
    print(f"Successfully executed UPDATE for user ID {user_id}.")

# --- Decorated function to demonstrate rollback ---
@with_db_connection
@transactional
def update_and_fail(conn, user_id, new_email):

    cursor = conn.cursor()
    print(f"\nAttempting to update user ID {user_id} email to {new_email} and then fail...")
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
    print(f"Successfully executed UPDATE for user ID {user_id}. Now raising an error...")
    raise ValueError("Simulating an error during transaction!")


# --- Main execution ---
if __name__ == "__main__":
    setup_database() # Ensure database is set up

    print("--- Initial state ---")
    print(f"User 1 email: {get_user_email(user_id=1)}")
    print(f"User 2 email: {get_user_email(user_id=2)}")

    print("\n--- Testing successful update (commit) ---")
    try:
        update_user_email(user_id=1, new_email='crawford_cartwright@hotmail.com')
        print(f"User 1 email after commit: {get_user_email(user_id=1)}")
    except Exception as e:
        print(f"An unexpected error occurred during commit test: {e}")

    print("\n--- Testing failed update (rollback) ---")
    try:
        update_and_fail(user_id=2, new_email='rollback_test@example.com')
    except ValueError as e:
        print(f"Caught expected error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during rollback test: {e}")

    print(f"User 2 email after rollback attempt: {get_user_email(user_id=2)}")