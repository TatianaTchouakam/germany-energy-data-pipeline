FROM python:3.12-slim

WORKDIR /app

COPY ingestion/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ingestion/ ingestion/

ENTRYPOINT ["python", "ingestion/fetch_data.py", "--upload"]
