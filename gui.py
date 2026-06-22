import customtkinter as ctk
from tkinter import messagebox, filedialog
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from piesa import Piesa
from accesoriu import Accesoriu
from proiect import Proiect
from export import Exportator
from catalog_materiale import CatalogMateriale
from exceptii import GrosimeInvalidaError, DimensiuneInvalidaError, MaterialIndisponibilError

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

MARCA = "CRA WOODCRAFT"
CULOARE_MARCA = "#C8A165"

# cantul se da in notatie de tamplarie: L/l = o latura, 2L/2l = ambele laturi
CANT_LUNGIME = {"fara": 0, "L": 1, "2L": 2}
CANT_LATIME = {"fara": 0, "l": 1, "2l": 2}
CANT_LUNGIME_INV = {v: k for k, v in CANT_LUNGIME.items()}
CANT_LATIME_INV = {v: k for k, v in CANT_LATIME.items()}


class FormularPiesa(ctk.CTkFrame):
    def __init__(self, master, callback_adauga, catalog, **kwargs):
        super().__init__(master, **kwargs)
        self._callback = callback_adauga
        self._catalog = catalog
        self._var_cant_lungime = ctk.StringVar(value="fara")
        self._var_cant_latime = ctk.StringVar(value="fara")
        self._construieste()

    def _construieste(self):
        ctk.CTkLabel(self, text="Adauga piesa", font=ctk.CTkFont(size=14, weight="bold")).grid(
            row=0, column=0, columnspan=2, pady=(10, 6), padx=10
        )

        for text, row in [("Nume piesa", 1), ("Nr. bucati", 2), ("Lungime (mm)", 3),
                          ("Latime (mm)", 4), ("Categorie", 5), ("Material", 6)]:
            ctk.CTkLabel(self, text=text).grid(row=row, column=0, padx=10, pady=3, sticky="w")

        self._intrari = {}

        self._intrari["Nume piesa"] = ctk.CTkEntry(self, width=220)
        self._intrari["Nume piesa"].grid(row=1, column=1, padx=10, pady=3, sticky="w")

        self._intrari["Nr. bucati"] = ctk.CTkEntry(self, width=60)
        self._intrari["Nr. bucati"].insert(0, "1")
        self._intrari["Nr. bucati"].grid(row=2, column=1, padx=10, pady=3, sticky="w")

        self._intrari["Lungime (mm)"] = ctk.CTkEntry(self, width=100)
        self._intrari["Lungime (mm)"].grid(row=3, column=1, padx=10, pady=3, sticky="w")

        self._intrari["Latime (mm)"] = ctk.CTkEntry(self, width=100)
        self._intrari["Latime (mm)"].grid(row=4, column=1, padx=10, pady=3, sticky="w")

        categorii = self._catalog.categorii()
        self._var_categorie = ctk.StringVar(value=categorii[0])
        ctk.CTkOptionMenu(self, values=categorii, variable=self._var_categorie,
                          width=220, command=self._on_categorie).grid(row=5, column=1, padx=10, pady=3, sticky="w")

        self._var_produs = ctk.StringVar()
        self._menu_produs = ctk.CTkOptionMenu(self, values=[""], variable=self._var_produs,
                                              width=220, command=self._on_produs)
        self._menu_produs.grid(row=6, column=1, padx=10, pady=3, sticky="w")

        ctk.CTkLabel(self, text="Pret material (lei/m2)").grid(row=7, column=0, padx=10, pady=3, sticky="w")
        self._intrari["Pret material (lei/m2)"] = ctk.CTkEntry(self, width=100)
        self._intrari["Pret material (lei/m2)"].grid(row=7, column=1, padx=10, pady=3, sticky="w")

        ctk.CTkLabel(self, text="Pret cant (lei/ml)").grid(row=8, column=0, padx=10, pady=3, sticky="w")
        self._intrari["Pret cant (lei/ml)"] = ctk.CTkEntry(self, width=100)
        self._intrari["Pret cant (lei/ml)"].insert(0, "3.5")
        self._intrari["Pret cant (lei/ml)"].grid(row=8, column=1, padx=10, pady=3, sticky="w")

        ctk.CTkLabel(self, text="Cant laturi lungi (L):").grid(row=9, column=0, padx=10, pady=3, sticky="w")
        ctk.CTkOptionMenu(self, values=list(CANT_LUNGIME.keys()),
                          variable=self._var_cant_lungime, width=100).grid(row=9, column=1, padx=10, pady=3, sticky="w")

        ctk.CTkLabel(self, text="Cant laturi scurte (l):").grid(row=10, column=0, padx=10, pady=3, sticky="w")
        ctk.CTkOptionMenu(self, values=list(CANT_LATIME.keys()),
                          variable=self._var_cant_latime, width=100).grid(row=10, column=1, padx=10, pady=3, sticky="w")

        ctk.CTkButton(self, text="+ Adauga piesa", command=self._adauga).grid(
            row=11, column=0, columnspan=2, pady=10, padx=10
        )

        self._on_categorie(self._var_categorie.get())

    def _seteaza_pret_material(self, valoare):
        camp = self._intrari["Pret material (lei/m2)"]
        camp.delete(0, "end")
        camp.insert(0, f"{valoare:.2f}")

    def _on_categorie(self, categorie):
        produse = self._catalog.nume_produse(categorie)
        self._menu_produs.configure(values=produse)
        if produse:
            self._var_produs.set(produse[0])
            self._on_produs(produse[0])

    def _on_produs(self, nume):
        if not nume:
            return
        material = self._catalog.material(self._var_categorie.get(), nume)
        self._seteaza_pret_material(material.pret_mp)

    def _adauga(self):
        try:
            nume = self._intrari["Nume piesa"].get().strip()
            if not nume:
                raise ValueError("Numele piesei nu poate fi gol.")
            cantitate = int(self._intrari["Nr. bucati"].get())
            if cantitate < 1:
                raise ValueError("Numarul de bucati trebuie sa fie cel putin 1.")
            lungime = float(self._intrari["Lungime (mm)"].get().replace(",", "."))
            latime = float(self._intrari["Latime (mm)"].get().replace(",", "."))
            pret_cant = float(self._intrari["Pret cant (lei/ml)"].get().replace(",", "."))

            material = self._catalog.material(self._var_categorie.get(), self._var_produs.get())
            pret_txt = self._intrari["Pret material (lei/m2)"].get().strip().replace(",", ".")
            if pret_txt:
                material.pret_mp = float(pret_txt)

            cant_lungime = CANT_LUNGIME[self._var_cant_lungime.get()]
            cant_latime = CANT_LATIME[self._var_cant_latime.get()]
            piesa = Piesa(nume, lungime, latime, material,
                          cant_lungime, cant_latime, pret_cant, cantitate)
            self._callback(piesa)
            self._reseteaza()
        except (ValueError, GrosimeInvalidaError, DimensiuneInvalidaError, MaterialIndisponibilError, KeyError) as e:
            messagebox.showerror("Eroare", str(e))

    def incarca_piesa(self, piesa):
        # folosit la editare: pune valorile piesei inapoi in formular
        self._intrari["Nume piesa"].delete(0, "end")
        self._intrari["Nume piesa"].insert(0, piesa.nume)
        self._intrari["Nr. bucati"].delete(0, "end")
        self._intrari["Nr. bucati"].insert(0, str(piesa.cantitate))
        self._intrari["Lungime (mm)"].delete(0, "end")
        self._intrari["Lungime (mm)"].insert(0, str(piesa.lungime))
        self._intrari["Latime (mm)"].delete(0, "end")
        self._intrari["Latime (mm)"].insert(0, str(piesa.latime))

        categorie = piesa.material.categorie
        self._var_categorie.set(categorie)
        self._menu_produs.configure(values=self._catalog.nume_produse(categorie))
        self._var_produs.set(piesa.material.nume)
        self._seteaza_pret_material(piesa.material.pret_mp)

        self._intrari["Pret cant (lei/ml)"].delete(0, "end")
        self._intrari["Pret cant (lei/ml)"].insert(0, str(piesa.pret_cant_ml))
        self._var_cant_lungime.set(CANT_LUNGIME_INV[piesa.cant_lungime])
        self._var_cant_latime.set(CANT_LATIME_INV[piesa.cant_latime])

    def _reseteaza(self):
        self._intrari["Nume piesa"].delete(0, "end")
        self._intrari["Nr. bucati"].delete(0, "end")
        self._intrari["Nr. bucati"].insert(0, "1")
        self._intrari["Lungime (mm)"].delete(0, "end")
        self._intrari["Latime (mm)"].delete(0, "end")
        self._var_cant_lungime.set("fara")
        self._var_cant_latime.set("fara")


