# Use official Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY app.py .

# Expose port
EXPOSE 10000

# Environment variables (optional)
ENV USERNAME=C2008497
ENV PASSWORD=5REo3OcRpk
ENV SENDER_ID=38541
ENV PORT=10000

# Run the app
CMD ["python", "app.py"]
