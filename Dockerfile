# Use the official Python slim image as the base
FROM python:3.10-slim

# Set environment variables to keep Python output clean and predictable
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    WORKDIR=/app

# Set the working directory inside the container
WORKDIR ${WORKDIR}

# Install essential lightweight network utilities if required by your script,
# without installing full system daemons like systemd or openssh-server.
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    iproute2 \
    && rm -rf /var/lib/apt/lists/*

# Copy python dependency architecture files first to utilize Docker layer caching
COPY requirements.txt .

# Install dependencies smoothly
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Expose your app port if applicable (adjust if your configuration expects a specific port)
EXPOSE 8080

# Define the command to start your application (replace main.py with your entry point)
CMD ["python", "main.py"]
