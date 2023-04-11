# Use the official Python base image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the application files to the container
COPY app.py /app

# Install dependencies
RUN pip install --no-cache-dir Flask

# Expose the port that the application will run on
EXPOSE 5000

# Define the command to run the application
CMD ["python", "app.py"]
