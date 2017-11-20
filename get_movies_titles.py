from amazon.api import AmazonAPI
from keys_amazon_api import *
import csv
import time
from urllib.error import HTTPError
import random

AWS_ACCESS_KEY_ID = AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = AWS_SECRET_ACCESS_KEY
AWS_ASSOCIATE_TAG = AWS_ASSOCIATE_TAG


def get_movies_ids():
    ids_movies = []
    with open('Dataset_SNAP.csv', 'r', encoding='utf-8') as movie_file:
        reader = csv.reader(movie_file)
        next(reader)  # passar a primeira linha à frente
        for i in reader:
            ids_movies.append(i[0].split(',')[0].strip())
    return ids_movies


def remove_duplicates(ids_movies):
    uniques_movies_ids = []
    for i in ids_movies:
        if i not in uniques_movies_ids:
            uniques_movies_ids.append(i)
    return uniques_movies_ids


def error_handler(err):
    ex = err['exception']
    if isinstance(ex, HTTPError) and ex.code == 503:
        time.sleep(random.expovariate(0.1))
        print('oi')
        return True


movies_ids = remove_duplicates(get_movies_ids())
movies_ids.remove('B002LSIAQU') # é preciso remover este filme porque nao existe no site já da amazon
movies_ids.remove('B0041XQRR2') # é preciso remover este filme porque nao existe no site já da amazon
movies_titles = []
amazon = AmazonAPI(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_ASSOCIATE_TAG, MaxQPS=0.9, ErrorHandler=error_handler)

def write_txt():
    file = open('movies_titles_id.txt', 'w', encoding='utf-8')

    file.write('movie_id' + ',' +'movie_title' + '\n')
    i = 0
    for ids in movies_ids:
        movie_title = amazon.lookup(ItemId=ids)
        movies_titles.append(movie_title)
        print(i, '-', movie_title)
        file.write(movies_ids[i] + ',' + str(movies_titles[i])+'\n')
        i = i + 1

write_txt()
