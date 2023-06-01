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
# Modified Spring 2021 by Kiran Ramnath
"""
Part 1: Simple baseline that only uses word statistics to predict tags
"""
from collections import Counter
def baseline(train, test):
    '''
    input:  training data (list of sentences, with tags on the words)
            test data (list of sentences, no tags on the words)
    output: list of sentences, each sentence is a list of (word,tag) pairs.
            E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
    '''
    tag_dict = {}
    for sentence in train:
        for word, tag in sentence:
            if tag in tag_dict:
                tag_dict[tag] += 1
            else:
                tag_dict[tag] = 1

    word_tag_list = []
    for sentence in train:
        word_tag_list += sentence
    pos_tag_vocab = Counter(word_tag_list)
    finalresult = []
    tag_max = max(tag_dict, key=tag_dict.get)

    pos_tag_dict = {}
    for word, tag in pos_tag_vocab:
        if word in pos_tag_dict and pos_tag_vocab[(word, tag)] > pos_tag_vocab[(word,pos_tag_dict[word])]:
            pos_tag_dict[word] = tag
        elif word not in pos_tag_dict:
            pos_tag_dict[word] = tag

    for sentence in test:
        result = []
        for word in sentence:
            if word in pos_tag_dict:
                result.append((word, pos_tag_dict[word]))
            else:
                result.append((word, tag_max))

        finalresult.append(result)

    return finalresult