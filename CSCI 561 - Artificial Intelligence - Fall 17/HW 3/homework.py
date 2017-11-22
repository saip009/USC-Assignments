import copy


def make_sentence(sentence, index):    # return list form
    sentence = sentence.replace(' ', '').split('|')
    new_sentence = []
    for item in sentence:
        term = []
        start = 0
        for i in xrange(len(item)):
            # print item[i]
            if item[i] in ['(', ',', ')']:
                newitem = item[start:i]
                if newitem[0]<='z' and newitem[0]>='a':           # UNCOMMENT IF REQD. MAKES VAR UNIQUE
                    newitem = newitem + str(index)
                # print newitem
                # print index
                term.append(newitem)
                # raw_input('Enter')
                start = i+1

        new_sentence.append(term)

    return new_sentence
# End of fn


def NOT(query):
    query2 = copy.deepcopy(query)
    if query2[0][0][0] == '~':
        query2[0][0] = query2[0][0].replace('~', '')
    else:
        query2[0][0] = '~' + query2[0][0]

    return query2
# End of fn


def is_same_predicate(predicate_i, predicate_j):
    # for i in xrange(len(predicate_i)):
    #     if predicate_i[i][0] <='z' and predicate_i[i][0] >= 'a':
    #         if not (predicate_j[i][0] <='z' and predicate_j[i][0] >= 'a'):
    #             return False
    #     elif predicate_j[i][0] <='z' and predicate_j[i][0] >= 'a':
    #         if not (predicate_i[i][0] <='z' and predicate_i[i][0] >= 'a'):
    #             return False
    #     elif predicate_i[i] != predicate_j[i]:
    #         return False

    for i in xrange(len(predicate_j)):
        if predicate_i[i] != predicate_j[i]:
            return False

    return True

# End of fn


def is_same_clause(ci, cj):
    if len(ci) != len(cj):
        return False
    count = 0
    newcount = -1
    for predicate_i in ci:
        for predicate_j in cj:
            if is_same_predicate_name(predicate_i, predicate_j):
                if is_same_predicate(predicate_i, predicate_j):       # DEFINE THIS, COMPARE PARAMETERS
                    newcount = count+1
                    break
        if newcount == count:
            break
        count = newcount

    if count == len(ci):
        return True

    return False

    # FILL IT UP. CHECK ALL PREDICATES AND THEIR PARAMETERS -> DONE


def unify_var(y, x, theta):
    if theta is not False:
        first = []
        for sub in theta:
            first.append(sub[0])

        if y[0] in first:
            for i in range(len(first)):
                if theta[i][0] == y[0]:
                    break
            tmp = []
            tmp.append(theta[i][1])
            return unify(tmp, x, theta)
        elif x[0] in first:
            for i in range(len(theta)):
                if theta[i][0] == x[0]:
                    break
            tmp = []
            tmp.append(theta[i][1])
            return unify(y, tmp, theta)
        else:
            theta.append(list((y[0], x[0])))
            return theta
    else:
        return theta

# End of fn


def IN(clause, clauses):
    for item in clauses:
        if is_same_clause(item, clause):
            return True

    return False
# End of fn


def unify(x, y, theta):

    # count = 0
    # for i in xrange(len(x)):
    #     if x[i] != y[i]:
    #         count += 1
    #
    # if count == 0:
    #     theta = list()

    if theta is False:
        return False
    elif y == x and len(y) == 1 and len(x) == 1:
        return theta
    elif len(x) > 1 and len(y) > 1:
        return unify(x[1:], y[1:], unify(x[0:1], y[0:1], theta))
    elif x[0][0] >= 'a' and x[0][0] <= 'z':
        return unify_var(x, y, theta)
    elif y[0][0] >= 'a' and y[0][0] <= 'z':
        return unify_var(y, x, theta)
    else:
        return False

# End of fn


def is_same_predicate_name(predicate_i, predicate_j):
    if predicate_i[0] == predicate_j[0]:
        return True
    if '~' in predicate_j[0]:
        if predicate_j[0][1:] == predicate_i[0]:
            return True
    if '~' in predicate_i[0]:
        if predicate_i[0][1:] == predicate_j[0]:
            return True

    return False
# End of fn


def is_same_predicate_name_not(predicate_i, predicate_j):
    if '~' in predicate_j[0]:
        if predicate_j[0][1:] == predicate_i[0]:
            return True
    if '~' in predicate_i[0]:
        if predicate_i[0][1:] == predicate_j[0]:
            return True

    return False
# End of fn



def unification_substitution(ci, cj, theta):
    ci2 = copy.deepcopy(ci)
    cj2 = copy.deepcopy(cj)
    # print ci
    # print cj

    for i in xrange(len(cj2)):
        for j in xrange(1, len(cj2[i])):
            if cj2[i][j] in theta:
                cj2[i][j] = theta[cj2[i][j]]

    resolved = list(cj2)

    for i in xrange(len(ci2)):
        for j in xrange(1, len(ci2[i])):
            if ci2[i][j] in theta:
                ci2[i][j] = theta[ci2[i][j]]

        # print ci[i]
        tmp = copy.deepcopy(ci2[i])
        tmp = [tmp]
        notcii = NOT(tmp)
        # notcii = ['a','a']
        # print ci[i]
        # print cj

        if ci2[i] in resolved:
            continue
        elif notcii[0] in resolved:
            # print 'aa'
            resolved.remove(notcii[0])
            continue
        else:
            resolved.append(ci2[i])

    return resolved
