import os
from tfidf import oblicz_tfidf
from frekwencja import generate_frekwencja
from flask import Flask, render_template, request
from collections import defaultdict
from role_wagi import ROLES, WORDS

#Flask instance
app = Flask(__name__)

def analyze_roles_in_text(content):
    """Analizuje tekst i zwraca role oraz związane z nimi słowa."""
    roles_found = defaultdict(list)
    for role, words in WORDS.items():
        for word in words:
            if word in content:
                roles_found[role].append(word)
    return roles_found

def highlight_text(content, roles_found):
    """Podkreśla znalezione słowa w treści tekstu za pomocą znaczników <span>."""
    for role, words in roles_found.items():
        for word in words:
            # Dodanie znacznika <span> z klasą dla roli
            highlighted_word = f'<span class="{role}">{word}</span>'
            content = content.replace(word, highlighted_word)
    return content


def calculate_roles_weight(roles_found):
    """Oblicza wagę na podstawie unikalnych znalezionych ról."""
    # Pobieramy unikalne role jako posortowaną krotkę
    unique_roles = tuple(sorted(roles_found.keys()))

    # Przechodzimy przez klucze w ROLES, aby sprawdzić, czy są takie same
    for key in ROLES:
        if set(key) == set(unique_roles):  # Porównujemy zbiory ról
            return ROLES[key]

    # Jeśli nie znaleziono, zwracamy domyślną wartość
    return "Brak przypisanej wagi"


def load_texts(folder_path, sort_order="desc", sort_by="weight"):
    texts = []
    for idx, filename in enumerate(os.listdir(folder_path)):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                roles_in_text = analyze_roles_in_text(content)
                highlighted_content = highlight_text(content, roles_in_text)
                weight = calculate_roles_weight(roles_in_text)

                # Jeśli brak wagi, przypisz domyślną wartość (np. 0)
                numeric_weight = weight if isinstance(weight, (int, float)) else 0

                texts.append({
                    'title': f'Tekst {idx + 1}',
                    'content': highlighted_content,
                    'roles': roles_in_text,
                    'weight': numeric_weight,  # Używamy liczbowej wagi
                    'weight_display': weight  # Oryginalna waga do wyświetlania
                })

    # Sortowanie tekstów
    reverse = True if sort_order == "desc" else False

    if sort_by == "title":
        # Sortowanie po nazwie tekstu
        texts.sort(key=lambda x: x['title'].lower(), reverse=reverse)
    else:
        # Sortowanie po wadze
        texts.sort(key=lambda x: x['weight'], reverse=reverse)

    return texts

TEXT_FOLDER = 'teksty'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/teksty')
def teksty():
    # Pobieranie parametrów sort_order (domyślnie malejąco) i sort_by (domyślnie po wadze)
    sort_order = request.args.get('sort', 'desc')
    sort_by = request.args.get('by', 'weight')

    texts = load_texts(TEXT_FOLDER, sort_order=sort_order, sort_by=sort_by)
    return render_template('teksty.html', texts=texts, sort_order=sort_order, sort_by=sort_by)

@app.route('/formularz')
def formularz():
    return render_template('formularz.html', roles=ROLES, words=WORDS)

@app.route('/wagi')
def wagi():
    # Przekazujemy słownik ROLES, który zawiera wagi ról i ich kombinacji
    return render_template('wagi.html', roles_weights=ROLES)



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