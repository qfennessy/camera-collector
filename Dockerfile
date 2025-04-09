FROM python:3.9-slim

WORKDIR /app

# Install dependencies needed for bcrypt
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libffi-dev

# Install Poetry
RUN pip install poetry==1.5.1

# Copy project files to cache dependencies
COPY pyproject.toml poetry.lock* README.md /app/
COPY camera_collector /app/camera_collector/

# Configure poetry to not use a virtual environment
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --only main --no-interaction --no-ansi

# Copy the rest of the project
COPY . /app/

# Run the application
CMD ["uvicorn", "camera_collector.main:app", "--host", "0.0.0.0", "--port", "8000"]