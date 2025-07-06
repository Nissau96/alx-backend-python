# ALX Backend Python - Python Generators 0x00

## About the Project

This project introduces advanced usage of Python generators to efficiently handle large datasets, process data in batches, and simulate real-world scenarios involving live updates and memory-efficient computations. The tasks focus on leveraging Python's `yield` keyword to implement generators that provide iterative access to data, promoting optimal resource utilization, and improving performance in data-driven applications.

## Learning Objectives

By completing this project, you will:

- **Master Python Generators**: Learn to create and utilize generators for iterative data processing, enabling memory-efficient operations.
- **Handle Large Datasets**: Implement batch processing and lazy loading to work with extensive datasets without overloading memory.
- **Simulate Real-world Scenarios**: Develop solutions to simulate live data updates and apply them to streaming contexts.
- **Optimize Performance**: Use generators to calculate aggregate functions like averages on large datasets, minimizing memory consumption.
- **Apply SQL Knowledge**: Use SQL queries to fetch data dynamically, integrating Python with databases for robust data management.

## Requirements

- Proficiency in Python 3.x
- Understanding of `yield` and Python's generator functions
- Familiarity with SQL and database operations (MySQL and SQLite)
- Basic knowledge of database schema design and data seeding
- Ability to use Git and GitHub for version control and submission

## Project Structure

```
python-generators-0x00/
├── seed.py                    # Database setup and seeding
├── 0-stream_users.py         # Stream users from database
├── 1-batch_processing.py     # Batch processing of users
├── 2-lazy_paginate.py        # Lazy pagination implementation
├── 4-stream_ages.py          # Memory-efficient age aggregation
├── user_data.csv             # Sample data file
└── README.md                 # This file
```

## Database Schema

The project uses MySQL database `ALX_prodev` with a `user_data` table:

| Field   | Type    | Constraints          |
| ------- | ------- | -------------------- |
| user_id | UUID    | Primary Key, Indexed |
| name    | VARCHAR | NOT NULL             |
| email   | VARCHAR | NOT NULL             |
| age     | DECIMAL | NOT NULL             |

## Tasks

### 0. Getting Started with Python Generators

**Objective**: Set up the MySQL database and seed it with sample data.

**File**: `seed.py`

**Functions**:

- `connect_db()`: Connects to the MySQL database server
- `create_database(connection)`: Creates the database `ALX_prodev` if it doesn't exist
- `connect_to_prodev()`: Connects to the `ALX_prodev` database in MySQL
- `create_table(connection)`: Creates the `user_data` table if it doesn't exist
- `insert_data(connection, data)`: Inserts data from CSV file if it doesn't exist

**Usage**:

```python
#!/usr/bin/python3
seed = __import__('seed')

connection = seed.connect_db()
if connection:
    seed.create_database(connection)
    connection.close()
    print("connection successful")

    connection = seed.connect_to_prodev()
    if connection:
        seed.create_table(connection)
        seed.insert_data(connection, 'user_data.csv')
```

### 1. Generator That Streams Rows from SQL Database

**Objective**: Create a generator that streams rows from the `user_data` table one by one.

**File**: `0-stream_users.py`

**Function**: `stream_users()`

**Requirements**:

- Must use the `yield` Python generator
- Function should have no more than 1 loop
- Returns user data as dictionaries

**Usage**:

```python
#!/usr/bin/python3
from itertools import islice
stream_users = __import__('0-stream_users')

# Iterate over the generator function and print only the first 6 rows
for user in islice(stream_users(), 6):
    print(user)
```

### 2. Batch Processing Large Data

**Objective**: Create a generator to fetch and process data in batches from the users database.

**File**: `1-batch_processing.py`

**Functions**:

- `stream_users_in_batches(batch_size)`: Fetches rows in batches
- `batch_processing(batch_size)`: Processes each batch to filter users over age 25

**Requirements**:

- Must use no more than 3 loops
- Must use the `yield` generator
- Filters users over age 25

**Usage**:

```python
#!/usr/bin/python3
import sys
processing = __import__('1-batch_processing')

# Print processed users in a batch of 50
try:
    processing.batch_processing(50)
except BrokenPipeError:
    sys.stderr.close()
```

### 3. Lazy Loading Paginated Data

**Objective**: Simulate fetching paginated data from the users database using a generator to lazily load each page.

**File**: `2-lazy_paginate.py`

**Functions**:

- `lazy_paginate(page_size)`: Implements lazy pagination
- `paginate_users(page_size, offset)`: Fetches a specific page of users

**Requirements**:

- Must use only one loop
- Must use the `yield` generator
- Implements lazy loading - fetches next page only when needed

**Usage**:

```python
#!/usr/bin/python3
lazy_paginator = __import__('2-lazy_paginate').lazy_pagination

for page in lazy_paginator(100):
    for user in page:
        print(user)
```

### 4. Memory-Efficient Aggregation with Generators

**Objective**: Use a generator to compute a memory-efficient aggregate function (average age) for a large dataset.

**File**: `4-stream_ages.py`

**Functions**:

- `stream_user_ages()`: Yields user ages one by one
- Function to calculate average age without loading entire dataset into memory

**Requirements**:

- Must use no more than two loops
- Cannot use SQL AVERAGE function
- Must print: "Average age of users: [average_age]"

## Installation and Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Nissau96/alx-backend-python.git
   cd alx-backend-python/python-generators-0x00
   ```

2. **Set up MySQL database**:

   - Ensure MySQL is installed and running
   - Create appropriate user credentials
   - Run the seed script to set up the database

3. **Install dependencies**:

   ```bash
   pip install mysql-connector-python
   ```

4. **Run the setup**:
   ```bash
   python3 seed.py
   ```

## Usage Examples

### Basic Stream Usage

```python
from itertools import islice
stream_users = __import__('0-stream_users')

# Get first 10 users
for user in islice(stream_users(), 10):
    print(f"User: {user['name']}, Age: {user['age']}")
```

### Batch Processing

```python
processing = __import__('1-batch_processing')

# Process users in batches of 100
processing.batch_processing(100)
```

### Lazy Pagination

```python
lazy_paginator = __import__('2-lazy_paginate').lazy_pagination

# Process data page by page
for page in lazy_paginator(50):
    print(f"Processing page with {len(page)} users")
    for user in page:
        # Process each user
        pass
```

## Key Concepts Demonstrated

### Python Generators

- **Memory Efficiency**: Generators don't load entire datasets into memory
- **Lazy Evaluation**: Data is produced on-demand
- **Iteration Protocol**: Implements `__iter__` and `__next__` methods

### Database Integration

- **Connection Management**: Proper database connection handling
- **SQL Operations**: Dynamic query execution
- **Data Streaming**: Efficient data retrieval patterns

### Performance Optimization

- **Batch Processing**: Reduces database round trips
- **Lazy Loading**: Loads data only when needed
- **Memory Management**: Minimizes memory footprint

## Best Practices

1. **Always close database connections** to prevent resource leaks
2. **Use generators for large datasets** to maintain memory efficiency
3. **Handle exceptions properly** especially for database operations
4. **Use appropriate batch sizes** to balance memory usage and performance
5. **Implement proper error handling** for robust applications

## Testing

Run the provided test files to verify implementation:

```bash
# Test database setup
python3 0-main.py

# Test user streaming
python3 1-main.py

# Test batch processing
python3 2-main.py

# Test lazy pagination
python3 3-main.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is part of the ALX Backend Python curriculum.

## Author

**Nissau96** - [GitHub Profile](https://github.com/Nissau96)

---

_This project is designed to demonstrate mastery of Python generators, database operations, and memory-efficient data processing techniques._
