# Use an official Python runtime as a parent image
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /spam_recognition_service

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends postgresql-client libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /spam_recognition_service/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /code/
COPY . /spam_recognition_service/

