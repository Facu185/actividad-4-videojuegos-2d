"""
Genera los efectos de sonido WAV sintetizando tonos simples (solo librería
estándar de Python, sin archivos externos).
Correr una sola vez: python assets/generar_sonidos.py
"""
import math
import os
import struct
import wave

BASE = os.path.dirname(os.path.abspath(__file__))
SFX_DIR = os.path.join(BASE, "sfx")
os.makedirs(SFX_DIR, exist_ok=True)

SAMPLE_RATE = 44100


def tono(notas, volumen=0.4):
    """notas: lista de (frecuencia_hz, duracion_seg). Devuelve las muestras
    concatenadas, con un fade in/out en cada nota para evitar "clicks"."""
    muestras = []
    for freq, dur in notas:
        n = int(SAMPLE_RATE * dur)
        borde = max(1, int(n * 0.1))
        for i in range(n):
            t = i / SAMPLE_RATE
            fade = min(i / borde, (n - i) / borde, 1.0)
            valor = math.sin(2 * math.pi * freq * t) * volumen * fade
            muestras.append(int(valor * 32767))
    return muestras


def guardar_wav(muestras, nombre):
    ruta = os.path.join(SFX_DIR, nombre)
    with wave.open(ruta, "w") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(SAMPLE_RATE)
        f.writeframes(struct.pack("<" + "h" * len(muestras), *muestras))
    print("Generado:", nombre)


guardar_wav(tono([(440, 0.06)]), "rebote.wav")
guardar_wav(tono([(880, 0.08)]), "ladrillo.wav")
guardar_wav(tono([(300, 0.15), (200, 0.2)]), "vida_perdida.wav")
guardar_wav(tono([(523, 0.1), (659, 0.1), (784, 0.1), (1046, 0.25)]), "ganaste.wav")
guardar_wav(tono([(400, 0.15), (300, 0.15), (200, 0.35)]), "perdiste.wav")

print("Listo.")
