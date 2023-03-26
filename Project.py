# -*- coding: utf-8 -*-
"""Group_08_NLP_Code (1).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1koDPyKTaFd905m8JcVwWb_b0i55wXjrK
"""

# Standard libraries for analysing data
import spacy
import string
import pandas as pd
from collections import Counter
import re

# For visualisation
import matplotlib.pyplot as plt
import seaborn as sns

# For PDF reading
import PyPDF2
import fitz

# For text analysis & NLP
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher
import spacy

# For sentiment analysis
from textblob import TextBlob

# For word cloud creation
from wordcloud import WordCloud

# For topic modelling
from gensim.corpora import Dictionary
from gensim.similarities import MatrixSimilarity
from gensim.models import TfidfModel
from gensim.matutils import corpus2dense
from gensim.corpora import Dictionary
import gensim
import pyLDAvis
import pyLDAvis.gensim_models

"""## Load the Pdf file"""

# Open the PDF file in read-binary mode
with open('budget_speech.pdf', 'rb') as pdf_file:

    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Read the PDF content and display it
    for page in range(len(pdf_reader.pages)):
        text = pdf_reader.pages[page].extract_text()
        print(text)

# Close the PDF file
pdf_file.close()

doc1=fitz.open('budget_speech.pdf')
doc1

"""# Pre-processing of Doc"""

output1 = ""
for page in doc1:
    text=page.get_text()
    output1 =" ".join([output1, text])

text=" ".join(output1.split())

text = text.translate(str.maketrans('', '', string.punctuation))

text=text.replace('•','')

nlp=spacy.load('en_core_web_sm')
doc=nlp(text)

doc = nlp(text)

char_to_remove = ""

new_text = ""
for token in doc:
    if token.text != char_to_remove:
        new_text += token.text + token.whitespace_

"""## Total Number of Words"""

word_count = len(new_text)

# print the word count
print("Word count:", word_count)

"""## Tokenisation"""

text = new_text
doc = nlp(new_text)

# Tokenize the text
tkn = [token.text for token in doc]

stop_count=0
n_stop_count=0
punct_count=0
n_punct_count=0
left_punct_count=0
right_punct_count=0
alpha_count=0
digit_count=0
lower_case_count=0
upper_case_count=0
title_case_count=0
brack_count=0
q_count=0
num_count=0

# Check if the token is a stop word
for token in doc:
    if token.is_stop==True:
        stop_count=stop_count+1
print('\n The count of stop tokens:', stop_count)  

# Check if the token is non-stop words 
for token in doc:
    if token.is_stop==False:
        n_stop_count=n_stop_count+1
print('\n The count of non-stop tokens:', n_stop_count)  

# Check if the token is punctuation
for token in doc:
    if token.is_punct==True:
        punct_count=punct_count+1
print('\n The count of punctuation tokens:', punct_count)

for token in doc:
    if token.is_punct==False:
        n_punct_count=n_punct_count+1
print('\n The count of non-punctuation tokens:', n_punct_count)

for token in doc:
    if token.is_left_punct==True:
        left_punct_count=left_punct_count+1
print('\n The count of left punctuation tokens:', left_punct_count) 

for token in doc:
    if token.is_right_punct==True:
        right_punct_count=right_punct_count+1
print('\n The count of right punctuation tokens:', right_punct_count)

# Check if the token is alphabetic
for token in doc:
    if token.is_alpha==True:
        alpha_count=alpha_count+1
print('\n The count of alphabet-tokens:', alpha_count)

# Check if the token is digit
for token in doc:
    if token.is_digit==True:
        digit_count=digit_count+1
print('\n The count of digit tokens:', digit_count)

for token in doc:
    if token.is_lower==True:
        lower_case_count=lower_case_count+1
print('\n The count of lower case tokens:', lower_case_count)

for token in doc:
    if token.is_upper==True:
        upper_case_count=upper_case_count+1
print('\n The count of upper case tokens:', upper_case_count)

for token in doc:
    if token.is_title==True:
        title_case_count=title_case_count+1
