FROM python:2
COPY . /
EXPOSE 4000
CMD ["python script.py"]
