from flask import Flask, render_template
from flask import request
import jsonify
import requests 
import pickle
import numpy as np
import sklearn
from sklearn import tree
from sklearn.preprocessing import StandardScaler


app = Flask(__name__)
model = pickle.load(open('xgb_reg_model.pkl','rb'))
@app.route('/', methods = ['GET','POST'])
def home ():
    return render_template('index.html')


standard_to=StandardScaler()

@app.route('/predict', methods=['POST'])
def predict():
    Fuel_Type_Diesel=0
    if request.method =='POST':
        Year = int(request.form['Year'])
        Present_Price = float(request.form['Present_Price'])
        Kms_Driven = int(request.form['Kms_Driven'])
        Kms_Driven2= np.log(Kms_Driven)
        Owner = int(request.form['Owner'])
        Fuel_Type_Petrol= request.form['Fuel_Type_Petrol']
        if(Fuel_Type_Petrol=='Petrol'):
            Fuel_Type_Petrol=1
            Fuel_Type_Diesel=0
        else:
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=1
        Year = 2020-Year
        Seller_Type_Individual = request.form['Seller_Type_Individual']
        if (Seller_Type_Individual == 'Individual'):
            Seller_Type_Individual=1
        else:
            Seller_Type_Individual=0
        Transmission_Mannual = request.form['Transmission_Mannual']
        if (Transmission_Mannual == 'Manual'):
            Transmission_Mannual=1
        else:
            Transmission_Mannual=0
        prediction=model.predict([[Year,Present_Price,Kms_Driven2,Owner,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Mannual]])
        output = round(prediction[0],2)
        if output < 0:
            return render_template('result.html', prediction_texts="Sorry you cannot sell this Vehicle")
        else:
            return render_template('result.html', prediction_texts="You can sell the Vehicle at {}".format(output) + " " + "Lakhs")
    else:
        return render_template('index.html')        

if __name__=="__main__":
    app.run(debug=True)