import sys
import pygame

pygame.init()
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
reloj = pygame.time.Clock()

pala = pygame.Rect(ANCHO // 2 - 60, ALTO - 40, 120, 15)
pelota = pygame.Rect(ANCHO // 2 - 8, ALTO // 2, 16, 16)
vel_x, vel_y = 5, -5

# Ladrillos: una fila de rectángulos
FILAS, COLS = 4, 10
ladrillos = []
for fila in range(FILAS):
    for col in range(COLS):
        ladrillos.append(pygame.Rect(col * 80 + 5, fila * 30 + 40, 70, 20))

vidas = 3
puntos = 0
ladrillos_destruidos = 0
ganaste = False
fuente = pygame.font.SysFont(None, 72)

ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    # Paleta sigue al mouse
    pala.x = pygame.mouse.get_pos()[0] - pala.width // 2
    pala.x = max(0, min(ANCHO - pala.width, pala.x))

    if not ganaste:
        # Mover la pelota
        pelota.x += vel_x
        pelota.y += vel_y

        # Rebotes con paredes
        if pelota.left <= 0 or pelota.right >= ANCHO:
            vel_x *= -1
        if pelota.top <= 0:
            vel_y *= -1
        if pelota.colliderect(pala) and vel_y > 0:
            vel_y *= -1

        # Destruir ladrillos
        for ladrillo in ladrillos[:]:
            if pelota.colliderect(ladrillo):
                ladrillos.remove(ladrillo)
                vel_y *= -1
                puntos += 10
                ladrillos_destruidos += 1
                if ladrillos_destruidos % 5 == 0:
                    vel_x += 1 if vel_x > 0 else -1
                    vel_y += 1 if vel_y > 0 else -1
                break

        # Victoria
        if len(ladrillos) == 0:
            ganaste = True

        # Perder vida
        if pelota.bottom >= ALTO:
            vidas -= 1
            pelota.center = (ANCHO // 2, ALTO // 2)
            if vidas == 0:
                ejecutando = False

    # Dibujar
    pantalla.fill((15, 15, 30))
    pygame.draw.rect(pantalla, (90, 180, 255), pala)
    pygame.draw.rect(pantalla, (255, 255, 255), pelota)
    for ladrillo in ladrillos:
        pygame.draw.rect(pantalla, (255, 120, 120), ladrillo)

    if ganaste:
        texto = fuente.render("¡Ganaste!", True, (255, 220, 60))
        rect = texto.get_rect(center=(ANCHO // 2, ALTO // 2))
        pantalla.blit(texto, rect)

    pygame.display.set_caption(f"Arkanoid - Puntos: {puntos} - Vidas: {vidas} - Ladrillos: {len(ladrillos)}")
    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
sys.exit()
