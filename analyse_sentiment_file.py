data = open('sentiment_analysis_without_stopwords.txt')
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