import pandas as pd
import spacy
from collections import Counter

nlp = spacy.load("en_core_web_sm")

# df = pd.read_csv('../data/collection629.csv')
df = pd.read_csv('../data/combined.csv')

# text = df['text'][0]
words = []
for text in df['text']:

    doc = nlp(text)

    words += [token.text for token in doc if token.is_stop != True and token.is_punct != True]

word_freq = Counter(words)
common_words = word_freq.most_common(20)

for word, count in common_words:
    print(word + ': ' + str(count))