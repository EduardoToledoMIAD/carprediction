
from base64 import encode
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
from flask_restful import   Api,Resource,reqparse
from marshmallow import Schema, fields, validate, ValidationError
import pickle
import models
from models.schemas import BatchSchema, Batch1Schema
import category_encoders as ce
import joblib
import traceback






class CarPrediction(Resource):
    def _features_selection(self, df:pd.DataFrame):
        features=['Year', 'Mileage', 'Make_3', 'Model_2', 'Model_1', 'Make_5', 'Model_6', 'Model_7', 'Model_8', 'State_4', 'Make_2', 'Model_3', 'Model_4', 'Model_5']
        df= df[features]
        return df

    def _encoder(self, json):
        global encoder
        df = pd.DataFrame(json)
        df= encoder.transform(df)
        return df
    def post(self):
        global model_extra
        data= request.get_json()
        try:
            result =BatchSchema().load(data)
            df=self._encoder(result['batch'])
            df= self._features_selection(df)
            predictions= model_extra.predict(df)
            return {'predictions': np.ravel(predictions).tolist()},200
          
        except ValidationError as err:
            print(err.messages)
            return err.messages, 400
        except Exception as e:
            traceback.print_exc()
            return traceback.print_exc(),500
       
    def xxx(self):
        global model
        data= request.get_json()
        try:
            result =Batch1Schema().load(data)
        except ValidationError as err:
            print(err.messages)
            return err.messages, 400
    
        df = pd.DataFrame(result['batch'])
        df.rename(columns = {'RDSpend':'R&DSpend'}, inplace = True)
        column_names=['R&DSpend','Administration','MarketingSpend','State']
        predictions= model.predict(df)
        return {'predictions': np.ravel(predictions).tolist()},200


app= Flask(__name__, template_folder="templates")
# Definición API Flask

api = Api(app)


model = pickle.load(open('model.pkl', 'rb'))
model_extra = joblib.load('model_extra.pkl')
encoder =  joblib.load('binary_encoder.pkl')

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