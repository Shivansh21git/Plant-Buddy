# Use Python 3.13 slim image
FROM python:3.13-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory inside container
WORKDIR /app

# Install system dependencies for Postgres & build tools
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into container
COPY . .

# Collect static files for production
RUN python manage.py collectstatic --noinput

# Expose Gunicorn port
EXPOSE 8000

# Run Gunicorn (Django app entry point)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "backend.wsgi:application"]
