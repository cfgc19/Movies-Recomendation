from amazon.api import AmazonAPI
from keys_amazon_api import *
import csv
import time
from urllib.error import HTTPError
import random
import numpy as np
import pandas as pd

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
#movies_ids.remove('B002LSIAQU') # é preciso remover este filme porque nao existe no site já da amazon
#this movie was deleted from the dataset - a total of 11 reviews
#movies_ids.remove('B0041XQRR2') # é preciso remover este filme porque nao existe no site já da amazon
#this movie was deleted from the dataset - a total of 47 reviews
movies_titles = []
amazon = AmazonAPI(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_ASSOCIATE_TAG, MaxQPS=0.9, ErrorHandler=error_handler)

def write_txt():
    file = open('movies_titles_id_.txt', 'w', encoding='utf-8')

    file.write('movie_id' + ',' +'movie_title' + '\n')
    i = 0
    for ids in movies_ids:
        movie_title = amazon.lookup(ItemId=ids)
        movies_titles.append(movie_title)
        #print(i, '-', movie_title)
        file.write(movies_ids[i] + ',' + str(movies_titles[i])+'\n')
        i = i + 1

#write_txt()

def found_movie_name(ID, list_names_ids):
    for i in range(0, len(list_names_ids)):
        if list_names_ids[i][0]==ID:
            return str(list_names_ids[i][1])


def dataset_with_moviename(names_file, data_file):
    names = open(names_file)
    names = names.readlines()
    list_names = []
    for name in names:
        name = name.split(',')
        #remove \n
        name[1] = name[1][:-1]
        list_names.append(name)
    #remove header
    list_names = list_names[1:]
    new_data = []
    with open(data_file, 'r', encoding='utf-8') as movie_file:
        reader = csv.reader(movie_file)
        next(reader)
        for line in reader:
            print(line)
            if len(line) == 1:
                line_list = line[0].split(',')
            else:
                line_list = line
            # remove empty string at the end of the list
            if line_list[-1]=='':
                line_list = line_list[:-1]
            # remove white spaces from productID, userID, profileName, helpfulness, score and time
            for i in range(0, len(line_list)-2):
                line_list[i] = line_list[i].replace(" ", "")
            line_list.insert(0, found_movie_name(line_list[0],list_names))
            new_data.append(line_list)
    np.savetxt('Dataset_SNAP_with_movies.csv', new_data, fmt= '%s,%s,%s,%s,%s,%s,%s,%s,%s')
    with open('Dataset_SNAP_with_movies.txt', 'w', encoding='utf-8' ) as file:
        for line in new_data:
            print(','.join(line))
            file.write(','.join(line))
            file.write('\n')
    print(reader)
#dataset_with_moviename('movies_titles_id.txt', 'Dataset_SNAP.csv')

'''
#reading test
data_file ='Dataset_SNAP_with_movies.txt'
with open(data_file, 'r', encoding='utf-8') as movie_file:
    reader = csv.reader(movie_file)
    for line in reader:
        print(line)
'''