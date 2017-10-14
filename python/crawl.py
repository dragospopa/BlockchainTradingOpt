import newspaper
import codecs

str = raw_input('Give my a website, m8: ')
x = newspaper.build(str)

print(len(x.articles))
print(x.brand)

i = 1
for article in x.articles:
    article.download()
    article.parse()
    print(article.title)
    f = codecs.open(article.title,'w', 'utf-8')
    f.write(article.text)
    i= i+1
    if i>5: break


