import os
import re
from clp3 import CLP
from collections import defaultdict

def load_texts(folder_path):
    texts_war = []  # Teksty o wojnie zimowej
    texts_non_war = []  # Teksty nie o wojnie zimowej

    for idx, filename in enumerate(os.listdir(folder_path)):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                # Rozdzielamy teksty na dwie grupy na podstawie nazwy pliku
                if "wojna_zimowa" in filename.lower():  # Teksty o wojnie zimowej
                    texts_war.append({
                        'title': f'Tekst {idx + 1} (Wojna Zimowa)',
                        'content': f.read().lower()
                    })
                else:  # Pozostałe teksty
                    texts_non_war.append({
                        'title': f'Tekst {idx + 1} (Inne)',
                        'content': f.read().lower()
                    })

    return texts_war, texts_non_war


def bform(clp_instance, slowo):
    try:
        ids = clp_instance.rec(slowo)
        if ids:
            return clp_instance.bform(ids[0])
    except Exception as e:
        print(f"Nie udało się przetworzyć słowa '{slowo}': {e}")
    return slowo

def is_pronoun(clp_instance, word):
    """Sprawdza, czy słowo jest słowem 'być', nieodmiennym lub zaimkiem na podstawie etykiety CLP."""

    word_bform = bform(clp_instance, word)
    if word_bform == 'być':
        return True
    try:
        ids = clp_instance.rec(word)
        if ids:
            for id in ids:
                label = clp_instance.label(id)
                if label.startswith("E") or label.startswith("G"):  # "E" to typ zaimka
                    return True
    except Exception as e:
        print(f"Nie udało się sprawdzić etykiety słowa '{word}': {e}")
    return False

def generate_frekwencja(folder, tekst_type='war'):
    clp_instance = CLP()
    word_count = defaultdict(int)

    # Ładowanie tekstów z folderu, uwzględniając typ tekstów (wojenne lub inne)
    if tekst_type == 'war':
        teksty_war, _ = load_texts(folder)
        teksty = teksty_war
    else:
        _, teksty_non_war = load_texts(folder)
        teksty = teksty_non_war

    for tekst in teksty:
        content = tekst['content']
        # Usuwanie znaków specjalnych i liczb
        content = re.sub(r'[^\w\s]|[\d_]', ' ', content)
        words = content.split()

        for word in words:
            if word.isdigit() or any(char.isdigit() for char in word):
                continue  # Pomijamy cyfry lub słowa zawierające cyfry
            if is_pronoun(clp_instance, word):
                continue
            base_form = bform(clp_instance, word)
            word_count[base_form] += 1

    sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
    return sorted_words




