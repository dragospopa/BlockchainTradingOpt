FROM python:2

RUN pip install pandas
RUN pip install scikit_learn
RUN pip install newspaper
RUN pip install nltk 
RUN pip install scipy

RUN mkdir app

COPY . /app

EXPOSE 8000

WORKDIR app

CMD ["python", "script.py", "&","python", "sklearn1.py"]
