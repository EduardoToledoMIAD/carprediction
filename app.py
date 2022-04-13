import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
import pickle


app= Flask(__name__, template_folder="templates")
#model = pickle.load(open('model.pkl', 'rb'))

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    features = [x for x in request.form.values()]
    print(features)
    return render_template('index.html', id='predict', prediction_text='${}'.format(30))

if __name__ == '__main__':
    app.run()