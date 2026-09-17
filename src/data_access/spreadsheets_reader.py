import pandas as pd
from pathlib import Path
from typing import Dict
from models.student import Student
import unicodedata

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
        dni_raw = str(row["dni"]).strip()
        if not dni_raw or dni_raw.lower() == "nan" or not any(c.isdigit() for c in dni_raw):
            continue
        res[normalize_dni(str(row["dni"]))] = Student(
                                            dni=normalize_dni(str(row["dni"])),
                                            name=str(row["nombre"]).split(",")[1].strip(),
                                            lastname=str(row["nombre"]).split(",")[0].strip(),
                                            corp=str(row["corporación"]),
                                            movil=str(row["teléfono móvil"]),
                                            phone=str(row["teléfono fijo"]),
                                            mail=str(row["email"]),
                                            job=str(row["datoscargo"]),
                                            student_type=str(row["tipo"]),
                                            state=str(row["cód. estado"]),
                                        )
    return res

def _build_name_index(students_by_dni: Dict[str, Student]) -> Dict[str, Student]:
    """
    Índice secundario: nombre normalizado -> Student. Solo para los
    CSV que no traen DNI (como el de horas). No sustituye al
    diccionario indexado por DNI, lo complementa.
    """
    return {_normalize_name_key(s.full_name_v1)
            : s for s in students_by_dni.values()}
    
def _normalize_name_key(nombre: str) -> str:
    return unicodedata.normalize('NFKD', nombre.lower().replace(" ", "")).encode('ascii', 'ignore').decode('ascii')

def read_notes_csv(csv_path: Path, students_by_DNI: Dict[str, Student]) -> None:
    """
    Lee el CSV de notas y ACTUALIZA los Student que ya existen en
    alumnos_por_dni (ev1, ev2, ev3, evf).

    No devuelve nada porque muta el diccionario que recibe. Decide
    aquí qué hacer si un DNI del CSV de notas no está en el
    diccionario: ¿lo ignoras con un aviso, o lo consideras un error
    y paras la ejecución?
    """
    students_by_name = _build_name_index(students_by_DNI)
    file = pd.read_csv(csv_path, sep=";")
    for idx, row in file.iterrows(): 
        student = students_by_name[_normalize_name_key(str(row["nombre"]) + " " + str(row["apellido(s)"]))] 
        student.ev1 = _parse_grade(str(row["cuestionario:test bloque i (real)"]))
        student.ev2 = _parse_grade(str(row["cuestionario:test bloque ii (real)"]))
        student.evf = _parse_grade(str(row["cuestionario:test final (real)"]))
        
        


def read_time_csv(csv_path: Path, students_by_DNI: Dict[str, Student]) -> None:
    """
    Igual que read_notes_csv pero para tiempo de conexión y
    firstconection. Mismo dilema del DNI huérfano que arriba.
    """
    students_by_name = _build_name_index(students_by_DNI)
    file = pd.read_csv(csv_path, sep=";")
    for idx, row in file.iterrows(): 
        key = _normalize_name_key(str(row["nombre completo con imagen y enlace"])[2:])
        if key in students_by_name:
            student = students_by_name[key] 
            student.time = str(row["duración"])
            student.firstconection = " "


def _parse_grade(raw_value) -> float | None:
    """
    Convierte un valor de nota leído del CSV a float, o None si
    está vacío/no es válido. Aísla aquí el problema del separador
    decimal (coma vs punto) para no repetirlo en read_notes_csv.
    """
    if raw_value is None or pd.isna(raw_value):
        return None

    if isinstance(raw_value, (int, float)):
        return float(raw_value)

    texto = str(raw_value).strip().replace(",", ".")

    if texto == "":
        return None

    try:
        return float(texto)
    except ValueError:
        return None


def load_all(students_csv: Path, notes_csv: Path, time_csv: Path) -> Dict[str, Student]:
    """
    Orquestador: llama a las tres funciones anteriores en orden y
    devuelve el diccionario final ya completo. Es la única función
    que gui/ o repo.py necesitan conocer — no deberían llamar a las
    tres funciones sueltas por separado.
    """
    students_by_DNI = read_students_csv(students_csv)
    read_notes_csv(notes_csv, students_by_DNI)
    read_time_csv(time_csv, students_by_DNI)
    return students_by_DNI