# Use the official Python 3.12 slim image as the base
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Accept the Hugging Face token as a secure build-time argument
ARG HF_TOKEN

# Set HF_TOKEN as an environment variable for the huggingface_hub library
ENV HF_TOKEN=${HF_TOKEN}

# Copy and install dependencies from requirements.txt
# This will install FastAPI, Uvicorn, and the Prisma Python client
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application source code, including the prisma directory
COPY . .

# Generate the Prisma Client for Python.
# This command uses the pip-installed prisma CLI and requires schema.prisma.
RUN prisma generate

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
