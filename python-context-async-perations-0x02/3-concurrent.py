import asyncio
import aiosqlite
import sqlite3


def setup_database():

    # Connect to a new database file (or open it if it exists)
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Drop the table if it exists to start fresh each time
    cursor.execute('DROP TABLE IF EXISTS users')

    # Create a 'users' table
    cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER NOT NULL
    )
    ''')

    # Add some sample data
    users_to_add = [
        ('Alice', 30),
        ('Bob', 45),
        ('Charlie', 25),
        ('Diana', 50),
        ('Eve', 38)
    ]

    cursor.executemany('INSERT INTO users (name, age) VALUES (?, ?)', users_to_add)

    # Save (commit) the changes and close the connection
    conn.commit()
    conn.close()
    print("Database 'users.db' created successfully with sample data.")


async def async_fetch_users():

    print("Starting to fetch all users...")
    async with aiosqlite.connect('users.db') as db:
        # Wait for 1 second to simulate a slow query
        await asyncio.sleep(1)
        async with db.execute('SELECT * FROM users') as cursor:
            result = await cursor.fetchall()
            print("✅ Finished fetching all users.")
            return result


async def async_fetch_older_users():

    print("Starting to fetch older users...")
    async with aiosqlite.connect('users.db') as db:
        # Wait for 1 second to simulate a slow query
        await asyncio.sleep(1)
        async with db.execute('SELECT * FROM users WHERE age > 40') as cursor:
            result = await cursor.fetchall()
            print("✅ Finished fetching older users.")
            return result


async def fetch_concurrently():
    
    print("Running queries concurrently...")

    # asyncio.gather() runs both awaitables (coroutines) at the same time
    # and waits for both to complete.
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    print("\n--- All Users (Result) ---")
    for user in all_users:
        print(user)

    print("\n--- Users Older Than 40 (Result) ---")
    for user in older_users:
        print(user)


# This is the main entry point of the script
if __name__ == "__main__":
    # Set up the database first
    setup_database()

    # Run the main async function
    # asyncio.run() starts the event loop and runs the coroutine
    print("\nStarting the asynchronous execution...")
    asyncio.run(fetch_concurrently())