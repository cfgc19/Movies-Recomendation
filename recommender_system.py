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
import math
from sklearn.cluster import AgglomerativeClustering, DBSCAN


np.set_printoptions(threshold='nan')
list_users = get_all_users()

list_movies = get_movies('id')

list_movie_user_review = get_user_and_movie_and_review_id()


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
            # print(i)
            # print(review_id)
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
    # dados['users_ids'] = list_users
    l = 0
    for user in list_users:
        # print(l)
        list_movies_by_user = get_movies_of_a_user(user)
        for movie in list_movies_by_user:
            review_id = get_review_id(movie, user)
            sentiment = get_sentiment_review(review_id)
            # print(sentiment)
            dados[movie][user] = sentiment
        l= l+1
    dados = dados.fillna('-2')  # preenche os nan com -2
    dados.to_csv('Dataset_clusters_ola.txt', header=None, index=None, sep=',', mode='w')
    return dados


def complete_dataset():
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


def plot_pca(data, num_components, type):
    """
    Plot data from PCA

    :param data: data matrix
    :param num_components: number of components for the PCA
    :return:
    """
    data = data.astype(int)
    pca = PCA(n_components=num_components, svd_solver='full')
    pca.fit(data)
    data = pca.transform(data)
    if type == '3d':
        fig = plt.figure()

        ax = fig.add_subplot(111, projection = '3d')
        ax.scatter(data[:, 0], data[:, 1], data[:, 2])
        #plt.title('Dados resultantes do PCA. Escolha de '+str(num_components)+' componentes')
        plt.show()

    elif type == '2d':
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.scatter(data[:, 0], data[:, 1])
        #plt.title('Dados resultantes do PCA. Escolha de '+str(num_components)+' componentes')
        plt.show()

    return data


def kmean_cluster(data, n, type):
    """
    Clustering with k-means algorithm

    :param data: reduced data from PCA
    :param n: number of clusters
    :param type: number of dimensions, could be '2d' or '3d'
    :return:
    """
    kmeans = KMeans(n_clusters=n).fit(data)
    clusters_numbers = np.array(kmeans.labels_)
    matrix_labels = np.concatenate((list_users[np.newaxis].T, clusters_numbers[np.newaxis].T), axis=1)

    centroids = kmeans.cluster_centers_
    plot_cluster(data, n, type, clusters_numbers, 'Kmeans', centroids)

    return matrix_labels


def hierarchical_cluster(data, n, type):
    """
    Clustering with hirarchical agglomerative algorithm

    :param data: reduced data from PCA
    :param n: number of clusters
    :param type: number of dimensions, could be '2d' or '3d'
    :return:
    """
    hierarchical = AgglomerativeClustering(n_clusters=n, linkage='average').fit(data)  # linkage pode ser ward, average, complete
    clusters_numbers = np.array(hierarchical.labels_)


    matrix_labels = np.concatenate((list_users[np.newaxis].T, clusters_numbers[np.newaxis].T), axis=1)

    plot_cluster(data, n, type, clusters_numbers, 'Hierarchical', None)

    return matrix_labels


def dbscan(data, type):
    """
    Clustering with DBSCAN algorithm

    :param data: reduced data from PCA
    :param type: number of dimensions, could be '2d' or '3d'
    :return:
    """
    dbscan = DBSCAN(min_samples=6, metric='euclidean').fit(data)
    clusters_numbers = np.array(dbscan.labels_)

    number_of_labels = len(set(clusters_numbers)) -1

    matrix_labels = np.concatenate((list_users[np.newaxis].T, clusters_numbers[np.newaxis].T), axis=1)

    plot_cluster(data, number_of_labels, type, clusters_numbers, 'DBSCAN', None)

    return matrix_labels



