"""Lectura del CSV de textos.

Cada fila con texto no vacío produce un reel independiente.
"""
import csv as _csv


def cargar_textos(ruta_csv, prefijo="reel"):
    """Lee el CSV y devuelve una lista de items, uno por fila con texto.

    Cada item es un dict: {indice, texto, nombre_salida, fila}.
    - `fila` conserva todas las columnas de la fila, para tolerar columnas
      extra a futuro (p. ej. "musica" o "fondo" por fila) sin romper.
    - Las filas con la columna "texto" vacía se ignoran.
    """
    items = []
    with open(ruta_csv, "r", encoding="utf-8-sig", newline="") as f:
        lector = _csv.DictReader(f)
        if lector.fieldnames is None or "texto" not in lector.fieldnames:
            raise ValueError(
                f'El CSV {ruta_csv} debe tener una columna llamada "texto".'
            )

        indice = 0
        for fila in lector:
            texto = (fila.get("texto") or "").strip()
            if not texto:
                continue
            indice += 1
            items.append(
                {
                    "indice": indice,
                    "texto": texto,
                    "nombre_salida": f"{prefijo}_{indice:02d}.mp4",
                    "fila": fila,
                }
            )

    if not items:
        raise ValueError(
            f"No se encontraron textos en {ruta_csv} (¿columna 'texto' vacía?)."
        )

    return items
