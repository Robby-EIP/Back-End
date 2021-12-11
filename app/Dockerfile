FROM python:3.9

COPY requirements.txt /app/

WORKDIR /app

EXPOSE 8080

RUN pip install -r requirements.txt

COPY . /app

RUN pio platform install atmelavr

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8080", "--reload", "--reload-dir", "./", "main:app"]