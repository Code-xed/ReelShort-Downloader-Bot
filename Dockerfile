# Use the official Python 3.11 image based on Alpine Linux
FROM python:3.11-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies and build tools
RUN apk update \
    && apk add --no-cache \
    build-base \
    gcc \
    musl-dev \
    libffi-dev \
    tzdata

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Define the command to run your bot
CMD ["python", "bot.py"]