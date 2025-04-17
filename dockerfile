FROM python:3.9-slim

WORKDIR /app

RUN pip install uv

RUN uv sync

COPY . .

EXPOSE 5001

CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5001"]