class TabelPiese(ctk.CTkScrollableFrame):
    COLOANE = ["#", "Nume", "Buc.", "L (mm)", "l (mm)", "Material", "Gros.",
               "Supraf. m2", "Mat. lei", "Cant lei", "Total lei", "", ""]

    def __init__(self, master, callback_editeaza, callback_sterge, **kwargs):
        super().__init__(master, **kwargs)
        self._callback_editeaza = callback_editeaza
        self._callback_sterge = callback_sterge
        self._randuri = []
        self._deseneaza_antet()

    def _deseneaza_antet(self):
        for col, text in enumerate(self.COLOANE):
            ctk.CTkLabel(self, text=text, font=ctk.CTkFont(weight="bold"),
                         fg_color=("gray80", "gray25"), corner_radius=4).grid(
                row=0, column=col, padx=2, pady=2, sticky="ew"
            )

    def actualizeaza(self, piese):
        for widgets in self._randuri:
            for w in widgets:
                w.destroy()
        self._randuri = []

        for i, piesa in enumerate(piese):
            valori = [
                str(i + 1),
                piesa.nume,
                str(piesa.cantitate),
                str(piesa.lungime),
                str(piesa.latime),
                piesa.material.nume,
                str(piesa.material.grosime),
                f"{piesa.suprafata_mp:.4f}",
                f"{piesa.cost_material:.2f}",
                f"{piesa.cost_cant:.2f}",
                f"{piesa.cost_total:.2f}",
            ]
            widgets = []
            for col, val in enumerate(valori):
                lbl = ctk.CTkLabel(self, text=val)
                lbl.grid(row=i + 1, column=col, padx=2, pady=1, sticky="ew")
                widgets.append(lbl)

            btn_edit = ctk.CTkButton(self, text="Edit", width=44, fg_color="gray40",
                                     command=lambda x=i: self._callback_editeaza(x))
            btn_edit.grid(row=i + 1, column=len(self.COLOANE) - 2, padx=2, pady=1)
            widgets.append(btn_edit)

            btn_sterge = ctk.CTkButton(self, text="X", width=30, fg_color="red",
                                       command=lambda x=i: self._callback_sterge(x))
            btn_sterge.grid(row=i + 1, column=len(self.COLOANE) - 1, padx=2, pady=1)
            widgets.append(btn_sterge)
            self._randuri.append(widgets)


