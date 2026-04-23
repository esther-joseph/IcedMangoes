# Use official Python image
FROM python:3.11-slim

# Set environment
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

# Collect static files
RUN mkdir -p /vol/web/media /vol/web/static
RUN DJANGO_SECRET_KEY=build-secret python manage.py collectstatic --noinput

# Run server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