# END of fn


def standardize(resolvent):
    for i in xrange(len(resolvent)):
        for j in xrange(len(resolvent[i])):
            if resolvent[i][j][0] >= 'a' and resolvent[i][j][0] <= 'z':
                resolvent[i][j] += '1'

    return resolvent


def is_constant_clause(sentence):
    for predicate in sentence:
        for param in predicate:
            if param[0] >= 'a' and param[0] <= 'z':
                return False

    return True


def resolve(ci, cj):

    ci2 = copy.deepcopy(ci)
    cj2 = copy.deepcopy(cj)
    # print ci
    # print cj
    # for i in xrange(len(ci)):
    #     for j in xrange(len(ci[i])):
    #         if ci[i][j]<='z' and ci[i][j]>='a':
    #             ci[i][j] = ci[i][j] + str(1)
    #
    # for i in xrange(len(cj)):
    #     for j in xrange(len(cj[i])):
    #         if cj[i][j]<='z' and cj[i][j]>='a':
    #             cj[i][j] = cj[i][j] + str(2)

    change = 0
    theta = list()
    newclauses = []         # Should be [ [ [] [] ] ]

    for predicate_i in ci2:
        for predicate_j in cj2:
            # print predicate_i
            # print predicate_j
            if is_same_predicate_name_not(predicate_i, predicate_j):
                # print 'isSamePredicate'

                theta = unify(predicate_i[1:], predicate_j[1:], theta)
                # print "i = " + str(predicate_i) + "   j = " + str(predicate_j)
                # print "clause i = " + str(ci) + "  clause  j = " + str(cj)
                change += 1
                if theta is False:
                    return False
                theta2 = dict(theta)
                newclause = unification_substitution(ci2, cj2, theta2)         # Substitutes and 'OR's
                # for i in xrange(len(newclause)):
                #     for j in xrange(len(newclause[i])):
                #         if newclause[i][j] >= 'a' and newclause[i][j] <= 'z':
                #             newclause[i][j] = newclause[i][j][:-1]

                if not IN(newclause, newclauses):
                    newclauses.append(newclause)
                # print theta

    if change == 0:
        newclause = unification_substitution(ci2, cj2, theta)
        # for i in xrange(len(newclause)):
        #     for j in xrange(len(newclause[i])):
        #         if newclause[i][j] >= 'a' and newclause[i][j] <= 'z':
        #             newclause[i][j] = newclause[i][j][:-1]
        newclauses.append(newclause)

            # raw_input('Press <ENTER> ')

    return newclauses  #EDIT
# End of fn


def resolution(kb, query):       # return true false

    clauses = copy.deepcopy(kb)
    clause_removed = 0

    for predicate_j in query:
        for sentence in clauses:
            for predicate_i in sentence:
                if is_same_predicate_name_not(predicate_i, predicate_j):

                    if predicate_j[1:] == predicate_i[1:]:
                        resolvents = []
                        tmpsentence = copy.deepcopy(sentence)
                        tmpsentence.remove(predicate_i)
                        tmpsentence2 = copy.deepcopy(query)
                        tmpsentence2.remove(predicate_j)
                        for tmpp in tmpsentence2:
                            if not IN(tmpp, tmpsentence):
                                tmpsentence.append(tmpp)
                        resolvents.append(tmpsentence)


                    else:
                        resolvents = resolve(sentence, query)

                    if resolvents is False:
                        continue
                    for resolvent in resolvents:
                        # print len(resolvent)
                        if not resolvent:
                            return True

                    for resolvent in resolvents:
                        if not IN(resolvent, clauses):
                            indx = clauses.index(sentence)
                            if not is_constant_clause(sentence):
                                clauses.remove(sentence)
                                clause_removed = 1
                            # clauses.append(clauses.pop(clauses.index(sentence)))
                            resolvent = standardize(resolvent)
                            if resolution(clauses, resolvent) is True:
                                return True
                            if clause_removed == 1:
                                clauses.insert(indx, sentence)
                                clause_removed = 0


    return False

# End of fn


def main():
    ipfile = open('./input.txt', 'r')
    opfile = open('./output.txt', 'w')

    kb = []

    lines = ipfile.read().split('\n')
    index = 0
    nq = int(lines[index])
    index += 1
    queries = []
    for i in xrange(nq):
        queries.append(make_sentence(lines[index], index))     # Queries in list form
        index += 1

    ns = int(lines[index])
    index += 1

    for i in xrange(index, index+ns):
        kb.append(make_sentence(lines[i], i))              # kb in list form
        # print lines[i]
        # print kb[i-index]

    # input is done

    added = 0

    for query in queries:
        # print query
        notquery = NOT(query)
        if not IN(notquery, kb):
            added = 1
            kb.insert(0, notquery)
        # print query
        ans = resolution(kb, notquery)
        if added == 1:
            del kb[0]
        print str(ans).upper()
        opfile.write(str(ans).upper() + '\n')

# end of main

if __name__ == '__main__':
    # ci = [['A', 'x'], ['B', 'x', 'y']]
    # cj = [['C', 'x']]
    # print resolve(ci, cj)
    main()