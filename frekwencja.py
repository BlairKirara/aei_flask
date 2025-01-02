import os
import re
from clp3 import CLP
from collections import defaultdict

def load_texts(folder_path):
    texts = []
    for idx, filename in enumerate(os.listdir(folder_path)):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                texts.append({
                    'title': f'Tekst {idx + 1}',
                    'content': f.read().lower()
                })
    return texts

def bform(clp_instance, slowo):
    try:
        ids = clp_instance.rec(slowo)
        if ids:
            return clp_instance.bform(ids[0])
    except Exception as e:
        print(f"Nie udało się przetworzyć słowa '{slowo}': {e}")
    return slowo

def generate_frekwencja(folder):
    clp_instance = CLP()
    word_count = defaultdict(int)

    teksty = load_texts(folder)

    for tekst in teksty:
        content = tekst['content']
        content = re.sub(r'[^\w\s]', ' ', content)  # Wszystko, co nie jest literą lub cyfrą
        words = content.split()

        for word in words:
            base_form = bform(clp_instance, word)
            word_count[base_form] += 1

    sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
    return sorted_words

