"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel

import re
from pathlib import Path

import pandas as pd


def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.
    """
    with open("files/input/clusters_report.txt", "r", encoding="utf-8") as f:
      lines = f.readlines()

    records = []
    current_record = None

    for line in lines:
        if not line.strip():
            continue
        if line.lstrip().startswith("Cluster"):
            continue
        if set(line.strip()) <= {"-"}:
            continue
        if re.match(r"^\s*\d+\s", line):
            if current_record is not None:
                records.append(current_record)
            current_record = line.strip()
        elif current_record is not None:
            current_record = f"{current_record} {line.strip()}"

    if current_record is not None:
        records.append(current_record)

    parsed_records = []
    pattern = re.compile(r"^\s*(\d+)\s+(\d+)\s+([0-9,]+)\s*%\s*(.*)$")

    for record in records:
        match = pattern.match(record)
        if match is None:
            continue

        cluster, count, percentage, keywords = match.groups()
        keywords = re.sub(r"\s+", " ", keywords).strip()
        keywords = re.sub(r"\s*,\s*", ", ", keywords)
        keywords = re.sub(r"\s+", " ", keywords).strip().rstrip(".")

        parsed_records.append(
            {
                "cluster": int(cluster),
                "cantidad_de_palabras_clave": int(count),
                "porcentaje_de_palabras_clave": float(percentage.replace(",", ".")),
                "principales_palabras_clave": keywords,
            }
        )

    df = pd.DataFrame(parsed_records)
    df.columns = [column.lower().replace(" ", "_") for column in df.columns]
    return df
