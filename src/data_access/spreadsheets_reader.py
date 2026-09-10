import pandas as pd
from pathlib import Path
from typing import Dict
from models.student import Student


def normalize_dni(raw_dni: str) -> str:
    """
    Limpia un DNI tal como puede venir de un Excel: quita espacios,
    guiones, y lo pasa a mayúsculas. Debe ser la ÚNICA función de todo
    el proyecto que hace esto — si la lógica de limpieza se repite
    en varios sitios, el día que cambie el formato (por ejemplo, si
    aparecen DNIs con puntos) tendrías que tocar varios archivos
    en vez de uno.
    """
    return raw_dni.replace("-", "").strip().upper()


def read_students_csv(csv_path: Path) -> Dict[str, Student]:
    """
    Lee el CSV de selección de alumnado (students.csv) y CREA los
    objetos Student desde cero. Es el único lector que crea alumnos;
    los otros dos (notas, horas) solo actualizan alumnos que ya existen.

    Devuelve el diccionario alumnos_por_dni ya construido, para que
    repo.py simplemente lo reciba y lo guarde.
    """
    file = pd.read_csv(csv_path, sep=";")
    res = {}
    for idx, row in file.iterrows(): 
        res[normalize_dni(row["DNI"])] = Student(
                                            dni=normalize_dni(row["DNI"]),
                                            name=row["Nombre"].split(",")[1].strip(),
                                            lastname=row["Nombre"].split(",")[0].strip(),
                                            corp=row["Corporación"],
                                            movil=row["Teléfono móvil"],
                                            phone=row["Teléfono fijo"],
                                            mail=row["Email"],
                                            job=row["Datoscargo"],
                                            student_type=row["Tipo"],
                                            state=row["Cód. estado"],
                                        )
    return res


def read_notes_csv(csv_path: Path, students_by_DNI: Dict[str, Student]) -> None:
    """
    Lee el CSV de notas y ACTUALIZA los Student que ya existen en
    alumnos_por_dni (ev1, ev2, ev3, ev4, evf).

    No devuelve nada porque muta el diccionario que recibe. Decide
    aquí qué hacer si un DNI del CSV de notas no está en el
    diccionario: ¿lo ignoras con un aviso, o lo consideras un error
    y paras la ejecución?
    """
    # TODO: implementar cuando tenga el CSV real de notas
    return students_by_DNI


def read_time_csv(csv_path: Path, students_by_DNI: Dict[str, Student]) -> None:
    """
    Igual que read_notes_csv pero para tiempo de conexión y
    firstconection. Mismo dilema del DNI huérfano que arriba.
    """
    # TODO: implementar cuando tenga el CSV real de horas
    return students_by_DNI


def _parse_grade(raw_value) -> float | None:
    """
    Convierte un valor de nota leído del CSV a float, o None si
    está vacío/no es válido. Aísla aquí el problema del separador
    decimal (coma vs punto) para no repetirlo en read_notes_csv.
    """
    pass


def load_all(students_csv: Path, notes_csv: Path, time_csv: Path) -> Dict[str, Student]:
    """
    Orquestador: llama a las tres funciones anteriores en orden y
    devuelve el diccionario final ya completo. Es la única función
    que gui/ o repo.py necesitan conocer — no deberían llamar a las
    tres funciones sueltas por separado.
    """
    students_by_DNI = read_students_csv(students_csv)
    students_by_DNI_notes = read_notes_csv(notes_csv, students_by_DNI)
    return read_time_csv(time_csv, students_by_DNI_notes)