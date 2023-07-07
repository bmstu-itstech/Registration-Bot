FROM python:3.10-alpine

WORKDIR /ApiGateWay

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python3", "./main.py"]