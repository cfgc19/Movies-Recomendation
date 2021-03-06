from open_data import get_user_and_movie_and_review_id
import numpy as np
import matplotlib.pyplot as plt


vec = get_user_and_movie_and_review_id()


with open('Sentiment_Analysis.txt', 'r') as data:
    data = data.readlines()
data_new  = open('Sentiment_Analysis_new.txt', 'w')


data_scores = open('Sentiment_analysis_4scores.txt')
data_scores_m = data_scores.readlines()

def occurrences(list_scores):
    unq_scores = np.unique(list_scores)
    occur = []
    for score in unq_scores:
        count = np.count_nonzero(list_scores==score)
        occur.append(count)
    return occur

def final_score(score1, score2, score3, score4):
    list_scores = np.array([score1,score2,score3,score4])
    unq_scores = np.unique(list_scores)
    if len(unq_scores) == 1:
        return unq_scores[0]
    elif len(unq_scores) == 2:
        occur = occurrences(list_scores)
        if occur == [1,3]:
            return unq_scores[1]
        elif occur == [3,1]:
            return unq_scores[0]
        elif occur == [2,2]:
            if '0' in unq_scores:
                return '0'
            else:
                return -1
    elif len(unq_scores) == 3:
        occur = occurrences(list_scores)
        return unq_scores[np.where( np.array(occur) == 2)[0]][0]

def write_file(data, data1):
    """

    :param data: matrix with readlines() from the original data
    :param data1: new file
    :return:
    """
    i=0
    for line in data[1:]:
        print(line)
        line_list = line.split(',')
        line_list.insert(0, vec[i][0])
        i += 1
        string = ','.join(line_list)
        data1.write(string)

def write_4_scores_file(data_new):
    """

    :param data_new: new writable file
    :return:
    """
    data_new.write('id'+','+ 'opinion_lexicon_withoutSW_DT_IN'+','+'nltk_withoutSW_DT_IN'+','+ 'afinn_withoutSW_DT_IN'+','+'afinn_handling_negation'+'\n')
    for line in data.readlines()[1:]:
        line_list=line.split(',')
        line1 = str(line_list[0]+','+line_list[7]+','+line_list[8]+','+line_list[9]+','+line_list[10])
        print(final_score(line_list[7],line_list[8],line_list[9],line_list[10][:-1]))
        data_new.write(line1)

def plot_scores(data):
    """

    :param data: file opened with the data that will be plotted
    :return:
    """
    score1 = []
    score2 = []
    score3 = []
    score4 = []
    score5 = []
    score6 = []
    score7 = []
    score8 = []
    score9 = []
    score10 = []
    for line in data.readlines()[1:]:
        line_list = line.split(',')
        score1.append(line_list[1])
        score2.append(line_list[2])
        score3.append(line_list[3])
        score4.append(line_list[4])
        score5.append(line_list[5])
        score6.append(line_list[6])
        score7.append(line_list[7])
        score8.append(line_list[8])
        score9.append(line_list[9])
        score10.append(line_list[10][:-1])

    a=len(score1)
    score1 = score1[0:a]
    score2 = score2[0:a]
    score3 = score3[0:a]
    score4 = score4[0:a]
    score5 = score5[0:a]
    score6 = score6[0:a]
    score7 = score7[0:a]
    score8 = score8[0:a]
    score9 = score9[0:a]
    score10 = score10[0:a]



    x = np.arange(0,len(score1))
    plt.scatter(x=x,y=score1)
    plt.scatter(x=x ,y=score2)
    plt.scatter(x=x,y=score3)
    plt.scatter(x=x,y=score4)
    plt.scatter(x=x,y=score5)
    plt.scatter(x=x,y=score6)
    plt.scatter(x=x,y=score7)
    plt.scatter(x=x,y=score8)
    plt.scatter(x=x,y=score9)
    plt.scatter(x=x,y=score10)
    plt.show()

def diff_score(score, other_score):
    count = 0
    for i in range(0, len(score)):
        if score[i] == other_score[i]:
            count += 1
    return (count*1.0/len(score))

def write_final_score(data_scores_m, new_data_scores):
    header = data_scores_m[0]
    header = header.split(',')
    header[-1] = header[-1][:-1]
    new_data_scores.write(','.join(header)+',final score\n')
    for line in data_scores_m[1:]:
        line_list = line.split(',')
        score1 = line_list[2]
        score2 = line_list[3]
        score3 = line_list[4]
        score4 = line_list[5][:-1]
        score = final_score(score1,score2, score3, score4)
        line_list[-1] = line_list[-1][:-1]
        line_list.append(str(score)+'\n')
        new_data_scores.write(','.join(line_list))

        # for 4680 reviews the four scores are equal
        #if np.equal(score,1) or np.equal(score,-1) or np.equal(score,0):
        #    count+=1

def write_review_id(data_matrix, new_data_file):
    new_data_file.write("review_id,"+data_matrix[0])
    id=0
    for line in data_matrix[1:]:
        line_list = line.split(',')
        line_list.insert(0, str(id))
        id+=1
        new_data_file.write(','.join(line_list))
write_review_id(data, data_new)









