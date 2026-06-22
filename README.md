# MobiOferta — CRA WOODCRAFT

Aplicatie desktop (Python + CustomTkinter) pentru calculul costului si
ofertarea mobilierului la comanda.

Introduci piesele unui proiect (placa cu lungime, latime, material, cant pe
laturi, numar de bucati) iar aplicatia calculeaza automat costul de material,
cantul, accesoriile, adaosul de pierdere la debitare si manopera estimativa,
apoi scoate totalul. La final poti exporta o lista de debitat (CSV) si o
oferta pentru client (JSON).

## Functionalitati

- Catalog de materiale pe categorii (PAL melaminat, PAL simplu, MDF simplu /
  melaminat / infoliat si furniruit, Placaj, HDF si PFL) cu preturi reale.
- Pretul se ia pe placa si se transforma automat in lei/m2.
- Cant pe laturi in notatie de tamplarie: L / l / 2L / 2l.
- Accesorii adaugate manual (nume, pret, cantitate) cu lista si stergere.
- Adaos de pierdere (%), factor de manopera si grad de dificultate.
- Editare / stergere piese, salvare proiect in JSON.
- Export cut list CSV (pentru optimizatorul de croit) si oferta JSON.

## Rulare

```bash
pip install -r requirements.txt
python main.py
```

Singura dependinta externa este `customtkinter`.

## Structura

| Fisier | Rol |
|--------|-----|
| `main.py` | porneste aplicatia |
| `gui.py` | interfata (FormularPiesa, TabelPiese, PanouTotal, App) |
| `materiale.py` | clasa abstracta `Material` + subclasele pe categorii |
| `catalog_materiale.py` | citeste catalogul de produse |
| `catalog.json` | catalogul cu preturi reale |
| `piesa.py` | clasa `Piesa` (suprafata, costuri, cant) |
| `accesoriu.py` | clasa `Accesoriu` |
| `proiect.py` | clasa `Proiect` (aduna tot, total, salvare) |
| `export.py` | export CSV + JSON |
| `exceptii.py` | exceptiile personalizate |
| `Preturi/` | capturile cu preturi + Structura.jpg |

## Concepte OOP folosite

Clase si obiecte, mostenire si `super()`, clasa abstracta (`ABC`,
`@abstractmethod`), polimorfism, incapsulare cu `@property` si validare,
`@classmethod` ca factory, `__str__` / `__repr__`, exceptii personalizate,
lucru cu fisiere JSON si CSV.

## Nota despre preturi

Preturile la placi sunt tinute intr-un catalog local (`catalog.json`), cu
valori reale luate de pe site (vezi folderul `Preturi/`). Se schimba rar, deci
un catalog local este o solutie stabila.
