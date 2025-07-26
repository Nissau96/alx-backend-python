# Python Generators Database Project

## About the Project

This project introduces advanced usage of Python generators to efficiently handle large datasets, process data in batches, and simulate real-world scenarios involving live updates and memory-efficient computations. The tasks focus on leveraging Python's `yield` keyword to implement generators that provide iterative access to data, promoting optimal resource utilization, and improving performance in data-driven applications.

## Learning Objectives

By completing this project, you will:

1. **Master Python Generators**: Learn to create and utilize generators for iterative data processing, enabling memory-efficient operations.
2. **Handle Large Datasets**: Implement batch processing and lazy loading to work with extensive datasets without overloading memory.
3. **Simulate Real-world Scenarios**: Develop solutions to simulate live data updates and apply them to streaming contexts.
4. **Optimize Performance**: Use generators to calculate aggregate functions like averages on large datasets, minimizing memory consumption.
5. **Apply SQL Knowledge**: Use SQL queries to fetch data dynamically, integrating Python with databases for robust data management.

## Project Structure

```
python-generators-database/
├── README.md
├── seed.py
├── user_data.csv
├── requirements.txt
└── generators/
    ├── __init__.py
    ├── stream_users.py
    └── batch_processor.py
```

## Database Schema

### `user_data` Table Structure

| Column  | Type         | Constraints                |
| ------- | ------------ | -------------------------- |
| user_id | VARCHAR(36)  | Primary Key, UUID, Indexed |
| name    | VARCHAR(255) | NOT NULL                   |
| email   | VARCHAR(255) | NOT NULL                   |
| age     | DECIMAL(5,2) | NOT NULL                   |

## Prerequisites

- Python 3.7+
- MySQL Server 5.7+
- pip (Python package manager)

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Nissau96/alx-backend-python.git
   cd alx-backend-python
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up MySQL database**
   - Ensure MySQL server is running
   - Create a MySQL user with appropriate privileges
   - Update database credentials in `seed.py`

## Configuration

Update the database configuration in `seed.py`:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',      # Replace with your MySQL username
    'password': 'Pesem1000',  # Replace with your MySQL password
    'port': 3306
}s
```

## Usage

### 1. Database Setup

Run the seed script to set up the database and populate it with sample data:

```bash
python seed.py
```

This script will:

- Create the `ALX_prodev` database
- Create the `user_data` table with proper schema
- Insert 20 sample users from `user_data.csv`
- Handle duplicates automatically

### 2. Verify Database Setup

Connect to MySQL and verify the setup:

```sql
USE ALX_prodev;
DESCRIBE user_data;
SELECT COUNT(*) FROM user_data;
SELECT * FROM user_data LIMIT 5;
```

### 3. Using Generators (Future Implementation)

```python
from generators.stream_users import stream_users_from_db

# Stream users one by one
for user in stream_users_from_db():
    print(f"Processing user: {user['name']}")
    # Process individual user data
```

## Features

### Database Management

- **Automated Setup**: Complete database and table creation
- **Data Validation**: Ensures data integrity and prevents duplicates
- **Error Handling**: Comprehensive error handling for database operations
- **Connection Management**: Proper connection handling and cleanup

### Data Processing

- **Memory Efficient**: Uses generators for streaming data processing
- **Batch Processing**: Handles large datasets in manageable chunks
- **Lazy Loading**: Loads data only when needed
- **Real-time Simulation**: Supports live data update scenarios

## Sample Data

The project includes sample data with 20 users featuring:

- Diverse names and realistic email addresses
- Age range from 22 to 41.25 years
- Email providers: Gmail, Yahoo, Hotmail, Outlook
- Proper data formatting for database insertion

## Functions Overview

### `seed.py` Functions

| Function                        | Purpose                             |
| ------------------------------- | ----------------------------------- |
| `connect_db()`                  | Connects to MySQL database server   |
| `create_database(connection)`   | Creates the ALX_prodev database     |
| `connect_to_prodev()`           | Connects to the ALX_prodev database |
| `create_table(connection)`      | Creates the user_data table         |
| `insert_data(connection, data)` | Inserts CSV data into the database  |

## Requirements

```txt
mysql-connector-python>=8.0.0
pandas>=1.3.0
```

## Error Handling

The project includes comprehensive error handling for:

- Database connection issues
- File reading errors
- Data validation problems
- Duplicate data prevention
- Transaction rollback on failures

## Performance Considerations

- **Memory Efficiency**: Generators prevent loading entire datasets into memory
- **Batch Processing**: Optimized for handling large datasets
- **Indexed Queries**: Database queries use indexed columns for better performance
- **Connection Pooling**: Efficient database connection management

## Best Practices

- **Data Validation**: Input validation before database operations
- **Security**: Parameterized queries to prevent SQL injection
- **Error Recovery**: Graceful error handling with informative messages
- **Resource Management**: Proper cleanup of database connections and cursors

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Troubleshooting

### Common Issues

1. **MySQL Connection Error**

   - Verify MySQL server is running
   - Check database credentials
   - Ensure user has proper privileges

2. **CSV File Not Found**

   - Verify `user_data.csv` is in the same directory as `seed.py`
   - Check file permissions

3. **Import Errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Verify Python version compatibility

### Getting Help

- Check the [Issues](https://github.com/Nissau96/alx-backend-python/issues) page
- Review the troubleshooting section
- Ensure all prerequisites are met

## Acknowledgments

- Python Software Foundation for the excellent generator documentation
- MySQL team for the robust database system
- The open-source community for the amazing libraries used in this project
