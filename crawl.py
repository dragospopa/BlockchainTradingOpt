import newspaper
import string
import re
import collections
from datetime import datetime

def sentiment(article):
	good_words_file = open("good_words.txt", "r") 
	text = good_words_file.read()
	good_words = re.split(', ', text)

	bad_words_file = open("bad_words.txt", "r")
	text = bad_words_file.read()
	bad_words = re.split(', ', text)

	article_text = article.text
	article_title = article.title

	positive_text_score = 0
	negative_text_score = 0

	positive_title_score = 0
	negative_title_score = 0

	for word in good_words:
		if word in article_text.lower():
			positive_text_score += 1
		if word in article_title.lower():
			positive_title_score += 1

	for word in bad_words:
		if word in article_text.lower():
			negative_text_score += 1
		if word in article_title.lower():
			negative_title_score += 1

	return (positive_title_score - negative_title_score);

def bitcoin_related(article_title):
	article_title = article_title.lower()
	return "blockchain" in article_title or "bitcoin" in article_title or "cryptocurrenc" in article_title or "ico" in article_title

bloomberg_paper = newspaper.build('https://www.coindesk.com/')
print(bloomberg_paper.size())
index = 0
ArticleTuple = collections.namedtuple('ArticleTuple', 'publish_date publish_date_string title text')
articles = []

for i in range(len(bloomberg_paper.articles)):
	if i<12: 
		article = bloomberg_paper.articles[i]
		article.download()
		article.parse()
		if bitcoin_related(article.title) and article.publish_date is not None:
			naivePublishDate = article.publish_date.replace(tzinfo=None)
			articles.append(ArticleTuple(naivePublishDate, article.publish_date.isoformat(), article.title, article.text))

articles.sort(key=lambda x: x.publish_date)

csv_sentiments = open('sentiment_analysis2.csv', 'w')

last_excel_serial = -1
day_sentiment_total = 0
total_day_news = 0

for article in articles:
	startDate = datetime(1899, 12, 30, 0, 0, 0)
	naivePublishDate = article.publish_date.replace(tzinfo=None)
	naiveStartDate = startDate.replace(tzinfo=None)
	diff = naivePublishDate - naiveStartDate

	excel_date_number = diff.days
	article_sentiment = sentiment(article)
	total_day_news += 1
	day_sentiment_total += article_sentiment

	if last_excel_serial == -1:
		last_excel_serial = excel_date_number

	if excel_date_number != last_excel_serial:
		print excel_date_number
		print last_excel_serial
		
		average_sentiment = day_sentiment_total / total_day_news
		csv_sentiments.write( str(last_excel_serial) + ", " + str(average_sentiment) + "\n")
		last_excel_serial = excel_date_number
		day_sentiment_total = 0
		total_day_news = 0

#the news of the last day as well
if total_day_news != 0:
	average_sentiment = day_sentiment_total / total_day_news
	csv_sentiments.write( str(excel_date_number) + "," + str(average_sentiment) + "\n")



