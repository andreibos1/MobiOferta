import csv
import json
from datetime import datetime
from proiect import Proiect


class Exportator:
    def __init__(self, proiect: Proiect):
        self._proiect = proiect

    def export_cut_list_csv(self, cale: str = None) -> str:
        if cale is None:
            cale = f"cut_list_{self._proiect.nume}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(cale, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(["Nume piesa", "Buc.", "Lungime (mm)", "Latime (mm)", "Grosime (mm)", "Material", "Cant"])
            for piesa in self._proiect.piese:
                writer.writerow([
                    piesa.nume,
                    piesa.cantitate,
                    piesa.lungime,
                    piesa.latime,
                    piesa.material.grosime,
                    piesa.material.nume,
                    piesa.eticheta_cant(),
                ])
        return cale

    def export_oferta_json(self, cale: str = None) -> str:
        if cale is None:
            cale = f"oferta_{self._proiect.nume}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        oferta = {
            "proiect": self._proiect.nume,
            "data": datetime.now().isoformat(),
            "sumar": {
                "suprafata_totala_m2": round(self._proiect.suprafata_totala_mp, 4),
                "cost_materiale": round(self._proiect.cost_materiale, 2),
                "cost_cant": round(self._proiect.cost_cant, 2),
                "cost_accesorii": round(self._proiect.cost_accesorii, 2),
                "adaos_pierdere": round(self._proiect.adaos_pierdere, 2),
                "factor_manopera": self._proiect.factor_manopera,
                "grad_dificultate": self._proiect.grad_dificultate,
                "manopera_estimativa": round(self._proiect.manopera_estimativa, 2),
                "total": round(self._proiect.total, 2),
            },
            "piese": [p.to_dict() for p in self._proiect.piese],
            "accesorii": [a.to_dict() for a in self._proiect.accesorii],
        }
        with open(cale, "w", encoding="utf-8") as f:
            json.dump(oferta, f, ensure_ascii=False, indent=2)
        return cale
