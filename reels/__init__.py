"""Paquete del generador de reels.

Cada módulo encapsula una responsabilidad:
- config: carga y valida config.yaml
- csv_loader: lee los textos del CSV
- background: prepara el video de fondo
- audio: prepara la pista de audio
- text: crea las capas de texto (con contorno y sombra)
- branding: crea el logo / marca de agua
- renderer: compone las capas y exporta el MP4
"""
