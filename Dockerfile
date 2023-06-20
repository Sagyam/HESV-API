ARG VARIANT='3.9-bullseye'
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

# Download the required packages
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends ffmpeg libsm6 libxext6

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

# Run App
CMD ["gunicorn", "--bind", ":8000", "djangoBackend.wsgi:application"]
