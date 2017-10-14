FROM python:2

RUN mkdir app
COPY . /app
EXPOSE 8000
WORKDIR /app
CMD ["python", "script.py"]
