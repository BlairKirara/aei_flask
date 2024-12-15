from flask import Flask, render_template

#Flask instance
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/teksty')
def teksty():
    return render_template('teksty.html')

@app.route('/formularz')
def formularz():
    return render_template('formularz.html')

@app.route('/tabela_wag')
def wagi():
    return render_template('wagi.html')

@app.route('/lista_frekwencyjna')
def frekwencja():
    return render_template('frekwencja.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12121, debug=True)