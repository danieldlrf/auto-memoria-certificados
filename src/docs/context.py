import math
from typing import Dict, List, Any, Optional
from models.student import Student


def _clean_value(value: Any, default: str = "-") -> str:
    """
    Convierte un valor cualquiera (que puede ser None, NaN, float,
    str...) en lo que se va a mostrar literalmente en el Word.
    """
    if isinstance(value, float):
        if math.isnan(value):
            return default
        return str(value)
    elif bool(value):
        return str(value)
    else:
        return default


def student_to_dict(student: Student) -> Dict[str, str]:
    """
    Convierte UN Student en el diccionario plano que docxtpl necesita
    para rellenar una fila o un bloque.
    """
    return {
        "dni": _clean_value(student.dni),
        "name": _clean_value(student.name),
        "lastname": _clean_value(student.lastname),
        "full_name_v1": _clean_value(student.full_name_v1()),
        "full_name_v2": _clean_value(student.full_name_v2()),
        "corp": _clean_value(student.corp),
        "movil": _clean_value(student.movil),
        "phone": _clean_value(student.phone),
        "mail": _clean_value(student.mail),
        "job": _clean_value(student.job),
        "student_type": _clean_value(student.student_type),
        "state": _clean_value(student.state),
        "ev1": _clean_value(student.ev1),
        "ev2": _clean_value(student.ev2),
        "ev3": _clean_value(student.ev3),
        "ev4": _clean_value(student.ev4),
        "evf": _clean_value(student.evf),
        "time": _clean_value(student.time),
        "firstconection": _clean_value(student.firstconection),
    }


def build_student_list(students_by_dni: Dict[str, Student]) -> List[Dict[str, str]]:
    """
    Convierte TODO el diccionario de alumnos en la lista de
    diccionarios que necesita el {%tr for%} de docxtpl, ordenada
    alfabéticamente por apellido.
    """
    students_sorted = sorted(students_by_dni.values(), key=lambda s: s.lastname)
    return [student_to_dict(student) for student in students_sorted]


def build_certificate_context(students_by_dni: Dict[str, Student]) -> Dict[str, Any]:
    """
    Contexto para la plantilla del certificado: solo la lista de
    alumnos, sin datos sueltos del curso.
    """
    return {"students": build_student_list(students_by_dni)}


def build_memory_context(students_by_dni: Dict[str, Student]) -> Dict[str, Any]:
    """
    Contexto para la memoria: la misma lista de alumnos, reutilizada
    en las tres tablas de la plantilla bajo la clave 'students'.
    """
    return {"students": build_student_list(students_by_dni)}