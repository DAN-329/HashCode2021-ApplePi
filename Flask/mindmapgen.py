import os
import docx
import PyPDF2
import spacy
import json
import re
'''import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download  ('omw-1.4')'''
from nltk.corpus import stopwords
from nltk import pos_tag
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from rake_nltk import Rake

def extract(filepath):
    file_ext = os.path.splitext(filepath)[1]
    if file_ext == '.docx':
        doc = docx.Document(filepath)
        fullText = []
        for para in doc.paragraphs:
            fullText.append(para.text)
        return '\n'.join(fullText)
    if file_ext == '.pdf':
        pdfFileObj = open(filepath, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
        pageObj = pdfReader.getPage(0)
        text = pageObj.extractText()
        pdfFileObj.close()
        return text
    if file_ext == '.txt':
        myfile = open(filepath, "rt")
        contents = myfile.read() 
        myfile.close()
        return contents

def paras(text):
    p = []
    for para in text.split('\n\n'):
        if para.count('.') > 2:
            p.append(para)
    return '\n\n'.join(p)

def prenlp(string):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(string)
    lemmatizer = WordNetLemmatizer()
    filtered_sentence = ' '.join([lemmatizer.lemmatize(w.lower(), pos=penn2morphy(tag)) for w, tag in pos_tag(word_tokens) if not w.lower() in stop_words])
    return filtered_sentence

def penn2morphy(penntag):
    morphy_tag = {'NN':'n', 'JJ':'a', 'VB':'v', 'RB':'r'}
    try:
        return morphy_tag[penntag[:2]]
    except:
        return 'n' 

def keyword_extraction(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    return doc.ents

def keyword_extraction2(text):
    rake_nltk_var = Rake()
    rake_nltk_var.extract_keywords_from_text(text)
    keyword_extracted = rake_nltk_var.get_ranked_phrases()
    return keyword_extracted

def text_summarization(text):
    stopWords = set(stopwords.words("english"))
    words = word_tokenize(text)
    freqTable = dict()
    for word in words:
        word = word.lower()
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1
    sentences = sent_tokenize(text)
    sentenceValue = dict()
    for sentence in sentences:
        for word, freq in freqTable.items():
            if word in sentence.lower():
                if sentence in sentenceValue:
                    sentenceValue[sentence] += freq
                else:
                    sentenceValue[sentence] = freq
    sumValues = 0
    for sentence in sentenceValue:
        sumValues += sentenceValue[sentence]
    average = int(sumValues / len(sentenceValue))
    summary = ""
    for sentence in sentences:
        if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)):
            summary += " " + sentence
    return summary

text = extract("mitochondria.txt")
title = text.split('\n', 1)[0]
ll = [{"id": 1, "label": "Interests"}]
curr = 1
d = {}
p = paras(text)
prep = prenlp(text)
summary = text_summarization(p)
keywords = keyword_extraction2(summary)
p = p.replace('.\n\n', '. ')
p = p.replace('.\n', '. ')
sentences = p.split('. ')
for sent in sentences:
    for key in keywords[:len(keywords)//3]:
        curr += 1
        if key not in d:
            d[key] = curr
            ll.append({"id": curr, "label": key, "parent": 1})
        if key in sent:
            curr += 1
            ll.append({"id": curr, "label": sent, "parent": d[key]})

print(ll)