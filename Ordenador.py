#Para que me detecte el encoding del archivo
#-*- coding: utf-8 -*-

import cv2
import time
import numpy as np

class fruta():
    def __init__(self, tipo):
        self.seleccion=tipo
        self.puntos=0
        self.alfa=0
        self.disponible=1
        self.pos_x=np.random.random_integers(ancho_img);
        self.pos_y=np.random.random_integers(alto_img);
        self.sel_img()
        self.sel_puntaje()
        
    def sel_img(self):
        self.imagenes = { 'banano': 'banano.png', 'cereza': 'cereza.png', 'fresa': 'fresa.png', 'limon': 'limon.png', 'pina': 'pina.png', 'sandia': 'sandia.png' }
        self.imagen=cv2.imread(self.imagenes[self.seleccion],-1)
        self.alto, self.ancho = self.imagen.shape[:2]
        self.pos_x=np.random.random_integers(ancho_img-(self.ancho+1));
        self.pos_y=np.random.random_integers(alto_img-(self.alto+1));
               
    def sel_puntaje(self):
        self.puntajes = { 'banano': 20, 'cereza': 1, 'fresa': 15, 'limon': 10, 'pina': 15, 'sandia': 5  }
        self.puntos=self.puntajes[self.seleccion]
        

    def dibujar(self,fondo):
        self.fondo=fondo
        if self.disponible==0:
            self.sel_img()
            self.disponible = 1
        for i in range(self.alto):
            for j in range(self.ancho):
                if self.imagen[i,j,3]>20:
                    self.fondo[self.pos_y+i,self.pos_x+j,[0,1,2]]=self.imagen[i,j,[0,1,2]];
        return self.fondo;
    
    def matar(self,punto_x, punto_y,puntuacion):
        if self.disponible==1:
            self.punto_x=punto_x
            self.punto_y=punto_y
            if self.punto_x>self.pos_x and self.punto_x<self.pos_x+self.ancho: 
                    if self.punto_y>self.pos_y and self.punto_y<self.pos_y+self.alto: 
                        self.disponible=0
                        print("Muerto "+ self.seleccion)
                        puntuacion = puntuacion + 1
        return puntuacion

# A partir de aqui se hace la ejecucion del programa
cam = cv2.VideoCapture(0)

winName = "Detector de Movimiento"
#cv2.namedWindow(winName, cv2.CV_WINDOW_AUTOSIZE)

# Read three images first:
primera =cam.read()[1]
segunda = cam.read()[1]

alto_img, ancho_img = primera.shape[:2]

banano=fruta('banano')
cereza=fruta('cereza')
fresa=fruta('fresa')
limon=fruta('limon')
pina=fruta('pina')
sandia=fruta('sandia')

puntuacion = 0

while True:

    pblur=cv2.blur(primera,(3,3))
    sblur=cv2.blur(segunda,(3,3))
    img = cv2.absdiff(cv2.cvtColor(pblur, cv2.COLOR_RGB2GRAY), cv2.cvtColor(sblur, cv2.COLOR_RGB2GRAY))
    
    ret, thresh = cv2.threshold(img,18,255,0)
    img2, contornos, hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)   
    
    n = 0
    cx = np.ones(len(contornos))
    cy = np.ones(len(contornos))
    
    if len(contornos) > 0:
        for i in range(len(contornos)):
            if cv2.contourArea(contornos[i-1]) > 1:  
                cv2.drawContours(sblur,[contornos[i-1]],0 ,(0,255,0), 3)
                Momento = cv2.moments(contornos[i-1])
                cx[i-1],cy[i-1] =[int(Momento['m01']/Momento['m00']),int(Momento['m10']/Momento['m00'])]
                cv2.circle(sblur, (int(cy[i-1]),int(cx[i-1])),5,255,-1)
                for j in range(len(contornos[i-1])):
                    '''
                    print('---')
                    print(contornos[i-1][j][0][0])
                    print('---')
                    '''
                    puntuacion= banano.matar(contornos[i-1][j][0][0],contornos[i-1][j][0][1],puntuacion)
                    puntuacion=cereza.matar(contornos[i-1][j][0][0],contornos[i-1][j][0][1],puntuacion)
                    puntuacion=fresa.matar(contornos[i-1][j][0][0],contornos[i-1][j][0][1],puntuacion)
                    puntuacion=limon.matar(contornos[i-1][j][0][0],contornos[i-1][j][0][1],puntuacion)
                    puntuacion=pina.matar(contornos[i-1][j][0][0],contornos[i-1][j][0][1],puntuacion)
                    puntuacion=sandia.matar(contornos[i-1][j][0][0],contornos[i-1][j][0][1],puntuacion)
                    #'''
                puntuacion=banano.matar(cx[i-1],cy[i-1],puntuacion)
                puntuacion=cereza.matar(cx[i-1],cy[i-1],puntuacion)
                puntuacion=fresa.matar(cx[i-1],cy[i-1],puntuacion)
                puntuacion=limon.matar(cx[i-1],cy[i-1],puntuacion)
                puntuacion=pina.matar(cx[i-1],cy[i-1],puntuacion)
                puntuacion=sandia.matar(cx[i-1],cy[i-1],puntuacion)
                n = n + 1
    fuente = cv2.FONT_HERSHEY_SIMPLEX
    #PARA DIBUJAR EL NÚMERO DE PARAMECIOS
    #cv2.putText(sblur,str(n),(360,50),fuente,2,(0,255,0),2,cv2.LINE_AA)

    #DIBUJAMOS PUNTUACIÓN
    cv2.putText(sblur,'Has comido ' + str(puntuacion) + ' frutas',(150,50),fuente,1,(0,255,0),2,cv2.LINE_AA)
    
    sblur=banano.dibujar(sblur)
    sblur=cereza.dibujar(sblur)
    sblur=fresa.dibujar(sblur)
    sblur=limon.dibujar(sblur)
    sblur=pina.dibujar(sblur)
    sblur=sandia.dibujar(sblur)
    
    cv2.imshow("Comer Frutillas",sblur)
    
    # Read next image
    primera = segunda
    segunda = cam.read()[1]
    
    if banano.disponible==0 and cereza.disponible==0 and fresa.disponible==0 and limon.disponible==0 and pina.disponible==0 and sandia.disponible==0:
        cv2.destroyWindow(winName)
        print("Sin fruticas :(")
        break

    key = cv2.waitKey(5)
    if key == 27:
        cv2.destroyWindow(winName)
        break

print "Hasta Luego"