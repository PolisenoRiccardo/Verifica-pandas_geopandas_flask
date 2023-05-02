from flask import Flask, render_template, request, Response
app = Flask(__name__)

import pandas as pd
df = pd.read_excel("milano_housing_02_2_23.xlsx")
df = df.dropna(subset='neighborhood')

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/quartiere', methods=['GET'])
def quartiere():  
    return render_template('input1.html')

@app.route('/risultatoquartiere', methods=['GET'])
def risultatoquartiere():
    inQuartiere = request.args.get('quartiere')
    table = df[df['neighborhood'] == inQuartiere].sort_values(by='date')
    return render_template('risultato.html', table = table.to_html())

@app.route('/elencoset', methods=['GET'])
def elencoset():
    table = df['neighborhood'].tolist()
    table = sorted(list(set(table)))
    return render_template('risultato.html', table = table)

quartieri = sorted(list(set(df.dropna(subset='neighborhood')['neighborhood'].tolist())))

@app.route('/elencodrop', methods=['GET'])
def elencodrop():
    table = quartieri
    return render_template('risultato.html', table = table.tolist())

@app.route('/prezzo', methods=['GET'])
def prezzo():  
    return render_template('input2.html', quartieri = quartieri)

@app.route('/risultatoprezzo', methods=['GET'])
def risultatoprezzo():
    inQuartiere = request.args.get('quartiere')
    serieQuartiere = df[df['neighborhood'] == inQuartiere]['price'].mean()
    return render_template('risultatodato.html', dato = round(serieQuartiere))

prezziQuartieri = df.groupby('neighborhood')[['price']].mean().sort_values(by='price', ascending=False)

@app.route('/prezzi', methods=['GET'])
def prezzi(): 
    return render_template('risultato.html',  table = prezziQuartieri.to_html() )

@app.route('/prezziremake', methods=['GET'])
def prezziremake():
    return render_template('input3.html')

@app.route('/risultatoprezziremake', methods=['GET'])
def risultatoprezziremake():
    def conversione(prezzo=1, tasso=1):
        return prezzo * tasso
    tassodiConversione = request.args.get('tassoconversione')
    tassodiConversione = float(tassodiConversione)
    prezziQuartieri['mediaConvertito'] = conversione(prezziQuartieri['price'], tassodiConversione)
    return render_template('risultato.html',  table = prezziQuartieri.to_html() )
    
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=32245, debug=True)