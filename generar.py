"""Generador de reels — orquestador del batch.

Lee la configuración (config.yaml) y el CSV de textos, y genera un reel
independiente por cada fila. Uso:

    python generar.py [ruta_config.yaml]
"""
import os
import sys

from reels import audio, background, branding, csv_loader, renderer, text
from reels.config import cargar_config


def main(ruta_config="config.yaml"):
    cfg = cargar_config(ruta_config)

    render_cfg = cfg["render"]
    tamano = (render_cfg["ancho"], render_cfg["alto"])
    duracion_max = render_cfg["duracion_max"]

    # Recursos compartidos por todos los reels.
    ruta_fondo = background.elegir_fondo(cfg["entrada"]["carpeta_fondos"])
    ruta_musica = cfg["entrada"]["musica"]

    items = csv_loader.cargar_textos(
        cfg["entrada"]["csv"], prefijo=cfg["salida"]["prefijo"]
    )

    carpeta_salida = cfg["salida"]["carpeta"]
    os.makedirs(carpeta_salida, exist_ok=True)

    total = len(items)
    exitos = 0
    print(f"Se generarán {total} reel(s) desde {cfg['entrada']['csv']}.\n")

    for item in items:
        ruta_salida = os.path.join(carpeta_salida, item["nombre_salida"])
        print(f"[{item['indice']}/{total}] generando {item['nombre_salida']}: "
              f"\"{item['texto']}\"")
        try:
            fondo, duracion = background.preparar_fondo(
                ruta_fondo, duracion_max, *tamano
            )
            pista = audio.preparar_audio(ruta_musica, duracion)
            capas_texto = text.crear_capas_texto(
                item["texto"], cfg["texto"], tamano, duracion
            )
            logo = branding.crear_logo(cfg["branding"], tamano, duracion)

            renderer.renderizar(
                ruta_salida, fondo, pista, capas_texto, logo, render_cfg
            )
            exitos += 1
        except Exception as e:  # no abortar todo el batch por una fila
            print(f"  [error] No se pudo generar {item['nombre_salida']}: {e}")

    print(f"\nListo: {exitos}/{total} reel(s) generados en {carpeta_salida}/")


if __name__ == "__main__":
    ruta = sys.argv[1] if len(sys.argv) > 1 else "config.yaml"
    main(ruta)
