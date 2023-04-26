from flask import Flask, render_template, request, Response
app = Flask(__name__)

import pandas as pd
df = pd.read_excel("milano_housing_02_2_23.xlsx", sheet_name='Sheet1')

@app.route('/', methods=['GET'])
def form():
    return render_template('home.html')

@app.route('/quartiere', methods=['GET'])
def quartiere():  
    return render_template('input.html')

@app.route('/risultatoquartiere', methods=['GET'])
def risultatoquartiere():
    inQuartiere = request.args.get('quartiere')
    table = df[df['neighborhood'] == inQuartiere].sort_values(by='date')
    return render_template('risultato.html', table = table.to_html)

@app.route('/elencoset', methods=['GET'])
def elencoset():
    table = df['neighborhood'].tolist()
    table = sorted(list(set(quartieri))[1:])
    return render_template('risultato.html', table = table.to_html )

@app.route('/elencodrop', methods=['GET'])
def elencodrop():
    table = df.sort_values(by='neighborhood').drop_duplicates(subset='neighborhood')['neighborhood']
    return render_template('risultato.html', table = table.to_html())

@app.route('/prezzo', methods=['GET'])
def prezzo():  
    return render_template('input2.html')

@app.route('/risultatoprezzo', methods=['GET'])
def risultatoprezzo():
    inQuartiere = request.args.get('quartiere')
    serieQuartiere = df[df['neighborhood'] == inQuartiere]['price'].values
    return render_template('risultato.html', dato = int(serieQuartiere.sum()) // len(serieQuartiere))

@app.route('/prezzi', methods=['GET'])
def prezzi():
    prezziQuartieri = df.groupby('neighborhood').sum()['price']
    numeroPrezzi = df.groupby('neighborhood').count()['price']
    prezziQuartieri['media'] = prezziQuartieri // numeroPrezzi
    return render_template('risultato.html',  table = prezziQuartieri['media'].to_html() )

@app.route('/prezziremake', methods=['GET'])
def prezziremake():
    return render_template('input3.html')
    
@app.route('/risultatoprezziremake', methods=['GET'])
def risultatoprezziremake():
    def conversione(prezzo=1, tasso=1):
        return prezzo * tasso
    tassodiConversione = request.args.get('tassoconversione')
    tassodiConversione = float(tassodiConversione)
    prezziQuartieri['mediaConvertito'] = conversione(prezziQuartieri['media'], tassodiConversione)
    return render_template('risultato.html',  table = prezziQuartieri['mediaConvertito'].to_html() )
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=32245, debug=True)