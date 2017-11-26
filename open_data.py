import csv
import os
products = {}
a=0;

def get_all_dataset():
    with open('Dataset_SNAP_with_movies.txt', 'r', encoding='utf-8') as movie_file:
        reader = csv.reader(movie_file)
        for i in reader:
            print(i[-1])
            for element in i:
                print(element)


def get_text_reviews_and_id():
    reviews =[]
    ids_reviews=[]
    with open('Dataset_SNAP_with_movies.txt', 'r', encoding='utf-8') as movie_file:
        reader = csv.reader(movie_file)
        for i in reader:
            reviews.append(i[-1]) # last index
            ids_reviews.append(i[3])
    return reviews, ids_reviews


def open_opinion_lexicon_neg():
    list_neg=[]
    with open('opinion-lexicon-English/negative-words.txt', 'r', encoding='utf-8') as opinion_lexicon_file:
        reader = csv.reader(opinion_lexicon_file)
        for i in reader:
            list_neg.append(i[0])
    return list_neg

def open_opinion_lexicon_pos():
    list_pos=[]
    with open('opinion-lexicon-English/positive-words.txt', 'r', encoding='utf-8') as opinion_lexicon_file:
        reader = csv.reader(opinion_lexicon_file)
        for i in reader:
            list_pos.append(i[0])
    return list_pos
