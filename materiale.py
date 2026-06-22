from abc import ABC, abstractmethod
from exceptii import GrosimeInvalidaError, MaterialIndisponibilError


class Material(ABC):
    # clasa de baza pentru placi. pretul de lucru e in lei/m2.
    # categoriile (subclasele) urmaresc arborele din magazin / Structura.jpg
    CATEGORIE = "Material"

    def __init__(self, nume, grosime, pret_mp):
        if grosime <= 0:
            raise GrosimeInvalidaError(f"Grosimea {grosime}mm nu este valida (trebuie > 0).")
        if pret_mp <= 0:
            raise MaterialIndisponibilError("Pretul pe m2 trebuie sa fie pozitiv.")
        self._nume = nume
        self._grosime = grosime
        self._pret_mp = pret_mp

    @property
    def nume(self):
        return self._nume

    @property
    def categorie(self):
        return self.CATEGORIE

    @property
    def grosime(self):
        return self._grosime

    @property
    def pret_mp(self):
        return self._pret_mp

    @pret_mp.setter
    def pret_mp(self, valoare):
        if valoare <= 0:
            raise MaterialIndisponibilError("Pretul trebuie sa fie pozitiv.")
        self._pret_mp = valoare

    @abstractmethod
    def cost_mp(self):
        pass

    @classmethod
    def din_catalog(cls, intrare):
        # pretul din catalog e pe PLACA; il facem lei/m2 cu dimensiunile placii
        klass = CATEGORII.get(intrare["categorie"])
        if klass is None:
            raise MaterialIndisponibilError(f"Categorie necunoscuta: {intrare['categorie']}")
        suprafata_placa = (intrare["lungime_placa"] / 1000) * (intrare["latime_placa"] / 1000)
        pret_mp = round(intrare["pret_placa"] / suprafata_placa, 2)
        return klass(intrare["nume"], intrare["grosime"], pret_mp)

    @classmethod
    def din_piesa_dict(cls, date):
        # reface materialul cand incarcam un proiect salvat
        klass = CATEGORII.get(date.get("categorie"), PALMelaminat)
        return klass(date.get("material", "Material"), date["grosime"], date.get("pret_mp", 1.0))

    def __str__(self):
        return f"{self._nume} ({self.CATEGORIE}) {self._grosime}mm - {self.cost_mp():.2f} lei/m2"

    def __repr__(self):
        return f"{self.__class__.__name__}(nume={self._nume!r}, grosime={self._grosime}, pret_mp={self._pret_mp})"


class PALMelaminat(Material):
    CATEGORIE = "PAL melaminat"

    def cost_mp(self):
        return self._pret_mp


class PALSimplu(Material):
    CATEGORIE = "PAL simplu"

    def cost_mp(self):
        return self._pret_mp


class MDFSimplu(Material):
    CATEGORIE = "MDF simplu"

    def cost_mp(self):
        return self._pret_mp


class MDFMelaminat(Material):
    CATEGORIE = "MDF melaminat"

    def cost_mp(self):
        return self._pret_mp


class MDFInfoliat(Material):
    CATEGORIE = "MDF infoliat si furniruit"

    def cost_mp(self):
        return self._pret_mp


class Placaj(Material):
    CATEGORIE = "Placaj"

    def cost_mp(self):
        return self._pret_mp


class HDFPFL(Material):
    CATEGORIE = "HDF si PFL"

    def cost_mp(self):
        return self._pret_mp


CATEGORII = {
    PALMelaminat.CATEGORIE: PALMelaminat,
    PALSimplu.CATEGORIE: PALSimplu,
    MDFSimplu.CATEGORIE: MDFSimplu,
    MDFMelaminat.CATEGORIE: MDFMelaminat,
    MDFInfoliat.CATEGORIE: MDFInfoliat,
    Placaj.CATEGORIE: Placaj,
    HDFPFL.CATEGORIE: HDFPFL,
}
