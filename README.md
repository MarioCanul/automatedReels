# MisReels

Generador de reels verticales (9:16, 1080×1920) para redes sociales. A partir de un **video de fondo**, una **pista de música** y un **CSV con frases**, produce un MP4 profesional **por cada fila del CSV** — con texto legible (contorno + sombra), tipografía personalizable y logo/marca de agua opcional.

Construido en Python con [MoviePy](https://zulko.github.io/moviepy/) 2.x.

## Requisitos

- Python 3.13 (incluido en el `venv/` del proyecto)
- FFmpeg (se instala automáticamente vía `imageio-ffmpeg`)

## Instalación

```bash
# Crear el entorno (si no existe)
python -m venv venv

# Instalar dependencias
./venv/Scripts/python.exe -m pip install -r requirements.txt
```

> En macOS/Linux usa `./venv/bin/python` en lugar de `./venv/Scripts/python.exe`.

## Uso

1. Coloca uno o más videos `.mp4` en `fondos/` (se usa el primero por orden alfabético).
2. Coloca tu música en `musica/musica.mp3` (o cambia la ruta en `config.yaml`).
3. (Opcional) Pon una fuente `.ttf` en `assets/fonts/` y un logo en `assets/logo.png`.
4. Escribe tus frases en `textos.csv`, una por línea bajo la columna `texto`.
5. Genera los reels:

```bash
./venv/Scripts/python.exe generar.py
```

Cada fila del CSV produce un archivo independiente en `salida/`: `reel_01.mp4`, `reel_02.mp4`, … (nunca se sobrescriben).

Para usar otra configuración:

```bash
./venv/Scripts/python.exe generar.py mi-config.yaml
```

## El CSV

Una sola columna obligatoria llamada `texto`. Las filas vacías se ignoran.

```csv
texto
La disciplina vence a la motivación
Empieza antes de sentirte listo
Nunca subestimes el interés compuesto
```

## Configuración (`config.yaml`)

Todo el estilo y los ajustes se controlan desde `config.yaml`, sin tocar código. Si falta una clave, se usa un valor por defecto. Secciones principales:

| Sección | Controla |
|---|---|
| `entrada` | Carpeta de fondos, archivo de música, ruta del CSV |
| `salida` | Carpeta de salida y prefijo del nombre (`reel` → `reel_01.mp4`) |
| `render` | Ancho, alto, fps, duración máxima, codecs |
| `texto` | Fuente, tamaño, color, posición vertical, contorno y sombra |
| `branding` | Logo/marca de agua: activado, ruta, posición, escala y opacidad |

El branding viene **desactivado** por defecto; actívalo con `branding.activado: true` y una imagen en `assets/`. Si la fuente `.ttf` configurada no existe, se usa la fuente por defecto del sistema (con un aviso).

## Estructura del proyecto

```
MisReels/
├── config.yaml          # configuración central
├── requirements.txt     # dependencias
├── generar.py           # orquestador del batch
├── reels/               # módulos (config, csv_loader, background, audio, text, branding, renderer)
├── textos.csv           # frases de entrada
├── fondos/              # videos de fondo (.mp4)
├── musica/              # música
├── assets/              # fuentes (.ttf) y logo
└── salida/              # reels generados
```

> Las carpetas de medios (`fondos/`, `musica/`, `salida/`, `assets/`) están en `.gitignore` y no se versionan; las fuentes en `assets/fonts/` sí.
