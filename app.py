from apispec import APISpec
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
from flask_restful import Resource, Api, reqparse
import pickle

class CarPrediction(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('price1',
            type=float,
            required=True,
            help="This field cannot be left blank!"
        )
        parser.add_argument('price2',
            type=float,
            required=True,
            help="This field cannot be left blank!"
        )
        data = parser.parse_args()
        item = {'name': 'Hola', 'price':10}
        items.append(item)
        return {'items': items},200





app= Flask(__name__, template_folder="templates")
# Definición API Flask
api = Api(app)

model = pickle.load(open('model.pkl', 'rb'))
items = []

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    features = [x for x in request.form.values()]
    print(features)
    final_features = [np.array(features)]
    column_names=['R&DSpend','Administration','MarketingSpend','State']
    final_features=pd.DataFrame(final_features,columns=column_names)
    prediction= model.predict(final_features)
    temp=0.0
    for i in prediction:
        for j in i:
            temp=j
    return render_template('index.html', id='predict', prediction_text='${}'.format(temp))

@app.route('/api/doc',methods=['GET'])
def api_documentation():
     return render_template('documentation.html')

api.add_resource(CarPrediction, '/api/car-prediction')
if __name__ == '__main__':
    app.run()