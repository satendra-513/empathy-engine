# Use Python 3.10 slim as base
FROM python:3.10-slim

# Install system dependencies for pyttsx3
# espeak-ng is needed for the Linux backend of pyttsx3
RUN apt-get update && apt-get install -y \
    espeak-ng \
    libespeak-ng1 \
    alsa-utils \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create outputs directory
RUN mkdir -p outputs && chmod 777 outputs

# Expose the port Flask runs on
EXPOSE 5000

# Use Gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
