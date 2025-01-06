FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r ./requirements.txt

# ENV FLASK_ENV=development

COPY . .

EXPOSE 5000

CMD ["flask", "run", "--host", "0.0.0.0"]