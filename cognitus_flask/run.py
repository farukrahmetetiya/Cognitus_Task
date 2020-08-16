from celery import Celery
from flask import Flask
from api.train import train_api
from api.predict import predict_api

app = Flask(__name__)

app.register_blueprint(train_api)
app.register_blueprint(predict_api)

@app.route("/")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    app.run(host="0.0.0.0")
