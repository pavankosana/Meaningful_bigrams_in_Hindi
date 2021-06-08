# -*- coding: utf-8 -*-
"""Required Programs and functions only.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17oI3O68pyRUWtUmJpH5OPK0cqoheFOHe
"""

# -*- coding: utf-8 -*-
"""MidSem.ipynb
 
Automatically generated by Colaboratory.
 
Original file is located at
    https://colab.research.google.com/drive/1dB-4gzbC3DApvfjJHpRXXbdqoCAYdyie
"""
 
from nltk.tag import pos_tag
import nltk
from nltk.tag import BigramTagger
from sklearn.metrics import f1_score, accuracy_score,confusion_matrix, recall_score, precision_score
from nltk.corpus import indian
from nltk.tag import tnt
import random
import pandas as pd
 
nltk.download('averaged_perceptron_tagger')
nltk.download('indian')
 
tag = []
bi_word = []
dataset = []
with open("/content/drive/MyDrive/sharesd/sms-cw_2/CN-MWE-Dataset-from-wordnet.txt") as file:
  dataset = file.readlines()
#print(dataset)
 
for row in dataset:
  row = row.split("\t")
  count = 0
  for i in row[1]:
    if i == "_":
      count += 1
  if count > 1:
    continue
  count = 0
  for i in row[1]:
    if i == "-":
      count += 1
  if count > 1:
    continue
  if "_" in row[1]:
    old = len(bi_word)
    bi_word.append(row[1].split("_"))
    new = len(bi_word)
    if new > old:
      tag.append(row[0].split("+"))
  elif "-" in row[1]:
    old = len(bi_word)
    bi_word.append(row[1].split("-"))
    new = len(bi_word)
    if new > old:
      tag.append(row[0].split("+"))
#print(tag)
#print(bi_word)
 
#print(len(tag), len(bi_word))
 
with open("/content/drive/MyDrive/sharesd/sms-cw_2/LVC-MWE-Dataset-from-wordnet.txt") as file:
  dataset = file.readlines()
#print(dataset)
 
for row in dataset:
  row = row.split("\t")
  count = 0
  for i in row[1]:
    if i == "_":
      count += 1
  if count > 1:
    continue
  count = 0
  for i in row[1]:
    if i == "-":
      count += 1
  if count > 1:
    continue
 
  if "_" in row[1]:
    old = len(bi_word)
    bi_word.append(row[1].split("_"))
    new = len(bi_word)
    if new > old:
      tag.append(row[0].split("+"))
  elif "-" in row[1]:
    old = len(bi_word)
    bi_word.append(row[1].split("-"))
    new = len(bi_word)
    if new > old:
      tag.append(row[0].split("+"))
#print(tag)
#print(bi_word)
wordnet_wrd = bi_word.copy
# Trainining the Dataset
dataset = []
#print(len(tag), len(bi_word))
for i in range(len(tag)):
  current_set = []
  first_pair = (bi_word[i][0], tag[i][0])
  second_pair = (bi_word[i][1], tag[i][1])
  dataset.append([first_pair, second_pair])
#print(dataset[0])
 
random.shuffle(dataset)
#print(dataset)
 
train_data = dataset[0: 20000]
test_data = dataset[20000: ]
 
pos_tagger = tnt.TnT()
pos_tagger.train(train_data)
 
print("POS TAGGER ACCURACY = {}".format(pos_tagger.evaluate(test_data)))
 
actual_tags = []
for val in dataset[20000:]:
  #print((val[0][0], val[1][0]))
  actual_tags.append((val[0][1], val[1][1]))
 
#print(actual_tags)
print("ALL DIFFERENT TAGS PAIR = {}".format(set(actual_tags)))
 
pos_tags = []
for val in dataset[20000: ]:
  curr_word = val[0][0] + " " +  val[1][0]
  pos_tags.append((pos_tagger.tag(curr_word.split(" "))[0][1], pos_tagger.tag(curr_word.split(" "))[1][1]))
print(pos_tags)
 
bigram_tagger = BigramTagger(train=dataset[0: 20000])
print("Accuracy of Bigram Tagging = {}".format(bigram_tagger.evaluate(dataset[20000:])))
 
bigram_tags = []
for val in dataset[20000: ]:
  curr_word = val[0][0] + " " +  val[1][0]
  bigram_tags.append((bigram_tagger.tag(curr_word.split(" "))[0][1], bigram_tagger.tag(curr_word.split(" "))[1][1]))
