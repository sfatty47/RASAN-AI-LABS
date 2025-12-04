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

# Copy application code - ensure proper directory structure
# Copy the entire backend/app directory preserving structure
COPY backend/app/ /app/app/

# Verify all critical files exist
RUN test -f /app/app/main.py && \
    test -f /app/app/models/__init__.py && \
    test -f /app/app/models/schemas.py && \
    echo "All files verified" || (echo "Missing files!" && ls -la /app/app/ && exit 1)

# Create necessary directories
RUN mkdir -p models data

# Expose port (Railway will set PORT env var)
EXPOSE 8000

# Set PYTHONPATH to /app so Python can find the app package
ENV PYTHONPATH=/app

# Run the application (use shell form to expand PORT env var)
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
