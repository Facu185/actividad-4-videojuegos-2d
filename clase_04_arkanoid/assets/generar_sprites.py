"""
Genera los sprites PNG del Arkanoid con Pygame (sin depender de archivos externos).
Correr una sola vez: python assets/generar_sprites.py
"""
import os
import pygame

pygame.init()

BASE = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE, "img")
os.makedirs(IMG_DIR, exist_ok=True)


def guardar(surf, nombre):
    pygame.image.save(surf, os.path.join(IMG_DIR, nombre))
    print("Generado:", nombre)


# Paleta 120x15, con un brillo arriba para dar sensación de volumen
paleta = pygame.Surface((120, 15), pygame.SRCALPHA)
pygame.draw.rect(paleta, (60, 140, 220), (0, 0, 120, 15), border_radius=6)
pygame.draw.rect(paleta, (150, 205, 255), (4, 2, 112, 5), border_radius=3)
guardar(paleta, "paddle.png")

# Pelota 16x16, con un punto de brillo para simular esfera
pelota = pygame.Surface((16, 16), pygame.SRCALPHA)
pygame.draw.circle(pelota, (255, 255, 255), (8, 8), 8)
pygame.draw.circle(pelota, (190, 215, 255), (6, 6), 3)
guardar(pelota, "ball.png")

# Ladrillos 70x20 — un color por fila, con borde oscuro y brillo superior
colores = {
    "brick_red.png": (220, 70, 70),
    "brick_orange.png": (230, 140, 60),
    "brick_yellow.png": (230, 210, 70),
    "brick_green.png": (90, 200, 110),
}
for nombre, color in colores.items():
    b = pygame.Surface((70, 20), pygame.SRCALPHA)
    pygame.draw.rect(b, color, (0, 0, 70, 20), border_radius=4)
    claro = tuple(min(255, c + 45) for c in color)
    pygame.draw.rect(b, claro, (3, 2, 64, 5), border_radius=3)
    oscuro = tuple(max(0, c - 45) for c in color)
    pygame.draw.rect(b, oscuro, (0, 0, 70, 20), 2, border_radius=4)
    guardar(b, nombre)

pygame.quit()
print("Listo.")
