from open_data import get_text_reviews_and_id, open_opinion_lexicon_pos, open_opinion_lexicon_neg
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from nltk.corpus import stopwords
import nltk

# LABEL -1 : NEG
# LABEL 0 : NEUTRAL
# LABEL 1 : POS

def nltk_method(review):
    # stop_words = set(stopwords.words('english')) #podemos remover stop_words do nosso dataset
    # print(stopwords)

    # words = nltk.word_tokenize(review)
    # tokens = nltk.pos_tag(words) # buscar as tags das palavras 
    sia = SIA()
    polarity = sia.polarity_scores(review).get('compound')  # "compound" é a metrica que diz se é positivo ou negativo.
                                                            # vai de -1 a 1
    if polarity > 0.2:
        score = 1
    elif polarity < 0.2:
        score = -1
    else:
        score = 0
    return score


def intersect(x, y):  # para encontrar as palavras comuns em ambas as listas
    return list(set(x) & set(y))


def opinion_lexicon_method(review):
    positive_words = open_opinion_lexicon_pos()
    negative_words = open_opinion_lexicon_neg()

    review = review.split(' ')  # tornar a nossa review na lista de palavras
    words_found_pos = intersect(review, positive_words)  # lista de palavras positivas encontras no texto
    words_found_neg = intersect(review, negative_words)  # lista de palavras negativas encontras no texto

    positive_counts = len(words_found_pos)
    negative_counts = len(words_found_neg)
    counts = positive_counts - negative_counts
    if counts > 0:
        score = 1
    elif counts < 0:
        score = -1
    else:
        score = 0

    return score


[reviews, ids_reviews] = get_text_reviews_and_id()

scores_1 = []
scores_2 = []

#for review in reviews:
#    scores_1.append(opinion_lexicon_method(review))
#    scores_2.append(nltk_method(review))


def save_scores():
    with open('Sentiment_Analysis.txt', 'w', encoding='utf-8') as file:
        file.write('{},{},{}\n'.format('id', 'opinion_lexicon', 'nltk'))
        for i in range(0, len(scores_1)):
            file.write('{},{},{}\n'.format(ids_reviews[i], scores_1[i], scores_2[i]))


def cenas(review):

    words = nltk.word_tokenize(review)
    tokens = nltk.pos_tag(words)

    return tokens

#stop_words = set(stopwords.words('english')) #podemos remover stop_words do nosso dataset
#print(stopwords)

# save_scores()
words = nltk.word_tokenize(reviews[1])
tokens = nltk.pos_tag(words)
print(tokens)