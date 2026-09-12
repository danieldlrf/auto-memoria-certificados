import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

from data_access import file_ingest, repo
from data_access.spreadsheets_reader import load_all
from docs.cert_generator import generate_certificate
from docs.mem_generator import generate_memory


TEMPLATE_CERT_PATH = Path("data/templates/certif.docx")
TEMPLATE_MEM_PATH = Path("data/templates/memory.docx")
OUTPUT_DIR = Path("data/output")

EXCEL_TYPES = {
    "students": "Selección de alumnado",
    "notes": "Notas",
    "time": "Horas de conexión",
}


class MainScreen:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.excel_paths_display: dict[str, str] = {tipo: "" for tipo in EXCEL_TYPES}
        self.excel_labels: dict[str, tk.Label] = {}
        self._build_widgets()

    def _build_widgets(self) -> None:
        for tipo, etiqueta in EXCEL_TYPES.items():
            frame = tk.Frame(self.root)
            frame.pack(fill="x", padx=10, pady=5)

            btn = tk.Button(
                frame,
                text=f"Cargar {etiqueta}",
                command=lambda t=tipo: self._on_select_excel(t),
            )
            btn.pack(side="left")

            label = tk.Label(frame, text="(sin archivo cargado)", anchor="w")
            label.pack(side="left", padx=10)
            self.excel_labels[tipo] = label

        botones_frame = tk.Frame(self.root)
        botones_frame.pack(fill="x", padx=10, pady=15)

        tk.Button(botones_frame, text="Iniciar", command=self._on_iniciar).pack(side="left", padx=5)
        tk.Button(botones_frame, text="Nuevo curso", command=self._on_nuevo_curso).pack(side="left", padx=5)

    def _on_select_excel(self, tipo: str) -> None:
        ruta_original = filedialog.askopenfilename(
            title=f"Selecciona el Excel de {EXCEL_TYPES[tipo]}",
            filetypes=[("Excel files", "*.xlsx *.xls")],
        )
        if not ruta_original:
            return  # el usuario canceló el diálogo, no hacemos nada

        try:
            file_ingest.ingest_spreadsheet(Path(ruta_original), tipo)
        except Exception as e:
            messagebox.showerror("Error al cargar el archivo", str(e))
            return

        self.excel_paths_display[tipo] = ruta_original
        self.excel_labels[tipo].config(text=ruta_original)

    def _on_iniciar(self) -> None:
        faltantes = [
            etiqueta for tipo, etiqueta in EXCEL_TYPES.items()
            if not self.excel_paths_display[tipo]
        ]
        if faltantes:
            messagebox.showwarning(
                "Faltan archivos",
                "Todavía no has cargado: " + ", ".join(faltantes),
            )
            return

        try:
            students_csv = Path("data/spreadsheets/students.csv")
            notes_csv = Path("data/spreadsheets/notes.csv")
            time_csv = Path("data/spreadsheets/time.csv")

            students_by_dni = load_all(students_csv, notes_csv, time_csv)
            repo.set_students(students_by_dni)

            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            cert_path = generate_certificate(
                TEMPLATE_CERT_PATH, repo.get_students(), OUTPUT_DIR / "certificado_generado.docx"
            )
            mem_path = generate_memory(
                TEMPLATE_MEM_PATH, repo.get_students(), OUTPUT_DIR / "memoria_generada.docx"
            )

            messagebox.showinfo(
                "Proceso completado",
                f"Documentos generados:\n{cert_path}\n{mem_path}",
            )
        except Exception as e:
            messagebox.showerror("Error durante la generación", str(e))

    def _on_nuevo_curso(self) -> None:
        repo.clear()
        for tipo in EXCEL_TYPES:
            self.excel_paths_display[tipo] = ""
            self.excel_labels[tipo].config(text="(sin archivo cargado)")


def main():
    root = tk.Tk()
    root.title("Gestor de cursos")
    MainScreen(root)
    root.mainloop()


if __name__ == "__main__":
    main()