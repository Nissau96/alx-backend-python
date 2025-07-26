import sqlite3
import os

# --- My updated dummy database setup ---
def setup_database():

    db_file = 'users.db'
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Create or alter table to include 'age'
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                age INTEGER
            )
        ''')

        # Insert/update data with ages. Using INSERT OR REPLACE to handle existing entries.
        cursor.execute("INSERT OR REPLACE INTO users (id, name, email, age) VALUES (1, 'Alice Smith', 'alice@example.com', 30)")
        cursor.execute("INSERT OR REPLACE INTO users (id, name, email, age) VALUES (2, 'Bob Johnson', 'bob@example.com', 22)")
        cursor.execute("INSERT OR REPLACE INTO users (id, name, email, age) VALUES (3, 'Charlie Brown', 'charlie@example.com', 45)")
        cursor.execute("INSERT OR REPLACE INTO users (id, name, email, age) VALUES (4, 'David Lee', 'david@example.com', 28)")
        cursor.execute("INSERT OR REPLACE INTO users (id, name, email, age) VALUES (5, 'Eve Davis', 'eve@example.com', 19)")


        conn.commit()
        print(f"My database '{db_file}' and 'users' table (with age) are all set up.")
    except sqlite3.Error as e:
        print(f"Oops, ran into a database setup error: {e}")
    finally:
        if conn:
            conn.close() # Always close the connection

# --- My custom ExecuteQuery context manager ---
class ExecuteQuery:

    def __init__(self, db_name, query, params=None):

        self.db_name = db_name
        self.query = query
        # Ensure params is a tuple/list, even if None or a single item
        self.params = params if params is not None else ()
        # If params is a single non-iterable item (e.g., an int), make it a tuple
        if isinstance(self.params, (int, float, str, bool)):
            self.params = (self.params,)

        self.conn = None
        self.cursor = None
        self.results = None # To store the query results

    def __enter__(self):

        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print(f"Database connection to '{self.db_name}' opened for query execution.")

            # Execute the query, safely handling parameters
            if self.params:
                print(f"Executing query: '{self.query}' with parameters: {self.params}")
                self.cursor.execute(self.query, self.params)
            else:
                print(f"Executing query: '{self.query}' (no parameters)")
                self.cursor.execute(self.query)

            # Fetch and store results. For SELECT queries.
            if self.query.strip().upper().startswith("SELECT"):
                self.results = self.cursor.fetchall()
            else:
                # For non-SELECT queries (like INSERT, UPDATE, DELETE),
                # results typically mean rowcount. Also commit changes.
                self.results = self.cursor.rowcount
                self.conn.commit() # Commit changes immediately for non-SELECT queries

            return self.results # This is what I'll get as 'as query_results'
        except sqlite3.Error as e:
            print(f"Ran into an SQLite error during query execution: {e}")
            raise # Re-raise the exception if the query fails

    def __exit__(self, exc_type, exc_val, exc_tb):

        if self.conn:
            # Commit for any pending transactions if not already done by a non-SELECT query
            # For SELECT, commit isn't strictly needed as no changes are made.
            # Only commit if no exception occurred and it was a DML operation not committed yet.
            if exc_type is None and not self.query.strip().upper().startswith("SELECT"):
                 # This check is a bit redundant if we commit DML in __enter__
                 # but ensures commitment if logic changes or if an error happens *after* execute but *before* fetchall.
                 self.conn.commit()
            self.conn.close()
            print(f"Database connection to '{self.db_name}' closed after query.")

        # Let Python handle any exceptions that occurred in the 'with' block by default
        return False

# --- Putting my new ExecuteQuery context manager to use ---
if __name__ == "__main__":
    # First, make sure my database is ready and has 'age' data
    setup_database()

    print("\n--- Using my ExecuteQuery context manager for specific queries ---")

    # Example 1: Query for users older than 25
    my_select_query_1 = "SELECT name, age FROM users WHERE age > ?"
    # Parameters must be a tuple or list, even for a single one
    my_select_params_1 = (25,)

    try:
        with ExecuteQuery('users.db', my_select_query_1, my_select_params_1) as users_over_25:
            print(f"\nResults for '{my_select_query_1}' with param {my_select_params_1}:")
            if users_over_25:
                for user in users_over_25:
                    print(user)
            else:
                print("No users found older than 25.")
    except Exception as e:
        print(f"Oops, something went wrong with query 1: {e}")


    # Example 2: Query for all users (no parameters)
    my_select_query_2 = "SELECT id, name, email, age FROM users"
    try:
        with ExecuteQuery('users.db', my_select_query_2) as all_users:
            print(f"\nResults for '{my_select_query_2}':")
            if all_users:
                for user in all_users:
                    print(user)
            else:
                print("No users found at all.")
    except Exception as e:
        print(f"Oops, something went wrong with query 2: {e}")

    # Example 3: An UPDATE query (demonstrates non-SELECT handling)
    my_update_query = "UPDATE users SET age = ? WHERE name = ?"
    my_update_params = (31, 'Alice Smith')
    try:
        with ExecuteQuery('users.db', my_update_query, my_update_params) as row_count:
            print(f"\nResults for '{my_update_query}' with params {my_update_params}:")
            print(f"Rows updated: {row_count}")
        # To verify the update, I'll run a SELECT query immediately after
        with ExecuteQuery('users.db', "SELECT name, age FROM users WHERE name = ?", ('Alice Smith',)) as updated_alice:
            print("Alice's updated age (verified):", updated_alice)
    except Exception as e:
        print(f"Oops, something went wrong with the update query: {e}")

    # Example 4: An INSERT query
    my_insert_query = "INSERT INTO users (name, email, age) VALUES (?, ?, ?)"
    my_insert_params = ('Frank Green', 'frank@example.com', 29)
    try:
        with ExecuteQuery('users.db', my_insert_query, my_insert_params) as row_count:
            print(f"\nResults for '{my_insert_query}' with params {my_insert_params}:")
            print(f"Rows inserted: {row_count}")
        # Verify the insert
        with ExecuteQuery('users.db', "SELECT name, age FROM users WHERE name = ?", ('Frank Green',)) as new_frank:
            print("New user Frank Green (verified):", new_frank)
    except Exception as e:
        print(f"Oops, something went wrong with the insert query: {e}")


    print("\n--- Done with all my context manager usage examples ---")

    # Just a quick check to see if my database file is there
    if os.path.exists('users.db'):
        print(f"\nYep, 'users.db' file is still there.")
    else:
        print(f"\nUh oh, 'users.db' file is missing (this shouldn't happen!).")