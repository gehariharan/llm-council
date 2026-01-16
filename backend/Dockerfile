# Backend Dockerfile for LLM Council
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY pyproject.toml ./
RUN pip install --no-cache-dir .

# Copy backend code
COPY backend/ ./backend/
COPY data/ ./data/ 2>/dev/null || mkdir -p ./data/conversations

# Create data directory if it doesn't exist
RUN mkdir -p /app/data/conversations

# Expose port
EXPOSE 8001

# Run the FastAPI server
CMD ["python", "-m", "backend.main"]
