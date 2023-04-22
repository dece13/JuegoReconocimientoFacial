import cv2
import mediapipe as mp
import time

bocaAbierta=False

cap= cv2.VideoCapture(0)
ret,frame= cap.read()

pTime=0

mpDraw = mp.solutions.drawing_utils
mpFaceMesh =mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces=1) 

pointYArriba=0
pointYAbajo=0

while cap.isOpened():
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
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(frame, f'fps: {int(fps)}',(20,70),cv2.FONT_HERSHEY_PLAIN,
                3,(0,255,0),3)


    # Mostrar camra en pantalla
    cv2.imshow('video',frame)


    # Oprimir q para salir
    if cv2.waitKey(1)& 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

cap= cv2.VideoCapture(0)

cap.isOpened()

cap.release()

 