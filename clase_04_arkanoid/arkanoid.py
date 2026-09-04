import os
import sys
import pygame

pygame.init()
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
reloj = pygame.time.Clock()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, "assets", "img")
SFX_DIR = os.path.join(BASE_DIR, "assets", "sfx")

# --- Sprites ---
img_pala = pygame.image.load(os.path.join(IMG_DIR, "paddle.png")).convert_alpha()
img_pelota = pygame.image.load(os.path.join(IMG_DIR, "ball.png")).convert_alpha()
imgs_ladrillos = [
    pygame.image.load(os.path.join(IMG_DIR, "brick_red.png")).convert_alpha(),
    pygame.image.load(os.path.join(IMG_DIR, "brick_orange.png")).convert_alpha(),
    pygame.image.load(os.path.join(IMG_DIR, "brick_yellow.png")).convert_alpha(),
    pygame.image.load(os.path.join(IMG_DIR, "brick_green.png")).convert_alpha(),
]

# --- Sonidos ---
sonido_rebote = pygame.mixer.Sound(os.path.join(SFX_DIR, "rebote.wav"))
sonido_ladrillo = pygame.mixer.Sound(os.path.join(SFX_DIR, "ladrillo.wav"))
sonido_vida = pygame.mixer.Sound(os.path.join(SFX_DIR, "vida_perdida.wav"))
sonido_ganaste = pygame.mixer.Sound(os.path.join(SFX_DIR, "ganaste.wav"))
sonido_perdiste = pygame.mixer.Sound(os.path.join(SFX_DIR, "perdiste.wav"))

fuente_grande = pygame.font.SysFont(None, 72)
fuente_boton = pygame.font.SysFont(None, 36)
BOTON = pygame.Rect(ANCHO // 2 - 90, ALTO // 2 + 30, 180, 50)

FILAS, COLS = 4, 10


def nuevos_ladrillos():
    lista = []
    for fila in range(FILAS):
        img = imgs_ladrillos[fila % len(imgs_ladrillos)]
        for col in range(COLS):
            rect = pygame.Rect(col * 80 + 5, fila * 30 + 40, 70, 20)
            lista.append({"rect": rect, "img": img})
    return lista


def reiniciar():
    global pala, pelota, vel_x, vel_y, ladrillos, vidas, puntos
    global ladrillos_destruidos, ganaste, perdiste
    pala = pygame.Rect(ANCHO // 2 - 60, ALTO - 40, 120, 15)
    pelota = pygame.Rect(ANCHO // 2 - 8, ALTO // 2, 16, 16)
    vel_x, vel_y = 5, -5
    ladrillos = nuevos_ladrillos()
    vidas = 3
    puntos = 0
    ladrillos_destruidos = 0
    ganaste = False
    perdiste = False


reiniciar()

ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if (ganaste or perdiste) and BOTON.collidepoint(evento.pos):
                reiniciar()

    # Paleta sigue al mouse
    pala.x = pygame.mouse.get_pos()[0] - pala.width // 2
    pala.x = max(0, min(ANCHO - pala.width, pala.x))

    if not ganaste and not perdiste:
        # Mover la pelota
        pelota.x += vel_x
        pelota.y += vel_y

        # Rebotes con paredes
        if pelota.left <= 0 or pelota.right >= ANCHO:
            vel_x *= -1
            sonido_rebote.play()
        if pelota.top <= 0:
            vel_y *= -1
            sonido_rebote.play()
        if pelota.colliderect(pala) and vel_y > 0:
            vel_y *= -1
            sonido_rebote.play()

        # Destruir ladrillos
        for ladrillo in ladrillos[:]:
            if pelota.colliderect(ladrillo["rect"]):
                ladrillos.remove(ladrillo)
                vel_y *= -1
                puntos += 10
                ladrillos_destruidos += 1
                sonido_ladrillo.play()
                if ladrillos_destruidos % 5 == 0:
                    vel_x += 1 if vel_x > 0 else -1
                    vel_y += 1 if vel_y > 0 else -1
                break

        # Victoria
        if len(ladrillos) == 0:
            ganaste = True
            sonido_ganaste.play()

        # Perder vida
        if pelota.bottom >= ALTO:
            vidas -= 1
            pelota.center = (ANCHO // 2, ALTO // 2)
            vel_y = -abs(vel_y)  # relanzar hacia arriba, no seguir cayendo
            if vidas == 0:
                perdiste = True
                sonido_perdiste.play()
            else:
                sonido_vida.play()

    # Dibujar
    pantalla.fill((15, 15, 30))
    pantalla.blit(img_pala, pala)
    pantalla.blit(img_pelota, pelota)
    for ladrillo in ladrillos:
        pantalla.blit(ladrillo["img"], ladrillo["rect"])

    if ganaste or perdiste:
        mensaje = "¡Ganaste!" if ganaste else "Perdiste"
        color = (255, 220, 60) if ganaste else (255, 90, 90)
        texto = fuente_grande.render(mensaje, True, color)
        rect_texto = texto.get_rect(center=(ANCHO // 2, ALTO // 2 - 40))
        pantalla.blit(texto, rect_texto)

        pygame.draw.rect(pantalla, (60, 200, 100), BOTON, border_radius=8)
        etiqueta = fuente_boton.render("Reintentar", True, (15, 15, 30))
        rect_etiqueta = etiqueta.get_rect(center=BOTON.center)
        pantalla.blit(etiqueta, rect_etiqueta)

    pygame.display.set_caption(f"Arkanoid - Puntos: {puntos} - Vidas: {vidas} - Ladrillos: {len(ladrillos)}")
    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
sys.exit()
