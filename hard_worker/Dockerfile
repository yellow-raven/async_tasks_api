FROM python:3.8-slim

# Create and set the working directory
WORKDIR /hard_worker

# Copy the Celery worker code and requirements file to the container
COPY . /hard_worker

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Start the Celery worker
CMD ["celery", "-A", "tasks", "worker", "-Q", "hard", "--loglevel=info"]