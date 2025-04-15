# Use Python base image
FROM python:3.11-slim

# Install system dependencies for OpenCV and pyttsx3
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    espeak \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy project files to the container
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port Flask runs on
EXPOSE 5000

# Run your app
CMD ["python", "app.py"]
