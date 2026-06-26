# 1. Start with a lightweight, official Python image from Docker Hub
FROM python:3.11-slim

# 2. Set the working directory inside the container's file system
WORKDIR /app

# 3. Copy just the requirements file first (this optimizes build caching)
COPY requirements.txt .

# 4. Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your application code into the container
COPY . .

# 6. Expose the port your backend framework runs on (e.g., 8000 for FastAPI)
EXPOSE 8000

# 7. The command to start your application when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
