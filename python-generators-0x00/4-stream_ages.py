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


def stream_user_ages():
    
    connection = None
    cursor = None
    
    try:
        # Establish database connection
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Execute query to fetch only ages
        query = "SELECT age FROM user_data"
        cursor.execute(query)
        
        # Loop 1: Fetch and yield ages one by one
        while True:
            # Fetch one row at a time
            row = cursor.fetchone()
            
            # If no more rows, break the loop
            if row is None:
                break
            
            
            yield row[0]
            
    except Error as e:
        print(f"Database error: {e}")
    finally:
        # Clean up resources
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def calculate_average_age():
   
    total_age = 0
    user_count = 0
    
    # Loop 2: Process each age from the generator
    for age in stream_user_ages():
        total_age += age
        user_count += 1
    
    # Calculate and return average
    if user_count > 0:
        return total_age / user_count
    else:
        return None


def demonstrate_memory_efficiency():
    
    print("=== Memory Efficiency Demonstration ===")
    print("Processing ages one by one...")
    
    # Create the generator
    age_generator = stream_user_ages()
    
    # Process first few ages to show the streaming nature
    print("First 5 ages from the stream:")
    for i, age in enumerate(age_generator):
        print(f"  Age {i+1}: {age}")
        if i >= 4:  # Show first 5 ages
            break
    
    print("...")
    print("(continuing to process remaining ages without storing them)")


if __name__ == "__main__":
    try:
        print("=== Memory-Efficient Average Age Calculator ===")
        print("Using generator to stream user ages...")
        print("-" * 50)
        
        # Calculate the average age
        average_age = calculate_average_age()
        
        if average_age is not None:
            print(f"Average age of users: {average_age:.2f}")
        else:
            print("No users found in the database")
        
        print("\n" + "-" * 50)
        demonstrate_memory_efficiency()
        
       
        print("\n=== Multiple Iterations Example ===")
        print("Each iteration opens a fresh database connection...")
        
        # First iteration - count users
        user_count = 0
        for age in stream_user_ages():
            user_count += 1
        print(f"Total users processed: {user_count}")
        
        # Second iteration - find min/max age
        min_age = float('inf')
        max_age = float('-inf')
        
        for age in stream_user_ages():
            if age < min_age:
                min_age = age
            if age > max_age:
                max_age = age
        
        if user_count > 0:
            print(f"Age range: {min_age} to {max_age}")
        
        print("-" * 50)
        print("Memory usage: Only a few variables stored at any time!")
        print("- Current age being processed")
        print("- Running total of ages")
        print("- Count of users processed")
        print("- NO large arrays or lists of ages in memory")
        
    except Exception as e:
        print(f"An error occurred: {e}")


