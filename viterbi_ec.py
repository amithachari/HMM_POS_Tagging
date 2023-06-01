# mp4.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created Fall 2018: Margaret Fleck, Renxuan Wang, Tiantian Fang, Edward Huang (adapted from a U. Penn assignment)
# Modified Spring 2020: Jialu Li, Guannan Guo, and Kiran Ramnath
# Modified Fall 2020: Amnon Attali, Jatin Arora
# Modified Spring 2021 by Kiran Ramnath (kiranr2@illinois.edu)

"""
Extra Credit: Here should be your best version of viterbi, 
with enhancements such as dealing with suffixes/prefixes separately
"""
import numpy as np


def create_dict(train):
    transition_dict = {}
    words_dict = {}
    start_tag_dic = {}
    tag_dict = {}
    emission_dict = {}
    wordcount = 1
    hapax_corpus = {}

    for sentence in train:
        for word, tag in sentence[1:-1]:
            lensen = len(sentence)
            hapax_corpus[word] = tag

            if word in words_dict:
                words_dict[word] += 1
            else:
                words_dict[word] = 1

            if wordcount == 1 and tag in start_tag_dic:
                start_tag_dic[tag] += 1
            elif wordcount == 1 and tag not in start_tag_dic:
                start_tag_dic[tag] = 1

            if tag in tag_dict:
                tag_dict[tag] += 1
            else:
                tag_dict[tag] = 1

            if (word, tag) in emission_dict:
                emission_dict[(word, tag)] += 1
            else:
                emission_dict[(word, tag)] = 1

            if wordcount > 0 and wordcount < lensen - 2:
                word2, tag2 = sentence[wordcount + 1]
                if (tag, tag2) in transition_dict:
                    transition_dict[(tag, tag2)] += 1
                else:
                    transition_dict[(tag, tag2)] = 1

            wordcount += 1
        wordcount = 1

    return emission_dict, transition_dict, tag_dict, start_tag_dic, words_dict, hapax_corpus

def transition_matrix(transition_dict, tag_dict, alpha):
    T = {}
    tag_len = len(tag_dict)
    for j in transition_dict:
        tag1 = j[0]
        tag2 = j[1]
        T[(tag1, tag2)] = (transition_dict[j] + alpha)/(tag_dict[tag1] + alpha*tag_len)
    return T

def emission_matrix(emission_dict, tag_dict, words_dict, alpha):
    tags = sorted(tag_dict.keys())
    words_len = len(words_dict)
    E = {}
    for tag in tags:
        for word in words_dict:
            count = 0
            key = (word, tag)
            if key in emission_dict:
                count = emission_dict[key]
            count_tag = tag_dict[tag]
            E[key] = (count + alpha)/ (count_tag + alpha*(words_len+1))

    return E

def viterbi_ec(train, test):
    '''
    input:  training data (list of sentences, with tags on the words)
            test data (list of sentences, no tags on the words)
    output: list of sentences with tags on the words
            E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
    '''
    emission_dict, transition_dict, tag_dict, start_tagdic, words_dict, hapax_corpus = create_dict(train)

    null_E = {}
    null_T = {}
    k = 0.00001
    T = transition_matrix(transition_dict, tag_dict, alpha=k)
    E = emission_matrix(emission_dict, tag_dict, words_dict, alpha=k)
    L = len(train)
    W = {}
    finalresult = []

    N = len(start_tagdic)
    hapax = []
    hapax_tag = {}
    for word in words_dict:
        if words_dict[word] == 1:
            hapax.append(word)
    hapax_len = len(hapax)
    for word in hapax:
        temp_tag = hapax_corpus[word]
        if temp_tag in hapax_tag:
            hapax_tag[temp_tag] += 1 / hapax_len
        else:
            hapax_tag[temp_tag] = 1 / hapax_len
    print(hapax_tag)
    for j in transition_dict:
        tag1 = j[0]
        null_T[tag1] = k / (tag_dict[tag1] + k * N)

    for words in emission_dict:
        tag = words[1]
        null_E[tag] = (hapax_tag.get(tag, 0.000000001) * k / (tag_dict[tag] + k * (len(words_dict) + 1)))

    for sentence in test:
        V_start = {}
        V = {}
        max_tag_dict = {}
        tag_list_dict = {}
        V_prev = {}
        count = 0
        reverse_list = []
        backtrack = {}
        word_list = []
        result = []
        for word in sentence[1:-1]:
            word_list.append(word)
            if count == 0:
                for tag in tag_dict:
                    max_tr_prob = np.log((start_tagdic.get(tag, 0) + k) / (L + k * N))
                    if (word, tag) in E:
                        V_start['START', tag] = max_tr_prob + np.log(E[(word, tag)])
                        V_prev[tag] = max_tr_prob + np.log(E[(word, tag)])

                    else:
                        V_start['START', tag] = max_tr_prob + np.log(null_E[tag])
                        V_prev[tag] = max_tr_prob + np.log(null_E[tag])

                    backtrack['START', tag] = V_start['START', tag]
                reverse_list.append(backtrack)
                backtrack = {}

                for words in tag_dict:
                    tag_list_dict[words] = 1
            else:
                for tag1 in tag_dict:
                    for tag2 in tag_dict:
                        if (word, tag2) in E and (tag1, tag2) in T:
                            W[(tag1, tag2)] = (np.log(T[(tag1, tag2)]) + np.log(E[(word, tag2)]))
                        elif (word, tag2) in E and (tag1, tag2) not in T:
                            W[(tag1, tag2)] = (np.log(null_T[tag1]) + np.log(E[(word, tag2)]))
                        elif (tag1, tag2) in T and (word, tag2) not in E:
                            W[(tag1, tag2)] = (np.log(T[(tag1, tag2)]) + np.log(null_E[tag2]))
                        else:
                            W[(tag1, tag2)] = (np.log(null_T[tag1]) + np.log(null_E[tag2]))
                for tag1 in tag_dict:
                    for tag2 in tag_dict:
                        V[tag2, tag1] = V_prev[tag2] + (W[(tag2, tag1)])

                    max_tag_dict[tag1] = max(V.values())
                    backtrack[max(V, key=V.get)] = max(V.values())
                    V = {}

                reverse_list.append(backtrack)
                backtrack = {}
                V_prev = {}
                for key in max_tag_dict:
                    V_prev[key] = max_tag_dict[key]

                tag_list_dict = {}
                for wordpair in max_tag_dict:
                    tag_list_dict[wordpair] = 1

                W = {}
                max_tag_dict = {}

            count += 1

        word_tag = max(reverse_list[count - 1], key=reverse_list[count - 1].get)
        result.insert(0, (word_list[count - 1], word_tag[1]))
        max_word = word_tag[0]
        count -= 1

        while count > 0:
            count -= 1
            for keys in reverse_list[count]:
                if max_word == keys[1]:
                    result.insert(0, (word_list[count], keys[1]))
                    max_word = keys[0]
                    break
        result.insert(0, ('START', 'START'))
        result.append(('END', 'END'))
        finalresult.append(result)
    return finalresult