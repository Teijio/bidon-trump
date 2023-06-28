import os
import time

from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer
import numpy as np
from scipy.special import softmax
import csv
import urllib.request

start_time = time.time()
# Preprocess text (username and link placeholders)
def preprocess(text):
    new_text = []
    for t in text.split(" "):
        t = "@user" if t.startswith("@") and len(t) > 1 else t
        t = "http" if t.startswith("http") else t
        new_text.append(t)
    return " ".join(new_text)

# Tasks:
# emoji, emotion, hate, irony, offensive, sentiment
# stance/abortion, stance/atheism, stance/climate, stance/feminist, stance/hillary

task = "sentiment"
MODEL = f"cardiffnlp/twitter-roberta-base-{task}"
MODEL_DIR = "/mnt/d/pets/bidon-trump/model_dir/"
MODEL_NAME = "twitter-roberta-base"

tokenizer = AutoTokenizer.from_pretrained(MODEL)

# Download label mapping
labels = []
mapping_link = f"https://raw.githubusercontent.com/cardiffnlp/tweeteval/main/datasets/{task}/mapping.txt"
with urllib.request.urlopen(mapping_link) as f:
    html = f.read().decode("utf-8").split("\n")
    csvreader = csv.reader(html, delimiter="\t")
    labels = [row[1] for row in csvreader if len(row) > 1]

import json

with open("data_3.json", "r") as json_file:
    data_first = json.load(json_file)

# texts = list(data_first.values())[:100]


texts = ["The United States and India have resolved six separate trade disputes at the World Trade Organization, including a fight over former President Donald Trump\u2019s tariffs on steel and aluminum and India\u2019s retaliatory duties.\n\u201cWe have decided to resolve long-pending trade-related issues and make a new beginning,\u201d Indian Prime Minister Narendra Modi said at a joint news conference with President Joe Biden following their White House meeting.\nThe agreements are a surprising development, after that National Security Council spokesperson John Kirby told reporters at a press briefing earlier this week not to expect \u201ca specific resolution on trade issues coming out of these next few days.\u201d\nIn fact, India has agreed to remove retaliatory tariffs on certain U.S. products, including chickpeas, lentils, almonds, walnuts, apples, boric acid and diagnostic reagents, that it imposed after Trump slapped duties on steel and aluminum imports using Section 232 of the 1962 Trade Expansion Act.\n\u201cToday\u2019s agreement represents the culmination of intensified bilateral engagement over the last two years, including through the U.S.-India Trade Policy Forum, to deepen our economic and trade ties,\u201d U.S. Trade Representative Katherine Tai said in a statement. \u201cAs a result of our work, U.S. agricultural producers and manufacturers will now enjoy renewed access to a critical global market and we will strengthen our trade relationship with one of our closest partners.\nUSTR said the resolution \u201calso maintains the integrity of the U.S. Section 232 measures.\u201d That means India agreed to lift its trade retaliation without the U.S. altering the steel and aluminum tariffs that Trump imposed, a USTR spokesperson said.\nIn addition to the two cases related to Trump\u2019s tariffs, the United States and India also agreed to terminate four other WTO disputes. Two of those had been filed by India and two by the United States.\nThat still leaves one filed by the United States in 2012 challenging India\u2019s poultry trade barriers. However, one former U.S. "]
preprocessed_texts = [preprocess(t) for t in texts]
encoded_inputs = tokenizer(preprocessed_texts, return_tensors="pt", padding=True, truncation=True)


# Load or download model
if os.path.exists(MODEL_DIR):
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
else:
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)

# Save model and tokenizer
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)
    model.save_pretrained(MODEL_DIR)
    tokenizer.save_pretrained(MODEL_DIR)

output = model(**encoded_inputs)
scores = output.logits.detach().numpy()
scores = softmax(scores, axis=1)

results_list = []

for i in range(scores.shape[0]):
    results = []
    for j in range(scores.shape[1]):
        label = labels[j]
        score = scores[i, j]
        results.append((label, score))

    results_list.append(results)

print(results_list)
# for key, value in zip(data.keys(), results_list):
#     data[key] = value

# with open("updated_dict.json", "w") as json_file:
#     json.dump(data, json_file)