import pandas as pd
from pathlib import Path

DESTINATION_NAME = {
    "students": "students.csv",
    "notes": "notes.csv",
    "time": "time.csv",
}

def ingest_spreadsheet(origin_path:Path, type_csv: str ) -> Path : 
    
    if type_csv not in DESTINATION_NAME: 
        raise  ValueError(f"tipo desconocido: {type_csv}")
    
    path = Path("data") / "spreadsheets" / DESTINATION_NAME[type_csv]
    row_search_header = pd.read_excel(origin_path, header=None, nrows=15)
    key_words = ["nombre"]
    
    idx_header = 0
    find = False
    for idx, row in row_search_header.iterrows():
        values = {str(v).strip().lower() for v in row.tolist()}
        if any(keyword in valor for valor in values for keyword in key_words):
            idx_header = idx
            find = True
            break
    if find is False:
        raise ValueError(f"Header no encontrado en el csv {origin_path}")
    file = pd.read_excel(origin_path, header=idx_header)
    file.to_csv(Path(path), index=False, encoding="utf-8", sep=';')
    return Path(path)