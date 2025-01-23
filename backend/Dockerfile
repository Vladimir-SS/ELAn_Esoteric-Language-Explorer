FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY . .

RUN pip install -e .

EXPOSE 5000

CMD ["fastapi", "run", "/app/main.py", "--port", "5000"]