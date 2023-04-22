import cv2
import mediapipe as mp
import time

bocaAbierta=False


pTime=0

mpDraw = mp.solutions.drawing_utils
mpFaceMesh =mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces=1) 

pointYArriba=0
pointYAbajo=0
def camaraJuego():
    cap= cv2.VideoCapture(0)
    
    ret, frame = cap.read()
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = faceMesh.process(frameRGB)
    if results.multi_face_landmarks:
        for faceLms in results.multi_face_landmarks:
            mpDraw.draw_landmarks(frame,faceLms,mpFaceMesh.FACEMESH_CONTOURS)

            for id,lm in enumerate(faceLms.landmark):
                ih, iw, ic = frame.shape
                x,y = int(lm.x*iw), int(lm.y*ih)
                if id==13:
                    pointYAbajo=y
                if id==14:
                    pointYArriba=y
                   

        if pointYArriba-pointYAbajo<6:
            bocaAbierta=False
        if pointYArriba-pointYAbajo>6:
            bocaAbierta=True
        
    # Mostrar fps en pantalla no necesario pero chimba

    # Mostrar camra en pantalla
    # Oprimir q para salir
    