"""Creación de las capas de texto (texto principal + sombra).

El envoltura (wrapping) se hace aquí a mano, midiendo con Pillow, en vez de
delegarlo a MoviePy: su `method="caption"` parte palabras a la mitad
(bug en `TextClip.__break_text`). Aquí cortamos solo en espacios y luego
dibujamos con `method="label"`, que respeta nuestros saltos de línea.
"""
import os

from moviepy import TextClip
from PIL import Image, ImageDraw, ImageFont


def _fuente_valida(ruta):
    """Devuelve la ruta de la fuente si existe; si no, None (fuente por defecto)."""
    if ruta and os.path.isfile(ruta):
        return ruta
    if ruta:
        print(f"[aviso] No se encontró la fuente {ruta}; usando la fuente por defecto.")
    return None


def _cargar_fuente_pil(ruta, tamano):
    """Carga la fuente en Pillow para poder medir el ancho del texto."""
    if ruta:
        return ImageFont.truetype(ruta, tamano)
    return ImageFont.load_default(tamano)


def _envolver(texto, fuente_pil, ancho_max, stroke_width):
    """Envuelve el texto en líneas que caben en `ancho_max`, cortando solo en
    espacios (nunca a mitad de palabra). Respeta los saltos de línea ya presentes.
    """
    draw = ImageDraw.Draw(Image.new("RGB", (1, 1)))

    def ancho(cadena):
        izq, _, der, _ = draw.textbbox(
            (0, 0), cadena, font=fuente_pil, stroke_width=stroke_width
        )
        return der - izq

    lineas = []
    for parrafo in texto.split("\n"):
        linea = ""
        for palabra in parrafo.split(" "):
            candidata = palabra if not linea else f"{linea} {palabra}"
            # Si la línea está vacía aceptamos la palabra aunque exceda (no hay
            # dónde cortarla sin partirla): se reducirá vía autoajuste.
            if not linea or ancho(candidata) <= ancho_max:
                linea = candidata
            else:
                lineas.append(linea)
                linea = palabra
        lineas.append(linea)
    return "\n".join(lineas)


def _crear_clip(texto, ruta_fuente, color, stroke_color, stroke_width, tamano):
    """Crea un TextClip con saltos de línea ya resueltos (method='label')."""
    return TextClip(
        font=ruta_fuente,
        text=texto,
        font_size=tamano,
        color=color,
        method="label",
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

    `cfg` es la sección `texto` de la configuración. El tamaño de la fuente se
    reduce automáticamente (re-envolviendo el texto en cada paso) hasta que todo
    el texto quepa en el área disponible, de modo que nunca se recorte.
    """
    ancho_video, alto_video = tamano_video
    contorno = cfg.get("contorno", {}) or {}
    sombra = cfg.get("sombra", {}) or {}

    ruta_fuente = _fuente_valida(cfg.get("fuente"))
    color = cfg.get("color", "white")
    stroke_color = contorno.get("color", "black")
    stroke_width = contorno.get("grosor", 0)

    margen = cfg.get("margen", 200)
    alto_max = max(1, alto_video - 2 * margen)
    ancho_caja = cfg.get("ancho_caja", 1000)
    # Margen interno para que el contorno no haga que la línea exceda la caja.
    ancho_max = max(1, ancho_caja - 2 * stroke_width)

    tamano = cfg.get("tamano", 70)
    tamano_min = cfg.get("tamano_min", 30)
    autoajustar = cfg.get("autoajustar", True)

    def construir(tamano_actual):
        """Envuelve y crea el clip principal para un tamaño de fuente dado."""
        fuente_pil = _cargar_fuente_pil(ruta_fuente, tamano_actual)
        envuelto = _envolver(texto, fuente_pil, ancho_max, stroke_width)
        clip = _crear_clip(
            envuelto, ruta_fuente, color, stroke_color, stroke_width, tamano_actual
        )
        return clip, envuelto

    principal, envuelto = construir(tamano)
    if autoajustar:
        while (principal.h > alto_max or principal.w > ancho_video) and tamano > tamano_min:
            tamano = max(tamano_min, tamano - 4)
            principal, envuelto = construir(tamano)
        if principal.h > alto_max:
            print(
                f"[aviso] El texto no cabe ni con el tamaño mínimo ({tamano_min}); "
                "puede recortarse. Considera reducir 'tamano_min' o acortar el texto."
            )

    px, py = _posicion(principal, cfg, ancho_video, alto_video)
    principal = principal.with_duration(duracion).with_position((px, py))

    capas = []

    # Sombra: misma forma y tamaño del texto, desplazada y semitransparente.
    if sombra.get("activada", False):
        clip_sombra = _crear_clip(
            envuelto,
            ruta_fuente,
            color=sombra.get("color", "black"),
            stroke_color=sombra.get("color", "black"),
            stroke_width=stroke_width,
            tamano=tamano,
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
