import matplotlib.pyplot as plt
import numpy as np
import difflib

data = open('Sentiment_Analysis.txt')
data_new = open('Sentiment_anlaysis_4scores.txt', 'w')
'''
#num de reviews com resultado igual nos tres metodos
count1 = 0
#num de reviews com resultado igual em dois metodos
count2 = 0
#num de reviews em que o resultado e diferente nas tres
count3 = 0
for line in data.readlines()[1:]:
    line_list = line.split(",")
    if line_list[1] == line_list[2] and line_list[2] == line_list[3]:
        count1 += 1
    elif line_list[1] != line_list[2] and line_list[2] != line_list[3]:
        count3 += 1
    else:
        count2 += 1
print(count1, count2, count3)
'''
def final_score(score1, score2, score3, score4):
    list_scores = np.array([score1,score2,score3,score4])
    unq_scores = np.unique(list_scores)
    if len(unq_scores) == 1:
        return unq_scores[0]
    elif len(unq_scores) == 2:

        return unq_scores


data_new.write('id'+','+ 'opinion_lexicon_withoutSW_DT_IN'+','+'nltk_withoutSW_DT_IN'+','+ 'afinn_withoutSW_DT_IN'+','+'afinn_handling_negation'+'\n')
for line in data.readlines()[1:]:
    line_list=line.split(',')
    line1 = str(line_list[0]+','+line_list[7]+','+line_list[8]+','+line_list[9]+','+line_list[10])
    print(final_score(line_list[7],line_list[8],line_list[9],line_list[10][:-1]))
    data_new.write(line1)

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


print('oi')
'''
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
'''
def diff_score(score, other_score):
    count = 0
    for i in range(0, len(score)):
        if score[i] == other_score[i]:
            count += 1
    return (count*1.0/len(score))











