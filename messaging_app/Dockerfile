# 1. Use an official Python runtime as a parent image
FROM python:3.10-slim

# 2. Set environment variables to prevent Python from buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Set the working directory in the container
WORKDIR /app

# 4. Install system dependencies required for mysqlclient
# This is the new block that fixes the error
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       pkg-config \
       default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. Upgrade pip to latest version
RUN pip install --upgrade pip

# 6. Copy the requirements file into the container at /app
COPY requirements.txt /app/

# 7. Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 8. Copy the rest of the application's code into the container at /app
COPY . /app/

# 9. Expose the port the app runs on
EXPOSE 8000

# 10. Define the command to run your app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]