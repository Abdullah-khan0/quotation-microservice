# 1️⃣ Use official Python slim image
FROM python:3.11-slim

# 2️⃣ Set working directory
WORKDIR /app

# 3️⃣ Copy requirements first for caching
COPY requirements.txt .

# 4️⃣ Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5️⃣ Copy the project files
COPY . .

# 6️⃣ Expose FastAPI port
EXPOSE 8000

# 7️⃣ Command to run the server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]