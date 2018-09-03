import time
import math
import copy
import pickle
import sys
from io import open


def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)

def clean_word(word):
    cleaned = word.replace('/', '_')
    cleaned = rreplace(cleaned, '_', '/', 1)
    return cleaned


def main():
    # path = './data/sample_train.txt'

    path = './data/en_train_tagged.txt'
    # path = './data/zh_train_tagged.txt'
    # path = sys.argv[1]

    en_train = open(path, 'r', encoding="utf-8").read()

    tagset = set()
    transition_matrix = {}
    transition_matrix['start'] = {'start': 0.0}
    emission_matrix = {}
    emission_matrix['word_list'] = {}
    possible_tags = {}

    lines = en_train.split('\n')

    for line in lines:
        # print line
        if line.count(' ') <= 1:
            line = '/start '+ line
        tagged_words = line.split()
        # print tagged_words
        tagged_words_len = len(tagged_words)
        tagged_words_iter = tagged_words_len - 1
        processed_start = False
        for i in range(tagged_words_iter):
            thing = tagged_words[i]
            # print thing
            if thing.count('/') > 1:
                thing = clean_word(thing)

            # print
            # print thing
            # print
            item = thing.split('/')

            next_thing = tagged_words[i + 1]
            if next_thing.count('/')>1:
                next_thing = clean_word(next_thing)

            next_item = next_thing.split('/')

            if i == 0:
                if item[0] in possible_tags:
                    if item[1] in possible_tags[item[0]]:
                        pass
                    else:
                        possible_tags[item[0]].append(item[1])
                else:
                    possible_tags[item[0]] = [item[1]]

            if next_item[0] in possible_tags:
                if next_item[1] in possible_tags[next_item[0]]:
                    pass
                else:
                    possible_tags[next_item[0]].append(next_item[1])
            else:
                possible_tags[next_item[0]] = [next_item[1]]


            # if next_item[0] == '.':
            #     print next_thing
            #     print tagged_words[i+2]
            #     print tagged_words[i+3]
            #     if next_item[1] == ',':
            #         pass

            # print item     # # ['eat', 'VB']

            # # Building transition matrix

            if item[1] not in transition_matrix:
                for key in transition_matrix:
                    transition_matrix[key][item[1]] = 0.0
                transition_matrix[item[1]] = {}
                for key in transition_matrix['start']:
                    transition_matrix[item[1]][key] = 0.0

            if next_item[1] not in transition_matrix:
                for key in transition_matrix:
                    transition_matrix[key][next_item[1]] = 0.0
                transition_matrix[next_item[1]] = {}
                for key in transition_matrix['start']:
                    transition_matrix[next_item[1]][key] = 0.0

            if i == 0:
                transition_matrix['start'][item[1]] += 1.0
            transition_matrix[item[1]][next_item[1]] += 1.0

            # #  Building Emission Matrix

            # print item     # # ['eat', 'VB']
            if item[0] not in emission_matrix['word_list']:
                for key in emission_matrix:
                    emission_matrix[key][item[0]] = 0.000000

            if item[1] not in emission_matrix:
                emission_matrix[item[1]] = {}
                for word in emission_matrix['word_list']:
                    emission_matrix[item[1]][word] = 0.000000

            if next_item[0] not in emission_matrix['word_list']:
                for key in emission_matrix:
                    emission_matrix[key][next_item[0]] = 0.000000

            if next_item[1] not in emission_matrix:
                emission_matrix[next_item[1]] = {}
                for word in emission_matrix['word_list']:
                    emission_matrix[next_item[1]][word] = 0.000000

            if i == 0:
                emission_matrix[item[1]][item[0]] += 1
            emission_matrix[next_item[1]][next_item[0]] += 1

    tags_list = emission_matrix.keys()
    words_list = emission_matrix['word_list'].keys()

    # print tags_list
    # print words_list

    for key, val in transition_matrix.items():
        # print key, val
        sum_row = 0.0
        for each_item in val:
            sum_row += val[each_item]
        # print key, sum_row
        for each_item in val:
            # print key, each_item, val[each_item], sum_row
            # if sum_row != 0:
            #     # val[each_item] = (val[each_item] + 1) / (sum_row + len(tags_list))
            #     val[each_item] = (val[each_item]) / (sum_row)
            # else:
            #     # val[each_item] = 0.35
            #     pass
            multiplier = 1
            val[each_item] = (val[each_item] + (1*multiplier)) / (sum_row + (len(tags_list)*multiplier))
            # val[each_item] = (val[each_item]) / (sum_row)

            # if val[each_item] != 0.0:
            #     val[each_item] = math.log(val[each_item], 10)  # LOGIFY! Uncomment later   # without 10 it's to the base e
                # if val[each_item] <0:                       ## FOR MAKING LOGS POSITIVE. MAY NOT BE REQD.
                #     val[each_item] *= -1

    transition_matrix2 = copy.deepcopy(transition_matrix)
    # transition_matrix2['start']['start'] = 1000
    # print transition_matrix['start']['start']
    for it1 in transition_matrix.keys():
        for it2 in transition_matrix.keys():
            transition_matrix2[it1][it2] = transition_matrix[it2][it1]

    for key, val in emission_matrix.items():
        sum_row = 0.0
        for each_item in val:
            sum_row += val[each_item]

        # print key, sum_row

        if sum_row == 0:
            sum_row = 1
        for each_item in val:
            val[each_item] /= sum_row
            if val[each_item] != 0.0:
                val[each_item] = math.log(val[each_item],
                                          10)  # LOGIFY! Uncomment later   # without 10 it's to the base e
                # if val[each_item] <0:                       ## FOR MAKING LOGS POSITIVE. MAY NOT BE REQD.
                #     val[each_item] *= -1

    # for key, val in transition_matrix2.items():
    #     print "'" + key + "':", val, ","
        #    # DONE? Transition matrix


    # # Store in pickle
    # # transition_matrix, emission_matrix, tags, words

    tags_list.remove('word_list')
    # print tags_list

    # for key, val in possible_tags.items():
    #     print key, val

    # print len(tags_list)
    # print tags_list

    to_store = [transition_matrix2, emission_matrix, tags_list, words_list, possible_tags]

    with open('hmmmodel.txt', 'wb') as handle:
        pickle.dump(to_store, handle)

    # print possible_tags['.']


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("\n\n--- %s seconds ---" % (time.time() - start_time))
