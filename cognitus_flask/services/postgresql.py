import psycopg2
import json
from flask import jsonify

def get_data():
    connection = psycopg2.connect(
        user="postgres",
        password="postgres",
        host="db",
        port="5432",
        database="cognitus"
    )
    cursor = connection.cursor()

    sql = '''
    select *
    from data_data
    '''

    cursor.execute(sql)
    data = cursor.fetchall()
    texts = []
    labels = []
    for d in data:
        texts.append(
            d[1]
        )
        labels.append(
            d[2]
        )
    print(texts,labels)
    return texts, labels
