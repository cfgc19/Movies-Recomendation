from open_data import get_text_reviews_and_id, open_opinion_lexicon_pos, open_opinion_lexicon_neg
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from afinn import Afinn
from nltk.corpus import stopwords
import nltk
import re

# LABEL -1 : NEG
# LABEL 0 : NEUTRAL
# LABEL 1 : POS

# TAGS QUE QUEREMOS : JJ, JJR,JJS, RB, RBR, RP, UH, VB VBD, VBG, VBN, VBP, VBZ

NEGATION_RE = re.compile("""(?x)(?:
^(?:never|no|nothing|nowhere|noone|none|not|
    havent|hasnt|hadnt|cant|couldnt|shouldnt|
    wont|wouldnt|dont|doesnt|didnt|isnt|arent|aint
 )$
)
|
n't""")

CLAUSE_PUNCT = r'^[.:;!?]$'
CLAUSE_PUNCT_RE = re.compile(CLAUSE_PUNCT)

def nltk_method(review):
    #stop_words = set(stopwords.words('english')) #podemos remover stop_words do nosso dataset
    #print (stopwords.words('english'))
    #print(stopwords)

    #words = nltk.word_tokenize(review)
    #tokens = nltk.pos_tag(words) # buscar as tags das palavras
    #for token in tokens:
        #print(token)

    sia = SIA()
    polarity = sia.polarity_scores(review).get('compound')  # "compound" e a metrica que diz se e positivo ou negativo.
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

def sentiment_afinn(review):
    afinn = Afinn()
    score_afinn = afinn.score(review)
    if score_afinn>0:
        score = 1
    elif score_afinn<0:
        score = -1
    else:
        score = 0

    return score

def get_final_score(score_1,score_2,score_3):
    if score_1 == score_2 and score_2 == score_3:
        final_score = score_1
    elif score_1 != score_2 and score_2 != score_3 and score_1!=score_3:
        final_score = 0
    elif score_1 == score_2 and score_1 != score_3:
        final_score = score_1
    elif score_1 == score_3 and score_1 != score_2:
        final_score = score_1
    elif score_2 == score_3 and score_1 != score_2:
        final_score = score_2
    return final_score

def remove_stopwords(review):
    stop_words = stopwords.words('english')
    list_words = review.split(' ')
    print(len(list_words))
    list_words_new = []
    for word in list_words:
        if word in stop_words:
            a=0
        else:
            list_words_new.append(word)
    return ' '.join(list_words_new)

def final_review(review):

    score_1 = nltk_method(review)
    score_2 = opinion_lexicon_method(review)
    score_3 = sentiment_afinn(review)

    final_score = get_final_score(score_1,score_2,score_3)

    if final_score==1:
        score_str = "Positive"
    elif final_score==-1:
        score_str = "Negative"
    else:
        score_str = "Neutral"
    return score_str

def add_negation_suffixes(tokens):
    """
    INPUT: List of strings (tokenized sentence)
    OUTPUT: List of string with negation suffixes added
    Adds negation markings to a tokenized string.
    """

    # negation tokenization
    neg_tokens = []
    append_neg = False  # stores whether to add "_NEG"
    for token in tokens:
        # if we see clause-level punctuation,
        # stop appending suffix
        if CLAUSE_PUNCT_RE.match(token):
            append_neg = False
        # Do or do not append suffix, depending
        # on state of 'append_neg'
        if append_neg:
            neg_tokens.append(token + "_NEG")
        else:
            neg_tokens.append(token)
            # if we see negation word,
        # start appending suffix
        if NEGATION_RE.match(token):
            append_neg = True
    return neg_tokens
def afinn_handling_neg_score(review):
    """
    'inv' the score must be inverted
    'inc' score must be included
    'not_inc' score must be excluded
    """
    words = nltk.word_tokenize(review)
    tokens = nltk.pos_tag(words)
    neg_tags = add_negation_suffixes(words)
    print(neg_tags)
    length = len(tokens)
    code = []
    count = 0
    score = 0

    for i in range(0, length):
        afinn = Afinn()
        afinn_score = afinn.score(words[i])
        if afinn_score != 0:
            count = count + 1
        if tokens[i][1] != "DT" and tokens[i][1] != "IN":
            if neg_tags[i][-3:] == "NEG":
                code.append('inv')
                score = score + afinn_score*-1
            else:
                code.append('inc')
                score = score + afinn_score
        else:
            code.append('not_inc')
    if score == 0:
        final_score = 0
    else:
        final_score = score / count
    if final_score > 0:
        return 1
    elif final_score < 0:
        return -1
    else:
        return 0


def save_file():

    [reviews, ids_reviews] = get_text_reviews_and_id()

    scores_1 = []
    scores_2 = []
    scores_3 = []
    scores_4 = []
    scores_5 = []
    scores_6 = []
    scores_7 = []
    scores_8 = []
    scores_9 = []
    scores_10 = []
    final_scores = []

    for review in reviews:
        words = nltk.word_tokenize(review)
        tokens = nltk.pos_tag(words)

        review_without_sw = remove_stopwords(review)
        words_without_sw = nltk.word_tokenize(review_without_sw)
        tokens_without_sw = nltk.pos_tag(words_without_sw)

        list_words_without_DT_IN = []
        list_words_without_DT_IN_stopwords = []

        for token in tokens:
            if token[1] != 'DT' or token[1] != 'IN':
                list_words_without_DT_IN.append(token[0])

        for token in tokens_without_sw:
            if token[1] != 'DT' or token[1] != 'IN':
                list_words_without_DT_IN_stopwords.append(token[0])

        string_DT_IN = ' '.join(list_words_without_DT_IN)
        string_DT_IN_SW = ' '.join(list_words_without_DT_IN_stopwords)


        score_1 = opinion_lexicon_method(review)
        score_2 = nltk_method(review)
        score_3 = sentiment_afinn(review)

        score_4 = opinion_lexicon_method(string_DT_IN)
        score_5 = nltk_method(string_DT_IN)
        score_6 = sentiment_afinn(string_DT_IN)

        score_7 = opinion_lexicon_method(string_DT_IN_SW)
        score_8 = nltk_method(string_DT_IN_SW)
        score_9 = sentiment_afinn(string_DT_IN_SW)

        score_10 = afinn_handling_neg_score(review)

        scores_1.append(score_1)
        scores_2.append(score_2)
        scores_3.append(score_3)
        scores_4.append(score_4)
        scores_5.append(score_5)
        scores_6.append(score_6)
        scores_7.append(score_7)
        scores_8.append(score_8)
        scores_9.append(score_9)
        scores_10.append(score_10)
    '''
    with open('sentiment_analysis.txt', 'w') as file:
        file.write('{},{},{},{},{},{},{},{},{},{},{}\n'.format('id', 'opinion_lexicon', 'nltk', 'afinn', 'opinion_lexicon_without_DT_IN',
                                             'nltk_without_DT_IN', 'afinn_without_DT_IN', 'opinion_lexicon_withoutSW_DT_IN',
                                             'nltk_withoutSW_DT_IN', 'afinn_withoutSW_DT_IN', 'afinn_handling_negation'))
        for i in range(0, len(scores_1)):
            file.write('{},{},{},{},{},{},{},{},{},{},{}\n'.format(ids_reviews[i], scores_1[i], scores_2[i], scores_3[i], scores_4[i], scores_5[i],scores_6[i], scores_7[i], scores_8[i], scores_9[i], scores_10[i]))
    '''
save_file()