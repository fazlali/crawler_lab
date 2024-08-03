# Use the official Python image as a base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . /app/

# Expose port 80 to the outside world
EXPOSE 80

# Command to run the application
CMD python3 -m gunicorn main:app -k uvicorn.workers.UvicornWorker -b 0.0.0.0:80 --workers ${SERVER_WORKERS:-1}
