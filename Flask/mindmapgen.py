import os
import docx
import spacy
import RAKE
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import PDFPageAggregator
from pdfminer3.converter import TextConverter
import io
from collections import Counter
from string import punctuation
from nltk.corpus import stopwords, wordnet
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

def extract(filepath):
    file_ext = os.path.splitext(filepath)[1]
    if file_ext == '.docx':
        doc = docx.Document(filepath)
        fullText = []
        for para in doc.paragraphs:
            fullText.append(para.text)
        return '\n'.join(fullText)
    if file_ext == '.pdf':
        resource_manager = PDFResourceManager()
        fake_file_handle = io.StringIO()
        converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
        page_interpreter = PDFPageInterpreter(resource_manager, converter)
        with open(filepath, 'rb') as fh:
            for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
                page_interpreter.process_page(page)
            text = fake_file_handle.getvalue()
        converter.close()
        fake_file_handle.close()
        return text
    if file_ext == '.txt':
        myfile = open(filepath, "rt")
        contents = myfile.read() 
        myfile.close()
        return contents

def paras(text):
    p = []
    for line in text.split('\n'):
        if line.count('. ') > 1:
            p.append(line)
    return '\n'.join(p)

def prenlp(string):
    text = ''
    for c in string:
        if c.isalpha() or c == ' ' or c == '\n':
            text += c
        else:
            text += ' '
    paras = text.split('\n')
    output = ""
    filtered_sentence = ""
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    for para in paras:
        output = ' '.join(para.split())
        word_tokens = word_tokenize(output)
        filtered_sentence += ' '.join([lemmatizer.lemmatize(w.lower(), get_wordnet_pos((w))) for w in word_tokens if w.lower() not in stop_words and pos_tag([w])[0][1].upper() != 'PROPN']) + '\n'
    return filtered_sentence

def get_wordnet_pos(word):
    tag = pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ, "N": wordnet.NOUN, "V": wordnet.VERB, "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)

def rake_extraction(text):
    stop_dir = 'StopWords.txt'
    rake_object = RAKE.Rake(stop_dir)
    keywords = Sort_Tuple(rake_object.run(text))[-3:]
    keyphrases = [x[0] for x in keywords]
    return keyphrases

def Sort_Tuple(tup):
    tup.sort(key = lambda x: x[1])
    return tup

def spacy_extraction(text):
    nlp = spacy.load("en_core_web_lg")
    result = []
    pos_tag = ['PROPN', 'ADJ', 'NOUN']
    doc = nlp(text.lower())
    for token in doc:
        if(token.text in nlp.Defaults.stop_words or token.text in punctuation):
            continue
        if(token.pos_ in pos_tag):
            result.append(token.text)
    output = [(x[0]) for x in Counter(result).most_common(5)]
    return output

def keyphrase_extraction(text, keywords):
    d = {}
    for key in keywords:
        d[key] = []
    for line in text.split('\n'):
        freq = {}
        max = 0
        curr = keywords[0]
        for key in keywords:
            occur = line.split().count(key)
            freq[key] = occur
            if occur > max:
                max = occur
                curr = key
        if max != 0:
            d[curr].append(line)
    phrased = {}
    for key in keywords:
        subdoc = '\n'.join(d[key])
        subdoc_rem = ' '.join([w for w in subdoc.split() if w != key])
        phrased[key] = rake_extraction((subdoc_rem))
    return phrased

def nodes(title, d):
    l = {"1": {"id": 1, "label": title}}
    id = 2
    for key in d:
        curr = id
        l[str(curr)] = {"id": curr, "label": key, "parent": 1}
        id += 1
        for phrase in d[key]:
            l[str(id)] = ({"id": id, "label": phrase, "parent": curr})
            id += 1
    return l

doc = extract("smash.pdf")
title = doc.split('\n')[0]
text = prenlp(paras(doc))
keywords = spacy_extraction(text)
phrases = keyphrase_extraction(text, keywords)
print(nodes(title, phrases))