class Accesoriu:
    # feronerie sau orice extra adaugat manual: nume, pret pe bucata, cantitate
    def __init__(self, nume, pret_bucata, cantitate=1):
        self._nume = nume
        self._pret_bucata = pret_bucata
        self._cantitate = cantitate

    @property
    def nume(self):
        return self._nume

    @property
    def pret_bucata(self):
        return self._pret_bucata

    @property
    def cantitate(self):
        return self._cantitate

    @cantitate.setter
    def cantitate(self, val):
        if val < 0:
            raise ValueError("Cantitatea nu poate fi negativa.")
        self._cantitate = val

    @property
    def cost_total(self):
        return self._pret_bucata * self._cantitate

    def to_dict(self):
        return {
            "nume": self._nume,
            "pret_bucata": self._pret_bucata,
            "cantitate": self._cantitate,
        }

    @classmethod
    def din_dict(cls, date):
        return cls(date["nume"], date["pret_bucata"], date.get("cantitate", 1))

    def __str__(self):
        return f"{self._nume}: {self._cantitate} x {self._pret_bucata:.2f} = {self.cost_total:.2f} lei"

    def __repr__(self):
        return f"Accesoriu({self._nume!r}, {self._pret_bucata}, {self._cantitate})"
