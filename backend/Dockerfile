FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the entire backend/app directory to /app/app to preserve package structure
COPY backend/app /app/app

# Create necessary directories
RUN mkdir -p models data

# Expose port (Railway will set PORT env var)
EXPOSE 8000

# Set PYTHONPATH to ensure app package is discoverable
ENV PYTHONPATH=/app

# Run the application (use shell form to expand PORT env var)
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
