# 1. Use an official Python runtime as a parent image
FROM python:3.10-slim

# 2. Set environment variables to prevent Python from buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Set the working directory in the container
WORKDIR /app

# 4. Copy the requirements file into the container at /app
COPY requirements.txt /app/

# 5. Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of the application's code into the container at /app
COPY . /app/

# 7. Expose the port the app runs on
EXPOSE 8000

# 8. Define the command to run your app
# We use 0.0.0.0 to make the server accessible from outside the container
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]