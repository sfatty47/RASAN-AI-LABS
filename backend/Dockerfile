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

# Copy application code - copy app directory to /app/app
COPY backend/app /app/app

# Verify structure (for debugging)
RUN ls -la /app/app/ && ls -la /app/app/models/ || true

# Create necessary directories
RUN mkdir -p models data

# Expose port (Railway will set PORT env var)
EXPOSE 8000

# Set PYTHONPATH to ensure app package is discoverable from /app
ENV PYTHONPATH=/app

# Run the application (use shell form to expand PORT env var)
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
