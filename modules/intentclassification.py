import nltk
from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()
import numpy as np
import json
import neurolab as nl
import random

def bag_of_words(tokenized_sentence, words):
    sentence_words = [stemmer.stem(word.lower()) for word in tokenized_sentence]
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
    for intent in intents["intents"]:
        tag = intent["tag"]
        tags.append(tag)
        for pattern in intent["patterns"]:
            w = nltk.word_tokenize(pattern)
            all_words.extend(w)
            xy.append((w, tag))

    ignore_words = ["?", ".", "!"]
    all_words = [stemmer.stem(w.lower()) for w in all_words if w not in ignore_words]
    all_words = sorted(set(all_words))
    tags = sorted(set(tags))

    tempOutputOneHot = []
    for i, element in enumerate(intents["intents"]):
        one_hot = []
        for x in intents["intents"]:
            one_hot.append(0)
        one_hot[i] = 1
        tempOutputOneHot.append([one_hot, element["tag"]])

    X_train = []
    Y_train = []
    for (pattern_sentence, tag) in xy:
        bag = bag_of_words(pattern_sentence, all_words)
        X_train.append(bag)
        for element in tempOutputOneHot:
            if tag == element[1]:
                Y_train.append(element[0])

    X_train = np.array(X_train)
    Y_train = np.array(Y_train)

    num_epochs = 10000
    input_size = len(X_train[0])
    output_size = len(tags)
    
    net = nl.net.newff([[0, 1]]*input_size, [8, 8, output_size])
    net.train(X_train, Y_train, epochs=num_epochs, show=15, goal=0.05)
    net.save("./data/model.net")

def run(input):
    with open('data/intents.json', 'r') as json_data:
        intents = json.load(json_data)

    all_words = []
    tags = []

    for intent in intents["intents"]:
        tag = intent["tag"]
        tags.append(tag)
        for pattern in intent["patterns"]:
            w = nltk.word_tokenize(pattern)
            all_words.extend(w)

    ignore_words = ["?", ".", "!"]
    all_words = [stemmer.stem(w.lower()) for w in all_words if w not in ignore_words]
    all_words = sorted(set(all_words))

    sentence = nltk.word_tokenize(input)
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
            "trigger": False,
            "error": "No prediction with good probability!",
            "rnd_response": "I do not understand..."
        })