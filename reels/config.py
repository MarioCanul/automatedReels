"""Carga y validación de la configuración (config.yaml).

Aplica valores por defecto para cualquier clave faltante, de modo que un
config.yaml incompleto siga funcionando.
"""
import copy
import os

import yaml

# Valores por defecto. El YAML del usuario se fusiona encima de estos.
DEFAULTS = {
    "entrada": {
        "carpeta_fondos": "fondos",
        "musica": "musica/musica.mp3",
        "csv": "textos.csv",
    },
    "salida": {
        "carpeta": "salida",
        "prefijo": "reel",
    },
    "render": {
        "ancho": 1080,
        "alto": 1920,
        "fps": 30,
        "duracion_max": 10,
        "codec": "libx264",
        "audio_codec": "aac",
    },
    "texto": {
        "fuente": None,
        "tamano": 70,
        "color": "white",
        "ancho_caja": 1000,
        "posicion_vertical": "center",
        "margen": 200,
        "contorno": {"color": "black", "grosor": 3},
        "sombra": {
            "activada": True,
            "color": "black",
            "offset": [4, 4],
            "opacidad": 0.6,
        },
    },
    "branding": {
        "activado": False,
        "logo": "assets/logo.png",
        "posicion": "top-right",
        "escala": 0.15,
        "opacidad": 0.8,
        "margen": 40,
    },
}


def _merge(base, override):
    """Fusiona recursivamente `override` sobre una copia de `base`."""
    resultado = copy.deepcopy(base)
    for clave, valor in (override or {}).items():
        if (
            clave in resultado
            and isinstance(resultado[clave], dict)
            and isinstance(valor, dict)
        ):
            resultado[clave] = _merge(resultado[clave], valor)
        else:
            resultado[clave] = valor
    return resultado


def cargar_config(ruta="config.yaml"):
    """Lee el YAML, lo fusiona con los defaults y valida rutas críticas.

    Devuelve un dict con la configuración completa.
    """
    datos = {}
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            datos = yaml.safe_load(f) or {}
    else:
        print(f"[aviso] No se encontró {ruta}; usando configuración por defecto.")

    cfg = _merge(DEFAULTS, datos)

    # Validaciones de rutas críticas.
    carpeta_fondos = cfg["entrada"]["carpeta_fondos"]
    if not os.path.isdir(carpeta_fondos):
        raise FileNotFoundError(
            f"No existe la carpeta de fondos: {carpeta_fondos}"
        )

    csv = cfg["entrada"]["csv"]
    if not os.path.isfile(csv):
        raise FileNotFoundError(f"No existe el CSV de textos: {csv}")

    musica = cfg["entrada"]["musica"]
    if not os.path.isfile(musica):
        raise FileNotFoundError(f"No existe el archivo de música: {musica}")

    return cfg