print(bigram_tags)
 
precision_1 = []
precision_2 = []
recall_1 = []
recall_2 = []
accuray_1 = []
accuray_2 = []
count_1 = []
count_2 = []
actual = []
 
ALL_DIFFERENT_TAGS_PAIR = {('n', 'v'), ('adj', 'v'), ('adv', 'n'), ('adj', 'n'), ('adv', 'v'), ('n', 'n')}
 
# Noun(n) + Verb(v)
count_actual = []
count_pos_tagger_nltk = []
count_bigram = []
 
for i in range(len(actual_tags)):
  if "n" in actual_tags[i][0] and "v" in actual_tags[i][1]:
    count_actual.append(1)
  else:
    count_actual.append(0)
  if "n" in pos_tags[i][0] and "v" in pos_tags[i][1]:
    count_pos_tagger_nltk.append(1)
  else:
    count_pos_tagger_nltk.append(0)
  
  if bigram_tags[i][0] == None or bigram_tags[i][1] == None:
    count_bigram.append(0)
    continue
  if ("n" in bigram_tags[i][0] and "v" in bigram_tags[i][1]):
    count_bigram.append(1)
  else:
    count_bigram.append(0)
 
count_pos_tagger = 0
count_bigram_tagger = 0
for i in count_pos_tagger_nltk:
  count_pos_tagger += i
for i in count_bigram:
  count_bigram_tagger += i
 
 
accuracy_pos_tagger = accuracy_score(count_actual, count_pos_tagger_nltk)
accuracy_bigram_tagger = accuracy_score(count_actual, count_bigram)
precision_pos_tagger = precision_score(count_actual, count_pos_tagger_nltk)
precision_bigram_tagger = precision_score(count_actual, count_bigram)
recall_pos_tagger = recall_score(count_actual, count_pos_tagger_nltk)
recall_bigram_tagger = recall_score(count_actual, count_bigram)
 
precision_1.append(precision_pos_tagger)
precision_2.append(precision_bigram_tagger)
recall_1.append(recall_pos_tagger)
recall_2.append(recall_bigram_tagger)
accuray_1.append(accuracy_pos_tagger)
accuray_2.append(accuracy_bigram_tagger)
count_1.append(count_pos_tagger)
count_2.append(count_bigram_tagger)
actual.append(count_actual.count(1))
print("=================== POS TAGGER ====================")
print("Count of Actual (Noun and Verbs pair) =", count_actual.count(1))
print("Count of PosTagger (Noun and Verbs pair) =", count_pos_tagger)
print("accuracy =", accuracy_pos_tagger)
print("precision =", precision_pos_tagger)
print("recall =", recall_pos_tagger)
 
print()
print("=================== BIGRAM TAGGER ====================")
print("Count of Actual (Noun and Verbs pair) =", count_actual.count(1))
print("Count of Bigram Tagger (Noun and Verbs pair) =", count_bigram_tagger)
print("accuracy =", accuracy_bigram_tagger)
print("precision =", precision_bigram_tagger)
print("recall =", recall_bigram_tagger)
 
# Adjective(adj) + Verb(v)
count_actual = []
count_pos_tagger_nltk = []
count_bigram = []
 
for i in range(len(actual_tags)):
  if "adj" in actual_tags[i][0] and "v" in actual_tags[i][1]:
    count_actual.append(1)
  else:
    count_actual.append(0)
  if "adj" in pos_tags[i][0] and "v" in pos_tags[i][1]:
    count_pos_tagger_nltk.append(1)
  else:
    count_pos_tagger_nltk.append(0)
  
  if bigram_tags[i][0] == None or bigram_tags[i][1] == None:
    count_bigram.append(0)
    continue
  if ("adj" in bigram_tags[i][0] and "v" in bigram_tags[i][1]):
    count_bigram.append(1)
  else:
    count_bigram.append(0)
 
count_pos_tagger = 0
count_bigram_tagger = 0
for i in count_pos_tagger_nltk:
  count_pos_tagger += i
for i in count_bigram:
  count_bigram_tagger += i
 
 
