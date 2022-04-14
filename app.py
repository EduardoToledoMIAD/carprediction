import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
from flask_restful import  reqparse
from flask_restful_swagger_3 import Api,Resource,swagger, get_swagger_blueprint
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

api = Api(app, version='5',  title="APP")


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


#@app.route('/api/doc',methods=['GET'])
#def api_documentation():
#     return render_template('documentation.html')

SWAGGER_URL = '/api/doc'  # URL for exposing Swagger UI (without trailing '/')
API_URL = 'swagger.json'  # Our API url (can of course be a local resource)

swagger_blueprint = get_swagger_blueprint(
    api.open_api_object,
    swagger_prefix_url=SWAGGER_URL,
    swagger_url=API_URL)

api.add_resource(CarPrediction, '/api/car-prediction')
app.register_blueprint(swagger_blueprint)
if __name__ == '__main__':
    app.run()