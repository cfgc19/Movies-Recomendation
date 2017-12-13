from open_data import get_movies_of_a_user, get_all_users, get_movies, get_user_and_movie_and_review_id, get_dict_users_movies
import random
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

list_users = get_all_users()
print(len(list_users))

list_movies = get_movies('id')


list_movie_user_review = get_user_and_movie_and_review_id()



#dict = get_dict_users_movies()

def get_review_id(movie_id, user_id):
    """
    Get review ID
    :param movie_id:
    :param user_id:
    :return:
    """
    for i in list_movie_user_review:
        if i[1] == movie_id and i[2] == user_id:
            return i[0]

def get_sentiment_review(review_id):
    """

    Get score from a review.
    :param review_id:
    :return:
    """
    with open('Sentiment_analysis_4scores.txt', 'r') as movie_file:
        reader = csv.reader(movie_file)
        next(reader)
        for i in reader:
            if i[0] == review_id:
                return i[7]

def write_dataframe():
    """
    Creation of a dataset where users are instances and movies are features;
    Each feature could take the values bellow:
    -2 user didn't saw the movie
    -1 user dislike movie
    0 neutral
    1 user like movie

    :return:
    """
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
    return dados

def write_dataset():
    """
    Complete the previous matrix with header and instances id
    :return:
    """
    data = open('Dataset_clusters.txt', 'r')
    data = data.readlines()
    print(len(data))
    with open('Dataset_clusters_new.txt', 'w') as dataset_file:
        #write header
        dataset_file.write("users_id" + ",")
        for i in range(0, len(list_movies)-1):
            dataset_file.write(list_movies[i] + ",")

        dataset_file.write(list_movies[-1] + "\n")
        for i in range(0, len(data)):
            dataset_file.write(list_users[i]+','+data[i])


def open_file():
    """
    Open data matrix
    :return:
    """
    with open('Dataset_clusters.txt', 'r') as movie_file:
        reader = csv.reader(movie_file)
        matrix = []
        for line in reader:
            matrix.append(line[1:])
    matrix = matrix[1:]
    return matrix


# data that will be used for clustering
matrix = open_file()
matrix = np.array(matrix)



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
    plt.scatter(x=dados[:, 0], y=dados[:, 1])
    plt.scatter(x=centroids[:,0], y=centroids[:,1], marker='X')
    plt.show()
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    return matriz_labels
kmean_cluster()



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