accuracy_pos_tagger = accuracy_score(count_actual, count_pos_tagger_nltk)
accuracy_bigram_tagger = accuracy_score(count_actual, count_bigram)
precision_pos_tagger = precision_score(count_actual, count_pos_tagger_nltk)
precision_bigram_tagger = precision_score(count_actual, count_bigram)
recall_pos_tagger = recall_score(count_actual, count_pos_tagger_nltk)
recall_bigram_tagger = recall_score(count_actual, count_bigram)
 
precision_1.append(precision_pos_tagger)
precision_2.append(precision_bigram_tagger)
recall_1.append(recall_pos_tagger)
recall_2.append(recall_bigram_tagger)
accuray_1.append(accuracy_pos_tagger)
accuray_2.append(accuracy_bigram_tagger)
count_1.append(count_pos_tagger)
count_2.append(count_bigram_tagger)
actual.append(count_actual.count(1))
 
print("=================== POS TAGGER ====================")
print("Count of Actual (Adjective and Verbs pair) =", count_actual.count(1))
print("Count of PosTagger (Adjective and Verbs pair) =", count_pos_tagger)
print("accuracy =", accuracy_pos_tagger)
print("precision =", precision_pos_tagger)
print("recall =", recall_pos_tagger)
 
print()
print("=================== BIGRAM TAGGER ====================")
print("Count of Actual (Adjective and Verbs pair) =", count_actual.count(1))
print("Count of Bigram Tagger (Adjective and Verbs pair) =", count_bigram_tagger)
print("accuracy =", accuracy_bigram_tagger)
print("precision =", precision_bigram_tagger)
print("recall =", recall_bigram_tagger)
 
# Adjective(adj) + Noun(n)
count_actual = []
count_pos_tagger_nltk = []
count_bigram = []
 
for i in range(len(actual_tags)):
  if "adj" in actual_tags[i][0] and "n" in actual_tags[i][1]:
    count_actual.append(1)
  else:
    count_actual.append(0)
  if "adj" in pos_tags[i][0] and "n" in pos_tags[i][1]:
    count_pos_tagger_nltk.append(1)
  else:
    count_pos_tagger_nltk.append(0)
  
  if bigram_tags[i][0] == None or bigram_tags[i][1] == None:
    count_bigram.append(0)
    continue
  if ("adj" in bigram_tags[i][0] and "n" in bigram_tags[i][1]):
    count_bigram.append(1)
  else:
    count_bigram.append(0)
 
count_pos_tagger = 0
count_bigram_tagger = 0
for i in count_pos_tagger_nltk:
  count_pos_tagger += i
for i in count_bigram:
  count_bigram_tagger += i
 
 
accuracy_pos_tagger = accuracy_score(count_actual, count_pos_tagger_nltk)
accuracy_bigram_tagger = accuracy_score(count_actual, count_bigram)
precision_pos_tagger = precision_score(count_actual, count_pos_tagger_nltk)
precision_bigram_tagger = precision_score(count_actual, count_bigram)
recall_pos_tagger = recall_score(count_actual, count_pos_tagger_nltk)
recall_bigram_tagger = recall_score(count_actual, count_bigram)
 
precision_1.append(precision_pos_tagger)
precision_2.append(precision_bigram_tagger)
recall_1.append(recall_pos_tagger)
recall_2.append(recall_bigram_tagger)
accuray_1.append(accuracy_pos_tagger)
accuray_2.append(accuracy_bigram_tagger)
count_1.append(count_pos_tagger)
count_2.append(count_bigram_tagger)
actual.append(count_actual.count(1))
 
print("=================== POS TAGGER ====================")
print("Count of Actual (Adjective and Noun pair) =", count_actual.count(1))
print("Count of PosTagger (Adjective and Noun pair) =", count_pos_tagger)
print("accuracy =", accuracy_pos_tagger)
print("precision =", precision_pos_tagger)
print("recall =", recall_pos_tagger)
 
print()
print("=================== BIGRAM TAGGER ====================")
print("Count of Actual (Adjective and Noun pair) =", count_actual.count(1))
print("Count of Bigram Tagger (Adjective and Noun pair) =", count_bigram_tagger)
print("accuracy =", accuracy_bigram_tagger)
print("precision =", precision_bigram_tagger)
print("recall =", recall_bigram_tagger)
 
# Adjverb(adv) + Noun(n)
count_actual = []
count_pos_tagger_nltk = []
count_bigram = []
 
