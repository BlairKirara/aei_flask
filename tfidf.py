import os
import re
import math
from collections import Counter, defaultdict

def wczytaj_teksty(folder, wzorzec):
    teksty = {}
    for nazwa_pliku in os.listdir(folder):
        if re.match(wzorzec, nazwa_pliku):
            ścieżka = os.path.join(folder, nazwa_pliku)
            with open(ścieżka, encoding="utf-8") as plik:
                teksty[nazwa_pliku] = plik.read().lower()
    return teksty

def licz_tf(tekst):
    słowa = re.findall(r'\b[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ]+\b', tekst)
    liczba_słów = len(słowa)
    licznik_słów = Counter(słowa)
    return {słowo: licznik / liczba_słów for słowo, licznik in licznik_słów.items()}

def licz_idf(korpus):
    dokumenty_z_słowem = defaultdict(int)
    liczba_dokumentów = len(korpus)

    for tekst in korpus.values():
        unikalne_słowa = set(re.findall(r'\b[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ]+\b', tekst))
        for słowo in unikalne_słowa:
            dokumenty_z_słowem[słowo] += 1
    return {słowo: math.log(liczba_dokumentów / dokumenty) for słowo, dokumenty in dokumenty_z_słowem.items()}

def licz_tfidf(tf, idf):
    return {słowo: tf[słowo] * idf[słowo] for słowo in tf}

def znajdź_top_słowa(tfidf, liczba=10):
    return sorted(tfidf.items(), key=lambda x: x[1], reverse=True)[:liczba]

def oblicz_tfidf(folder_tekstów, wzorzec_pliku, top_n=10):
    korpus = wczytaj_teksty(folder_tekstów, wzorzec_pliku)
    idf_korpus = licz_idf(korpus)
    wyniki = []

    for nazwa, treść in korpus.items():
        tf = licz_tf(treść)
        tfidf = licz_tfidf(tf, idf_korpus)
        top_słowa = znajdź_top_słowa(tfidf, liczba=top_n)
        wyniki.append({'nazwa': nazwa, 'top_słowa': top_słowa})
    return wyniki