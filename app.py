
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
from flask_restful import   Api,Resource,reqparse
from marshmallow import Schema, fields, validate, ValidationError
import pickle


class CarPredictionSchema(Schema):
    RDSpend = fields.Float(required=True)
    Administration = fields.Float(required=True)
    MarketingSpend = fields.Float(required=True)
    State = fields.Str(required=True)
    
class BatchSchema(Schema):
    batch = fields.List(fields.Nested(CarPredictionSchema))

class CarPrediction(Resource):
    def post(self):
        global model
        data= request.get_json()
        try:
            result =BatchSchema().load(data)
        except ValidationError as err:
            print(err.messages)
            return {err.messages}, 400
    
        df = pd.DataFrame(result['batch'])
        df.rename(columns = {'RDSpend':'R&DSpend'}, inplace = True)
        column_names=['R&DSpend','Administration','MarketingSpend','State']
        predictions= model.predict(df)
        return {'predictions': np.ravel(predictions).tolist()}


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