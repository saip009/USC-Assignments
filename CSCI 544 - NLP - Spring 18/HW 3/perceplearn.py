import pickle
import re
import string
import sys

path = './sampletrain'
path = './train-labeled.txt'
# path = sys.argv[1]

file = open(path, 'r').read()

# change = string.maketrans('','',string.punctuation)


pattern = re.compile('[^a-zA-Z ]')
# file = re.sub(pattern, ' ', file)

stop_words = open('stop.txt', 'r').read().splitlines()
# stop_words = ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "as",
#               "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by",
#               "could", "did", "do", "does", "doing", "down", "during", "each", "few", "for", "from", "further",
#               "had", "has", "have", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers",
#               "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in",
#               "into", "is", "it", "it's", "its", "itself", "let's", "me", "more", "most", "my", "myself", "nor",
#               "of", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over",
#               "own", "same", "she", "she'd", "she'll", "she's", "should", "so", "some", "such", "than", "that",
#               "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these",
#               "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too",
#               "under", "until", "up", "very", "was", "we", "we'd", "we'll", "we're", "we've", "were", "what",
#               "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why",
#               "why's", "with", "would", "you", "you'd", "you'll", "you're", "you've", "your", "yours",
#               "yourself", "yourselves"]
for stop_word in stop_words:
    file.replace(stop_word, " ")

lines = file.splitlines()

tf_dict = {}
pn_dict = {}

avg_tf_dict = {}
avg_pn_dict = {}

linecounts = []

labelsall = []

tf_bias = 0
pn_bias = 0

avg_tf_bias = 0.0
avg_pn_bias = 0.0

counter_tf = 1.0
counter_pn = 1.0

max_iter = 50

for line in lines:

    linedict = {}
    labelssent = []

    words = line.split()
    id = words[0]
    tag1 = words[2]

    if tag1 == "Pos":
        pn = 1
    else:
        pn = -1

    labelssent.append(pn)

    tag2 = words[1]
    if tag2 == "True":
        tf = 1
    else:
        tf = -1

    labelssent.append(tf)

    words = words[3:]
    line = " ".join(words)
    line = re.sub(pattern, ' ', line)
    # line = line.translate(change)
    line = line.lower()
    words = line.split()

    for word in words:
        if word in linedict:
            linedict[word] += 1
        else:
            linedict[word] = 1

    linecounts.append(linedict)
    labelsall.append(labelssent)

# print labelsall
#
# print linecounts

count = len(lines)

for i in range(max_iter):
    for j in range(count):

        counter_pn += 1
        counter_tf += 1

        act = 0
        act1 = 0
        flag = False
        flag1 = False

        for word in linecounts[j]:
            if word in pn_dict:
                act += pn_dict[word] * linecounts[j][word]

            if word in tf_dict:
                act1 += tf_dict[word] * linecounts[j][word]

            act += pn_bias
            act1 += tf_bias

        if act*labelsall[j][0] <= 0:
            pn_bias = pn_bias + labelsall[j][0]
            avg_pn_bias = avg_pn_bias + labelsall[j][0]*counter_pn

            for word in linecounts[j]:

                if word in pn_dict:
                    pn_dict[word] += linecounts[j][word] * labelsall[j][0]
                    avg_pn_dict[word] += counter_pn * linecounts[j][word] * labelsall[j][0]


                else:
                    pn_dict[word] = linecounts[j][word]*labelsall[j][0]
                    avg_pn_dict[word] = counter_pn * linecounts[j][word] * labelsall[j][0]


        if act1*labelsall[j][1] <= 0:
            tf_bias = tf_bias + labelsall[j][1]
            avg_tf_bias = avg_tf_bias + labelsall[j][1]*counter_pn


            for word in linecounts[j]:

                if word in tf_dict:
                    tf_dict[word] += linecounts[j][word] * labelsall[j][1]
                    avg_tf_dict[word] += counter_tf * linecounts[j][word] * labelsall[j][1]


                else:
                    tf_dict[word] = linecounts[j][word] * labelsall[j][1]
                    avg_tf_dict[word] = counter_tf * linecounts[j][word] * labelsall[j][1]


# print pn_dict
# print tf_dict

to_store = [pn_dict, tf_dict, pn_bias , tf_bias]

with open('vanillamodel.txt', 'wb') as handle:
    pickle.dump(to_store, handle)


for word in tf_dict:
    tf_dict[word] = tf_dict[word] - (avg_tf_dict[word]/counter_tf)
tf_bias = tf_bias - (avg_tf_bias/counter_tf)

for word in pn_dict:
    pn_dict[word] = pn_dict[word] - (avg_pn_dict[word]/counter_pn)
pn_bias = tf_bias - (avg_pn_bias/counter_pn)



to_store = [pn_dict, tf_dict, pn_bias , tf_bias]

with open('averagedmodel.txt', 'wb') as handle:
    pickle.dump(to_store, handle)