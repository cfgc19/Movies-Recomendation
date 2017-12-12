from open_data import get_movies_of_a_user, get_all_users, get_movies, get_user_and_movie_and_review_id
import random
import csv
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

list_users = get_all_users()

list_movies = get_movies('id')

list_movie_user_review = get_user_and_movie_and_review_id()

def write_dataframe():
    dados = pd.DataFrame(columns=list_movies, index=list_users)
    #dados['users_ids'] = list_users
    l =0
    for user in list_users:
        print(l)
        list_movies_by_user = get_movies_of_a_user(user)
        for movie in list_movies_by_user:
            review_id = get_review_id(movie, user)
            sentiment = get_sentiment_review(review_id)
            dados[movie][user] = sentiment
        l= l+1

    dados = dados.fillna('-2') # preenche os nan com -2
    dados.to_csv('Dataset_clusters.txt', header=None, index=None, sep=',', mode='w')
    #np.savez('/tmp/123.npz', dados=dados.values)
    return dados


def get_review_id(movie_id, user_id):
    for i in list_movie_user_review:
        if i[0] == movie_id and i[1] == user_id:
            return i[-1]


def write_dataset():
    with open('Dataset_clusters.txt', 'w+') as dataset_file:
        dataset_file.write("users_id" + ",")
        for i in range(0, len(list_movies)-1):
            dataset_file.write(list_movies[i] + ",")
            print(i)
        dataset_file.write(list_movies[-1] + "\n")


def get_sentiment_review(review_id):
    with open('fake_dataset_with_ids_reviews.txt', 'r') as movie_file:
        reader = csv.reader(movie_file)
        next(reader)
        for i in reader:
            if i[0] == review_id:
                return i[1]

def open_file():
    with open('Dataset_clusters.txt', 'r') as movie_file:
        reader = csv.reader(movie_file)
        matriz = []
        for line in reader:
            matriz.append(line)
    return matriz

#write_dataset()
#sentiment = get_sentiment_review('1')
#print(sentiment)


def create_fake_dataset():
    with open('fake_dataset_with_ids_reviews.txt', 'w+') as dataset_file:
        dataset_file.write("review_id" + "," + "sentiment")
        numbers =[-2,-1,0,1]
        for line in list_movie_user_review:
            choosed_number = random.choice(numbers)
            print(choosed_number)
            dataset_file.write(line[-1] + "," + str(choosed_number) + "\n")
            #print(i)
        #dataset_file.write(list_movies[-1] + "\n")

#create_fake_dataset()

#dados = write_dataframe()
#print(dados['B004EPYZQM'])


#dados = pd.DataFrame(columns=['a','b','c'], index=['2','3'])
#dados['a']['2'] = '2'

#print(dados)

#for date, row in dados.T.iteritems():
    #print(row)
    #df.ix[]
#    for cenas in row:
#        if cenas == dat:
#            print(cenas)
    #        row
#dados = dados.fillna('-2')
#print(dados.values)

#data = open_file()
#print(data)

#oii = np.load('/tmp/123.npz')
#dados = oii['dados']
#dados.astype(int)


#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
def plot_pca(dados, num_components):
    #oii = np.load('/tmp/123.npz')
    #dados = oii['dados']
    dados.astype(int)
    pca = PCA(n_components=num_components, svd_solver='full')
    pca.fit(dados)
    dados = pca.transform(dados)
    #print(dados)
    return dados


def kmean_cluster(dados):
    kmeans = KMeans(n_clusters=3).fit(dados)
    clusters_numbers = np.array(kmeans.labels_)
    matriz_labels = np.concatenate((list_users[np.newaxis].T, clusters_numbers[np.newaxis].T), axis=1)
    centroids = kmeans.cluster_centers_
    #plt.scatter(x=dados[:, 0], y=dados[:, 1])
    #plt.scatter(x=centroids[:,0], y=centroids[:,1], marker='X')
    #plt.show()
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    return matriz_labels



def recommender_film(user_id):
    data = pd.read_csv('Dataset_clusters.txt', header=None)
    dados = plot_pca(dados=data, num_components=2)
    matriz= kmean_cluster(dados)
    label = matriz[np.where(matriz[:,0]==user_id)[0][0],1]

    ds = matriz[np.where(matriz[:,1] == label)[0],0]

    user_of_same_cluster = random.choice(ds)
    list_liked_movies_of_random_user_of_cluster = get_liked_movies(user_id, user_of_same_cluster)

    while not list_liked_movies_of_random_user_of_cluster : # enquanto a lista for vazia procura outro user
        user_of_same_cluster = random.choice(ds)
        list_liked_movies_of_random_user_of_cluster = get_liked_movies(user_id, user_of_same_cluster)
    choosed_film = random.choice(list_liked_movies_of_random_user_of_cluster)
    film_list = pd.read_csv('movies_titles_id.txt').values
    choosed_film_name = film_list[np.where(film_list[:,0] == choosed_film)[0],1][0]

    return choosed_film_name


def get_liked_movies(user_id_1, user_id_2):
    films_saw_by_user_1 = get_movies_of_a_user(user_id_1)  # filmes que o primeiro user deu review (viu)
    films_saw_by_user_2 = get_movies_of_a_user(user_id_2)  # filmes que o segundo user deu review (viu)
    list(set(films_saw_by_user_1).intersection(films_saw_by_user_2))
    films_user_2 = list(set(films_saw_by_user_2)-set(films_saw_by_user_1))  # filmes que o user_2 viu mas o user_1 nao
    list_liked_movies =[]
    for i in films_user_2:
        review_id = get_review_id(movie_id=i, user_id=user_id_2)
        sentiment = get_sentiment_review(review_id)
        if sentiment == '1':
            list_liked_movies.append(i)  # filmes que ele GOSTOU
    return list_liked_movies


#cenas =pd.read_csv('Dataset_clusters.txt', header=None)
#kmean_cluster(plot_pca(dados=cenas, num_components=2))
#film_name =recommender_film('A328S9RN3U5M68')

#print(film_name)