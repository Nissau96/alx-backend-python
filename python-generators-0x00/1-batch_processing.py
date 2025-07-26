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


def stream_users_in_batches(batch_size):

    connection = None
    cursor = None

    try:
        # Establish database connection
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)
        
        # Execute query to fetch all users
        query = "SELECT user_id, name, email, age FROM user_data"
        cursor.execute(query)
        
        # Loop 1: Fetch and yield batches
        while True:
            # Fetch batch_size number of rows
            batch = cursor.fetchmany(batch_size)
            
            # If no more rows, break the loop
            if not batch:
                break
                
            # Yield the current batch
            yield batch
            
    except Error as e:
        print(f"Database error: {e}")
    finally:
        # Clean up resources
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def batch_processing(batch_size):
    try:
        # Loop 2: Process each batch from the stream
        for batch in stream_users_in_batches(batch_size):
            # Filter users over 25 in the current batch
            filtered_batch = []

            # Loop 3: Filter users in current batch
            for user in batch:
                if user['age'] > 25:
                    filtered_batch.append(user)

            
            yield filtered_batch

    except Exception as e:
        print(f"Error in batch processing: {e}")
    finally:
        
        return 
        




if __name__ == "__main__":
    try:
        batch_size = 5
        print(f"Processing users in batches of {batch_size}...")
        print("Filtering users over 25 years old...")
        print("-" * 50)
        
        batch_number = 1
        total_users_over_25 = 0
        
        # Process batches and filter users over 25
        for filtered_batch in batch_processing(batch_size):
            print(f"\nBatch {batch_number}:")
            
            if filtered_batch:
                for user in filtered_batch:
                    print(user)
                    total_users_over_25 += 1
            else:
                print("No users over 25 in this batch")
            
            batch_number += 1
        
        print("-" * 50)
        print(f"Total users over 25: {total_users_over_25}")
        
    except Exception as e:
        print(f"An error occurred: {e}")