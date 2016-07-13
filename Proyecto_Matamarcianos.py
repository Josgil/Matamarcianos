#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Curso de "Tratamiento de datos, juegos y programación gráfica en Python
#Organizado por la Universidad de Granada.
#Proyecto final

#José Francisco Gil Sánchez
#@PichonceteGM    mail: jfgilsanchez@gmail.com
#Realizado en junio de 2016.
#Ultima actualización el 12 de julio de 2016


##############################################################################
############-----------------------Creditos-----------------------############
##############################################################################

#Juego Matamarcianos creado por José Francisco Gil Sánchez como proyecto final
#del curso "Tratamieto de datos, juegos y programación gráfica en Python,
#5ª edición", impartido el Centro de enseñanzas virtuales de la Universidad
#de Granada.

#Dedico este juego a mi padre, que aun a día de hoy, cuando me ve delante del
#PC, me sigue diciendo aquello de: "¿Ya estas matando marcianos?"

##############################################################################
############-----------------------Licencia-----------------------############
##############################################################################


############-----------------------Español-----------------------############

#Este programa es software libre; usted puede redistribuirlo y / o modificarlo
#bajo los términos de la Licencia Pública General de GNU según lo publicado por
#la Fundación para el Software Libre; ya sea la versión 2 de la Licencia, o
#(A su elección) cualquier versión posterior.

#Este programa se distribuye con la esperanza de que sea útil,
#pero SIN NINGUNA GARANTÍA; ni siquiera la garantía implícita de
#COMERCIALIZACIÓN o IDONEIDAD PARA UN FIN PARTICULAR. Ver la
#Licencia Pública General de GNU para más detalles.

#Debería haber recibido una copia de la Licencia Pública General de GNU
#junto con este programa; si no, escriba a la Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#MA 02110-1301, EE.UU..


############-----------------------English-----------------------############


#This program is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 2 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#MA 02110-1301, USA.


##############################################################################
############-----------------------Librerias----------------------############
##############################################################################

#Importamos libreria para sqlite3
#Se va a trabajar con sqlite3 para poder mover la Base de Datos junto con el...
#...resto de archivos del juego
import sqlite3

#Importamos librerias para PyGame, incluido random para crear las naves enemigas
import pygame
import random
#Importamos constantes locales de pygame
from pygame.locals import *

##############################################################################
####################----------------PyGame----------------####################
#####Aqui comenzamos a crear funciones para su uso posterior en el juego.#####
##############################################################################


##############################################################################
############------------------------Clases------------------------############
##############################################################################

#Esta clase define las naves enemigas
class Bloque(pygame.sprite.Sprite):
    def __init__(self, imagen):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([50, 50])
        self.image = pygame.image.load("Recursos/Killer.bmp")
        transparente = self.image.get_at((0, 0))
        self.image.set_colorkey(transparente)

        self.rect = self.image.get_rect()


#Esta clase define nuestra nave
class Protagonista(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([50, 50])

        self.image = pygame.image.load("Recursos/Factory1.bmp")
        transparente = self.image.get_at((0, 0))
        self.image.set_colorkey(transparente)

        self.rect = self.image.get_rect()

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0] - 50


