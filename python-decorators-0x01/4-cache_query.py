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

# --- Global cache dictionary ---
query_cache = {}

# --- New cache_query decorator ---
def cache_query(func):

    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        query = None
        if 'query' in kwargs:
            query = kwargs['query']
        elif len(args) > 0 and isinstance(args[0], str): # Check if query is the first of *args (i.e., second overall argument)
             query = args[0]

        if not query:
            print(f"Warning: Could not find query string in arguments for {func.__name__}. Skipping cache.")
            return func(conn, *args, **kwargs) # Execute without caching if query not found

        if query in query_cache:
            print(f"Retrieving result for '{query}' from cache.")
            return query_cache[query]
        else:
            print(f"Executing query '{query}' and caching result.")
            result = func(conn, *args, **kwargs)
            query_cache[query] = result
            return result
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
    conn.commit()
    conn.close()

# --- Decorated function for fetching users with cache ---
@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):

    print("--- Executing actual database query ---")
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### Main execution ####
if __name__ == "__main__":
    setup_database()

    print("--- First call: Should execute query and cache result ---")
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print("Users from first call:", users)
    print("Current cache:", query_cache)

    print("\n--- Second call (same query): Should use cached result ---")
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print("Users from second call:", users_again)
    print("Current cache:", query_cache)

    print("\n--- Third call (different query): Should execute query and cache new result ---")
    users_filtered = fetch_users_with_cache(query="SELECT name FROM users WHERE id = 1")
    print("Users (filtered) from third call:", users_filtered)
    print("Current cache:", query_cache)

    print("\n--- Fourth call (different query, again): Should use cached result ---")
    users_filtered_again = fetch_users_with_cache(query="SELECT name FROM users WHERE id = 1")
    print("Users (filtered) from fourth call:", users_filtered_again)
    print("Current cache:", query_cache)