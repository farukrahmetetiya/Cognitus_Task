import pickle
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import precision_score, accuracy_score, recall_score
from sklearn.model_selection import train_test_split
from flask import Blueprint
from celery import Celery

celery = Celery(broker='redis://redis:6379/0')

def tfidf(data, ma=0.6, mi=0.0001):
    tfidf_vectorize = TfidfVectorizer()
    tfidf_data = tfidf_vectorize.fit_transform(data)
    return tfidf_data, tfidf_vectorize


def train_SVM(x_train, x_test, y_train, y_test):
    SVM = SVC(kernel='linear')
    SVMClassifier = SVM.fit(x_train, y_train)
    return SVMClassifier


def dump_model(model, file_output):
    pickle.dump(model, open(file_output, 'wb'))


@celery.task(name='train.train_celery')
def train(text, label):
    training, vectorizer = tfidf(text)
    x_train, x_test, y_train, y_test = train_test_split(
        training, label, test_size=0.25, random_state=0
    )
    model = train_SVM(
        x_train, x_test, y_train, y_test
    )
    dump_model(model, 'model.pickle')
    dump_model(vectorizer, 'vectorizer.pickle')

