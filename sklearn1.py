# 

import pandas as pd
from sklearn import linear_model
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
import newspaper
import collections
import nltk
from datetime import datetime
from nltk.classify import NaiveBayesClassifier
import time
import random
#crawler

def format_sentence(sent):
	return({word: True for word in nltk.word_tokenize(sent)})

pos = []
with open("good_news.txt") as f:
    for i in f: 
        pos.append([format_sentence(i), 1])

neg = []
with open("bad_news.txt") as f:
    for i in f: 
        neg.append([format_sentence(i), -1])


#training data
training = pos + neg
classifier = NaiveBayesClassifier.train(training)

def sentiment(article):
	#classifier.show_most_informative_features()
	return classifier.classify(format_sentence(article))



news_paper = newspaper.build('https://news.bitcoin.com/', memoize_articles=False)
print(news_paper.size())
index = 0
ArticleTuple = collections.namedtuple('ArticleTuple', 'publish_date publish_date_string title text url')
articles = []
count = 0
for i in range(len(news_paper.articles)):
	count = count + 1
	if count >5: 
		break
	article = news_paper.articles[i]
	article.download()
	article.parse()
	print article.title
	print sentiment(article.title)
	if article.publish_date is not None:
		try:
			naivePublishDate = article.publish_date.replace(tzinfo=None)
			articles.append(ArticleTuple(naivePublishDate, article.publish_date.isoformat(), article.title, article.text, article.url))
		except:
			print "meh some err"	

articles.sort(key=lambda x: x.publish_date)

csv_sentiments = open('sentiment_analysis.csv', 'w')

last_excel_serial = -1
day_sentiment_total = 0
total_day_news = 0

for article in articles:
	print article.title
	startDate = datetime(1899, 12, 30, 0, 0, 0)
	naivePublishDate = article.publish_date.replace(tzinfo=None)
	naiveStartDate = startDate.replace(tzinfo=None)
	diff = naivePublishDate - naiveStartDate
	excel_date_number = diff.days

	if last_excel_serial == -1:
		last_excel_serial = excel_date_number

	if excel_date_number != last_excel_serial:
		print excel_date_number
		print last_excel_serial
		average_sentiment = day_sentiment_total / total_day_news
		csv_sentiments.write( str(last_excel_serial) + ", " + str(average_sentiment) + "\n")
		last_excel_serial = excel_date_number
		article_sentiment = sentiment(article.title)
		day_sentiment_total = article_sentiment
		total_day_news = 0
	total_day_news += 1

try:
	csv_sentiments.write( str(excel_date_number) + ", " + str(average_sentiment) + "\n")
except:
	print "meh some err"


#neural network

dataTrain = pd.read_csv("data/estimated-transaction-volume.csv", names=['x1','x2','x3','x4','x5','x6','y'])
dataTest = pd.read_csv("data/estimated-transaction-volume-test2.csv", names=['x1','x2','x3','x4','x5','x6','y'])

x_train = dataTrain[['x1','x2','x3','x4','x5','x6']]
y_train = dataTrain['y']

x_test = dataTest[['x1','x2','x3','x4','x5','x6']]
y_test = dataTest['y']

ols = linear_model.LinearRegression()
model = ols.fit(x_train, y_train)

scaler = StandardScaler()

while (True):
	scaler.fit(x_train)
	StandardScaler(copy=True, with_mean=True, with_std=True)
	x_train = scaler.transform(x_train)
	x_test = scaler.transform(x_test)
	mlp = MLPRegressor(solver="sgd",activation="identity",hidden_layer_sizes=(40),max_iter=100000, learning_rate_init=0.00001, learning_rate="invscaling", power_t=-0.02)
	mlp.fit(x_train,y_train)
	predictions = mlp.predict(x_test)
	'''plt.plot(dataTrain[['x4']])
	plt.plot(predictions)
	plt.ylabel('Bitcoin')
	plt.xlabel('Time')
	plt.show()'''

	predicted_value = predictions[0]

	rand1 = -1 - random.randrange(0,3,1)
	rand2 = rand1

	print predicted_value

	print articles[rand1].title
	print articles[rand1].url
	print news_paper.brand


	f1 = open("f1","r") 
	f2 = open("f2","r") 
	f3 = open("f3","r") 
	s1 = f1.read()
	s2 = f2.read()
	s3 = f3.read()
	
	html = s1 + str(predicted_value) + s2  + s3  
	#html = s1 + str(predicted_value) + s2 + articles[rand1].url + '">'+ news_paper.brand + '</a></h6><p class="card-text small">' + articles[rand1].title + s3
    
	print("Running script in daemon mode")
    
	target = open("index.html","w") 

	target.write(html)
	target.close()
	time.sleep(20)

