import os
from tfidf import oblicz_tfidf
from frekwencja import generate_frekwencja
from flask import Flask, render_template, request

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


def paginate(items, page, per_page=10):
    start = (page - 1) * per_page
    end = start + per_page
    return items[start:end]

@app.route('/tfidf')
def tfidf():
    folder_tekstów = "teksty"
    wzorzec_pliku = r"(tekst_aei_\d+|wojna_zimowa_\d+)\.txt"
    wyniki_tfidf = oblicz_tfidf(folder_tekstów, wzorzec_pliku)

    page = request.args.get('page', default=1, type=int)
    per_page = 10
    total_pages = (len(wyniki_tfidf) + per_page - 1) // per_page

    paginated_tfidf = paginate(wyniki_tfidf, page, per_page)

    return render_template('tfidf.html',
                           wyniki_tfidf=paginated_tfidf,
                           page=page, total_pages=total_pages)


@app.route('/lista_frekwencyjna')
def lista_frekwencyjna():
    folder_tekstów = "teksty"

    # Pobieranie typu tekstów z parametrów URL, domyślnie 'war' (wojna zimowa)
    tekst_type = request.args.get('type', default='war', type=str)
    wyniki_frekwencji = generate_frekwencja(folder_tekstów, tekst_type)

    page = request.args.get('page', default=1, type=int)
    per_page = 10
    total_pages = (len(wyniki_frekwencji) + per_page - 1) // per_page

    paginated_frekwencja = paginate(wyniki_frekwencji, page, per_page)

    return render_template('lista_frekwencyjna.html',
                           wyniki_frekwencji=enumerate(paginated_frekwencja, start=1),
                           page=page, total_pages=total_pages, tekst_type=tekst_type)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12121, debug=True)