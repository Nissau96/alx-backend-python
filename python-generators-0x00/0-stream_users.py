import mysql.connector
from mysql.connector import Error

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',      
    'password': 'Pesem1000',
    'database': 'ALX_prodev',
    'port': 3306
}

def stream_users():

    connection = None
    cursor = None
    
    try:
        # Establish database connection
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)
        
        # Execute query to fetch all users
        query = "SELECT user_id, name, email, age FROM user_data"
        cursor.execute(query)
        
        # Stream results one row at a time using a single loop
        for row in cursor:
            yield row
            
    except Error as e:
        print(f"Database error: {e}")
        raise
    except Exception as e:
        print(f"Error streaming users: {e}")
        raise
    finally:
        # Clean up resources
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    try:
        print("Starting to stream users from database...")
        
        # Use the generator to process users one by one
        for user in stream_users():
            print(f"Processing user: {user['name']} (ID: {user['user_id']}, Email: {user['email']}, Age: {user['age']})")
            

            
        print("Finished streaming all users!")
        
    except Exception as e:
        print(f"An error occurred: {e}")