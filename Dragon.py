import pygame
from pygame.locals import *
import os
import sys
import math
import random

pygame.init()

W, H = 910, 512
win = pygame.display.set_mode((W,H))
pygame.display.set_caption('Dragons')
bg = pygame.image.load(os.path.join('imagenes','fondo.png')).convert()
bgX = 0
bgX2 = bg.get_width()

clock = pygame.time.Clock()

class Player(object):
    run = [pygame.image.load(os.path.join('imagenes', str(x) + '.png')) for x in range(0,8)]
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.runCount = 0

    def draw(self, win):
        if self.runCount > 42:
            self.runCount = 0
        win.blit(self.run[self.runCount//6], (self.x,self.y))
        self.runCount += 1
        self.hitbox = (self.x,self.y+8,self.width-16,self.height-25)
        pygame.draw.rect(win,(255,0,0),self.hitbox,2)

class Projectile(object):
    def __init__(self,x,y,radius,color,facing):
         self.x=x
         self.y=y
         self.radius=radius
         self.color=color
         self.facing=facing
         self.vel = 8 * facing


    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)

def redrawWindow():
    win.blit(bg, (bgX,0))
    win.blit(bg, (bgX2,0))
    dragon.draw(win)
    font = pygame.font.SysFont('comicsans',30)
    text = font.render('Score: ' + str(score),1,(255,255,255))
    win.blit(text,(700,10))
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()

def UpdateFile():
    f= open('scores.txt','r')
    file = f.readlines()
    last = int(file[0])
    if last < int(score):
        f.close()
        file=open('scores.txt','w')
        file.write(str(score))
        file.close()
        return score
    return last

def endScreen():
    global pause, objects,fps,score
    pause = 0
    fps = 60
    run=True
    while run:
        pygame.time.delay(100)
        win.blit(bg,(0,0))
        largeFont = pygame.font.SysFont('comicsans',80)
        previousScore = largeFont.render('Previous Score: ' + str(UpdateFile()),1,(255,255,255))
        win.blit(previousScore, (W/2 - previousScore.get_width()/2,200))
        newScore= largeFont.render('Score: '+ str(score),1,(255,255,255))
        win.blit(newScore,(W/2 - newScore.get_width()/2,320))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type ==pygame.MOUSEBUTTONDOWN:
                run = False
    score = 0

dragon = Player(150,100,102,80)
pygame.time.set_timer(USEREVENT+1,500)
fps = 60
run=True

shootLoop = 0
bullets=[]
pause = 0

while run:
    score = fps//5 - 12
    bgX -= 1.4
    bgX2 -= 1.4
    if bgX < bg.get_width() * -1:
        bgX = bg.get_width()
    if bgX2 < bg.get_width() * -1:
        bgX2 = bg.get_width()

    if shootLoop > 0:
        shootLoop +=1
    if shootLoop > 3:
        shootLoop=0
    
    for bullet in bullets:  
        if bullet.x < 910 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootLoop == 0:
        facing = 1
        if len(bullets) < 5:
            bullets.append(Projectile(round(dragon.x + dragon.width //2), round(dragon.y + dragon.height//2), 6, (0,0,0), facing))
        shootLoop=1    
    if keys[pygame.K_UP]:
        if (dragon.y > 0):
            dragon.y = dragon.y -2
    if keys[pygame.K_DOWN]:
        if (dragon.y < 512-dragon.height):
            dragon.y = dragon.y +2
    redrawWindow()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
            pygame.quit()
            sys.exit
        if event.type == USEREVENT+1:
            fps +=1

    clock.tick(fps)

    