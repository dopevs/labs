# Use the official Python base image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the application files to the container
COPY app.py /app

# Install dependencies
RUN pip install --no-cache-dir Flask

# Expose a variable for the port number
ARG PORT

# Set the default value for the port number
ENV PORT=${PORT:-5000}

# Expose the port that the application will run on
EXPOSE ${PORT}

# Define the command to run the application
CMD ["python", "app.py"]
