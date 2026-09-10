from typing import Dict
from models.student import Student


_students_by_dni: Dict[str, Student] = {}
# Variable a nivel de módulo. Es la "fuente de verdad" del curso actual.
# Empieza vacía porque al arrancar el programa no hay ningún curso cargado.


def set_students(students: Dict[str, Student]) -> None:
    """
    Sustituye el curso actualmente cargado por uno nuevo. La GUI la
    llama justo después de ejecutar load_all() con éxito, pasándole
    el diccionario resultante.
    """
    global _students_by_dni
    _students_by_dni = students

def get_students() -> Dict[str, Student]:
    """
    Devuelve el diccionario del curso actual, para que la GUI se lo
    pase a los generadores de documentos.
    """
    return _students_by_dni


def clear() -> None:
    """
    Vacía el curso actual. Esta es la función que llama el botón
    'Nuevo curso' de la GUI.
    """
    _students_by_dni.clear()


def has_students() -> bool:
    """
    True si hay algún alumno cargado ahora mismo. Útil para que la
    GUI decida si el botón 'Iniciar' debe estar habilitado o no.
    """
    return len(_students_by_dni) > 0