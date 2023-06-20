FROM python:3.8-slim

# Download the required packages
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# Set the working directory
WORKDIR /app

# Copy the Python requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 8000
EXPOSE 8000

# CD into server
RUN cd server/djangoBackend

# Run gunicorn server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "wsgi:application"]
