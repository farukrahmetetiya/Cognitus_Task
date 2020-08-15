import pickle

def load_model(file_input):
    return pickle.load(open(file_input, 'rb'))


def predict(text):
    model = load_model('model.pickle')
    vectorizer = load_model('vectorizer.pickle')
    user_text = text
    if model and vectorizer:
        result = model.predict(vectorizer.transform([user_text]))
    else:
        return 'Önce Train işlemini yapmalısınız'
    return result[0]
