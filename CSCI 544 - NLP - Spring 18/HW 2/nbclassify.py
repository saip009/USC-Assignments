import pickle
import re
import math
import sys

path = 'dev-text.txt'
# path = sys.argv[1]

with open('nbmodel.txt', 'rb') as handle:
    pickle_data = pickle.load(handle)

freq_label_dict = pickle_data[0]
prior_prob = pickle_data[1]


stop_words = open('stop.txt', 'r').read().splitlines()
output = open('nboutput.txt', 'w')
output_str = ''


test_data = open(path, 'r').read()

pattern = re.compile('[^a-zA-Z ]')

lines = test_data.splitlines()

for line in lines:

    bayes_prob = {
        'true': 0.0,
        'fake': 0.0,
        'pos': 0.0,
        'neg': 0.0
    }

    words = line.split()

    if len(words) < 1:
        continue

    line_id = words[0]
    output_str = output_str + line_id + ' '

    line = " ".join(words[1:])
    line = re.sub(pattern, ' ', line)
    line = line.lower()
    words = line.split()


    for word in words:

        if word not in freq_label_dict:
            continue

        for key in bayes_prob:
            if freq_label_dict[word][key] == 999999:
                bayes_prob[key] = 0
            else:
                bayes_prob[key] += freq_label_dict[word][key]

    # # PRIOR

    for key in bayes_prob:
        bayes_prob[key] += prior_prob[key]

    if bayes_prob['true'] >= bayes_prob['fake']:
        output_str = output_str + 'True '
    else:
        output_str = output_str + 'Fake '


    if bayes_prob['pos'] >= bayes_prob['neg']:
        output_str = output_str + 'Pos\n'
    else:
        output_str = output_str + 'Neg\n'


output.write(output_str)




