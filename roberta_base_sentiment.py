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

# Preprocess text
text = "Good night"
# text = "The Supreme Court, in an 8-1 ruling on Friday, revived the Biden administration's immigration guidelines that prioritize which noncitizens to deport, dismissing a challenge from two Republican state attorneys general who argued the policies conflicted with immigration law.   The court said the states did not have the \"standing,\" or the legal right, to sue in the first place in a decision that will further clarify when a state can challenge a federal policy in court going forward.   The ruling is a major victory for President Joe Biden and the White House, who have consistently argued the need to prioritize who they detain and deport given limited resources. By ruling against the states, the court tightened the rules concerning when states may challenge federal policies with which they disagree.  Justice Brett Kavanaugh wrote the majority opinion. \"In Sum, the States have brought an extraordinarily unusual lawsuit,\" Kavanaugh wrote, in an opinion joined by Chief Justice John Roberts, and Justices Sonia Sotomayor, Elena Kagan and Ketanji Brown Jackson. \"They want a federal court to order the Executive Branch to alter its arrest policies so as to make more arrests. Federal courts have not traditionally entertained that kind of lawsuit; indeed, the States cite no precedent for a lawsuit like this.\"  Justice Neil Gorsuch, joined by Justices Clarence Thomas and Amy Coney Barrett, wrote a concurring an opinion that concluded that the states also lacked reasoning, but for different reasons than the majority opinion. Justice Samuel Alito dissented.  At the heart of the dispute was a September 2021 memo from Homeland Security Secretary Alejandro Mayorkas that laid out priorities for the apprehension and removal of certain non-citizens, reversing efforts by former President Donald Trump to increase deportations.  In his memo, Mayorkas stated that there are approximately 11 million undocumented or otherwise removable non-citizens in the country and that the United States does not have the ability to apprehend and seek to remove all of them. As such, the Department of Homeland Security sought to prioritize those who pose a threat to national security, public safety and border security.    This story has been updated with additional details."
text = preprocess(text)
encoded_input = tokenizer(text, return_tensors="pt")

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

output = model(**encoded_input)
scores = output.logits[0].detach().numpy()
scores = softmax(scores)

# Print results
ranking = np.argsort(scores)
ranking = ranking[::-1]
for i in range(scores.shape[0]):
    label = labels[ranking[i]]
    score = scores[ranking[i]]
    print(f"{i+1}) {label}: {score:.4f}")
end_time = time.time()
execution_time = end_time - start_time
print(f"Время выполнения: {execution_time} секунд")