print('\n The count of title case tokens:', title_case_count)

for token in doc:
    if token.is_bracket==True:
        brack_count=brack_count+1
print('\n The count of bracket tokens:', brack_count)

for token in doc:
    if token.is_quote==True:
        q_count=q_count+1
print('\n The count of quote tokens:', q_count)

for token in doc:
    if token.like_num==True:
        num_count=num_count+1
print('\n The count of num tokens:', num_count)

"""## Creating a dataframe"""

# Create a dictionary of the counts for each type of token
token_counts_dict = {'token_name':['stop','non-stop','punct','non-punct', 'left-punct', 'right-punct', 'alpha', 'digit','lower-case', 'upper-case', 'title-case', 'bracket', 'quote', 'number'],
                     'token_counts': [stop_count, n_stop_count, punct_count, n_punct_count, left_punct_count, right_punct_count, alpha_count, digit_count, lower_case_count, upper_case_count, title_case_count, brack_count, q_count, num_count]}
  

# Create a DataFrame from the dictionary
df = pd.DataFrame(token_counts_dict)

# Display the DataFrame
print(df)

"""### Dropping punctuations"""

text = new_text
doc = nlp(new_text)

# Remove punctuation and whitespace tokens
tokens = [token for token in doc if not token.is_punct and not token.is_space]

# Join remaining tokens to form a string without punctuation
clean_text = ' '.join([token.text for token in tokens])

"""### Dropping Numerical tokens and stop words"""

doc = nlp(clean_text)
filtered_text = []
for token in doc:
    if not token.is_stop and not token.is_digit:
        filtered_text.append(token.text)
# join the filtered text
clean_text = " ".join(filtered_text)

print(clean_text)

"""### Dataframe after removal of unwanted elements"""

# Create a Doc object from clean_text
doc = nlp(clean_text)

# Initialize counts
stop_count = 0
n_stop_count = 0
punct_count = 0
n_punct_count = 0
left_punct_count = 0
right_punct_count = 0
alpha_count = 0
digit_count = 0
lower_case_count = 0
upper_case_count = 0
title_case_count = 0
brack_count = 0
q_count = 0
num_count = 0

# Check if the token is a stop word
for token in doc:
    if token.is_stop:
        stop_count += 1
print('The count of stop tokens:', stop_count)

# Check if the token is non-stop words 
for token in doc:
    if not token.is_stop:
        n_stop_count += 1
print('The count of non-stop tokens:', n_stop_count)

# Check if the token is punctuation
for token in doc:
    if token.is_punct:
        punct_count += 1
print('The count of punctuation tokens:', punct_count)

for token in doc:
    if not token.is_punct:
        n_punct_count += 1
print('The count of non-punctuation tokens:', n_punct_count)

for token in doc:
    if token.is_left_punct:
        left_punct_count += 1
print('The count of left punctuation tokens:', left_punct_count) 

for token in doc:
    if token.is_right_punct:
        right_punct_count += 1
print('The count of right punctuation tokens:', right_punct_count)

# Check if the token is alphabetic
for token in doc:
    if token.is_alpha:
        alpha_count += 1
print('The count of alphabet-tokens:', alpha_count)

# Check if the token is digit
for token in doc:
    if token.is_digit:
        digit_count += 1
print('The count of digit tokens:', digit_count)

for token in doc:
    if token.is_lower:
        lower_case_count += 1
print('The count of lower case tokens:', lower_case_count)

for token in doc:
    if token.is_upper:
        upper_case_count += 1
print('The count of upper case tokens:', upper_case_count)

for token in doc:
    if token.is_title:
        title_case_count += 1
print('The count of title case tokens:', title_case_count)

for token in doc:
    if token.is_bracket:
        brack_count += 1
print('The count of bracket tokens:', brack_count)

for token in doc:
    if token.is_quote:
        q_count += 1
print('The count of quote tokens:', q_count)

for token in doc:
    if token.like_num:
        num_count+1
print('\n The count of num tokens:', num_count)

