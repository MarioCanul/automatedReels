"""Composición de capas y exportación del reel a MP4."""
import os

from moviepy import CompositeVideoClip


def renderizar(ruta_salida, fondo, audio, capas_texto, logo, render_cfg):
    """Compone fondo + texto + logo, añade el audio y exporta el MP4.

    - `capas_texto` es una lista (sombra, texto principal).
    - `logo` puede ser None.
    """
    ancho = render_cfg.get("ancho", 1080)
    alto = render_cfg.get("alto", 1920)

    capas = [fondo, *capas_texto]
    if logo is not None:
        capas.append(logo)

    video = CompositeVideoClip(capas, size=(ancho, alto))
    if audio is not None:
        video = video.with_audio(audio)

    os.makedirs(os.path.dirname(ruta_salida) or ".", exist_ok=True)

    video.write_videofile(
        ruta_salida,
        codec=render_cfg.get("codec", "libx264"),
        audio_codec=render_cfg.get("audio_codec", "aac"),
        fps=render_cfg.get("fps", 30),
    )
    video.close()
