FROM python:3.9-slim

WORKDIR /app

# Install Poetry
RUN pip install poetry==1.5.1

# Copy only requirements to cache them in docker layer
COPY pyproject.toml poetry.lock* /app/

# Configure poetry to not use a virtual environment
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --no-dev --no-interaction --no-ansi

# Copy project
COPY . /app/

# Run the application
CMD ["uvicorn", "camera_collector.main:app", "--host", "0.0.0.0", "--port", "8000"]