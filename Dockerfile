# Use a modern, supported version of Python
FROM python:3.10-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the requirements first (Better for build caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your training script
COPY train.py .

# Run the script
ENTRYPOINT ["python", "train.py"]