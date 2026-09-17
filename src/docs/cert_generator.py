from pathlib import Path
from typing import Dict
from docx import Document
from models.student import Student

def generate_certificate(template_path: Path, students_by_dni: Dict[str, Student], output_path: Path) -> Path:
    """
    Sanea la plantilla en disco y genera el documento final.
    """
    doc = Document(template_path)

    if doc.tables:
        table = doc.tables[0]

            # 1. Asegurar que solo quede la fila de encabezados
        while len(table.rows) > 1:
            tr = table.rows[-1]._tr
            tr.getparent().remove(tr)
            
            # 2. Agregar cada alumno como una nueva fila
        idx = 1
        for student in students_by_dni.values():
            # Conversión segura de nota a decimal
            try:
                evf_val = float(getattr(student, 'evf', 0))
            except (ValueError, TypeError):
                evf_val = 0.0

            # Filtrar alumnos no aptos
            if evf_val < 5.0:
                continue

            row_cells = table.add_row().cells
                
            # Asignación directa de texto por columna
            row_cells[0].text = str(idx)
            row_cells[1].text = getattr(student, 'lastname', '')
            row_cells[2].text = getattr(student, 'name', '')
            row_cells[3].text = getattr(student, 'dni', '')
            row_cells[4].text = getattr(student, 'corp', '')

            idx += 1

    doc.save(output_path)
    return output_path