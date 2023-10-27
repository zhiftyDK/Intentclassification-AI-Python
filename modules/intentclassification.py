import nltk
from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()
import numpy as np
import json
import neurolab as nl
import random
import os

def tokenize(sentence):
    """
    split sentence into array of words/tokens
    a token can be a word or punctuation character, or number
    """
    return nltk.word_tokenize(sentence)


def stem(word):
    """
    stemming = find the root form of the word
    examples:
    words = ["organize", "organizes", "organizing"]
    words = [stem(w) for w in words]
    -> ["organ", "organ", "organ"]
    """
    return stemmer.stem(word.lower())


def bag_of_words(tokenized_sentence, words):
    """
    return bag of words array:
    1 for each known word that exists in the sentence, 0 otherwise
    example:
    sentence = ["hello", "how", "are", "you"]
    words = ["hi", "hello", "I", "you", "bye", "thank", "cool"]
    bag   = [  0 ,    1 ,    0 ,   1 ,    0 ,    0 ,      0]
    """
    # stem each word
    sentence_words = [stem(word) for word in tokenized_sentence]
    # initialize bag with 0 for each word
    bag = np.zeros(len(words), dtype=np.float32)
    for idx, w in enumerate(words):
        if w in sentence_words: 
            bag[idx] = 1

    return bag

def train():
    with open("data/intents.json", "r") as f:
        intents = json.load(f)

    all_words = []
    tags = []
    xy = []
    # loop through each sentence in our intents patterns
    for intent in intents["intents"]:
        tag = intent["tag"]
        # add to tag list
        tags.append(tag)
        for pattern in intent["patterns"]:
            # tokenize each word in the sentence
            w = tokenize(pattern)
            # add to our words list
            all_words.extend(w)
            # add to xy pair
            xy.append((w, tag))

    # stem and lower each word
    ignore_words = ["?", ".", "!"]
    all_words = [stem(w) for w in all_words if w not in ignore_words]
    # remove duplicates and sort
    all_words = sorted(set(all_words))
    tags = sorted(set(tags))

    # print(len(xy), "patterns")
    # print(len(tags), "tags:", tags)
    # print(len(all_words), "unique stemmed words:", all_words)

    tempOutputOneHot = []
    for i, element in enumerate(intents["intents"]):
        one_hot = []
        for x in intents["intents"]:
            one_hot.append(0)
        one_hot[i] = 1
        tempOutputOneHot.append([one_hot, element["tag"]])

    # create training data
    X_train = []
    Y_train = []
    for (pattern_sentence, tag) in xy:
        # X: bag of words for each pattern_sentence
        bag = bag_of_words(pattern_sentence, all_words)
        X_train.append(bag)
        # Y: one-hot encoding
        for element in tempOutputOneHot:
            if tag == element[1]:
                Y_train.append(element[0])

    X_train = np.array(X_train)
    Y_train = np.array(Y_train)

    num_epochs = 10000
    input_size = len(X_train[0])
    output_size = len(tags)
    
    print(input_size, output_size)
    net = nl.net.newff([[0, 1]]*input_size, [8, 8, output_size])
    print(len(net.layers))
    net.train(X_train, Y_train, epochs=num_epochs, show=15, goal=0.05)
    net.save("./data/model.net")

def run(input):
    with open('data/intents.json', 'r') as json_data:
        intents = json.load(json_data)

    all_words = []
    tags = []

    for intent in intents["intents"]:
        tag = intent["tag"]
        # add to tag list
        tags.append(tag)
        for pattern in intent["patterns"]:
            # tokenize each word in the sentence
            w = tokenize(pattern)
            # add to our words list
            all_words.extend(w)

    # stem and lower each word
    ignore_words = ["?", ".", "!"]
    all_words = [stem(w) for w in all_words if w not in ignore_words]
    # remove duplicates and sort
    all_words = sorted(set(all_words))

    sentence = tokenize(input)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])

    net = nl.load("./data/model.net")
    output = net.sim(X)
    output = np.asarray(output[0])
    idx = (np.abs(output - 1)).argmin()
    tag = tags[idx]
    if output[idx] > 0.75:
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                return json.dumps({
                    "tag": tag,
                    "trigger": intent["trigger"],
                    "responses": intent["responses"],
                    "rnd_response": False if not intent["responses"] else random.choice(intent["responses"])
                })
    else:
        return json.dumps({
            "error": "No prediction with good probability!",
            "message": "I do not understand..."
        })