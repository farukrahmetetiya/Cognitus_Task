from flask import Flask
from flask import request
from services.postgresql import get_data
from flask import Blueprint

from services.predict import predict as pre

# from utils.celery import train_celery


predict_api = Blueprint('predict_api', __name__)


@predict_api.route('/prediction', methods=['POST', 'GET'])
def Prediction():
    # burda gelen text i işleme sokup return label dönücek yapaydan çıkan
    text = request.form.get('text')
    predict_label = pre(text)
    print('predict_label', predict_label)
    return {'label': predict_label}


# @predict_api.route('/celery/')
# def a():
#     # burda gelen text i işleme sokup return label dönücek yapaydan çıkan
#     task = train_celery.apply_async(args=[1, 2])
#     print('asdf', task)
#     return 'task'
