import csv
import numpy as np
products = {}
a=0;

def get_all_dataset():
    with open('Dataset_SNAP_with_movies.csv', 'r') as movie_file:
        reader = csv.reader(movie_file)
        for i in reader:
            print(i)
            for element in i:
                print(element)


def get_movies(type):
    with open('Dataset_SNAP_with_movies.csv', 'r') as movie_file:
        reader = csv.reader(movie_file)
        list_movies = []
        types = []
        for line in reader:
            for i in range(0, len(line)):
                types.append(line[0])
                if type=='all':
                    list_movies.append(line[1])
                else:
                    if line[0]==type:
                        list_movies.append(line[1])
        return np.unique(list_movies)

def get_users_of_a_movie(movie):
    with open('Dataset_SNAP_with_movies.csv', 'r') as movie_file:
        reader = csv.reader(movie_file)
        list_users = []
        for line in reader:
            for i in range(0, len(line)):
                if line[1] == movie:
                    list_users.append(line[3])
    return np.unique(list_users)


def get_review(movie, user):
    with open('Dataset_SNAP_with_movies.csv', 'r') as movie_file:
        reader = csv.reader(movie_file)
        for line in reader:
            for i in range(0, len(line)):
                if line[1] == movie:
                    if line[3] == user:
                        return line[-1]

def get_text_reviews_and_id():
    reviews =[]
    ids_reviews=[]
    with open('Dataset_SNAP_with_movies.txt', 'r') as movie_file:
        reader = csv.reader(movie_file)
        for i in reader:
            reviews.append(i[-1]) # last index
            ids_reviews.append(i[3])
    return reviews, ids_reviews


def open_opinion_lexicon_neg():
    list_neg=[]
    with open('opinion-lexicon-English/negative-words.txt', 'r') as opinion_lexicon_file:
        reader = csv.reader(opinion_lexicon_file)
        for i in reader:
            list_neg.append(i[0])
    return list_neg

def open_opinion_lexicon_pos():
    list_pos=[]
    with open('opinion-lexicon-English/positive-words.txt', 'r') as opinion_lexicon_file:
        reader = csv.reader(opinion_lexicon_file)
        for i in reader:
            list_pos.append(i[0])
    return list_pos
