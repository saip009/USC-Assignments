import pickle
import re
import math
import sys

path = 'train-labeled.txt'
# path = sys.argv[1]

train_data = open(path, 'r').read()

pattern = re.compile('[^a-zA-Z ]')

lines = train_data.splitlines()

freq_dict = {}
freq_label_dict = {}
words_set = set()
stop_words = open('stop.txt', 'r').read().splitlines()


total = {
    'true': 0.0,
    'fake': 0.0,
    'pos': 0.0,
    'neg': 0.0
}


prior_count = {
    'true': 0.0,
    'fake': 0.0,
    'pos': 0.0,
    'neg': 0.0
}

prior_prob = {
    'true': 0.0,
    'fake': 0.0,
    'pos': 0.0,
    'neg': 0.0
}

freq_sum_dict = {
    'true': 0.0,
    'fake': 0.0,
    'pos': 0.0,
    'neg': 0.0
}


for line in lines:
    # print line
    line = line.lower()

    words = line.split()

    # print words

    if len(words) < 1:
        continue

    line_id = words[0]
    tf = words[1]
    pn = words[2]

    prior_count[tf] += 1
    prior_count[pn] += 1

    line = " ".join(words[3:])
    line = re.sub(pattern, ' ', line)
    words = line.split()

    for word in words:

        if word in stop_words:
            continue

        if word in words_set:
            freq_dict[word] += 1
            freq_label_dict[word][tf] += 1
            freq_label_dict[word][pn] += 1

        else:
            words_set.add(word)
            freq_dict[word] = 0.0
            freq_label_dict[word] = {
                'true': 0.0,
                'fake': 0.0,
                'pos': 0.0,
                'neg': 0.0,
            }
            freq_dict[word] += 1
            freq_label_dict[word][tf] += 1
            freq_label_dict[word][pn] += 1


prior_prob['pos'] = prior_count['pos']/(prior_count['pos'] + prior_count['neg'])
prior_prob['neg'] = prior_count['neg']/(prior_count['pos'] + prior_count['neg'])

prior_prob['true'] = prior_count['true']/(prior_count['true'] + prior_count['fake'])
prior_prob['fake'] = prior_count['fake']/(prior_count['true'] + prior_count['fake'])

if prior_prob['neg'] == 0:
    prior_prob['neg'] = 999999
else:
    prior_prob['neg'] = math.log10(prior_prob['neg'])


if prior_prob['pos'] == 0:
    prior_prob['pos'] = 999999
else:
    prior_prob['pos'] = math.log10(prior_prob['pos'])


if prior_prob['true'] == 0:
    prior_prob['true'] = 999999
else:
    prior_prob['true'] = math.log10(prior_prob['true'])


if prior_prob['fake'] == 0:
    prior_prob['fake'] = 999999
else:
    prior_prob['fake'] = math.log10(prior_prob['fake'])


# print len(freq_label_dict)
# print len(freq_dict)

remove_list = set()

for word in freq_label_dict:
    mincount = 0
    if freq_dict[word] <= mincount:
        remove_list.add(word)

for word in remove_list:
    del freq_label_dict[word]
    del freq_dict[word]

print len(freq_label_dict)
print len(freq_dict)

true = 0
fake = 0
neg = 0
pos = 0

alpha = 0.75

for word in freq_label_dict:
    for key in freq_label_dict[word]:
        freq_label_dict[word][key] += alpha
        freq_sum_dict[key] += freq_label_dict[word][key]

for word in freq_label_dict:
    for key in freq_label_dict[word]:
        if freq_label_dict[word][key] == 0:
            freq_label_dict[word][key] = 999999
        else:
            freq_label_dict[word][key] = math.log10(freq_label_dict[word][key]/freq_sum_dict[key])

    # print freq_label_dict[word]


print len(freq_label_dict)
print len(freq_dict)


to_store = [freq_label_dict, prior_prob]

with open('nbmodel.txt', 'wb') as handle:
    pickle.dump(to_store, handle)



