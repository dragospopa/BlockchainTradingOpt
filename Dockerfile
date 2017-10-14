FROM python:3


RUN mkdir app

COPY . /app

EXPOSE 8000

WORKDIR /app

CMD ["python", "script.py"]
