import pickle
import sys
import time
import math
from io import open



def print_back(backpointer, tag, t):
    pos_tags = [tag]
    for i in reversed(range(1, t)):
        tag = backpointer[i][tag]
        pos_tags.append(tag)
    return pos_tags[::-1]


def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)



def viterbi(transition_matrix, emission_matrix, tags, words, obs, possible_tags):

    backpointer = {}
    previous = {'start': 0.0}

    # tags.remove('word_list')

    observations = obs.strip().split()

    index = -1
    for word in observations:
        index += 1
        current = {}
        backpointer[index] = {}
        if word in possible_tags:
            check_tags = possible_tags[word]
        else:
            check_tags = tags

        if len(check_tags) == 0:
            check_tags = tags

        for tag in check_tags:
            # print word
            # print tag
            # print emission_matrix[tag]
            # time.sleep(100000)
            # print tag


            if (word in words) and (emission_matrix[tag][word] == 0.0):
                continue

            em_p = 0
            if word in words:
                em_p = emission_matrix[tag][word]


            # if tag == 'word_list':
            #     print tag
            #     print emission_matrix[tag][word]

            # print previous
            # print
            # for key, val in backpointer.items():
            #     print key, val
            # print


            prob, back = max((previous[prev] + transition_matrix[tag][prev] + em_p, prev) for prev in previous)
            current[tag] = prob
            backpointer[index][tag] = back

        # print current
        previous = current

    # print previous
    #
    # if len(previous) == 0:
    #     previous = {'start': 0.0}


    # if len(previous):
    #     _, most_pos = max((previous[prev1], prev1) for prev1 in previous)
    # else:
    #     most_pos = 'NN'

    _, most_pos = max((previous[prev1], prev1) for prev1 in previous)


    return print_back(backpointer, most_pos, len(observations))


def write_line(tags, line):
    terms = line.strip().split()
    out = []
    for t in range(len(terms)):
        out.append(terms[t] + '/' + tags[t])
    return ' '.join(out) + '\n'



def main():
    # path = './data/sample_test.txt'

    path = './data/en_dev_raw.txt'
    # path = './data/zh_dev_raw.txt'
    # path = sys.argv[1]


    test_data = open(path).read()

    with open('hmmmodel.txt', 'rb') as handle:
        pickle_data = pickle.load(handle)

    transition_matrix = pickle_data[0]
    emission_matrix = pickle_data[1]
    tags_list = pickle_data[2]
    words_list = pickle_data[3]
    possible_tags = pickle_data[4]

    # print words_list


    # print tags_list
    # print words_list

    # for key, val in emission_matrix.items():
    #     print key, val


    lines = test_data.split('\n')
    # print emission_matrix['NNP']['Wall']


    # print viterbi(transition_matrix, emission_matrix, tags_list, words_list, "They work on Wall Street , after all , so when they hear a company who's stated goals include \" Do n't be evil , \" they imagine a company who's eventually history will be \" Do n't be profitable . ", possible_tags)
    # exit()

    # for line in lines:
        # print viterbi(transition_matrix, emission_matrix, tags_list, words_list, line)
        # print viterbi(transition_matrix, emission_matrix, tags_list, words_list, line)

    pred_tags = []
    output_line = []

    for line in lines:
        words = line.split()
        for word in words:
            word = word.replace('/', '_')
            if word not in words_list:
                for key in emission_matrix.keys():
                    emission_matrix[key][word] = 0.0


    for i, line in enumerate(lines):
        tags = viterbi(transition_matrix, emission_matrix, tags_list, words_list, line, possible_tags)
        print 'Line ' + str(i) + ': Processed'
        # print tags
        pred_tags += tags
        output_line.append(write_line(tags, line))

    # for line in real_lines:
    #     actual_tags += extract_tags_test(line)
    with open('hmmoutput.txt', 'w', encoding="utf-8") as fid:
        for line in output_line:
            fid.write(unicode(line))

if __name__ == "__main__":
    start = time.time()
    main()
    print("\n\n--- %s seconds ---" % (time.time() - start))


