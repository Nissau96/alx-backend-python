import sqlite3
import os # Need this to check if the database file exists

# --- Setting up my dummy database ---
def setup_database():

    db_file = 'users.db'
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Create my 'users' table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL
            )
        ''')

        # Populating it with some data (only inserts if the data isn't already there)
        cursor.execute("INSERT OR IGNORE INTO users (id, name, email) VALUES (1, 'Alice Smith', 'alice@example.com')")
        cursor.execute("INSERT OR IGNORE INTO users (id, name, email) VALUES (2, 'Bob Johnson', 'bob@example.com')")
        cursor.execute("INSERT OR IGNORE INTO users (id, name, email) VALUES (3, 'Charlie Brown', 'charlie@example.com')")
        cursor.execute("INSERT OR IGNORE INTO users (id, name, email) VALUES (4, 'David Lee', 'david@example.com')")


        conn.commit() # Don't forget to save changes!
        print(f"My database '{db_file}' and 'users' table are all set up.")
    except sqlite3.Error as e:
        print(f"Oops, ran into a database setup error: {e}")
    finally:
        if conn:
            conn.close() # Always close the connection

# --- My custom DatabaseConnection context manager ---
class DatabaseConnection:

    def __init__(self, db_name):

        self.db_name = db_name
        self.conn = None    # Will hold my connection object
        self.cursor = None  # Will hold my cursor object

    def __enter__(self):
        """
        This runs when I enter the 'with' block.
        It's where I establish the database connection and give back the cursor.
        """
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print(f"Database connection to '{self.db_name}' opened for me.")
            return self.cursor # This is what I'll get as 'as cursor'
        except sqlite3.Error as e:
            print(f"Couldn't connect to the database: {e}")
            raise # Gotta re-raise if it fails so I know something's wrong

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        This runs when I exit the 'with' block (even if there's an error!).
        It makes sure my database connection is closed properly.
        """
        if self.conn:
            self.conn.commit() # Commit any unsaved changes before closing
            self.conn.close()
            print(f"Database connection to '{self.db_name}' closed for me.")

        # If an exception happened, I'll let it re-raise (returning False or None).
        # I don't want to swallow errors here.
        return False

# --- Putting my context manager to use ---
if __name__ == "__main__":
    # First, make sure my database is ready to go
    setup_database()

    print("\n--- Using my DatabaseConnection context manager for a query ---")

    try:
        # The 'with' statement handles opening and closing for me!
        with DatabaseConnection('users.db') as cursor:
            print("Time to run my query: SELECT * FROM users")
            cursor.execute("SELECT * FROM users")
            my_users = cursor.fetchall()

            print("\nHere are my query results:")
            if my_users:
                for user in my_users:
                    print(user)
            else:
                print("Looks like no users were found.")

    except sqlite3.Error as e:
        print(f"Ran into an SQLite error during my query: {e}")
    except Exception as e:
        print(f"An unexpected error popped up: {e}")

    print("\n--- Done using my context manager ---")

    # Just a quick check to see if my database file is there
    if os.path.exists('users.db'):
        print(f"\nYep, 'example.db' file is still there.")
    else:
        print(f"\nUh oh, 'example.db' file is missing (this shouldn't happen!).")