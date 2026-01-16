# Backend Dockerfile for LLM Council
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY pyproject.toml ./
RUN pip install --no-cache-dir .

# Copy backend code
COPY backend/ ./backend/

# Create data directory (will be mounted as volume in production)
RUN mkdir -p /app/data/conversations

# Expose port
EXPOSE 8001

# Run the FastAPI server
CMD ["python", "-m", "backend.main"]
