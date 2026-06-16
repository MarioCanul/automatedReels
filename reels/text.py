"""Creación de las capas de texto (texto principal + sombra)."""
import os

from moviepy import TextClip


def _fuente_valida(ruta):
    """Devuelve la ruta de la fuente si existe; si no, None (fuente por defecto)."""
    if ruta and os.path.isfile(ruta):
        return ruta
    if ruta:
        print(f"[aviso] No se encontró la fuente {ruta}; usando la fuente por defecto.")
    return None


def _crear_clip(texto, cfg, color, stroke_color, stroke_width):
    """Crea un TextClip base con el estilo común (envoltura, alineación)."""
    return TextClip(
        font=_fuente_valida(cfg.get("fuente")),
        text=texto,
        font_size=cfg.get("tamano", 70),
        color=color,
        size=(cfg.get("ancho_caja", 1000), None),
        method="caption",
        text_align="center",
        stroke_color=stroke_color,
        stroke_width=stroke_width,
    )


def _posicion(clip, cfg, ancho_video, alto_video):
    """Calcula la posición (x, y) del texto según la config."""
    x = (ancho_video - clip.w) / 2  # centrado horizontal
    vertical = cfg.get("posicion_vertical", "center")
    margen = cfg.get("margen", 200)
    if vertical == "top":
        y = margen
    elif vertical == "bottom":
        y = alto_video - clip.h - margen
    else:  # center
        y = (alto_video - clip.h) / 2
    return x, y


def crear_capas_texto(texto, cfg, tamano_video, duracion):
    """Devuelve las capas de texto listas para componer (sombra debajo, texto encima).

    `cfg` es la sección `texto` de la configuración.
    """
    ancho_video, alto_video = tamano_video
    contorno = cfg.get("contorno", {}) or {}
    sombra = cfg.get("sombra", {}) or {}

    # Texto principal (con contorno nativo).
    principal = _crear_clip(
        texto,
        cfg,
        color=cfg.get("color", "white"),
        stroke_color=contorno.get("color", "black"),
        stroke_width=contorno.get("grosor", 0),
    )
    px, py = _posicion(principal, cfg, ancho_video, alto_video)
    principal = principal.with_duration(duracion).with_position((px, py))

    capas = []

    # Sombra: misma forma del texto, desplazada y semitransparente.
    if sombra.get("activada", False):
        clip_sombra = _crear_clip(
            texto,
            cfg,
            color=sombra.get("color", "black"),
            stroke_color=sombra.get("color", "black"),
            stroke_width=contorno.get("grosor", 0),
        )
        dx, dy = sombra.get("offset", [4, 4])
        clip_sombra = (
            clip_sombra.with_duration(duracion)
            .with_position((px + dx, py + dy))
            .with_opacity(sombra.get("opacidad", 0.6))
        )
        capas.append(clip_sombra)

    capas.append(principal)
    return capas
