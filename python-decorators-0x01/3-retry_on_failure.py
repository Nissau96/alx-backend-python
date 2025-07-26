import time
import sqlite3
import functools


# --- db_connection decorator ---
def with_db_connection(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        try:
            conn = sqlite3.connect('users.db')

            result = func(conn, *args, **kwargs)
            return result
        except sqlite3.Error as e:
            print(f"Database connection or operation error in with_db_connection: {e}")
            raise
        finally:
            if conn:
                conn.close()

    return wrapper


# --- New retry_on_failure decorator ---
def retry_on_failure(retries=3, delay=2):

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {i + 1}/{retries + 1} failed for {func.__name__}: {e}")
                    if i < retries:
                        print(f"Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        print(f"All {retries + 1} attempts failed for {func.__name__}. Re-raising the last error.")
                        raise

        return wrapper

    return decorator


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
    conn.commit()
    conn.close()


# --- Global counter to simulate transient failures ---
_failure_count = 0
_max_failures = 2


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    
    global _failure_count
    if _failure_count < _max_failures:
        _failure_count += 1
        print(f"Simulating a transient error for fetch_users_with_retry (fail count: {_failure_count})...")
        # Simulate a database operational error
        raise sqlite3.OperationalError("Database is temporarily unavailable.")

    print("Simulated success for fetch_users_with_retry.")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


#### attempt to fetch users with automatic retry on failure
if __name__ == "__main__":
    setup_database()  # Ensure database is set up

    print("--- Attempting to fetch users with retry mechanism ---")
    try:
        users = fetch_users_with_retry()
        print("\nSuccessfully fetched users:")
        for user in users:
            print(user)
    except Exception as e:
        print(f"\nFailed to fetch users after all retries: {e}")

    print("\n--- Resetting failure count and attempting again (should succeed faster) ---")
    _failure_count = 0  # Reset for a new demonstration
    try:
        users_again = fetch_users_with_retry()
        print("\nSuccessfully fetched users again:")
        for user in users_again:
            print(user)
    except Exception as e:
        print(f"\nFailed to fetch users again after all retries: {e}")