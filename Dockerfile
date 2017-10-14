FROM python:2

ADD . /
EXPOSE 8000

CMD [ "python", "./script.py" ]

