from pathlib import Path
from docxtpl import DocxTemplate
from typing import Dict
from models.student import Student
from docs.context import build_certificate_context


def generate_certificate(template_path: Path, students_by_dni: Dict[str, Student], output_path: Path) -> Path:
    """
    Abre la plantilla de certificado, la rellena con el contexto de
    alumnos y guarda el resultado en output_path.
    """
    doc = DocxTemplate(template_path)
    doc.render(build_certificate_context(students_by_dni))
    doc.save(output_path)
    return output_path