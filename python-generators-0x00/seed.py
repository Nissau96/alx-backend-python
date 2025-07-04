import mysql.connector
from mysql.connector import Error
import pandas as pd
import uuid
import sys

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Pesem1000',
    'port': 3306
}

DATABASE_NAME = 'ALX_prodev'


def connect_db():

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            print("Successfully connected to MySQL server")
            return connection
    except Error as e:
        print(f"Error connecting to MySQL server: {e}")
        return None


def create_database(connection):
    """Creates the database ALX_prodev if it does not exist"""
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}")
        print(f"Database '{DATABASE_NAME}' created successfully or already exists")
        cursor.close()
    except Error as e:
        print(f"Error creating database: {e}")


def connect_to_prodev():
    """Connects to the ALX_prodev database in MySQL"""
    try:
        config = DB_CONFIG.copy()
        config['database'] = DATABASE_NAME
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print(f"Successfully connected to {DATABASE_NAME} database")
            return connection
    except Error as e:
        print(f"Error connecting to {DATABASE_NAME} database: {e}")
        return None


def create_table(connection):
    """Creates a table user_data if it does not exist with the required fields"""
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY DEFAULT (UUID()),
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(5,2) NOT NULL,
            INDEX idx_user_id (user_id)
        )
        """
        cursor.execute(create_table_query)
        print("Table 'user_data' created successfully or already exists")
        cursor.close()
    except Error as e:
        print(f"Error creating table: {e}")


def insert_data(connection, data):
    """Inserts data in the database if it does not exist"""
    try:
        cursor = connection.cursor()

        # Check if data already exists to avoid duplicates
        check_query = "SELECT COUNT(*) FROM user_data WHERE email = %s"
        insert_query = """
        INSERT INTO user_data (user_id, name, email, age)
        VALUES (%s, %s, %s, %s)
        """

        inserted_count = 0
        for _, row in data.iterrows():
            cursor.execute(check_query, (row['email'],))
            if cursor.fetchone()[0] == 0:  # Email doesn't exist
                user_id = str(uuid.uuid4())
                cursor.execute(insert_query, (user_id, row['name'], row['email'], row['age']))
                inserted_count += 1

        connection.commit()
        print(f"Successfully inserted {inserted_count} new records")
        cursor.close()
    except Error as e:
        print(f"Error inserting data: {e}")
        connection.rollback()


def main():
    """Main function to orchestrate the database setup"""
    try:

        connection = connect_db()
        if not connection:
            return


        create_database(connection)
        connection.close()


        db_connection = connect_to_prodev()
        if not db_connection:
            return


        create_table(db_connection)


        try:
            data = pd.read_csv('user_data.csv')
            print(f"Successfully loaded {len(data)} records from CSV")

            # Validate required columns
            required_columns = ['name', 'email', 'age']
            if not all(col in data.columns for col in required_columns):
                print(f"Error: CSV must contain columns: {required_columns}")
                return

        except FileNotFoundError:
            print("Error: user_data.csv file not found")
            return
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            return


        insert_data(db_connection, data)

        # Close connection
        db_connection.close()
        print("Database setup completed successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()