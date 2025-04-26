FROM python:3.9-slim

WORKDIR /app

COPY pyproject.toml ./

# Install dependencies
RUN pip install -e .

# Copy application code
COPY . .

EXPOSE 5001

CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5001", "--reload"]