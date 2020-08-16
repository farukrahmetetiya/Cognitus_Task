from flask import Flask
from flask import request
from services.postgresql import get_data

from flask import Blueprint
from services.train import train

train_api = Blueprint('train_api', __name__)


@train_api.route('/train/')
def Train():
    texts, labels= get_data()
    # 2. train servisine git bu datayı ona ver.
    # 3. kullanıcıya status start traning dön.
    if texts and labels and len(texts) > 3:
        t = train.apply_async(args=[texts, labels])
    else:
        return 'Lütfen Train için veri ekleyin'
    # burda gelen datayı veya databaseden okunan datayı yapay zekada işleme sokup egitim yapılcak
    return 'OKEY'

