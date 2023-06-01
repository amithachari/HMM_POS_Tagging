# HMM_POS_Tagging
Implement part of speech (POS) tagging using an HMM model

## Part 1: Baseline tagger
The Baseline tagger considers each word independently, ignoring previous words and tags. For each word w, it counts how many times w occurs with each tag in the training data. When processing the test data, it consistently gives w the tag that was seen most often. For unseen words, it should guess the tag that's seen the most often in training dataset.

A correctly working baseline tagger should get about 93.9% accuracy on the Brown corpus development set, with over 90% accuracy on multitag words and over 69% on unseen words.

![image](https://github.com/amithachari/HMM_POS_Tagging/assets/64373075/f7a227cc-cd28-484e-970e-ef108d7c9c5b)

## Part 2: Viterbi_1
The Viterbi tagger should implement the HMM trellis (Viterbi) decoding algoirthm as seen in lecture or Jurafsky and Martin. That is, the probability of each tag depends only on the previous tag, and the probability of each word depends only on the corresponding tag. This model will need to estimate three sets of probabilities:

Initial probabilities (How often does each tag occur at the start of a sentence?)
Transition probabilities (How often does tag tb follow tag ta?)
Emission probabilities (How often does tag t yield word w?)
You can assume that all sentences will begin with a START token, whose tag is START. So your initial probabilities will have a very restricted form, whether you choose to handcode appropriate numbers or learn them from the data. The initial probabilities shown in the textbook/texture examples will be handled by transition probabilities from the START token to the first real word.

It's helpful to think of your processing in five steps:

Count occurrences of tags, tag pairs, tag/word pairs.
Compute smoothed probabilities
Take the log of each probability
Construct the trellis. Notice that for each tag/time pair, you must store not only the probability of the best path but also a pointer to the previous tag/time pair in that path.
Return the best path through the trellis.
You'll need to use smoothing to get good performance. Make sure that your code for computing transition and emission probabilities never returns zero. Laplace smoothing is the method we use to smooth zero probability cases for calculating initial probabilities, transition probabilities, and emission probabilities.

For example, to smooth the emission probabilities, consider each tag individually. For a fixed tag T, you need to ensure that Pe(W|T)
 produces a non-zero number no matter what word W you give it. You can use Laplace smoothing (as in MP 2) to fill in a probability for "UNKNOWN" which will be the return value for all words W that were not seen in the training data. For this initial implementation of Viterbi, use the same Laplace smoothing constant α
 for all tags.

This simple version of Viterbi will perform worse than the baseline code for the Brown development dataset (somewhat over 93% accuracy). However you should notice that it's doing better on the multiple-tag words (e.g. over 93.5%). You should write this simple version of Viterbi under viterbi_1 function in viterbi_1.py.

![image](https://github.com/amithachari/HMM_POS_Tagging/assets/64373075/5030f2ac-0989-48bd-9349-c12310840e35)

## Part 3: Viterbi_2
The previous Vitebi tagger fails to beat the baseline because it does very poorly on unseen words. It's assuming that all tags have similar probability for these words, but we know that a new word is much more likely to have the tag NOUN than (say) CONJ. For this part, you'll improve your emission smoothing to match the real probabilities for unseen words.

Words that appear zero times in the training data (out-of-vocabulary or OOV words) and words that appear once in the training data (hapax words) tend to have similar parts of speech (POS). For this reason, instead of assuming that OOV words are uniformly distributed across all POS, we can get a much better estimate of their distribution by measuring the distribution of hapax words. Extract these words from the training data and calculate the probability of each tag on them. When you do your Laplace smoothing of the emission probabilities for tag T, scale the Laplace smoothing constant by P(T|hapax), i.e., the probability that tag T occurs given that the word was hapax. Remember that Laplace smoothing acts by reducing probability mass for high-frequency words, and re-assigning some of that probability mass to low-frequency words. A large smoothing constant can end up skewing probability masses a lot, so experiment with small orders of magnitude for this hyperparameter.

This optimized version of the Viterbi code should have a significantly better unseen word accuracy on the Brown development dataset, e.g. over 66.5%. It also beat the baseline on overall accuracy (e.g. 95.5%). You should write your optimized version of Viterbi under the viterbi_2 function in viterbi_2.py.

The hapax word tag probabilities may be different from one dataset to another, so your viterbi_2 method should compute them dynamically from its training data each time it runs.

Hints

Tag 'X' rarely occurs in the dataset. Setting a high value for the Laplace smoothing constant may overly smooth the emission probabilities and break your statistical computations. A small value for the Laplace smoothing constant, e.g. 1e-5, may help.
It's not advisable to use global variables in your implementation since gradescope runs a number of different tests within the same python environment. Global values set during one test will carry over to subsequent tests.

![image](https://github.com/amithachari/HMM_POS_Tagging/assets/64373075/276244fb-4703-4e1d-b4c2-188688b6c73f)

## Extra Credit: Viterbi_ec
The task for the extra credit is to maximize the accuracy of the Viterbi code. You must train on only the provided training set (no external resources) and you should keep the basic Viterbi algorithm. However, you can make any algorithmic improvements you like. This optimized algorithm should be named viterbi_ec

We recommend trying to improve the algorithm's ability to guess the right tag for unseen words. If you examine the set of hapax words in the training data, you should notice that words with certain prefixes and certain suffixes typically have certain limited types of tags. For example, words with suffix "-ly" have several possible tags but the tag distribution is very different from that of the full set of hapax words. You can do a better job of handling these words by changing the emissions probabilities generated for them.

Recall what we did in Parts 2 and 3: we mapped hapax words (in the training data) and unseen words (in the development or test data) into a single pseudoword "UNKNOWN". To exploit the form of the word, you can map hapax/unseen words into several different pseudowords. E.g. perhaps all the words ending in "-ing" could be mapped to "X-ING". Then you can use the hapax words to calculate suitable probability values for X-ING, as in Part 3.

It is extremely hard to predict useful prefixes and suffixes from first principles. We strongly recommend building yourself a separate python tool to dump the hapax words, with their tags, into a separate file that you can inspect. You may assume that our completely hidden datasets are in English, so that word patterns from the Brown corpus should continue to be useful for the hidden corpus.

Using this method, our model solution gets over 76% accuracy on unseen words, and over 96% accuracy overall. (Both numbers on the Brown development dataset.)

It may also be possible to improve performance by using two previous tags (rather than just one) to predict each tag. A full version of this idea would use 256 separate tag pairs and may be too slow to run on the autograder. However, you may be able to gain accuracy by using only selected information from the first of the two tags. Also, beam search can be helpful to speed up decoding time.

![image](https://github.com/amithachari/HMM_POS_Tagging/assets/64373075/8f4938bf-e6c1-4caa-b9db-d3882a6cfee3)


