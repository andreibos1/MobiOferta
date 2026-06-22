import json
import os
from materiale import Material

CALE_CATALOG = os.path.join(os.path.dirname(__file__), "catalog.json")


class CatalogMateriale:
    # citeste catalog.json si da materialele grupate pe categorii (sursa de preturi)
    def __init__(self, cale=CALE_CATALOG):
        self._cale = cale
        self._produse = self._incarca()

    def _incarca(self):
        with open(self._cale, "r", encoding="utf-8") as f:
            date = json.load(f)
        return date.get("produse", [])

    def categorii(self):
        # categoriile in ordinea din catalog (adica ordinea din Structura)
        ordine = []
        for p in self._produse:
            if p["categorie"] not in ordine:
                ordine.append(p["categorie"])
        return ordine

    def produse(self, categorie):
        return [p for p in self._produse if p["categorie"] == categorie]

    def nume_produse(self, categorie):
        return [p["nume"] for p in self.produse(categorie)]

    def gaseste(self, categorie, nume):
        for p in self._produse:
            if p["categorie"] == categorie and p["nume"] == nume:
                return p
        return None

    def material(self, categorie, nume):
        intrare = self.gaseste(categorie, nume)
        if intrare is None:
            raise KeyError(f"Produs negasit in catalog: {categorie} / {nume}")
        return Material.din_catalog(intrare)
