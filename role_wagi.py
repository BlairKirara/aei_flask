ROLES = {
    "nic": 0,
    "sprawca": 0.15,
    "narzędzie": 0.1,
    "obiekt": 0.1,
    "miejsce": 0.1,
    "zdarzenie": 0.15,
    "cel": 0.15,

    ("sprawca", "narzędzie"): 0.25,
    ("sprawca", "obiekt"): 0.2,
    ("sprawca", "miejsce"): 0.25,
    ("sprawca", "zdarzenie"): 0.35,
    ("sprawca", "cel"): 0.35,

    ("narzędzie", "obiekt"): 0.2,
    ("narzędzie", "miejsce"): 0.2,
    ("narzędzie", "zdarzenie"): 0.25,
    ("narzędzie", "cel"): 0.25,

    ("obiekt", "miejsce"): 0.2,
    ("obiekt", "zdarzenie"): 0.25,
    ("obiekt", "cel"): 0.25,

    ("miejsce", "zdarzenie"): 0.25,
    ("miejsce", "cel"): 0.25,

    ("zdarzenie", "cel"): 0.35,

    ("sprawca", "narzędzie", "obiekt"): 0.4,
    ("sprawca", "narzędzie", "miejsce"): 0.45,
    ("sprawca", "narzędzie", "zdarzenie"): 0.5,
    ("sprawca", "narzędzie", "cel"): 0.5,

    ("sprawca", "obiekt", "miejsce"): 0.45,
    ("sprawca", "obiekt", "zdarzenie"): 0.5,
    ("sprawca", "obiekt", "cel"): 0.5,

    ("sprawca", "miejsce", "zdarzenie"): 0.5,
    ("sprawca", "miejsce", "cel"): 0.5,

    ("sprawca", "zdarzenie", "cel"): 0.55,

    ("narzędzie", "obiekt", "miejsce"): 0.4,
    ("narzędzie", "obiekt", "zdarzenie"): 0.45,
    ("narzędzie", "obiekt", "cel"): 0.45,

    ("narzędzie", "miejsce", "zdarzenie"): 0.45,
    ("narzędzie", "miejsce", "cel"): 0.45,

    ("narzędzie", "zdarzenie", "cel"): 0.5,

    ("obiekt", "miejsce", "zdarzenie"): 0.45,
    ("obiekt", "miejsce", "cel"): 0.45,

    ("obiekt", "zdarzenie", "cel"): 0.5,

    ("miejsce", "zdarzenie", "cel"): 0.5,

    ("sprawca", "narzędzie", "obiekt", "miejsce"): 0.6,
    ("sprawca", "narzędzie", "obiekt", "zdarzenie"): 0.7,
    ("sprawca", "narzędzie", "obiekt", "cel"): 0.7,

    ("sprawca", "narzędzie", "miejsce", "zdarzenie"): 0.7,
    ("sprawca", "narzędzie", "miejsce", "cel"): 0.7,

    ("sprawca", "narzędzie", "zdarzenie", "cel"): 0.75,

    ("sprawca", "obiekt", "miejsce", "zdarzenie"): 0.7,
    ("sprawca", "obiekt", "miejsce", "cel"): 0.7,

    ("sprawca", "obiekt", "zdarzenie", "cel"): 0.75,

    ("sprawca", "miejsce", "zdarzenie", "cel"): 0.75,

    ("narzędzie", "obiekt", "miejsce", "zdarzenie"): 0.6,
    ("narzędzie", "obiekt", "miejsce", "cel"): 0.6,

    ("narzędzie", "obiekt", "zdarzenie", "cel"): 0.7,

    ("narzędzie", "miejsce", "zdarzenie", "cel"): 0.7,

    ("obiekt", "miejsce", "zdarzenie", "cel"): 0.7,

    ("sprawca", "narzędzie", "obiekt", "miejsce", "zdarzenie"): 0.85,
    ("sprawca", "narzędzie", "obiekt", "miejsce", "cel"): 0.85,

    ("sprawca", "narzędzie", "obiekt", "zdarzenie", "cel"): 0.95,

    ("sprawca", "narzędzie", "miejsce", "zdarzenie", "cel"): 1,

    ("sprawca", "obiekt", "miejsce", "zdarzenie", "cel"): 0.95,

    ("narzędzie", "obiekt", "miejsce", "zdarzenie", "cel"): 0.85,

    ("narzędzie", "obiekt", "miejsce", "zdarzenie", "cel", "sprawca"): 1
}

# wersja z niektórymi istotnymi nazwami własnymi, kótre były wysoko, z wyjątkiem "wojna" i "zimowy"
# WORDS= {
#     "sprawca": ["Finowie", "ZSRR", "armia", "żołnierz"],
#     "narzędzie": ["siła", "czołg", "atak"],
#     "obiekt": ["fiński", "radziecki", "sowiecki", "czerwony"],
#     "miejsce": ["Finlandia", "linia", "kraj"],
#     "zdarzenie": ["walka", "bitwa", "strata"],
#     "cel": ["zostać", "mieć", "móc", "obrona"]
# }

#wybrane słowa z czołówki z pominięciem wszystkich nazw własnych (sowiecki, radziecki, finladnia, finowie, zsrr, sowieci, stalin)
# WORDS= {
#     "sprawca": ["armia", "żołnierz", "dywizja", "wojsko"],
#     "narzędzie": ["siła", "czołg", "atak"],
#     "obiekt": ["czerwony", "dzień", "lata", "czas"],
#     "miejsce": ["linia", "kraj", "granica"],
#     "zdarzenie": ["walka", "bitwa", "strata"],
#     "cel": ["zostać", "mieć", "móc", "obrona"]
# }

# wybrane słowa bliższe tematowi z top 100 słów, bez nazw własnych
WORDS= {
    "sprawca": ["żołnierz", "wojsko", "armia", "dywizja", "pułk", "oddział", "rząd"],
    "narzędzie": ["siła", "pozycja", "warunek"],
    "obiekt": ["jezioro", "linia", "czołg", "wojskowy"],
    "miejsce": ["kraj", "granica", "terytorium", "przesmyk"],
    "zdarzenie": ["walka", "konflikt", "bitwa", "strata"],
    "cel": ["obrona", "zwycięstwo", "atak"]
}