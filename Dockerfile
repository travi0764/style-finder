# Use the official Python image
FROM python:3.11-slim

# Create and set the working directory
WORKDIR /app

# Install required system dependencies and Chromium
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        wget \
        curl \
        unzip \
        gnupg \
        libnss3 \
        libx11-6 \
        libxcomposite1 \
        libxcursor1 \
        libxdamage1 \
        libxi6 \
        libxtst6 \
        libatk1.0-0 \
        libasound2 \
        libpangocairo-1.0-0 \
        libxrandr2 \
        libxkbcommon0 \
        fonts-liberation \
        xdg-utils \
        chromium \
        chromium-driver && \
    rm -rf /var/lib/apt/lists/*

# Copy the requirements file to the working directory
COPY requirements.txt .

# Create and activate a virtual environment
RUN python -m venv venv
SHELL ["/bin/bash", "-c"]
RUN source venv/bin/activate && pip install --upgrade pip setuptools

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the application code to the container
COPY . .

# Expose the port that your FastAPI application will run on
EXPOSE 8080

# Command to run the application using uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
