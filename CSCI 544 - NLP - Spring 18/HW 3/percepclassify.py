import pickle
import re
import string
import sys

# path = 'sampletest.txt'
path = './dev-text.txt'
# path = sys.argv[2]

modelpath = 'averagedmodel.txt'
# modelpath = 'vanilla.txt'
# modelpath = sys.argv[1]

with open(modelpath, 'rb') as handle:
    pickle_data = pickle.load(handle)

pn_dict = pickle_data[0]
tf_dict = pickle_data[1]
pn_bias = pickle_data[2]
tf_bias = pickle_data[3]

# print pn_dict
# print tf_dict
# print pn_bias
# print tf_bias

# change = str.maketrans('','',string.punctuation)

file = open(path, 'r').read()

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

output = ""

for line in lines:
    line_count = {}
    words = line.split()
    id = words[0]
    output += id + " "
    words = words[1:]

    line = " ".join(words)
    line = line.lower()
    line = re.sub(pattern, ' ', line)
    # line = line.translate(change)
    words = line.split()

    act = 0
    act1 = 0

    for word in words:
        if word in line_count:
            line_count[word] += 1
        else:
            line_count[word] = 1

    for word in line_count:
        if word in pn_dict:
            act += pn_dict[word] * line_count[word]

        if word in tf_dict:
            act1 += tf_dict[word] * line_count[word]

    act += pn_bias
    act1 += tf_bias

    if act1>0 :
        output += "True "
    else:
        output += "Fake "

    if act > 0:
        output += "Pos\n"
    else:
        output += "Neg\n"

open('percepoutput.txt', 'w').write(output)






