train = [[('START', 'START'), ('one', 'NUM'), ('said', 'VERB'), (',', 'PERIOD'), ('``', 'PUNCT'), ('when', 'ADV'), ('i', 'PRON'), ('get', 'VERB'), ('a', 'DET'), ('cold', 'NOUN'), ('i', 'PRON'), ('buy', 'VERB'), ('a', 'DET'), ('bottle', 'NOUN'), ('of', 'IN'), ('whiskey', 'NOUN'), ('for', 'IN'), ('it', 'PRON'), (',', 'PERIOD'), ('and', 'CONJ'), ('within', 'IN'), ('a', 'DET'), ('few', 'ADJ'), ('hours', 'NOUN'), ("it's", 'PRON'), ('gone', 'VERB'), ("''", 'PUNCT'), ('.', 'PERIOD'), ('END', 'END')], [('START', 'START'), ('the', 'DET'), ('speaker', 'NOUN'), ('referred', 'VERB'), ('to', 'IN'), ('the', 'DET'), ('whiskey', 'NOUN'), ('but', 'CONJ'), ('his', 'DET'), ('friend', 'NOUN'), ('thought', 'VERB'), ('he', 'PRON'), ('meant', 'VERB'), ('the', 'DET'), ('cold', 'NOUN'), ('.', 'PERIOD'), ('END', 'END')], [('START', 'START'), ('it-wit', 'NOUN'), ('is', 'VERB'), ('a', 'DET'), ('misnomer', 'NOUN'), ('because', 'CONJ'), ('it', 'PRON'), ('covers', 'VERB'), ('slips', 'NOUN'), ('as', 'ADV'), ('well', 'ADV'), ('as', 'CONJ'), ('wit', 'NOUN'), ('.', 'PERIOD'), ('END', 'END')], [('START', 'START'), ('an', 'DET'), ('excited', 'VERB'), ('woman', 'NOUN'), ('was', 'VERB'), ('making', 'VERB'), ('an', 'DET'), ('emergency', 'NOUN'), ('call', 'NOUN'), ('over', 'IN'), ('the', 'DET'), ('phone', 'NOUN'), (':', 'PERIOD'), ('``', 'PUNCT'), ('doctor', 'NOUN'), (',', 'PERIOD'), ('please', 'UH'), ('come', 'VERB'), ('over', 'PART'), ('right', 'ADV'), ('away', 'ADV'), ('.', 'PERIOD'), ('END', 'END')], [('START', 'START'), ('my', 'DET'), ('husband', 'NOUN'), ('is', 'VERB'), ('in', 'IN'), ('great', 'ADJ'), ('pain', 'NOUN'), ('.', 'PERIOD'), ('END', 'END')]]

test = [['START', 'she', 'could', 'see', 'that', 'mr.', 'gorboduc', 'was', 'intrigued', ';', ';', 'END'], ['START', 'the', 'hostess', 'in', 'her', 'took', 'over', '.', 'END'], ['START', 'she', 'was', 'rollickingly', 'happy', '.', 'END'], ['START', '``', 'you', 'what', "''", '?', '?', 'END'], ['START', 'my', 'uncle', 'looked', 'at', 'mr.', 'gorboduc', '.', 'END'], ['START', 'he', 'read', 'henry', 'james', 'and', 'used', 'to', 'pretend', 'profundity', 'through', 'eye-beamings', 'at', 'people', '.', 'END'], ['START', 'mr.', 'gorboduc', 'looked', 'down', '.', 'END'], ['START', 'he','would', 'not', 'look', 'up', '.', 'END'], ['START', 'he', 'was', 'very', 'funny', 'about','the', 'whole', 'thing', '.', 'END']]



word_tag_dict = {}
tags = set()
emission_dict = {}
finalresult = []
for sentence in train:
    for word, tag in sentence:
        tags.add(tag)
        if (word,tag) in emission_dict:
            emission_dict[(word, tag)] += 1
        else:
            emission_dict[(word, tag)] = 1

print(tags)
i = 0
# print(len(test))
print(tags)

# print(emission_dict[(word, tag)])
for sentence in test:
    result = []
    tag_final = 'START'
    for word in sentence:
        count_final = 0
        for tag in tags:
            if (word, tag) in emission_dict:
                print((word,tag))
                count = emission_dict.get((word, tag))
                if count > count_final:
                    tag_final = tag
                    count_final = count
        result.append((word, tag_final))
    finalresult.append(result)
print(finalresult)