# Create a dictionary of the counts for each type of token
token_counts_dict = {'token_name':['stop','non-stop','punct','non-punct', 'left-punct', 'right-punct', 'alpha', 'digit','lower-case', 'upper-case', 'title-case', 'bracket', 'quote', 'number'],
                     'token_counts': [stop_count, n_stop_count, punct_count, n_punct_count, left_punct_count, right_punct_count, alpha_count, digit_count, lower_case_count, upper_case_count, title_case_count, brack_count, q_count, num_count]}
  

# Create a DataFrame from the dictionary
df = pd.DataFrame(token_counts_dict)

# Display the DataFrame
print(df)

"""## Parts of speech

"""

cols=['Token','POS','Explain_POS','TAG','Explain_TAG']
cols

doc = nlp(' '.join(filtered_text))
rows = []
for token in doc:
    row = token.text, token.pos_, spacy.explain(token.pos_), token.tag_, spacy.explain(token.tag_)
    rows.append(row)
rows

# converting into df

token_df=pd.DataFrame(rows,columns=cols)
token_df

# count of each POS

token_df['POS'].value_counts()

# create a frequency table for POS tags
pos_counts = token_df['POS'].value_counts()

plt.figure(figsize=(8, 6))
plt.bar(pos_counts.index, pos_counts.values, width=0.5)

plt.xlabel('Part of Speech')
plt.ylabel('Frequency')
plt.title('Frequency of Part of Speech Tags')
plt.show()

"""# NER"""

# process the text with the NLP pipeline
doc = nlp(clean_text)

# iterate over the entities detected in the document
for ent in doc.ents:
    print(ent.text, ent.start_char, ent.end_char, ent.label_)

# collect all named entities in a list
ner_list = [ent.text for ent in doc.ents]

# count the frequency of each entity
ner_freq = Counter(ner_list)

# create a word cloud from the most common entities
wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(ner_freq)

