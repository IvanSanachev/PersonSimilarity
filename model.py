import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
from tqdm import tqdm
import datetime
from nltk.tokenize import TweetTokenizer
tokenizer = TweetTokenizer()
from pymorphy3 import MorphAnalyzer
analyzer = MorphAnalyzer()
import re
import gensim
import logging
import pandas as pd
import urllib.request
from gensim.models import word2vec
data = pd.read_csv('lenta.csv')
data = data.dropna()
import spacy
nlp = spacy.load("ru_core_news_lg")
sents = []
srn = []
for el in tqdm(range(len(data))):
    tx = data.iloc[el]['text']
    dtx = nlp(tx)
    surnames = []
    names = []
    per = [[ent.text.split(' '), ent.start, ent.end] for ent in dtx.ents if ent.label_ == "PER"]
    for x, y, z in per:
        srn.append(analyzer.normal_forms(str(dtx[z - 1]))[0])
        surnames.append(dtx[z - 1])
        for i in range(y, z - 1):
            names.append(dtx[i])
    punc = ['.', "'", '"', '-', '+', ',', ':', ';', '?', '!', ' ']
    for snt in dtx.sents:
        sent = []
        st = snt.start
        for i in range(len(snt)):
            # if dtx[i + st] in surnames:
            #     sent.append(analyzer.normal_forms(str(dtx[i + st]))[-1])
            if dtx[i + st] not in names and str(dtx[i + st]) not in punc:
                sent.append(analyzer.normal_forms(str(dtx[i + st]))[0])
        sents.append(sent)
srn = set(srn)
model = gensim.models.Word2Vec(sents, vector_size=300, window=5, min_count=2, workers=2)
model.save("model.vec")
with open("srn.txt", "w") as file:
    file.write(",".join(srn))
