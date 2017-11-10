import glob
import nltk
import string
from bs4 import BeautifulSoup
from gensim.models import TfidfModel
from gensim import corpora
from collections import Counter

stopwords_ = set(nltk.corpus.stopwords.words('english') + list(string.punctuation))

stop_sub_str = [".", "=", "_"]


def tokenize(text):

    """ Tokenize and filter a text sample. """

    words = nltk.word_tokenize(text.lower())

    words = list(set(words).difference(stopwords_))

    data = []

    for word in words:

        if not any(substring in word for substring in stop_sub_str):

            data.append(word)

    return data


def build_corpus(file_stump, stop_sites):
    tokens = []

    file_list = glob.glob(file_stump + "*")

    for idx, file in enumerate(glob.glob(file_stump + "*")):

        print('Building corpus file %d of %d ...' %(idx, len(file_list)))
        print('File name: %s' %file)

        if not any(substring in file for substring in stop_sites):

            with open(file, 'rb') as f:
                soup = BeautifulSoup(f.read().decode('utf-8', 'ignore'), "lxml")

                data = tokenize(soup.get_text())

                bigrams = list(nltk.bigrams(data))

                bigrams = [bigram[0] + ' ' + bigram[1] for bigram in bigrams]

                data.extend(bigrams)

                tokens.append(data)

    return tokens


def tfidf_processing(docs):
    dictionary = corpora.Dictionary(docs)

    corpus = [dictionary.doc2bow(text) for text in docs]

    tfidf = TfidfModel(corpus)

    corpus_tfidf = tfidf[corpus]

    return corpus_tfidf, dictionary, tfidf


def tfidf_saliency(corpus_tfidf, corpus_dictionary):

    tfidf_saliency = Counter()

    for doc in corpus_tfidf:

        for word, score in doc:
            tfidf_saliency[corpus_dictionary.get(word)] += score / len(corpus_tfidf)

    return tfidf_saliency


if __name__ == "__main__":

    file_stump = "jobs-"

    stop_sites = ['uber', 'facebook']

    corpus =  build_corpus(file_stump, stop_sites)

    corpus_tfidf, corpus_dictionary, tfidf = tfidf_processing(corpus)

    tfidf_saliency = tfidf_saliency(corpus_tfidf, corpus_dictionary)

    term_list = ['data science', 'python', 'hadoop', 'java', 'machine learning', 'data', "c++", "spark"]

    for term in term_list:
        print(tfidf_saliency[corpus_dictionary.get(term)])
        print(term, ': ', tfidf_saliency[term])








