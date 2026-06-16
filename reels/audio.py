"""Preparación de la pista de audio."""
from moviepy import AudioFileClip


def preparar_audio(ruta, duracion):
    """Carga el audio y lo recorta de forma segura a `duracion`.

    Si la música es más corta que la duración pedida, se usa la duración
    real del audio para no fallar (en lugar de pedir un subclip imposible).
    """
    audio = AudioFileClip(ruta)
    fin = min(duracion, audio.duration)
    return audio.subclipped(0, fin)
