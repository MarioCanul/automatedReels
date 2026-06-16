"""Preparación del video de fondo."""
import os

from moviepy import VideoFileClip


def elegir_fondo(carpeta_fondos):
    """Devuelve la ruta del primer .mp4 encontrado en la carpeta de fondos."""
    videos = [
        os.path.join(carpeta_fondos, f)
        for f in sorted(os.listdir(carpeta_fondos))
        if f.lower().endswith(".mp4")
    ]
    if not videos:
        raise FileNotFoundError(
            f"No hay videos MP4 en la carpeta {carpeta_fondos}"
        )
    return videos[0]


def preparar_fondo(ruta_video, duracion, ancho, alto):
    """Carga el fondo, lo recorta a `duracion` y lo ajusta a `ancho x alto`.

    Escala por altura y, si sobra ancho, hace un recorte centrado.
    Devuelve (clip, duracion_real).
    """
    fondo = VideoFileClip(ruta_video)
    duracion_real = min(duracion, fondo.duration)
    fondo = fondo.subclipped(0, duracion_real)

    fondo = fondo.resized(height=alto)
    if fondo.w > ancho:
        exceso = (fondo.w - ancho) / 2
        fondo = fondo.cropped(x1=exceso, y1=0, width=ancho, height=alto)

    return fondo, duracion_real
