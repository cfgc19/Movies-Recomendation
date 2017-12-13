import csv
import numpy as np


products = {}
a = 0


def get_all_dataset():
    with open('Dataset_SNAP_with_movies.txt', 'r') as movie_file:
        reader = csv.reader(movie_file)
        for i in reader:
            print(i)
            for element in i:
                print(element)


def get_user_and_movie_and_review_id():
    with open('Dataset_SNAP_with_movies.txt', 'r') as movie_file:
        reader = csv.reader(movie_file)
        list_review=[]
        for line in reader:
            list_review.append([line[2], line[3], line[-1]])  #movie_id, user_id and review_id
        return list_review


def get_movies(type):
    with open('Dataset_SNAP_with_movies.txt', 'r') as movie_file:
        list_movies = []
        reader = csv.reader(movie_file)
        for line in reader:
            if type == 'all':
                list_movies.append(line[1])
            elif type == 'id':
                list_movies.append(line[2])
            else:
                if type == line[0]:
                    list_movies.append(line[1])
        return np.unique(list_movies)


def get_all_users():
    with open('Dataset_SNAP_with_movies.txt', 'r') as movie_file:
        reader = csv.reader(movie_file)
        list_users = []
        for line in reader:
            list_users.append(line[3])
    return np.unique(list_users)


def get_users_of_a_movie(movie):
    with open('Dataset_SNAP_with_movies.txt', 'r') as movie_file:
        reader = csv.reader(movie_file)
        list_users = []
        for line in reader:
                if line[1] == movie:
                    list_users.append(line[3])
    return np.unique(list_users)


def get_movies_of_a_user(user):
    with open('Dataset_SNAP_with_movies.txt', 'r') as movie_file:
        reader = csv.reader(movie_file)
        list_movies = []
        for line in reader:
                if line[3] ==  user:
                    list_movies.append(line[2])
    return list_movies


def get_review(movie, user):
    with open('Dataset_SNAP_with_movies.txt', 'r') as movie_file:
        reader = csv.reader(movie_file)
        for line in reader:
                if line[1] == movie:
                    if line[3] == user:
                        return line[-2]

def get_dict_users_movies():
    d = {}
    with open('Dataset_SNAP_with_movies.txt', 'r') as movie_file:
        reader = csv.reader(movie_file)
        for line in reader:
            d[line[3]] = get_movies_of_a_user(line[3])
    return d


def get_text_reviews_and_id():
    reviews = []
    ids_reviews = []
    with open('Dataset_SNAP_with_movies.txt', 'r') as movie_file:
        reader = csv.reader(movie_file)
        for i in reader:
            reviews.append(i[-2])  # last but one index
            ids_reviews.append(i[-1]) #last index
    return reviews, ids_reviews


def open_opinion_lexicon_neg():
    list_neg = []
    with open('opinion-lexicon-English/negative-words.txt', 'r') as opinion_lexicon_file:
        reader = csv.reader(opinion_lexicon_file)
        for i in reader:
            list_neg.append(i[0])
    return list_neg


def open_opinion_lexicon_pos():
    list_pos = []
    with open('opinion-lexicon-English/positive-words.txt', 'r') as opinion_lexicon_file:
        reader = csv.reader(opinion_lexicon_file)
        for i in reader:
            list_pos.append(i[0])
    return list_pos