# plot the word cloud
plt.figure(figsize=(12, 8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

"""## Named Entity analysis    """

ent_word = []
ent_label = []
for ent in doc.ents:
    ent_word.append(ent.text)
    ent_label.append(ent.label_)
ent_counter = Counter(ent_label)
ent_counter

ent_labels =[key for key, _ in ent_counter.most_common(10)]
ent_count = [value for _, value in ent_counter.most_common(10)]
ent_df = pd.DataFrame(list(zip(ent_labels, ent_count)), columns =['Label', 'Frequency'])
ent_df.set_index('Label')
print(ent_df)

# set the figure size
fig, ax = plt.subplots(figsize=(18, 12))
barchart = sns.barplot(x=ent_df["Label"], y=ent_df["Frequency"], ax=ax)


barchart.bar_label(ax.containers[0], label_type='edge', padding=15);

plt.xlabel('Named Entity')
plt.ylabel('Frequency')
plt.title('Frequency of Named Entity')
plt.show()

ent_word_counter = Counter(ent_word)
ent_labels =[key for key, _ in ent_word_counter.most_common(10)]
ent_count = [value for _, value in ent_word_counter.most_common(10)]
ent_df = pd.DataFrame(list(zip(ent_labels, ent_count)), columns =['Label', 'Frequency'])
ent_df.set_index('Label')
print(ent_df)

# set the figure size
fig, ax = plt.subplots(figsize=(18, 12))
barchart = sns.barplot(x=ent_df["Label"], y=ent_df["Frequency"], ax=ax)


barchart.bar_label(ax.containers[0], label_type='edge', padding=15);

plt.xlabel('Entity')
plt.ylabel('Frequency')
plt.title('Frequency of Entities')
plt.show()

"""# WordCloud"""

# Convert filtered_text to a string
text = ' '.join(filtered_text)

# Generate the word cloud
wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='Spectral', stopwords=None).generate(text)

# Plot the word cloud
plt.figure(figsize=(12,8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

"""# Sentiment Analysis"""

blob = TextBlob(clean_text)

blob.sentiment

"""# Topic Modelling"""

doc = nlp(" ".join(filtered_text))
text_words = []
for token in doc:
    if token.is_stop == False and token.is_punct == False and token.like_num == False and token.text not in ['\n','/','|','•',' ',]:
        text_words.append(token.lemma_)

texts = [text_words]

"""### Creating a corpus"""

corpus = []

dict_1 = Dictionary(texts)

for words in texts:
    corpus.append(dict_1.doc2bow(words))
print(corpus)

"""### Creating an LDA Model"""

lda = gensim.models.ldamodel.LdaModel(corpus=corpus, num_topics=5, id2word=dict_1)

lda.print_topics()

pyLDAvis.enable_notebook()
plot = pyLDAvis.gensim_models.prepare(lda, corpus=corpus, dictionary= lda.id2word)

plot

"""# Entity Matching"""

matcher_1 = Matcher(nlp.vocab)
pattern_1 = [{'ENT_TYPE': 'PERSON'}]
## add pattern to object
matcher_1.add("patter_1_name", [pattern_1])
match_1 = matcher_1(doc)
print(len(match_1))
matched_entity = []
for match_id, start, end in match_1:
    span = doc[start:end]
    matched_entity.append(span)
print(Counter(matched_entity))

"""## Text matching"""

doc = nlp(clean_text)

Central_count = len(re.findall(r'\bcentral\b', doc.text))
State_count = len(re.findall(r'\bstate\b', doc.text))
Education_count = len(re.findall(r'\bEducation\b', doc.text))
Cigarettes_count = len(re.findall(r'\bCigarettes\b', doc.text))
Data_count = len(re.findall(r'\bData\b', doc.text))
Corruption_count = len(re.findall(r'\bCorruption\b', doc.text))
AI_count = len(re.findall(r'\bAI\b', doc.text))


print("Central count:", Central_count)
print("State count:", State_count)
print("Education count:",Education_count)
print("Cigarettes count:",Cigarettes_count)
print("Data count:",Data_count)
print("Corruption count:",Corruption_count)
print("AI count:",AI_count)

"""## Phrase Matching"""

matcher = PhraseMatcher(nlp.vocab)
phrases = ['Artificial Intelligence', 'inclusive development', 'Sustainable Development', 'Girl Child']
patterns = [nlp(text) for text in phrases]
matcher.add('PHRASE_MATCH', None, *patterns)
matches = matcher(doc)
matched_phrases = [doc[start:end].text for _, start, end in matches]
phrase_counts = Counter(matched_phrases)
print(phrase_counts)

"""![image-3.png](attachment:image-3.png)

"""

# Open the PDF file in read-binary mode
with open('Budget_Speech_22.pdf', 'rb') as pdf_file2:

    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfReader(pdf_file2)

    # Read the PDF content and display it
    for page in range(len(pdf_reader.pages)):
        text = pdf_reader.pages[page].extract_text()
        print(text)

# Close the PDF file
pdf_file2.close()

nlp=spacy.load('en_core_web_sm')
type(nlp)
doc2=fitz.open('Budget_Speech_22.pdf')
doc2

output2 = ""
for page in doc2:
    text2=page.get_text()
    output2 =" ".join([output2, text2])

text2=" ".join(output2.split())

text2 = text2.translate(str.maketrans('', '', string.punctuation))

text2=text2.replace('•','')

doc2=nlp(text2)

word_count = len(text2)

# print the word count
print("Word count:", word_count)

# Tokenisation
doc2 = nlp(text2)

# Tokenize the text
tkn2 = [token.text for token in doc2]

doc2 = nlp(doc2)

# Remove punctuation and whitespace tokens
tokens2 = [token for token in doc2 if not token.is_punct and not token.is_space]

# Join remaining tokens to form a string without punctuation
clean_text2 = ' '.join([token.text for token in tokens2])

doc2 = nlp(clean_text2)
filtered_text2 = []
for token in doc2:
    if not token.is_stop and not token.is_digit:
        filtered_text2.append(token.text)
# join the filtered text
clean_text2 = " ".join(filtered_text2)

"""# WordCloud"""

# Generate the word cloud
wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='Spectral', stopwords=None).generate(clean_text2)

# Plot the word cloud
plt.figure(figsize=(12,8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

"""# Word Matching"""

doc2 = nlp(clean_text2)

Central_count = len(re.findall(r'\bcentral\b', doc2.text))
State_count = len(re.findall(r'\bstate\b', doc2.text))
Education_count = len(re.findall(r'\bEducation\b', doc2.text))
Cigarettes_count = len(re.findall(r'\bCigarettes\b', doc2.text))
Data_count = len(re.findall(r'\bData\b', doc2.text))
Corruption_count = len(re.findall(r'\bCorruption\b', doc2.text))
AI_count = len(re.findall(r'\bAI\b', doc2.text))


print("Central count:", Central_count)
print("State count:", State_count)
print("Education count:",Education_count)
print("Cigarettes count:",Cigarettes_count)
print("Data count:",Data_count)
print("Corruption count:",Corruption_count)
print("AI count:",AI_count)

"""# Phrase Matching"""

matcher = PhraseMatcher(nlp.vocab)
phrases = ['Artificial Intelligence', 'inclusive development', 'Sustainable Development', 'Girl Child']
patterns = [nlp(text) for text in phrases]
matcher.add('PHRASE_MATCH', None, *patterns)
matches = matcher(doc2)
matched_phrases = [doc2[start:end].text for _, start, end in matches]
phrase_counts = Counter(matched_phrases)
print(phrase_counts)

"""# Sentiment Analysis"""

blob = TextBlob(clean_text2)

blob.sentiment

"""# Topic Modelling"""

doc2 = nlp(" ".join(filtered_text2))
text_words2 = []
for token in doc2:
    if token.is_stop == False and token.is_punct == False and token.like_num == False and token.text not in ['\n','/','|','•',' ',]:
        text_words.append(token.lemma_)

texts2 = [text_words2]

corpus2 = []
dict_2 = Dictionary(texts)

for words in texts2:
    corpus2.append(dict_2.doc2bow(words))
print(corpus)

lda = gensim.models.ldamodel.LdaModel(corpus=corpus, num_topics=5, id2word=dict_2)
pyLDAvis.enable_notebook()
plot = pyLDAvis.gensim_models.prepare(lda, corpus=corpus, dictionary= lda.id2word)

plot

"""# US Budget Analysis

![image-2.png](attachment:image-2.png)
"""

# Open the PDF file in read-binary mode
with open('US_Budget.pdf', 'rb') as pdf_file3:

    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfReader(pdf_file3)

    # Read the PDF content and display it
    for page in range(len(pdf_reader.pages)):
        text = pdf_reader.pages[page].extract_text()
        print(text)

# Close the PDF file
pdf_file3.close()

nlp=spacy.load('en_core_web_sm')
type(nlp)
doc3=fitz.open('US_Budget.pdf')
doc3

output3 = ""
for page in doc3:
    text3=page.get_text()
    output3 =" ".join([output3, text3])

text3=" ".join(output3.split())

text3 = text3.translate(str.maketrans('', '', string.punctuation))

text3=text3.replace('•','')

doc3=nlp(text3)

word_count = len(text3)

# print the word count
print("Word count:", word_count)

# Tokenisation
nlp = spacy.load('en_core_web_sm')
doc3 = nlp(text3)

# Tokenize the text
tkn3 = [token.text for token in doc3]

nlp = spacy.load('en_core_web_sm')
doc3 = nlp(doc3)

# Remove punctuation and whitespace tokens
tokens3 = [token for token in doc3 if not token.is_punct and not token.is_space]

# Join remaining tokens to form a string without punctuation
clean_text3 = ' '.join([token.text for token in tokens3])

print(clean_text3)

nlp = spacy.load('en_core_web_sm')
doc3 = nlp(clean_text3)
filtered_text3 = []
for token in doc3:
    if not token.is_stop and not token.is_digit:
        filtered_text3.append(token.text)
# join the filtered text
clean_text3 = " ".join(filtered_text3)

print(clean_text3)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Generate the word cloud
wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='Spectral', stopwords=None).generate(clean_text3)

# Plot the word cloud
plt.figure(figsize=(12,8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

"""# Word Matching"""

doc3 = nlp(clean_text3)

Central_count = len(re.findall(r'\bcentral\b', doc3.text))
State_count = len(re.findall(r'\bstate\b', doc3.text))
Education_count = len(re.findall(r'\bEducation\b', doc3.text))
Cigarettes_count = len(re.findall(r'\bCigarettes\b', doc3.text))
Data_count = len(re.findall(r'\bData\b', doc3.text))
Corruption_count = len(re.findall(r'\bCorruption\b', doc3.text))
AI_count = len(re.findall(r'\bAI\b', doc3.text))


print("Central count:", Central_count)
print("State count:", State_count)
print("Education count:",Education_count)
print("Cigarettes count:",Cigarettes_count)
print("Data count:",Data_count)
print("Corruption count:",Corruption_count)
print("AI count:",AI_count)

"""# Phrase Matching"""

matcher = PhraseMatcher(nlp.vocab)
phrases = ['Artificial Intelligence', 'inclusive development', 'Sustainable Development', 'Girl Child']
patterns = [nlp(text) for text in phrases]
matcher.add('PHRASE_MATCH', None, *patterns)
matches = matcher(doc3)
matched_phrases = [doc3[start:end].text for _, start, end in matches]
phrase_counts = Counter(matched_phrases)
print(phrase_counts)

"""# Sentiment Analysis"""

from textblob import TextBlob
blob = TextBlob(clean_text3)
blob.sentiment

"""# Topic Modelling"""

doc3 = nlp(" ".join(filtered_text3))
text_words3 = []
for token in doc3:
    if token.is_stop == False and token.is_punct == False and token.like_num == False and token.text not in ['\n','/','|','•',' ',]:
        text_words.append(token.lemma_)

texts3 = [text_words3]

corpus3 = []
from gensim.corpora import Dictionary
dict_3 = Dictionary(texts)

for words in texts3:
    corpus3.append(dict_3.doc2bow(words))
print(corpus)

lda = gensim.models.ldamodel.LdaModel(corpus=corpus, num_topics=5, id2word=dict_3)
pyLDAvis.enable_notebook()
plot = pyLDAvis.gensim_models.prepare(lda, corpus=corpus, dictionary= lda.id2word)

plot

"""# Vectorisation Similarity

### Similarity between US Budget and India's Budget
"""

# Open the PDF file in read-binary mode
with open('US_Budget.pdf', 'rb') as pdf_file:

    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Read the PDF content and display it
    for page in range(len(pdf_reader.pages)):
        text = pdf_reader.pages[page].extract_text()
        print(text)

# Close the PDF file
pdf_file.close()

doc3=fitz.open('US_Budget.pdf')
output3 = ""
for page in doc3:
    text3=page.get_text()
    output3 =" ".join([output3, text3])
text3=" ".join(output3.split())

text3 = text3.translate(str.maketrans('', '', string.punctuation))

text3=text3.replace('•','')
doc3 = nlp(text3)

text_words_3 = []
for token in doc3:
    if token.is_stop == False and token.is_punct == False and token.like_num == False and token.text not in ['\n','/','|','•',' ',]:
        text_words_3.append(token.lemma_)
texts_2 = [text_words, text_words_3]

corpus_2 = []
dict_2 = Dictionary(texts_2)
for words in texts_2:
    corpus_2.append(dict_2.doc2bow(words))

bow_matrix=corpus2dense(corpus_2,num_terms=len(dict_2))

tfidf=TfidfModel(corpus_2)
tfidf_vec=[]
for vec in corpus_2:
    tfidf_vec.append(tfidf[vec])
print(len(tfidf_vec))

sim=MatrixSimilarity(tfidf_vec,num_features=len(dict_2))

print(sim[tfidf_vec[0]])

print(sim[tfidf_vec[1]])