class PanouTotal(ctk.CTkFrame):
    def __init__(self, master, callback_export_csv, callback_export_oferta, callback_actualizeaza, **kwargs):
        super().__init__(master, **kwargs)
        self._construieste(callback_export_csv, callback_export_oferta, callback_actualizeaza)

    def _construieste(self, cb_csv, cb_oferta, cb_actualiz):
        ctk.CTkLabel(self, text="Sumar proiect", font=ctk.CTkFont(size=14, weight="bold")).grid(
            row=0, column=0, columnspan=2, pady=(10, 4), padx=10
        )

        etichete = [
            ("Suprafata totala (m2):", "lbl_suprafata"),
            ("Cost materiale (lei):", "lbl_materiale"),
            ("Cost cant (lei):", "lbl_cant"),
            ("Cost accesorii (lei):", "lbl_accesorii"),
            ("Adaos pierdere (lei):", "lbl_pierdere"),
            ("Manopera estimativa (lei):", "lbl_manopera"),
            ("TOTAL (lei):", "lbl_total"),
        ]
        self._labels = {}
        for row, (text, key) in enumerate(etichete, start=1):
            ctk.CTkLabel(self, text=text, anchor="w").grid(row=row, column=0, padx=10, pady=2, sticky="w")
            lbl = ctk.CTkLabel(self, text="-", anchor="e", font=ctk.CTkFont(weight="bold"))
            lbl.grid(row=row, column=1, padx=10, pady=2, sticky="e")
            self._labels[key] = lbl

        self._var_pierdere = ctk.StringVar(value="10")
        ctk.CTkLabel(self, text="% pierdere la debitare:").grid(row=8, column=0, padx=10, pady=4, sticky="w")
        ctk.CTkEntry(self, textvariable=self._var_pierdere, width=70).grid(row=8, column=1, padx=10, pady=4, sticky="e")

        self._var_factor_manopera = ctk.StringVar(value="1.0")
        ctk.CTkLabel(self, text="Factor manopera (x):").grid(row=9, column=0, padx=10, pady=4, sticky="w")
        ctk.CTkEntry(self, textvariable=self._var_factor_manopera, width=70).grid(row=9, column=1, padx=10, pady=4, sticky="e")

        self._var_dificultate = ctk.StringVar(value="1.0")
        ctk.CTkLabel(self, text="Grad dificultate (x):").grid(row=10, column=0, padx=10, pady=4, sticky="w")
        ctk.CTkEntry(self, textvariable=self._var_dificultate, width=70).grid(row=10, column=1, padx=10, pady=4, sticky="e")

        ctk.CTkButton(self, text="Recalculeaza", command=cb_actualiz).grid(row=11, column=0, columnspan=2, pady=4, padx=10)
        ctk.CTkButton(self, text="Export Cut List CSV", command=cb_csv).grid(row=12, column=0, columnspan=2, pady=4, padx=10)
        ctk.CTkButton(self, text="Export Oferta JSON", command=cb_oferta).grid(row=13, column=0, columnspan=2, pady=(4, 10), padx=10)

    def actualizeaza(self, proiect):
        self._labels["lbl_suprafata"].configure(text=f"{proiect.suprafata_totala_mp:.4f}")
        self._labels["lbl_materiale"].configure(text=f"{proiect.cost_materiale:.2f}")
        self._labels["lbl_cant"].configure(text=f"{proiect.cost_cant:.2f}")
        self._labels["lbl_accesorii"].configure(text=f"{proiect.cost_accesorii:.2f}")
        self._labels["lbl_pierdere"].configure(text=f"{proiect.adaos_pierdere:.2f}")
        self._labels["lbl_manopera"].configure(text=f"{proiect.manopera_estimativa:.2f}")
        self._labels["lbl_total"].configure(text=f"{proiect.total:.2f}")

    @property
    def procent_pierdere(self):
        try:
            return float(self._var_pierdere.get().replace(",", "."))
        except ValueError:
            return 10.0

    @property
    def factor_manopera(self):
        try:
            return float(self._var_factor_manopera.get().replace(",", "."))
        except ValueError:
            return 1.0

    @property
    def grad_dificultate(self):
        try:
            return float(self._var_dificultate.get().replace(",", "."))
        except ValueError:
            return 1.0


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(f"{MARCA} - MobiOferta")
        self.geometry("1320x800")
        self.minsize(980, 640)

        self._catalog = CatalogMateriale()
        self._proiect = Proiect(nume="Proiect nou", procent_pierdere=10.0)
        self._construieste_ui()

    def _construieste_ui(self):
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        bara_top = ctk.CTkFrame(self, height=50)
        bara_top.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=(10, 0))

        # logo / marca
        ctk.CTkLabel(bara_top, text=MARCA, font=ctk.CTkFont(size=18, weight="bold"),
                     text_color=CULOARE_MARCA).pack(side="left", padx=(12, 18))

        ctk.CTkLabel(bara_top, text="Proiect:", font=ctk.CTkFont(size=13)).pack(side="left", padx=(0, 4))
        self._var_nume_proiect = ctk.StringVar(value="Proiect nou")
        ctk.CTkEntry(bara_top, textvariable=self._var_nume_proiect, width=220).pack(side="left", padx=4)
        ctk.CTkButton(bara_top, text="Salveaza proiect", command=self._salveaza).pack(side="left", padx=10)
        ctk.CTkButton(bara_top, text="Proiect nou", fg_color="gray40", command=self._proiect_nou).pack(side="left", padx=4)

        col_stanga = ctk.CTkScrollableFrame(self, width=440)
        col_stanga.grid(row=1, column=0, sticky="nsew", padx=(10, 4), pady=10)

        self._formular_piesa = FormularPiesa(col_stanga, self._adauga_piesa, self._catalog)
        self._formular_piesa.pack(fill="x", padx=4, pady=4)

        self._frame_accesoriu = self._construieste_frame_accesoriu(col_stanga)
        self._frame_accesoriu.pack(fill="x", padx=4, pady=4)

        self._panou_total = PanouTotal(
            col_stanga,
            callback_export_csv=self._export_csv,
            callback_export_oferta=self._export_oferta,
            callback_actualizeaza=self._recalculeaza,
        )
        self._panou_total.pack(fill="x", padx=4, pady=4)

        self._tabel = TabelPiese(self, self._editeaza_piesa, self._sterge_piesa)
        self._tabel.grid(row=1, column=1, sticky="nsew", padx=(4, 10), pady=10)

    def _construieste_frame_accesoriu(self, master):
        frame = ctk.CTkFrame(master)
        ctk.CTkLabel(frame, text="Adauga accesoriu", font=ctk.CTkFont(size=13, weight="bold")).grid(
            row=0, column=0, columnspan=2, pady=(8, 4), padx=10
        )
        ctk.CTkLabel(frame, text="Nume").grid(row=1, column=0, padx=10, sticky="w")
        self._acc_nume = ctk.CTkEntry(frame, width=180)
        self._acc_nume.grid(row=1, column=1, padx=10, pady=2, sticky="w")

        ctk.CTkLabel(frame, text="Pret/buc (lei)").grid(row=2, column=0, padx=10, sticky="w")
        self._acc_pret = ctk.CTkEntry(frame, width=80)
        self._acc_pret.grid(row=2, column=1, padx=10, pady=2, sticky="w")

        ctk.CTkLabel(frame, text="Cantitate").grid(row=3, column=0, padx=10, sticky="w")
        self._acc_cant = ctk.CTkEntry(frame, width=80)
        self._acc_cant.insert(0, "1")
        self._acc_cant.grid(row=3, column=1, padx=10, pady=2, sticky="w")

        ctk.CTkButton(frame, text="+ Adauga accesoriu", command=self._adauga_accesoriu).grid(
            row=4, column=0, columnspan=2, pady=8, padx=10
        )

        # lista cu accesoriile adaugate
        self._lista_acc = ctk.CTkFrame(frame, fg_color="transparent")
        self._lista_acc.grid(row=5, column=0, columnspan=2, padx=8, pady=(0, 8), sticky="ew")
        return frame

    def _actualizeaza_lista_accesorii(self):
        for w in self._lista_acc.winfo_children():
            w.destroy()
        for i, acc in enumerate(self._proiect.accesorii):
            text = f"{acc.nume}  -  {acc.cantitate} x {acc.pret_bucata:.2f} = {acc.cost_total:.2f} lei"
            ctk.CTkLabel(self._lista_acc, text=text, anchor="w").grid(row=i, column=0, padx=4, pady=1, sticky="w")
            ctk.CTkButton(self._lista_acc, text="X", width=28, fg_color="red",
                          command=lambda x=i: self._sterge_accesoriu(x)).grid(row=i, column=1, padx=4, pady=1)

    def _adauga_piesa(self, piesa):
        self._proiect.adauga_piesa(piesa)
        self._refresh()

    def _editeaza_piesa(self, index):
        piese = self._proiect.piese
        if 0 <= index < len(piese):
            self._formular_piesa.incarca_piesa(piese[index])
            self._proiect.sterge_piesa(index)
            self._refresh()
            messagebox.showinfo("Editare", "Piesa a fost incarcata in formular. Modifica si apasa '+ Adauga piesa'.")

    def _sterge_piesa(self, index):
        self._proiect.sterge_piesa(index)
        self._refresh()

    def _adauga_accesoriu(self):
        try:
            nume = self._acc_nume.get().strip()
            if not nume:
                raise ValueError("Numele accesoriului nu poate fi gol.")
            pret = float(self._acc_pret.get().replace(",", "."))
            cant = int(self._acc_cant.get())
            self._proiect.adauga_accesoriu(Accesoriu(nume, pret, cant))
            self._acc_nume.delete(0, "end")
            self._acc_pret.delete(0, "end")
            self._acc_cant.delete(0, "end")
            self._acc_cant.insert(0, "1")
            self._refresh()
        except ValueError as e:
            messagebox.showerror("Eroare", str(e))

    def _sterge_accesoriu(self, index):
        self._proiect.sterge_accesoriu(index)
        self._refresh()

    def _recalculeaza(self):
        self._proiect.nume = self._var_nume_proiect.get()
        self._refresh()

    def _aplica_factori(self):
        self._proiect.procent_pierdere = self._panou_total.procent_pierdere
        self._proiect.factor_manopera = self._panou_total.factor_manopera
        self._proiect.grad_dificultate = self._panou_total.grad_dificultate

    def _refresh(self):
        self._aplica_factori()
        self._tabel.actualizeaza(self._proiect.piese)
        self._actualizeaza_lista_accesorii()
        self._panou_total.actualizeaza(self._proiect)

    def _salveaza(self):
        self._recalculeaza()
        self._proiect.salveaza()
        messagebox.showinfo("Salvat", f"Proiectul '{self._proiect.nume}' a fost salvat in proiecte.json.")

    def _proiect_nou(self):
        if messagebox.askyesno("Proiect nou", "Stergi proiectul curent si incepi unul nou?"):
            self._proiect = Proiect(nume="Proiect nou", procent_pierdere=10.0)
            self._var_nume_proiect.set("Proiect nou")
            self._refresh()

    def _export_csv(self):
        cale = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv")],
            initialfile=f"cut_list_{self._proiect.nume}.csv",
        )
        if cale:
            Exportator(self._proiect).export_cut_list_csv(cale)
            messagebox.showinfo("Export", f"Cut list salvat:\n{cale}")

    def _export_oferta(self):
        cale = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON", "*.json")],
            initialfile=f"oferta_{self._proiect.nume}.json",
        )
        if cale:
            Exportator(self._proiect).export_oferta_json(cale)
            messagebox.showinfo("Export", f"Oferta salvata:\n{cale}")
