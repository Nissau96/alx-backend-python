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


def paginate_users(page_size, offset):
    
    connection = None
    cursor = None
    
    try:
        # Establish database connection
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)
        
        # Execute query with LIMIT and OFFSET for pagination
        query = "SELECT * FROM user_data LIMIT %s OFFSET %s"
        cursor.execute(query, (page_size, offset))
        
        # Fetch all rows for this page
        users = cursor.fetchall()
        
        return users
        
    except Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        # Clean up resources
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def lazy_paginate(page_size):
    
    offset = 0
    
    # Single loop as required
    while True:
        # Fetch the next page of users
        users_page = paginate_users(page_size, offset)
        
        # If no more users, stop the generator
        if not users_page:
            break
            
        # Yield the current page
        yield users_page
        
        # Move to the next page
        offset += page_size


def process_paginated_users(page_size):
    
    try:
        # Process each page from the lazy paginator
        for users_page in lazy_paginate(page_size):
            # Filter users over 25 in the current page
            filtered_page = []
            
            # Filter users in current page
            for user in users_page:
                if user['age'] > 25:
                    filtered_page.append(user)
            
           
            yield filtered_page
            
    except Exception as e:
        print(f"Error in paginated processing: {e}")
    finally:
        return 


if __name__ == "__main__":
    try:
        page_size = 5
        print(f"Processing users in pages of {page_size}...")
        print("Using lazy pagination with database queries...")
        print("Filtering users over 25 years old...")
        print("-" * 50)
        
        page_number = 1
        total_users_over_25 = 0
        total_users_processed = 0
        
        # Process pages and filter users over 25
        for filtered_page in process_paginated_users(page_size):
            print(f"\nPage {page_number}:")
            
            # Count total users in this page (before filtering)
            original_page = paginate_users(page_size, (page_number - 1) * page_size)
            total_users_processed += len(original_page)
            
            if filtered_page:
                for user in filtered_page:
                    print(f"  User ID: {user['user_id']}, Name: {user['name']}, Email: {user['email']}, Age: {user['age']}")
                    total_users_over_25 += 1
            else:
                print("  No users over 25 in this page")
            
            page_number += 1
        
        print("-" * 50)
        print(f"Total pages processed: {page_number - 1}")
        print(f"Total users processed: {total_users_processed}")
        print(f"Total users over 25: {total_users_over_25}")
        
        print("\n" + "=" * 50)
        print("Direct lazy_paginate usage example:")
        print("=" * 50)
        
        # Direct usage of lazy_paginate
        user_paginator = lazy_paginate(3)
        
        for page_num, users_page in enumerate(user_paginator, 1):
            print(f"\nDirect Page {page_num} ({len(users_page)} users):")
            for user in users_page:
                print(f"  - {user['name']} (Age: {user['age']})")
            
            # Stop after 3 pages for demo
            if page_num >= 3:
                break
        
    except Exception as e:
        print(f"An error occurred: {e}")