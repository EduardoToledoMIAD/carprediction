
from base64 import encode
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
from flask_restful import   Api,Resource,reqparse
from marshmallow import Schema, fields, validate, ValidationError
import pickle
import models
from models.schemas import BatchSchema
import category_encoders as ce
import joblib
import traceback

class CarPrediction(Resource):
    def _features_selection(self, df:pd.DataFrame):
        features=['Year', 'Mileage', 'Make', 'Model', 'State']
        df= df[features]
        return df

    def _encoder(self, json):
        global encoder
        df = pd.DataFrame(json)
        df= encoder.transform(df)
        return df
    
    def post(self):
        global model
        data= request.get_json()
        try:
            result =BatchSchema().load(data)
            df=self._encoder(result['batch'])
            df= self._features_selection(df)
            predictions= model.predict(df)
            return {'predictions': np.ravel(predictions).tolist()},200
          
        except ValidationError as err:
            print(err.messages)
            return err.messages, 400
        except Exception as e:
            traceback.print_exc()
            return traceback.print_exc(),500
       
    
app= Flask(__name__, template_folder="templates")
# Definición API Flask

api = Api(app)

model = joblib.load('model.pkl')
encoder =  joblib.load('catboost_encoder.pkl')

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    global model
    global encoder
    
    try:
        features = [x for x in request.form.values()]
        print(features)
        final_features = [np.array(features)]
        column_names=['Year','Mileage','Make','Model','State']
        df=pd.DataFrame(final_features,columns=column_names)
        df= encoder.transform(df)
        selected_features=['Year', 'Mileage', 'Make', 'Model', 'State']
        df= df[selected_features]
        prediction= list(model.predict(df))
        temp=0.0
        for i in prediction:
            temp=i
        return render_template('index.html', id='predict', prediction_text='${}'.format(temp))
    except Exception as e:
        return render_template('index.html', id='predict', prediction_text='${}'.format("EXECUTION ERROR "))        

 
@app.route('/api/doc',methods=['GET'])
def api_documentation():
     return render_template('documentation.html')


api.add_resource(CarPrediction, '/api/car-prediction')
if __name__ == '__main__':
    app.run()