# Use the official Python 3.12 slim image as the base
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Accept the Hugging Face token as a secure build-time argument
ARG HF_TOKEN

# Set HF_TOKEN as an environment variable for the huggingface_hub library
ENV HF_TOKEN=${HF_TOKEN}

# Set PYTHONPATH to include the working directory
ENV PYTHONPATH=/app

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

#Copy all
COPY . .

# Debug: Verify lib directory is copied
RUN echo "=== Verifying lib directory ===" && \
    ls -la /app/lib/ && \
    echo "=== Testing lib import ===" && \
    python -c "import lib; print('lib directory imported successfully')"


# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["sh", "start.sh"]