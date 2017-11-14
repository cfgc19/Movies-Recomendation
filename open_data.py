import csv
import os
products = {}
with open('Dataset_SNAP.csv', 'r', encoding='utf-8') as movie_file:
    reader = csv.reader(movie_file)
    for i in reader:
        for element in i:
            list = element.split(',')
            for j in list:
                print(j)
            print('another one')

