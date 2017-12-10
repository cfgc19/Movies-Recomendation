import nltk
import nltk.util
from sentiment_analysis import  get_text_reviews_and_id
from nltk import word_tokenize
from nltk.sentiment.util import mark_negation
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.base import TransformerMixin
from afinn import Afinn
import re

[reviews, ids_reviews] = get_text_reviews_and_id()

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

    words = nltk.word_tokenize(review)
    tokens = nltk.pos_tag(words)
    neg_tags = add_negation_suffixes(words)
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
            code.append('not_incl')
    final_score = score / count
    return final_score


for review in reviews:
    final_score = afinn_handling_neg_score(review)
    print(final_score)


    print("oi")