for i in range(len(actual_tags)):
  if "adv" in actual_tags[i][0] and "n" in actual_tags[i][1]:
    count_actual.append(1)
  else:
    count_actual.append(0)
  if "adv" in pos_tags[i][0] and "n" in pos_tags[i][1]:
    count_pos_tagger_nltk.append(1)
  else:
    count_pos_tagger_nltk.append(0)
  
  if bigram_tags[i][0] == None or bigram_tags[i][1] == None:
    count_bigram.append(0)
    continue
  if ("adv" in bigram_tags[i][0] and "n" in bigram_tags[i][1]):
    count_bigram.append(1)
  else:
    count_bigram.append(0)
 
count_pos_tagger = 0
count_bigram_tagger = 0
for i in count_pos_tagger_nltk:
  count_pos_tagger += i
for i in count_bigram:
  count_bigram_tagger += i
 
 
accuracy_pos_tagger = accuracy_score(count_actual, count_pos_tagger_nltk)
accuracy_bigram_tagger = accuracy_score(count_actual, count_bigram)
precision_pos_tagger = precision_score(count_actual, count_pos_tagger_nltk)
precision_bigram_tagger = precision_score(count_actual, count_bigram)
recall_pos_tagger = recall_score(count_actual, count_pos_tagger_nltk)
recall_bigram_tagger = recall_score(count_actual, count_bigram)
 
precision_1.append(precision_pos_tagger)
precision_2.append(precision_bigram_tagger)
recall_1.append(recall_pos_tagger)
recall_2.append(recall_bigram_tagger)
accuray_1.append(accuracy_pos_tagger)
accuray_2.append(accuracy_bigram_tagger)
count_1.append(count_pos_tagger)
count_2.append(count_bigram_tagger)
actual.append(count_actual.count(1))
 
print("=================== POS TAGGER ====================")
print("Count of Actual (Adverb and Noun pair) =", count_actual.count(1))
print("Count of PosTagger (Adverb and Noun pair) =", count_pos_tagger)
print("accuracy =", accuracy_pos_tagger)
print("precision =", precision_pos_tagger)
print("recall =", recall_pos_tagger)
 
print()
print("=================== BIGRAM TAGGER ====================")
print("Count of Actual (Adverb and Noun pair) =", count_actual.count(1))
print("Count of Bigram Tagger (Adverb and Noun pair) =", count_bigram_tagger)
print("accuracy =", accuracy_bigram_tagger)
print("precision =", precision_bigram_tagger)
print("recall =", recall_bigram_tagger)
 
# Adverb(adv) + Verb(v)
count_actual = []
count_pos_tagger_nltk = []
count_bigram = []
 
for i in range(len(actual_tags)):
  if "adv" in actual_tags[i][0] and "v" in actual_tags[i][1]:
    count_actual.append(1)
  else:
    count_actual.append(0)
  if "adv" in pos_tags[i][0] and "v" in pos_tags[i][1]:
    count_pos_tagger_nltk.append(1)
  else:
    count_pos_tagger_nltk.append(0)
  
  if bigram_tags[i][0] == None or bigram_tags[i][1] == None:
    count_bigram.append(0)
    continue
  if ("adv" in bigram_tags[i][0] and "v" in bigram_tags[i][1]):
    count_bigram.append(1)
  else:
    count_bigram.append(0)
 
count_pos_tagger = 0
count_bigram_tagger = 0
for i in count_pos_tagger_nltk:
  count_pos_tagger += i
for i in count_bigram:
  count_bigram_tagger += i
 
 
accuracy_pos_tagger = accuracy_score(count_actual, count_pos_tagger_nltk)
accuracy_bigram_tagger = accuracy_score(count_actual, count_bigram)
precision_pos_tagger = precision_score(count_actual, count_pos_tagger_nltk)
precision_bigram_tagger = precision_score(count_actual, count_bigram)
recall_pos_tagger = recall_score(count_actual, count_pos_tagger_nltk)
recall_bigram_tagger = recall_score(count_actual, count_bigram)
 
precision_1.append(precision_pos_tagger)
precision_2.append(precision_bigram_tagger)
recall_1.append(recall_pos_tagger)
recall_2.append(recall_bigram_tagger)
accuray_1.append(accuracy_pos_tagger)
accuray_2.append(accuracy_bigram_tagger)
count_1.append(count_pos_tagger)
count_2.append(count_bigram_tagger)
actual.append(count_actual.count(1))
 