def plot_cluster(data, n, type, clusters_numbers, cluster_name, centroids):
    """

    :param data:
    :param n:
    :param type:
    :param clusters_numbers:
    :param cluster_name:
    :param centroids:
    :return:
    """

    begin = 0
    end = n
    if cluster_name == 'DBSCAN':
        begin = -1
        end = n +1
    if type == '2d':
        plt.figure()
        colors = ['b', 'y', 'c', 'm', 'r', 'g', 'k', '0.25', '0.75', '0.85', '0.1']
        for i in range(0, len(data[:, 0])):
            for j in range(begin, n):
                if clusters_numbers[i] == j:
                    plt.scatter(data[i, 0], data[i, 1], color=colors[j])
        if cluster_name == 'Kmeans':
            plt.scatter(centroids[:, 0], centroids[:, 1], marker='*', c='#050505', s=40)
        plt.title(cluster_name + ' for k=' + str(end))
        plt.show()
    elif type == '3d':

        fig = plt.figure()
        ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)
        colors = ['b', 'y', 'c', 'm','r', 'g', 'k', '0.25','0.75', '0.85', '0.1']

        for i in range(0, len(data[:, 0])):
            for j in range(0,n):
                if clusters_numbers[i] == j:
                    ax.scatter(data[i, 0], data[i, 1], data[i, 2], c=colors[j])
        if cluster_name == 'Kmeans':
            ax.scatter(centroids[:, 0], centroids[:, 1], centroids[:, 2], marker='*', c='#050505', s=40)
        plt.title(cluster_name + ' for k=' + str(end))
        plt.show()


def list_of_only_liked_movies():
    """
    Creation of a list with all movies liked by each user
    :return:
    """
    dataframe = pd.DataFrame(columns=['users_id', 'liked_movies'])
    for user in list_users:
        list_liked_movies = []
        films_saw_by_user_1 = get_movies_of_a_user(user)
        for movie in films_saw_by_user_1:
            review_id = get_review_id(movie_id=movie, user_id=user)
            sentiment = get_sentiment_review(review_id)
            if sentiment == '1':
                list_liked_movies.append(movie)  # filmes que ele GOSTOU
        dataframe = dataframe.append({'users_id': user, 'liked_movies': list_liked_movies}, ignore_index=True)
    dataframe.to_csv("list_of_liked_movies.txt", sep=',', mode='w', index=False)


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
    list_liked_movies = []

    for i in films_user_2:

        review_id = get_review_id(movie_id=i, user_id=user_id_2)
        sentiment = get_sentiment_review(review_id)

        if sentiment == '1':
            list_liked_movies.append(i)  # filmes dos quais o user_2 GOSTOU

    return list_liked_movies


