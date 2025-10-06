# Build stage
FROM python:3.11-slim

WORKDIR /app

# Install Poetry and project dependencies
# Copy only dependency manifests first to leverage Docker layer caching
COPY pyproject.toml poetry.lock ./
RUN pip install --no-cache-dir poetry \
	&& poetry config virtualenvs.create false \
	&& poetry install --no-interaction --no-ansi --no-root

# Copy the project files
COPY src/ src/

# Expose the port FastAPI runs on
EXPOSE 8000

# Run the FastAPI application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]