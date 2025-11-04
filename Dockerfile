# Use Python 3.9 (stable version)
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot code
COPY main.py .

# Start the bot
CMD ["python", "main.py"]
