# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    iputils-ping \
    traceroute \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Install the package
RUN pip install -e .

# Expose the port the web app runs on
EXPOSE 5000

# Metadata
LABEL maintainer="İsmail Taşdelen <pentestdatabase@gmail.com>"
LABEL version="1.5.0"

# Command to run the web app by default
# For CLI usage, user can override: docker run pyping pyping google.com
CMD ["python", "web/app.py"]
