import json
import os
from datetime import datetime
from piesa import Piesa
from accesoriu import Accesoriu
from materiale import Material


class Proiect:
    def __init__(self, nume: str, procent_pierdere: float = 10.0,
                 factor_manopera: float = 1.0, grad_dificultate: float = 1.0):
        self._nume = nume
        self._procent_pierdere = procent_pierdere  # % adaos la costul materialelor
        self._factor_manopera = factor_manopera    # x pe costul materialelor
        self._grad_dificultate = grad_dificultate  # x suplimentar pentru dificultate
        self._piese: list[Piesa] = []
        self._accesorii: list[Accesoriu] = []
        self._creat_la = datetime.now().isoformat()

    @property
    def nume(self):
        return self._nume

    @nume.setter
    def nume(self, val: str):
        self._nume = (val or "").strip() or "Proiect nou"

    @property
    def procent_pierdere(self):
        return self._procent_pierdere

    @procent_pierdere.setter
    def procent_pierdere(self, val: float):
        if not (0 <= val <= 100):
            raise ValueError("Procentul de pierdere trebuie sa fie intre 0 si 100.")
        self._procent_pierdere = val

    @property
    def factor_manopera(self):
        return self._factor_manopera

    @factor_manopera.setter
    def factor_manopera(self, val: float):
        if val < 0:
            raise ValueError("Factorul de manopera nu poate fi negativ.")
        self._factor_manopera = val

    @property
    def grad_dificultate(self):
        return self._grad_dificultate

    @grad_dificultate.setter
    def grad_dificultate(self, val: float):
        if val < 0:
            raise ValueError("Gradul de dificultate nu poate fi negativ.")
        self._grad_dificultate = val

    @property
    def piese(self):
        return list(self._piese)

    @property
    def accesorii(self):
        return list(self._accesorii)

    def adauga_piesa(self, piesa: Piesa):
        self._piese.append(piesa)

    def sterge_piesa(self, index: int):
        if 0 <= index < len(self._piese):
            self._piese.pop(index)

    def adauga_accesoriu(self, accesoriu: Accesoriu):
        self._accesorii.append(accesoriu)

    def sterge_accesoriu(self, index: int):
        if 0 <= index < len(self._accesorii):
            self._accesorii.pop(index)

    @property
    def suprafata_totala_mp(self) -> float:
        return sum(p.suprafata_mp for p in self._piese)

    @property
    def cost_materiale(self) -> float:
        return sum(p.cost_material for p in self._piese)

    @property
    def cost_cant(self) -> float:
        return sum(p.cost_cant for p in self._piese)

    @property
    def cost_accesorii(self) -> float:
        return sum(a.cost_total for a in self._accesorii)

    @property
    def adaos_pierdere(self) -> float:
        # procentul de pierdere la debitare, aplicat pe costul materialelor
        return (self._procent_pierdere / 100) * self.cost_materiale

    @property
    def manopera_estimativa(self) -> float:
        # manopera = cost materiale x factor manopera x grad dificultate
        return self.cost_materiale * self._factor_manopera * self._grad_dificultate

    @property
    def total(self) -> float:
        return (
            self.cost_materiale
            + self.cost_cant
            + self.cost_accesorii
            + self.adaos_pierdere
            + self.manopera_estimativa
        )

    def sumar(self) -> str:
        linii = [
            f"Proiect: {self._nume}",
            f"  Piese: {len(self._piese)}",
            f"  Suprafata totala: {self.suprafata_totala_mp:.4f} m2",
            f"  Cost materiale:   {self.cost_materiale:.2f} lei",
            f"  Cost cant:        {self.cost_cant:.2f} lei",
            f"  Cost accesorii:   {self.cost_accesorii:.2f} lei",
            f"  Adaos pierdere ({self._procent_pierdere}%): {self.adaos_pierdere:.2f} lei",
            f"  Manopera (x{self._factor_manopera} x{self._grad_dificultate}): {self.manopera_estimativa:.2f} lei",
            f"  TOTAL:            {self.total:.2f} lei",
        ]
        return "\n".join(linii)

    def to_dict(self) -> dict:
        return {
            "nume": self._nume,
            "procent_pierdere": self._procent_pierdere,
            "factor_manopera": self._factor_manopera,
            "grad_dificultate": self._grad_dificultate,
            "creat_la": self._creat_la,
            "piese": [p.to_dict() for p in self._piese],
            "accesorii": [a.to_dict() for a in self._accesorii],
        }

    def salveaza(self, cale: str = "proiecte.json"):
        date = []
        if os.path.exists(cale):
            with open(cale, "r", encoding="utf-8") as f:
                date = json.load(f)
        # actualizeaza daca exista, altfel adauga
        for i, p in enumerate(date):
            if p["nume"] == self._nume:
                date[i] = self.to_dict()
                break
        else:
            date.append(self.to_dict())
        with open(cale, "w", encoding="utf-8") as f:
            json.dump(date, f, ensure_ascii=False, indent=2)

    @staticmethod
    def _cant_din_dict(pd: dict):
        # cantul unei piese salvate (accepta si formatul vechi cu laturi_cant)
        if "cant_lungime" in pd or "cant_latime" in pd:
            return pd.get("cant_lungime", 0), pd.get("cant_latime", 0)
        laturi = pd.get("laturi_cant", [])
        cant_lungime = sum(1 for l in laturi if l in ("stanga", "dreapta"))
        cant_latime = sum(1 for l in laturi if l in ("sus", "jos"))
        return cant_lungime, cant_latime

    @classmethod
    def din_json(cls, date: dict):
        proiect = cls(
            nume=date["nume"],
            procent_pierdere=date.get("procent_pierdere", 10.0),
            factor_manopera=date.get("factor_manopera", 1.0),
            grad_dificultate=date.get("grad_dificultate", 1.0),
        )
        for pd in date.get("piese", []):
            mat = Material.din_piesa_dict(pd)
            cant_lungime, cant_latime = cls._cant_din_dict(pd)
            piesa = Piesa(
                nume=pd["nume"],
                lungime=pd["lungime"],
                latime=pd["latime"],
                material=mat,
                cant_lungime=cant_lungime,
                cant_latime=cant_latime,
                pret_cant_ml=pd.get("pret_cant_ml", 3.5),
                cantitate=pd.get("cantitate", 1),
            )
            proiect.adauga_piesa(piesa)
        for ad in date.get("accesorii", []):
            proiect.adauga_accesoriu(Accesoriu.din_dict(ad))
        return proiect
