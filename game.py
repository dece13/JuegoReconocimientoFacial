import pygame
import cv2
import mediapipe as mp
import time
import sys

ojoAbierto = True
bocaAbierta = False
jump = False
pointsSalto=0

#Variables para el reconocimiento facial
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces=1)

pointYArriba = 0
pointYAbajo = 0

PointYArribaOjo=0
PointYAbajoOjo=0

# Inicializa la ventana del juego con pygame
pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

# Carga la imagen del personaje
player_image = pygame.image.load("personaje.png")
player_image = pygame.transform.scale(player_image, (100, 100))
player_rect = player_image.get_rect()


# Carga la imagen del tronco 
imagen_tronco = pygame.image.load("tronco.png")
imagen_tronco = pygame.transform.scale(imagen_tronco, (100, 100))
tronco_rect= imagen_tronco.get_rect()

# Ubicacion del personaje
player_rect.x= 50
player_rect.y= 300

# Ubicacion del tronco
tronco_rect.x= 500
tronco_rect.y= 320

# Crear collider
collider_Tronco = pygame.Rect(tronco_rect.x, tronco_rect.y+28, 50, 50)
collider_Player = pygame.Rect(50, 300, 50, 50)

cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Camera", 640, 480)

gameOver=False

# Crear un objeto de fuente para mostrar texto
font = pygame.font.SysFont(None, 36)

while cap.isOpened():
    # Verifica si hay eventos de pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cap.release()
            pygame.quit()
            sys.exit()

    ret, frame = cap.read()

    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = faceMesh.process(frameRGB)

    # Dibuja la malla facial sobre el marco de la cámara
    if results.multi_face_landmarks:
        for faceLms in results.multi_face_landmarks:
            for id, lm in enumerate(faceLms.landmark):
                ih, iw, ic = frame.shape
                x, y = int(lm.x * iw), int(lm.y * ih)
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

    cv2.imshow("Camera", frame)
    
    pygame.display.update()
    clock.tick(60)
    if results.multi_face_landmarks:
        for faceLms in results.multi_face_landmarks:
            mpDraw.draw_landmarks(frame, faceLms, mpFaceMesh.FACEMESH_CONTOURS)

           
            for id, lm in enumerate(faceLms.landmark):
                ih, iw, ic = frame.shape
                x, y = int(lm.x * iw), int(lm.y * ih)

                

                if id == 13:
                    pointYAbajo = y

                if id == 14:
                    pointYArriba = y
                if id == 145:
                    PointYArribaOjo = y
                if id == 159:
                    PointYAbajoOjo = y

        if pointYArriba - pointYAbajo < 6:
            bocaAbierta = False
        if pointYArriba - pointYAbajo > 6:
            bocaAbierta = True

        if PointYArribaOjo - PointYAbajoOjo < 6:
            ojoAbierto = False
        if PointYArribaOjo - PointYAbajoOjo > 6:
            ojoAbierto = True
        
    

    # Actualiza el estado del personaje
    if bocaAbierta and not jump:
        jump = True
        player_rect.y -= 55
    elif not bocaAbierta and jump:
        jump = False
        player_rect.y += 55
    
    if tronco_rect.x <= -100:
        pointsSalto+=1
        tronco_rect.x = 500;
        collider_Tronco.x = 500;
    if gameOver==False:
        tronco_rect.x -= 10;
        collider_Tronco.x -=10;
    
    if ojoAbierto==False and gameOver==True:
        gameOver=False
        pointsSalto=0
        tronco_rect.x = 500;
        collider_Tronco.x = 500;
    
    if collider_Tronco.colliderect(player_rect):
        gameOver=True
    
    # Dibuja el fondo de la ventana
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (255, 0, 0), collider_Tronco, 1)
    pygame.draw.rect(screen, (255, 10, 0), player_rect, 1)
    screen.blit(player_image, player_rect)
    screen.blit(imagen_tronco, tronco_rect)

    # Mostrar el número de puntos de salto en la esquina superior derecha
    text = font.render(f'Puntos: {pointsSalto}', True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.topright = (630, 10)
    screen.blit(text, text_rect)

    pygame.display.update()

    clock.tick(60)


    #
