import os
from flask import Flask, render_template

#Flask instance
app = Flask(__name__)

def load_texts(folder_path):
    texts = []
    for idx, filename in enumerate(os.listdir(folder_path)):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                texts.append({
                    'title': f'Tekst {idx + 1}',
                    'content': f.read()
                })
    return texts

TEXT_FOLDER = 'teksty'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/teksty')
def teksty():
    texts = load_texts(TEXT_FOLDER)
    return render_template('teksty.html', texts=texts)

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