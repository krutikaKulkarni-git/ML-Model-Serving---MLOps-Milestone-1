FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and model
COPY main.py .
COPY model.pkl .

# Expose port (Cloud Run uses PORT env variable)
ENV PORT=8080
EXPOSE 8080

# Run the application
CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT}
