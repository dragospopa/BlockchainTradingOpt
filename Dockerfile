FROM python:2
COPY . /app
EXPOSE 8000
WORKDIR /app
CMD ["python", "script.py"]
