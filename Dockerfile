FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

# Upgrade pip and install dependencies
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 10000

ENV USERNAME=C2008497
ENV PASSWORD=5REo3OcRpk
ENV SENDER_ID=38541
ENV PORT=10000

CMD ["python", "app.py"]
