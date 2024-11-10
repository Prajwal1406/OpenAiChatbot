# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Install system dependencies and build tools
RUN apt-get update && apt-get install -y \
    gcc \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /backend

# Copy the current directory contents into the container at /backend
COPY . /backend

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install additional Python packages
RUN pip install python-multipart tensorflow-cpu

# Command to run the application
CMD ["python", "server.py"]
