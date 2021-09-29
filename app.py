from flask import Flask, render_template, request
# import jsonify
import pickle
# import numpy as np
import sklearn
import pandas as pd
import gunicorn

app = Flask(__name__)


# Loading the csv
df = pd.read_csv('brand_codes (1).csv')
html_df = df.to_html()

# Loading teh Random Forest Regressor Model
with open('Car_price_Rforest_regressor.pkl', 'rb') as f:
  model = pickle.load(f)

# Home Page
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')



# Skeleton
@app.route("/predict", methods=['POST'])
def predict():
    tipo_combustivel=0

    if request.method == 'POST':
        Ano = int(request.form['Ano'])

        Classe_carro =int(request.form['Classe_carro'])
        if (Classe_carro =='Popular, abaixo de 30 mil'):
            Classe_carro = 1
        elif (Classe_carro =='Intermediário, até 80 mil'):
            Classe_carro = 2
        elif (Classe_carro =='Top de linha, até 200 mil'):
            Classe_carro = 3
        elif (Classe_carro =='Super carros, acima de 201 mil'):
            Classe_carro = 4

        Combustivel =request.form['Combustivel']
        if (Combustivel =='Gasolina'):
            tipo_combustivel = 1
        elif (Combustivel =='Diesel'):
            tipo_combustivel = 0
        elif (Combustivel =='Álcool'):
            tipo_combustivel = 2

        Cambio =request.form['Cambio']
        if(Cambio =='Manual'):
            Cambio = 0
        else:
            Cambio = 1

        Marca = int(request.form['Marca'])

        prediction= model.predict([[Ano,tipo_combustivel, Cambio, Classe_carro, Marca]])
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="O valor do seu carro é {}".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)