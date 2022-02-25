import glob,codecs,sys,os,re,csv,math
from nltk.stem.porter import *
import numpy as np

# 6.3.1 Preprocessing
stopwords = codecs.open("stopwords.txt", 'r', encoding='Latin1').read()
li = re.split(r'\W+', stopwords)
for i in range(len(li)):
    li[i] = re.sub(r'[^a-z]', '', li[i].lower()).strip()

stemmer = PorterStemmer ()
d = []
datasets = os.listdir("dataset")
for document in datasets:
    for filename in os.listdir('dataset/'+document):
        path = "dataset/" + document + '/' +  filename
        dataset = codecs.open(path, 'r', encoding='Latin1').read() # read every file
        p = re.split(r'[^a-z]', dataset) # split the document text into words
        for i in range(len(p)-1,-1,-1):
            p[i] = re.sub(r'[^a-z]', '', p[i].lower()).strip() # lower case. Delete non-alphabet characters
            if p[i] in li or (p[i] == ''):
                del p[i] # Remove the stopwords
        p = [stemmer.stem(word) for word in p] # remove the word suffix
        d.append(p)

# 6.3.2 TFIDF Representation
N = len(d) # N: the number of documents in the dataset
n = dict()
f_list = []
for x in d:
    xx = set(x)
    for word in xx:
        if word not in n:
            n[word]=1
        else:
            n[word]+=1 # n[k]: the total number of times word k occurs in the dataset called the document frequency.
for i in d:
    f = dict()
    a = dict()
    A = dict()
    list = []
    sum = 0
    for word in n.keys():
        f[word] = i.count(word) # f[i][k]: the frequency of word k in document i
        a[word] = f[word] * math.log(N / n[word])  # a[i][k] = f[i][k] ∗ log(N/n[k])
        sum += a[word]*a[word]
    for word in n.keys():
        A[word] = a[word]/math.sqrt(sum) # normalize the representation of the document as A[i][k]
        list.append(A[word])
    f_list.append(list)
Aik = np.mat(f_list) # A = (a[i][k]) where a[i][k] is the weight of word k in document i.

np.savez('train-20ng.npz',X=Aik ) # the dataset is save into .npz file


