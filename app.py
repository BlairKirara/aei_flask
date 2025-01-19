import os
import re
import html
from clp3 import clp
from tfidf import oblicz_tfidf
from frekwencja import generate_frekwencja
from flask import Flask, render_template, request
from collections import defaultdict
from role_wagi import ROLES, WORDS

#Flask instance
app = Flask(__name__)


def truncate_to_word(content, max_length=200, suffix="..."):
    """
    Truncates the content to max_length characters but extends to the end of the current word.
    Adds suffix at the end of the truncated text.
    """
    if len(content) <= max_length:
        return content

    # Find the last space within max_length
    truncated = content[:max_length + 1]
    last_space = truncated.rfind(' ')

    if last_space != -1:
        truncated = truncated[:last_space]

    return truncated + suffix


def analyze_roles_in_text(content):
    """Analizuje tekst i zwraca role oraz związane z nimi słowa bazowe, używając CLP do dopasowania form."""
    roles_found = defaultdict(lambda: {'base': set(), 'all_forms': set()})
    words_in_text = content.split()

    for word in words_in_text:
        # Check if the word has any known ID (base form included)
        ids = clp(word)
        for id in ids:
            base = clp[id]  # Get base form directly
            for role, base_words in WORDS.items():
                if base in base_words:
                    roles_found[role]['base'].add(base)
                    roles_found[role]['all_forms'].add(word)
                    break  # We found the role for this base form, move to next word

    return {role: {'base': list(forms['base']), 'all_forms': list(forms['all_forms'])}
            for role, forms in roles_found.items()}

def highlight_text(content, roles_found):
    """Podkreśla wszystkie znalezione formy słów w treści tekstu."""
    for role, forms in roles_found.items():
        for word in forms['all_forms']:
            escaped_word = re.escape(word)
            pattern = r'\b' + escaped_word + r'\b'
            highlighted_word = f'<span class="{role}">{html.escape(word)}</span>'
            content = re.sub(pattern, highlighted_word, content, flags=re.IGNORECASE)
    return content


def calculate_roles_weight(roles_found):
    """Oblicza wagę na podstawie znalezionych ról, biorąc pod uwagę wszystkie kombinacje."""
    # Pobieramy unikalne role jako posortowaną krotkę
    unique_roles = tuple(sorted(roles_found.keys()))

    max_weight = 0
    for key in ROLES:
        if isinstance(key, tuple):  # Jeśli klucz to krotka (kombinacja ról)
            if set(key).issubset(set(unique_roles)):  # Sprawdza, czy wszystkie role z klucza są w znalezionych rolach
                max_weight = max(max_weight, ROLES[key])
        elif key in unique_roles:  # Sprawdzenie, czy pojedyncza rola jest w znalezionych rolach
            max_weight = max(max_weight, ROLES[key])

    # Jeśli nie znaleziono żadnych ról, przypisujemy wagę "nic"
    if not roles_found:
        return ROLES["nic"]

    # Zwracamy najwyższą wagę, jaką znaleziono
    return max_weight if max_weight > 0 else "Brak przypisanej wagi"


def load_texts(folder_path, sort_order="desc", sort_by="weight"):
    texts = []
    for idx, filename in enumerate(os.listdir(folder_path)):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                roles_in_text = analyze_roles_in_text(content)
                highlighted_content = highlight_text(content, roles_in_text)

                # Truncate and highlight the short version
                truncated_content = truncate_to_word(content, max_length=200)
                truncated_highlighted_content = highlight_text(truncated_content, roles_in_text)

                weight = calculate_roles_weight(roles_in_text)

                # Używamy numeru z nazwy pliku do generowania tytułu
                match = re.search(r'(\w+)_(\w+)_(\d+)\.txt', filename)
                if match:
                    theme, _, number = match.groups()
                    if theme == "wojna":
                        title = f"Tekst wojna zimowa {number}"
                    else:
                        title = f"Zwykły tekst {number}"
                else:
                    title = f"Tekst {idx + 1}"  # Domyślna nazwa, gdyby coś poszło nie tak

                # Jeśli brak wagi, przypisz domyślną wartość (np. 0)
                numeric_weight = weight if isinstance(weight, (int, float)) else 0

                # Only send base forms to template
                roles_for_display = {role: forms['base'] for role, forms in roles_in_text.items()}

                texts.append({
                    'title': title,
                    'content': html.escape(content),  # Cały tekst kodowany na encje HTML
                    'highlighted_content': highlighted_content,  # Full highlighted content
                    'truncated_highlighted_content': truncated_highlighted_content,
                    'roles': roles_for_display,  # Only base forms for listing
                    'weight': numeric_weight,
                    'weight_display': weight
                })

    # Sortowanie tekstów
    reverse = True if sort_order == "desc" else False

    if sort_by == "title":
        # Sortowanie po nazwie tekstu - najpierw po typie, potem po numerze
        texts.sort(key=lambda x: (x['title'].split()[0], int(re.search(r'\d+$', x['title']).group())), reverse=reverse)
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