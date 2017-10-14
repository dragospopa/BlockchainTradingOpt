FROM python:2
COPY . /app
EXPOSE 8000
CMD ["python", "script.py"]
