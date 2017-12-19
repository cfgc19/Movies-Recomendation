from open_data import get_movies_of_a_user, get_all_users, get_movies, get_user_and_movie_and_review_id, get_dict_users_movies
import random
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from collections import Counter


list_users = get_all_users()
#print(len(list_users))

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

        if i[0] == movie_id and i[1] == user_id:
            return i[2]

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
            #print(i)
            #print(review_id)
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
        #print(l)
        list_movies_by_user = get_movies_of_a_user(user)
        for movie in list_movies_by_user:
            review_id = get_review_id(movie, user)
            sentiment = get_sentiment_review(review_id)
            #print(sentiment)
            dados[movie][user] = sentiment
        l= l+1
    dados = dados.fillna('-2') # preenche os nan com -2
    dados.to_csv('Dataset_clusters_ola.txt', header=None, index=None, sep=',', mode='w')
    return dados


def write_dataset():
    """
    Complete the previous matrix with header and instances id
    :return:
    """
    data = open('Dataset_clusters.txt', 'r')
    data = data.readlines()
    #print(len(data))
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




def plot_pca(dados, num_components, type):
    """

    :param dados: data matrix
    :param num_components: number of components for the PCA
    :return:
    """
    dados = dados.astype(int)
    pca = PCA(n_components=num_components, svd_solver='full')
    pca.fit(dados)
    dados = pca.transform(dados)
    if type =='3d':
        fig = plt.figure()
        ax = fig.add_subplot(111, projection = '3d')
        ax.scatter(dados[:,0], dados[:,1], dados[:,2])
        plt.title('PCA with '+str(num_components)+' components')
        plt.show()

    elif type=='2d':
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.scatter(dados[:,0], dados[:,1])
        plt.title('PCA with '+str(num_components)+' components')
        plt.show()

    return dados


#dados = plot_pca(matrix, 2, '2d')

#a = 0
def kmean_cluster(dados, n, type):
    kmeans = KMeans(n_clusters=n).fit(dados)
    clusters_numbers = np.array(kmeans.labels_)
    matrix_labels = np.concatenate((list_users[np.newaxis].T, clusters_numbers[np.newaxis].T), axis=1)

    centroids = kmeans.cluster_centers_
    if type =='2d':
        plt.figure()
        colors = ['b', 'y', 'c', 'm', 'r', 'g']
        for i in range(0, len(dados[:, 0])):
            for j in range(0, n):
                if clusters_numbers[i] == j:
                    plt.scatter(dados[i, 0], dados[i, 1], color=colors[j])
        plt.scatter(centroids[:, 0], centroids[:, 1], marker='*', c='#050505', s=40)
        plt.title('k-Means for k=' + str(n))
        plt.show()
    elif type=='3d':

        fig = plt.figure()
        ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)
        colors = ['b', 'y', 'c', 'm','r', 'g']
        for i in range(0, len(dados[:, 0])):
            for j in range(0,n):
                if clusters_numbers[i] == j:
                    ax.scatter(dados[i, 0], dados[i, 1], dados[i, 2], color=colors[j])
        ax.scatter(centroids[:, 0], centroids[:, 1], centroids[:, 2], marker='*', c='#050505', s = 40)
        plt.title('k-Means for k='+str(n))
        plt.show()

    return matrix_labels



def get_liked_movies(user_id_1, user_id_2):
    """

    Get list of the movies that both users liked
    :param user_id_1: id of first user
    :param user_id_2: id of the second one
    :return:

    """
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


user_id = 'ASURJI83YT577'


def recommender_film(user_id, option):
    data = pd.read_csv('Dataset_clusters.txt')
    data = data.drop('users_id', axis=1)
    data = data.as_matrix()
    data = data.astype(int)
    dados_pca = plot_pca(dados=data, num_components=3, type=None)
    matrix = kmean_cluster(dados=dados_pca, n=6, type=None)

    film_list = pd.read_csv('movies_titles_id.txt').values
    label = matrix[np.where(matrix[:, 0] == user_id)[0][0], 1]

    users_of_same_cluster = matrix[np.where(matrix[:, 1] == label)[0], 0]

    if option == 1:
        user_of_same_cluster = random.choice(users_of_same_cluster)
        list_liked_movies_of_random_user_of_cluster = get_liked_movies(user_id, user_of_same_cluster)

        while not list_liked_movies_of_random_user_of_cluster:  # enquanto a lista for vazia procura outro user
            user_of_same_cluster = random.choice(users_of_same_cluster)
            list_liked_movies_of_random_user_of_cluster = get_liked_movies(user_id, user_of_same_cluster)
        choosed_film = random.choice(list_liked_movies_of_random_user_of_cluster)
        list_of_movies_liked = film_list[np.where(film_list[:, 0] == choosed_film)[0], 1]
        choosed_film_name = list_of_movies_liked[0]
    elif option == 2:
        list_movies_of_cluster = []
        for user_2 in users_of_same_cluster:
            for movie in get_liked_movies(user_id, user_2):
                list_movies_of_cluster.append(movie)

        most_liked_film = Counter(list_movies_of_cluster)
        choosed_film, count = most_liked_film.most_common(1)[0]
        choosed_film_name = film_list[np.where(film_list[:, 0] == choosed_film)[0], 1][0]

        print(choosed_film_name)

    return choosed_film_name, user_of_same_cluster

