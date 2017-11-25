import csv
import os
products = {}
a=0;
with open('Dataset_SNAP_with_movies.txt', 'r', encoding='utf-8') as movie_file:
    reader = csv.reader(movie_file)
    for i in reader:
        print(i)
        for element in i:
            print(element)
            #list = element.split(',')
            #print(list)
            #for j in list:
                # print(j)
        print('another one')

