FROM ubuntu:latest

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Download the required packages
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# Install Python 3.8
RUN apt-get update && apt-get install -y \
    python3.8 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set Python 3.8 as the default version
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1

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

# Run gunicorn server
CMD ["cd server" , "gunicorn djangoBackend.wsgi:application"]
