"""Creación del logo / marca de agua."""
import os

from moviepy import ImageClip


def _posicion(posicion, clip, ancho_video, alto_video, margen):
    """Convierte un nombre de esquina en coordenadas (x, y)."""
    derecha = ancho_video - clip.w - margen
    abajo = alto_video - clip.h - margen
    mapa = {
        "top-left": (margen, margen),
        "top-right": (derecha, margen),
        "bottom-left": (margen, abajo),
        "bottom-right": (derecha, abajo),
    }
    return mapa.get(posicion, mapa["top-right"])


def crear_logo(cfg, tamano_video, duracion):
    """Devuelve el clip del logo posicionado, o None si está desactivado.

    `cfg` es la sección `branding` de la configuración.
    """
    if not cfg.get("activado", False):
        return None

    ruta = cfg.get("logo")
    if not ruta or not os.path.isfile(ruta):
        print(f"[aviso] Branding activado pero no se encontró el logo: {ruta}")
        return None

    ancho_video, alto_video = tamano_video
    logo = ImageClip(ruta)

    # Escalar el logo a una fracción del ancho del video.
    ancho_logo = int(ancho_video * cfg.get("escala", 0.15))
    logo = logo.resized(width=ancho_logo)

    x, y = _posicion(
        cfg.get("posicion", "top-right"),
        logo,
        ancho_video,
        alto_video,
        cfg.get("margen", 40),
    )

    return (
        logo.with_duration(duracion)
        .with_position((x, y))
        .with_opacity(cfg.get("opacidad", 0.8))
    )
