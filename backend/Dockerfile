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
# First copy everything except models to see what we get
COPY backend/app/ /app/app/

# Explicitly verify and list what was copied
RUN echo "=== Directory structure ===" && \
    ls -la /app/app/ && \
    echo "=== Checking for models directory ===" && \
    ls -la /app/app/models/ 2>&1 || echo "MODELS DIRECTORY NOT FOUND!" && \
    echo "=== Checking models files ===" && \
    test -f /app/app/models/__init__.py && echo "models/__init__.py found" || echo "models/__init__.py MISSING!" && \
    test -f /app/app/models/schemas.py && echo "models/schemas.py found" || echo "models/schemas.py MISSING!"

# Create necessary directories
RUN mkdir -p models data

# Expose port (Railway will set PORT env var)
EXPOSE 8000

# Set PYTHONPATH to /app so Python can find the app package
ENV PYTHONPATH=/app

# Run the application (use shell form to expand PORT env var)
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