#Esta clase define el proyectil
class Proyectil(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([20, 20])

        self.image = pygame.image.load("Recursos/disparo.bmp")
        transparente = self.image.get_at((0, 0))
        self.image.set_colorkey(transparente)

        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y -= 5

#Esta clase define la posición del ratón
class Cursor(pygame.Rect):
    def __init__(self):
        pygame.Rect.__init__(self, 0, 0, 1, 1)

    def update(self):
        self.left, self.top = pygame.mouse.get_pos()

#Esta clase provoca el cambio de imagenes al sutuar el cursor sobre el botón
class Boton(pygame.sprite.Sprite):
    def __init__(self, imagen1, imagen2, x = 100, y = 100):
        self.imagen_normal = imagen1
        self.imagen_seleccion = imagen2
        self.imagen_actual = self.imagen_normal
        self.rect = self.imagen_actual.get_rect()
        self.rect.left, self.rect.top = (x, y)


    def update(self, pantalla, cursor):
        if cursor.colliderect(self.rect):
            self.imagen_actual = self.imagen_seleccion
        else: self.imagen_actual = self.imagen_normal

        pantalla.blit(self.imagen_actual, self.rect)
        transparente = self.imagen_actual.get_at((0, 0))
        self.imagen_actual.set_colorkey(transparente)

##############################################################################
############-----------------------Ventana------------------------############
##############################################################################

#Aquí comenzamos a crear la ventana

#Iniciamos PyGame
pygame.init()

#Dimensiones de la pantalla
largo_pantalla = 1200
alto_pantalla = 600
pantalla = pygame.display.set_mode([largo_pantalla, alto_pantalla])

#Titulo
pygame.display.set_caption("Matamarcianos")

#Fondo
Fondo = pygame.image.load("Recursos/Fondo.jpg")
Fondo_GameOver = pygame.image.load("Recursos/Fondo_GameOver.png")
Enemigos = pygame.image.load("Recursos/Killer.bmp")
Fondo_instrucciones = pygame.image.load("Recursos/Fondo_instrucciones.png")
Fondo_creditos = pygame.image.load("Recursos/Fondo_creditos.png")
texto_clasificacion = "Clasificación"

#Reloj
reloj = pygame.time.Clock()
numero_de_fotogramas = 0
tasa_fotogramas = 60
instante_de_partida = 90

#Fuente
Fuente = pygame.font.Font(None, 40)
puntuacion = 0
Mensaje = Fuente.render("Puntuacion: %d" % (puntuacion), 0, (0, 0, 255))

#Sonido del Disparo y Explosión
Disparo = pygame.mixer.Sound("Recursos/disparo.wav")
Explosion = pygame.mixer.Sound("Recursos/explosion.wav")
Explosion.set_volume(0.3)


#Para iniciar la interacción hasta que finalice el juego
hecho = False
mostrar_menu = True


#Cargamos los diferentes botones que se van a usar en los menús
jugar_off = pygame.image.load("Recursos/Botones/jugar_off.png")
jugar_on = pygame.image.load("Recursos/Botones/jugar_on.png")
instrucciones_off = pygame.image.load("Recursos/Botones/instrucciones_off.png")
instrucciones_on = pygame.image.load("Recursos/Botones/instrucciones_on.png")
clasificacion_off = pygame.image.load("Recursos/Botones/clasificacion_off.png")
clasificacion_on = pygame.image.load("Recursos/Botones/clasificacion_on.png")
creditos_off = pygame.image.load("Recursos/Botones/creditos_off.png")
creditos_on = pygame.image.load("Recursos/Botones/creditos_on.png")
salir_off = pygame.image.load("Recursos/Botones/salir_off.png")
salir_on = pygame.image.load("Recursos/Botones/salir_on.png")
volver_off = pygame.image.load("Recursos/Botones/volver_off.png")
volver_on = pygame.image.load("Recursos/Botones/volver_on.png")


#Cargamos el cursor
cursor1 = Cursor()

#Colores
blanco = (255, 255, 255)
rojo = (200, 0, 0)
azul = (0, 0, 200)
colordefondo = blanco
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

##############################################################################
############-------------------Lista de Sprites-------------------############
##############################################################################

#Esta es una lista de cada sprite, bloques y protagonista.
lista_de_todos_los_sprites = pygame.sprite.Group()

#Lista de cada bloque del juego
lista_bloques = pygame.sprite.Group()

#Lista de cada proyectil
lista_proyectiles = pygame.sprite.Group()

#-----Creamos las naves enemigas...
for i in range(25):
    bloque = Bloque(Enemigos)
    #Ubicación aleatoria
    bloque.rect.x = random.randrange(largo_pantalla - 50)
    bloque.rect.y = random.randrange(350)
    #Añadimos el bloque a la lista de objetos
    lista_bloques.add(bloque)
    lista_de_todos_los_sprites.add(bloque)

#...Protagonista
protagonista = Protagonista()
lista_de_todos_los_sprites.add(protagonista)

#Asiganado datos previos
puntuacion = 0
protagonista.rect.y = 500

#Controles del bucle
hecho = False
mostrar_menu = True
jugar = False
gameOver = False
instrucciones = False




##############################################################################
############-----------Aqui comienza el bucle del juego-----------############
##############################################################################

#El bucle principal depente de hecho, las opciones para salir del juego pasan...
#...por cambiar hecho a verdadero
while not hecho:

    #Se inicia mostrando el menú del juego
    while mostrar_menu:
        #Se cargan y situan los botones con sus dos imagenes
        boton1 = Boton(jugar_off, jugar_on, 500, 100)
        boton2 = Boton(instrucciones_off, instrucciones_on, 500, 200)
        boton3 = Boton(clasificacion_off, clasificacion_on, 500, 300)
        boton4 = Boton(creditos_off, creditos_on, 500, 400)
        boton5 = Boton(salir_off, salir_on, 500, 500)
        boton6 = Boton(volver_off, volver_on, 100, 500)
        #Si se clica sobre cada botón, pasa a su cometido.
        for evento in pygame.event.get():
            if evento.type == pygame.MOUSEBUTTONDOWN:

                #Jugar
                if cursor1.colliderect(boton1.rect):
                    mostrar_menu = False
                    jugar = True

                #Instrucciones
                if cursor1.colliderect(boton2.rect):
                    instrucciones = True
                    #Carga la pantalla instrucciones y el botón volver
                    while instrucciones:
                        pantalla.fill(NEGRO)
                        pantalla.blit(Fondo_instrucciones, [0, 0])
                        cursor1.update()
                        boton6.update(pantalla, cursor1)
                        reloj.tick(20)
                        pygame.display.flip()
                        for evento in pygame.event.get():
                            if evento.type == pygame.MOUSEBUTTONDOWN:
                                if cursor1.colliderect(boton6.rect):
                                    instrucciones = False

                #Clasificacion
                #Al entrar en Clasificación, se accede a la Base de Datos
                #Se cargan los 5 resultados más altos y se muestran
########## N O T A: Aunque es posible mostrarlos en pantalla, la falta de tiempo
########## me ha impedido añadir esta opción, así que se muestra en terminal
                if cursor1.colliderect(boton3.rect):
                    clasificacion = True
                    db = "Puntuaciones.db"
                    connection = sqlite3.connect(db)
                    cursor = connection.cursor()
                    query = "SELECT * FROM Puntuaciones ORDER BY Puntos DESC;"
                    cursor.execute(query)
                    #Ontenemos el resultado con fetchall
                    registros = cursor.fetchmany(5)
                    for registro in registros:
                        print registro

                    while clasificacion:
                        pantalla.fill(NEGRO)
                        texto = Fuente.render(texto_clasificacion, True, rojo)
                        pantalla.blit(texto, [10, 40])

                        cursor1.update()
                        boton6.update(pantalla, cursor1)
                        reloj.tick(20)
                        pygame.display.flip()
                        #Botón Volver
                        for evento in pygame.event.get():
                            if evento.type == pygame.MOUSEBUTTONDOWN:
                                if cursor1.colliderect(boton6.rect):
                                    clasificacion = False

                #Creditos
                if cursor1.colliderect(boton4.rect):
                    creditos = True
                    while creditos:
                        pantalla.fill(NEGRO)
                        pantalla.blit(Fondo_creditos, [0, 0])
                        cursor1.update()
                        boton6.update(pantalla, cursor1)
                        reloj.tick(20)
                        pygame.display.flip()
                        for evento in pygame.event.get():
                            if evento.type == pygame.MOUSEBUTTONDOWN:
                                if cursor1.colliderect(boton6.rect):
                                    creditos = False

                #Salir
                if cursor1.colliderect(boton5.rect):
                    mostrar_menu = False
                    hecho = True
            #Cerrar ventana desde X
            pygame.display.flip()
            if evento.type == pygame.QUIT:
                mostrar_menu = False
                hecho = True

        #Cargar todo
        reloj.tick(20)
        pantalla.blit(Fondo, (0, 0))
        cursor1.update()
        boton1.update(pantalla, cursor1)
        boton2.update(pantalla, cursor1)
        boton3.update(pantalla, cursor1)
        boton4.update(pantalla, cursor1)
        boton5.update(pantalla, cursor1)
        pygame.display.update()

#----------------Bucle principal-----------------
#Este bucle inicia el juego en si, manteniendose hasta que el tiempo cambie...
#... la opción jugar a False, que pasaría al siguiente bucle
    while jugar:
        pantalla.fill(NEGRO)
        pantalla.blit(Fondo, (0, 0))
        puntuacion = int(puntuacion)
        #Mostrar puntuación en pantalla
        Mensaje = Fuente.render("Puntuacion: %d" % (puntuacion), 0, (0, 0, 255))
        pantalla.blit(Mensaje, (5, 5))

        #El temporizador avanaza
        #calculamos los segundos totales
        segundos_totales = numero_de_fotogramas // tasa_fotogramas

        #Dividimos por 60 para obtener minutos totales
        minutos = segundos_totales // 60

        #Modulo resto para los segundos
        segundos = segundos_totales % 60

        #Usamos el formato de cadenas de texto para formatear los ceros
        texto_de_salida = "Tiempo: {0:02}:{1:02}".format(minutos, segundos)

        #Mostrar el tiempo en pantalla
        texto = Fuente.render(texto_de_salida, True, rojo)
        pantalla.blit(texto, [1000, 5])

        #Proceso de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                hecho = True
                jugar = False
            #Esta parte se podía haber hecho con el teclado muy facilmente,...
            #...pero me ha parecido más dinamico el ratón.
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                #Dispara si el usuario clika
                proyectil = Proyectil()
                #El proyectil sale de la nave protagonista
                proyectil.rect.x = (protagonista.rect.x + 40)
                proyectil.rect.y = protagonista.rect.y
                Disparo.play(0)

                #Añadimos proyectil a la lista
                lista_de_todos_los_sprites.add(proyectil)
                lista_proyectiles.add(proyectil)

        #-----Logica del juego
        lista_de_todos_los_sprites.update()

        #Mecanica de cada proyectil
        for proyectil in lista_proyectiles:
            #Vemos si alcanza un bloque
            #LTS = lista_bloque_alcanzados
            LTS = pygame.sprite.spritecollide(proyectil, lista_bloques, True)
            #Por cada bloque alcanzado, eliminamos proyectil y subimos puntos
            for bloque in LTS:
                lista_proyectiles.remove(proyectil)
                Explosion.play(0)
                lista_de_todos_los_sprites.remove(proyectil)
                puntuacion += 100
                #y por cada nave enemiga eliminada, creamos otra
                for i in range(1):
                    bloque = Bloque(Enemigos)
                    #Ubicación aleatoria
                    bloque.rect.x = random.randrange(largo_pantalla - 50)
                    bloque.rect.y = random.randrange(350)
                    #Añadimos el bloque a la lista de objetos
                    lista_bloques.add(bloque)
                    lista_de_todos_los_sprites.add(bloque)

            #Eliminamos proyectil si sale fuera de la pantalla
            if proyectil.rect.y < -10:
                lista_proyectiles.remove(proyectil)
                lista_de_todos_los_sprites.remove(proyectil)

        lista_de_todos_los_sprites.draw(pantalla)
        numero_de_fotogramas += 3
        reloj.tick(20)
        pygame.display.flip()

        #Cuando el tiempo llega a "segundos_totales, el juego finaliza
        if segundos_totales == 60:
            #Pone el contador de tiempo a cero, por si se reinicia el juego
            numero_de_fotogramas = 0
            gameOver = True
            jugar = False
            record = True

        while gameOver:
            boton1 = Boton(jugar_off, jugar_on, 100, 500)
            boton5 = Boton(salir_off, salir_on, 500, 500)
            boton6 = Boton(volver_off, volver_on, 300, 500)
            for evento in pygame.event.get():

                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if cursor1.colliderect(boton1.rect):
                        gameOver = False
                        jugar = True
                    #Salir
                    if cursor1.colliderect(boton5.rect):
                        gameOver = False
                        hecho = True
                    if cursor1.colliderect(boton6.rect):
                                    gameOver = False
                                    mostrar_menu = True

                pygame.display.flip()
                if evento.type == pygame.QUIT:
                    gameOver = False
                    hecho = True

            reloj.tick(20)
            pantalla.blit(Fondo_GameOver, (0, 0))
            cursor1.update()
            boton1.update(pantalla, cursor1)
            boton5.update(pantalla, cursor1)
            boton6.update(pantalla, cursor1)
            pygame.display.update()

            #Este bucle es para introducir el nombre del jugador en los records
            #Se podría haber hecho mediente pantalla y pygame, pero lo he visto
            #muy complejo para el poco tiempo que me queda.
            #Una vez introducido el nombre, añade nombre y puntos a la BdD
            while record:
                db = "Puntuaciones.db"
                connection = sqlite3.connect(db)
                cursor = connection.cursor()
                query = "SELECT * FROM Puntuaciones ORDER BY Puntos DESC;"
                cursor.execute(query)
                registros = cursor.fetchmany(5)
                for registro in registros:
                    ultima_posicion = registro

                for posicion in ultima_posicion:
                    puntos = posicion
                print puntos

                if puntuacion > puntos:

                    Nombre_nuevo = raw_input("Intruduzca su nombre: ")
                    puntuacion = str(puntuacion)
                    Nombre_nuevo = "('" + Nombre_nuevo + "', "
                    Puntuacion = "'" + puntuacion + "');"
                    Insert = "INSERT INTO Puntuaciones(Nombre, Puntos) Values"

                    query = (Insert + Nombre_nuevo + Puntuacion)
                    cursor.execute(query)
                    connection.commit()
                    if Nombre_nuevo == "":
                        print "No ha introducido ningún dato. Intentelo de nuevo"
                        continue
                    if Nombre_nuevo != "":
                        record = False

                else:
                    record = False

pygame.quit()

#Notas de Autor:
    #Por ahora se trata de un juego totalmente funcional, el cual, para su
    #funcionamiento hace uso de PyGame y de Bases de Datos mediante SQLite3
    #El juego aun tiene algunas posibles mejoras, las cuales se terminarán
    #para dejar un juego de fácil manejo para el usuario.
