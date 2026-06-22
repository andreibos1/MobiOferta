from materiale import Material
from exceptii import DimensiuneInvalidaError

PRET_CANT_ML = 3.5  # lei/metru liniar implicit


class Piesa:
    # cant_lungime = cate laturi lungi au cant (0/1/2 -> "L"/"2L")
    # cant_latime  = cate laturi scurte au cant (0/1/2 -> "l"/"2l")
    def __init__(
        self,
        nume: str,
        lungime: float,
        latime: float,
        material: Material,
        cant_lungime: int = 0,
        cant_latime: int = 0,
        pret_cant_ml: float = PRET_CANT_ML,
        cantitate: int = 1,
    ):
        if lungime <= 0 or latime <= 0:
            raise DimensiuneInvalidaError("Lungimea si latimea trebuie sa fie pozitive.")
        if cantitate < 1:
            raise ValueError("Cantitatea trebuie sa fie cel putin 1.")
        self._nume = nume
        self._lungime = lungime      # mm
        self._latime = latime        # mm
        self._material = material
        self._cant_lungime = max(0, min(2, int(cant_lungime)))
        self._cant_latime = max(0, min(2, int(cant_latime)))
        self._pret_cant_ml = pret_cant_ml
        self._cantitate = cantitate

    @property
    def nume(self):
        return self._nume

    @property
    def lungime(self):
        return self._lungime

    @property
    def latime(self):
        return self._latime

    @property
    def material(self):
        return self._material

    @property
    def cant_lungime(self):
        return self._cant_lungime

    @property
    def cant_latime(self):
        return self._cant_latime

    @property
    def pret_cant_ml(self):
        return self._pret_cant_ml

    @property
    def cantitate(self):
        return self._cantitate

    def eticheta_cant(self):
        # cantul scris ca L / l / 2L / 2l
        parti = []
        if self._cant_lungime:
            parti.append("L" if self._cant_lungime == 1 else "2L")
        if self._cant_latime:
            parti.append("l" if self._cant_latime == 1 else "2l")
        return " ".join(parti) if parti else "-"

    # --- suprafata si costuri per BUCATA ---

    @property
    def suprafata_mp_unitar(self) -> float:
        return (self._lungime / 1000) * (self._latime / 1000)

    @property
    def cost_material_unitar(self) -> float:
        return self.suprafata_mp_unitar * self._material.cost_mp()

    @property
    def metri_cant_unitar(self) -> float:
        return (
            self._cant_lungime * (self._lungime / 1000)
            + self._cant_latime * (self._latime / 1000)
        )

    @property
    def cost_cant_unitar(self) -> float:
        return self.metri_cant_unitar * self._pret_cant_ml

    @property
    def cost_total_unitar(self) -> float:
        return self.cost_material_unitar + self.cost_cant_unitar

    # --- totale pe TOATE bucatile ---

    @property
    def suprafata_mp(self) -> float:
        return self.suprafata_mp_unitar * self._cantitate

    @property
    def cost_material(self) -> float:
        return self.cost_material_unitar * self._cantitate

    @property
    def cost_cant(self) -> float:
        return self.cost_cant_unitar * self._cantitate

    @property
    def cost_total(self) -> float:
        return self.cost_total_unitar * self._cantitate

    def to_dict(self) -> dict:
        return {
            "nume": self._nume,
            "lungime": self._lungime,
            "latime": self._latime,
            "grosime": self._material.grosime,
            "categorie": self._material.categorie,
            "material": self._material.nume,
            "pret_mp": self._material.pret_mp,
            "cant_lungime": self._cant_lungime,
            "cant_latime": self._cant_latime,
            "pret_cant_ml": self._pret_cant_ml,
            "cantitate": self._cantitate,
        }

    def __str__(self):
        return (
            f"{self._nume} | {self._cantitate} buc | {self._lungime}x{self._latime}mm | "
            f"{self._material.nume} | cant {self.eticheta_cant()} | "
            f"Supraf. totala: {self.suprafata_mp:.4f} m2 | "
            f"Cost material: {self.cost_material:.2f} lei | "
            f"Cost cant: {self.cost_cant:.2f} lei | "
            f"TOTAL: {self.cost_total:.2f} lei"
        )

    def __repr__(self):
        return (
            f"Piesa(nume={self._nume!r}, lungime={self._lungime}, "
            f"latime={self._latime}, cantitate={self._cantitate}, material={self._material!r})"
        )