print("=================== POS TAGGER ====================")
print("Count of Actual (Adverb and Verb pair) =", count_actual.count(1))
print("Count of PosTagger (Adverb and Verb pair) =", count_pos_tagger)
print("accuracy =", accuracy_pos_tagger)
print("precision =", precision_pos_tagger)
print("recall =", recall_pos_tagger)
 
print()
print("=================== BIGRAM TAGGER ====================")
print("Count of Actual (Adverb and Verb pair) =", count_actual.count(1))
print("Count of Bigram Tagger (Adverb and Verb pair) =", count_bigram_tagger)
print("accuracy =", accuracy_bigram_tagger)
print("precision =", precision_bigram_tagger)
print("recall =", recall_bigram_tagger)
 
# Noun(n) + Noun(n)
count_actual = []
count_pos_tagger_nltk = []
count_bigram = []
 
for i in range(len(actual_tags)):
  if "n" in actual_tags[i][0] and "n" in actual_tags[i][1]:
    count_actual.append(1)
  else:
    count_actual.append(0)
  if "n" in pos_tags[i][0] and "n" in pos_tags[i][1]:
    count_pos_tagger_nltk.append(1)
  else:
    count_pos_tagger_nltk.append(0)
  
  if bigram_tags[i][0] == None or bigram_tags[i][1] == None:
    count_bigram.append(0)
    continue
  if ("n" in bigram_tags[i][0] and "n" in bigram_tags[i][1]):
    count_bigram.append(1)
  else:
    count_bigram.append(0)
 
count_pos_tagger = 0
count_bigram_tagger = 0
for i in count_pos_tagger_nltk:
  count_pos_tagger += i
for i in count_bigram:
  count_bigram_tagger += i
 
 
accuracy_pos_tagger = accuracy_score(count_actual, count_pos_tagger_nltk)
accuracy_bigram_tagger = accuracy_score(count_actual, count_bigram)
precision_pos_tagger = precision_score(count_actual, count_pos_tagger_nltk)
precision_bigram_tagger = precision_score(count_actual, count_bigram)
recall_pos_tagger = recall_score(count_actual, count_pos_tagger_nltk)
recall_bigram_tagger = recall_score(count_actual, count_bigram)
 
precision_1.append(precision_pos_tagger)
precision_2.append(precision_bigram_tagger)
recall_1.append(recall_pos_tagger)
recall_2.append(recall_bigram_tagger)
accuray_1.append(accuracy_pos_tagger)
accuray_2.append(accuracy_bigram_tagger)
count_1.append(count_pos_tagger)
count_2.append(count_bigram_tagger)
actual.append(count_actual.count(1))
 
print("=================== POS TAGGER ====================")
print("Count of Actual (Noun and Noun pair) =", count_actual.count(1))
print("Count of PosTagger (Noun and Noun pair) =", count_pos_tagger)
print("accuracy =", accuracy_pos_tagger)
print("precision =", precision_pos_tagger)
print("recall =", recall_pos_tagger)
 
print()
print("=================== BIGRAM TAGGER ====================")
print("Count of Actual (Noun and Noun pair) =", count_actual.count(1))
print("Count of Bigram Tagger (Noun and Noun pair) =", count_bigram_tagger)
print("accuracy =", accuracy_bigram_tagger)
print("precision =", precision_bigram_tagger)
print("recall =", recall_bigram_tagger)
 
# POS TAGGER
data_frame = pd.DataFrame(actual, index=["Noun + Verb",
                                          "Adjective + verb", 
                                          "Adjective + Noun",
                                          "Adverb + Noun",
                                          "Adverb + Verb",
                                          "Noun + Noun"],
                          columns=["Actual"])
data_frame["count"] = count_1
data_frame["precision"] = precision_1
data_frame["recall"] = recall_1
data_frame["accuracy"] = accuray_1
#print("===================== BIGRAM TAGGED (using pos tagger) =====================")
print("===================== BIGRAM TAGGED (using pos tagger) =====================")
print(data_frame)
 
# POS TAGGER
data_frame = pd.DataFrame(actual, index=["Noun + Verb",
                                          "Adjective + verb", 
                                          "Adjective + Noun",
                                          "Adverb + Noun",
                                          "Adverb + Verb",
                                          "Noun + Noun"],
                          columns=["Actual"])
