# Use the official Python image as a base
FROM python:3.12-slim-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install build backend for pyproject.toml (PEP 517/518)
RUN pip install --upgrade pip setuptools wheel

# Copy only dependency files first for better caching
COPY requirements.txt /app/

# Install uv and dependencies from requirements file
RUN pip install uv && uv pip install --system --requirements requirements.txt

# Now copy the rest of the code
COPY . /app/

# Expose port 8000
EXPOSE 8000

# Command to run the Quart app
CMD ["python", "-m", "quart", "run", "--host=0.0.0.0", "--port=8000"]

# Note: To access the host's Ollama server from inside Docker on macOS, use host.docker.internal as the base URL in your code or Ollama client config.