def recommender_film(user_id, option, clustering_option):
    """
    Recommendation

    :param user_id: user that need a recommendation
    :param option: 1,2,3
    :param clustering_option: algorithm used for clustering
    :return:
    """
    data = pd.read_csv('Dataset_clusters.txt')
    movies_liked = pd.read_csv('list_of_liked_movies.txt').values
    users_list = data['users_id'].values
    data = data.drop('users_id', axis=1)
    data = data.as_matrix()
    data = data.astype(int)
    dados_pca = plot_pca(data=data, num_components=3, type=None)

    if clustering_option == 'kmeans':
        matrix = kmean_cluster(data=dados_pca, n=6, type=None)
    elif clustering_option == 'hierarchical':
        matrix = hierarchical_cluster(data=dados_pca, n=6, type=None)
    elif clustering_option == 'dbscan':
        matrix = dbscan(data=dados_pca, type=None)

    film_list = pd.read_csv('movies_titles_id.txt').values
    label = matrix[np.where(matrix[:, 0] == user_id)[0][0], 1]
    indexes_of_users_of_same_cluster = np.where(matrix[:, 1] == label)[0]

    users_of_same_cluster = movies_liked[indexes_of_users_of_same_cluster, :]
    users_of_same_cluster_with_positive_reviews = users_of_same_cluster[np.where(users_of_same_cluster[:, 1] != '[]')[0]]
    choosed_film_list = set()
    film_list_first_user = []
    films_saw_by_user = get_movies_of_a_user(user_id)  # filmes que o primeiro user deu review (viu)

    films_positives_by_first_user = eval(movies_liked[np.where(movies_liked[:, 0] == user_id)[0][0],1])
    for film in films_positives_by_first_user:
        list_of_movies_liked = film_list[np.where(film_list[:, 0] == film)[0], 1]
        film_name = list_of_movies_liked[0]
        film_list_first_user.append(film_name)

    similar_users = []
    while(True):
        if option == 1:
            index_random_user = random.choice(range(len(users_of_same_cluster_with_positive_reviews[:,0])))
            films_positives_by_user_random = eval(users_of_same_cluster_with_positive_reviews[index_random_user,1]) # filmes que o segundo user viu e GOSTOU
            best_movies_of_random_user = list(set(films_positives_by_user_random)-set(films_saw_by_user))  # filmes que o user_2 viu mas o user_1 nao

            while not best_movies_of_random_user:  # enquanto a lista for vazia procura outro user
                print(len(users_of_same_cluster_with_positive_reviews))
                users_of_same_cluster = np.delete(users_of_same_cluster_with_positive_reviews,index_user,0)
                index_random_user = random.choice(range(len(users_of_same_cluster_with_positive_reviews[:,0])))
                films_positives_by_user_random = eval(users_of_same_cluster_with_positive_reviews[index_random_user, 1]) # filmes que o segundo user viu e GOSTOU
                best_movies_of_random_user = list(set(films_positives_by_user_random) - set(films_saw_by_user))  # filmes que o user_2 viu mas o user_1 nao
            choosed_film = random.choice(best_movies_of_random_user)
            list_of_movies_liked = film_list[np.where(film_list[:, 0] == choosed_film)[0], 1]
            choosed_film_name = list_of_movies_liked[0]
            choosed_film_list.add(choosed_film_name)
        elif option == 2:
            list_movies_of_cluster = []
            for user_2 in users_of_same_cluster:
                for movie in get_liked_movies(user_id, user_2):
                    list_movies_of_cluster.append(movie)

            best_movies = Counter(list_movies_of_cluster)
            for i in range(0, 3):
                choosed_film, count = best_movies.most_common(3)[i]
                choosed_film_name = film_list[np.where(film_list[:, 0] == choosed_film)[0], 1][0]
                choosed_film_list.add(choosed_film_name)

        elif option == 3:
            nearest_user, index_user = get_nearest_user(user_id, users_of_same_cluster_with_positive_reviews[:,0], dados_pca, users_list)
            films_positives_by_nearest_user = eval(users_of_same_cluster_with_positive_reviews[
                index_user, 1] ) # filmes que o segundo user viu e GOSTOU

            best_movies_of_nearest_user = list(set(films_positives_by_nearest_user) - set(
                films_saw_by_user))  # filmes que o user_2 viu mas o user_1 nao

            while not best_movies_of_nearest_user:  # enquanto a lista for vazia procura outro user
                users_of_same_cluster_with_positive_reviews = np.delete(users_of_same_cluster_with_positive_reviews,index_user, 0)
                nearest_user, index_user = get_nearest_user(user_id, users_of_same_cluster_with_positive_reviews[:, 0],
                                                            dados_pca, users_list)
                films_positives_by_nearest_user = eval(users_of_same_cluster_with_positive_reviews[
                    index_user, 1])  # filmes que o segundo user viu e GOSTOU
                best_movies_of_nearest_user = list(set(films_positives_by_nearest_user) - set(films_saw_by_user))  # filmes que o user_2 viu mas o user_1 nao
            users_of_same_cluster_with_positive_reviews = np.delete(users_of_same_cluster_with_positive_reviews,
                                                                    index_user, 0)
            choosed_film = random.choice(best_movies_of_nearest_user)

            list_of_movies_liked = film_list[np.where(film_list[:, 0] == choosed_film)[0], 1]
            choosed_film_name = list_of_movies_liked[0]
            choosed_film_list.add(choosed_film_name)
            similar_users.append(nearest_user)

        if(len(choosed_film_list) == 3):
            choosed_film_list = list(choosed_film_list)
            break
    return choosed_film_list, film_list_first_user, similar_users


def get_nearest_user(user_id, others_users, pca_data, users_list):
    """
    Get nearest user to user_id
    :param user_id:
    :param others_users:
    :param pca_data:
    :param users_list:
    :return:
    """
    list_distances = []
    point_user = np.where(users_list == user_id)[0]
    #print(others_users)
    for user in others_users:
        coordinate = np.where(users_list == user)[0]
        distance = math.sqrt(math.pow(point_user - pca_data[coordinate, 0], 2) + math.pow(point_user -
                            pca_data[coordinate, 1],2) + math.pow(point_user - pca_data[coordinate, 2], 2))
        list_distances.append(distance)

    list_distances_2 = np.array(list_distances)
    min_index_value = np.argmin(list_distances_2)
    nearest_user = others_users[min_index_value]

    return nearest_user, min_index_value



#############################################################################
# EXAMPLE
#############################################################################
#user_ID = 'A141HP4LYPWMSR'
#recommender_film(user_id=user_ID, option=3, clustering_option='hierarchical')

