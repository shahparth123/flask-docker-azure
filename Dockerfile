# Use Python 3.10 image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code into the container
COPY . /app/

# Expose the port the app runs on
EXPOSE 5000

# Command to run the app using Gunicorn
CMD ["gunicorn", "-c", "gunicorn_config.py", "app:app"]