data_frame["count"] = count_2
data_frame["precision"] = precision_2
data_frame["recall"] = recall_2
data_frame["accuracy"] = accuray_2
print("===================== BIGRAM TAGGED (using bigram tagger) =====================")
print(data_frame)


bi_wordss = bi_word

!pip install inltk

!pip install torch==1.3.1+cpu -f https://download.pytorch.org/whl/torch_stable.html

!pip install flask-ngrok

#ignore the error 'This event loop is already running' if it occurs and run from the next cell
from inltk.inltk import setup
setup('hi')

import warnings
warnings.filterwarnings("ignore")

from inltk.inltk import get_sentence_similarity
wor = bi_word[:20]                                 #using only first 20 words in CN-MWE-Dataset-from-wordnet.txt
for i in wor:
  bi = i[0]+ " " + i[1]
  sim_val = get_sentence_similarity('20वां वर्ष',bi,'hi')       # '20वां वर्ष' is in first 20 words in dataset.so it should detect the word as similar one
  print(sim_val)
  if sim_val>0.9:
    print(bi)

#20वां वर्ष
#मानव विज्ञानी               #word is in dataset but not in first 20 words

import warnings
warnings.filterwarnings("ignore")
from inltk.inltk import get_sentence_similarity

def sim_words_in_dataset_inputtext(inp,bi_wordsss):
  word_s = bi_wordsss[:20]
  text_tokenss = []
  oup_bi = []
  text_tokenss.append(inp.split(" "))
  #print(text_tokenss[0])
  for k in range(len(text_tokenss[0])-1):
    for i in word_s:
      inp_bi = i[0]+ " " + i[1]
      dataset_bi = text_tokenss[0][k]+ " "+text_tokenss[0][k+1]
      sim_val = get_sentence_similarity(inp_bi,dataset_bi,'hi')
      #print(sim_val)
      if sim_val>0.98:
        #print(inp_bi)
        oup_bi.append(inp_bi)
  return oup_bi

#Pos_tagger for given text/paragraph

def Meaningful_Bigrams(dataset):
  tag = []
  bi_word = []
  tags = []
  words = []
  words.append(dataset[0].split(" "))

  tag.append(pos_tagger.tag(words[0]))

  for i in tag:
    for j in i:
      tags.append(j[1])

  for i in tag:
    for j in i:
      bi_word.append(j[0])

  k = len(tags)-1
  bigram_note = []
  for i in range(k):
    if tags[i] == 'n' and tags[i+1]=='n':
      bigram_note.append(i)
    elif tags[i] == 'n' and tags[i+1]=='v':
      bigram_note.append(i)
    elif tags[i] == 'adj' and tags[i+1]=='v':
      bigram_note.append(i)
    elif tags[i] == 'adv' and tags[i+1]=='n':
      bigram_note.append(i)
    elif tags[i] == 'adv' and tags[i+1]=='v':
      bigram_note.append(i)
    elif tags[i] == 'adj' and tags[i+1]=='n':
      bigram_note.append(i)

  final_tags = []
  for i in bigram_note:
    final_tags.append(bi_word[i]+" "+bi_word[i+1])
  return(final_tags)
'''
  print("Total number of words in the text file: " + str(k))
  print("Calculated Meaningful bigrams: " + str(len(bigram_note)))
  print("The Meaningful Bigrams: ")

  print(final_tags)
  return(final_tags)
'''
  
#for i in bigram_note:
#  print(bi_word[i]+" "+bi_word[i+1])

from flask import Flask, request, render_template
#import spacy
from flask_ngrok import run_with_ngrok

app = Flask(__name__, template_folder= '/content/drive/MyDrive/sharesd/sms-cw_2')
run_with_ngrok(app)

@app.route('/', methods=['GET', 'POST'])
def homepage():
  #return "<h1>GFG is great platform to learn</h1>"
  return render_template('index.html')

@app.route('/pos_tag', methods=['GET', 'POST'])
def pos_tags():
  doc = Meaningful_Bigrams(request.form['text'].strip())
  response = doc
  doc = sim_words_in_dataset_inputtext(request.form['text'].strip(),bi_wordss)
  #tokens = [token.text for token in doc]
  #pos = [token.pos_ for token in doc]      
  #data = listOfTuples(tokens, pos)   
  response.append(doc)
  return render_template('index.html', data=request.form['text'], response=response)

if __name__ == '__main__':
  app.run()
#हिंदी में टायपिंग करना 20वां वर्ष बहुत आसान बना