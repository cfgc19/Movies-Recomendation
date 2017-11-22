import nltk
import random
from nltk.corpus import movie_reviews

#nltk.download()
documents = [(list(movie_reviews.words(fileid)), category)
             for category in movie_reviews.categories()
             for fileid in movie_reviews.fileids(category)]

all_words = []
for w in movie_reviews.words():
    all_words.append(w.lower())
print(all_words)
all_words = nltk.FreqDist(all_words)




