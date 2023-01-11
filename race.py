import sys
sys.path.append('/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages')
import pygame
from pygame.locals import *
import sys, random
from ctypes import addressof
import socket
from ssl import SSLSocket
from typing import Text
import pygame
from dataclasses import dataclass, field
import queue
from pygame.constants import *
from Server_game import Server
import random

# 変数の初期化
maze_w = 19 # 迷路の列数
maze_h = 19 # 迷路の行数

maze = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1],
        [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
        [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
        [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
        [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
        [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
        [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
        [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
        [1,0,1,0,1,0,1,0,1,2,1,0,1,0,1,0,1,0,1],
        [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
        [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
        [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
        [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
        [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
        [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
        [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
        [1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]


tile_w = 34
tile_h = 34

WIDTH = tile_w * maze_w
HEIGHT = tile_h * maze_h

px1 = 1 # プレイヤーの座標
py1 = 1

px2 = 17 # プレイヤーの座標
py2 = 17

# 色を定義
black = (0, 0, 0)
red = (255, 0, 0)
white = (255,255,255)
brown = (115, 66, 41)
orange = (233,168, 38)
maze_color = [white, brown, orange]

counter = 0
player = 0

Goal1 = False
Goal2 = False

class Race:
    def __init__(self, q, address, port, player):
        self.q = q
        pygame.init()
        pygame.display.set_caption("race")
        self.screen = pygame.display.set_mode((maze_w * tile_w, maze_h * tile_h))
        self.font = pygame.font.Font(None, 55)
        self.address = address
        self.port = port
        self.player = player

        self.moveSound = pygame.mixer.Sound("src/カーソル移動1.mp3")
        self.moveSound.set_volume(0.5)
        self.winSound = pygame.mixer.Sound("src/win2.mp3")
        self.loseSound = pygame.mixer.Sound("src/lose.mp3")
        self.decisionSound = pygame.mixer.Sound("src/カーソル移動11.mp3")
        self.bgm = pygame.mixer.Sound("src/race.mp3")
        self.bgm.set_volume(0.5)
        self.bgm.play(-1)

    def c2s(self, ip, port, msg):  # サーバー側へ送信
        s =  socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        serv_address = (ip, port)
        s.sendto(msg.encode('utf-8'), serv_address)

    def getCount(self):
        return counter

    def draw(self):
        # ゲームの初期化処理
        global px1, py1
        global px2, py2
        global counter
        global maze
        global Goal1, Goal2

        #maze = make_maze()

        old_x1, old_y1 = px1, py1
        old_x2, old_y2 = px2, py2

        loop = True

        wall = pygame.image.load("src/壁.png").convert()
        wall2 = pygame.image.load("src/壁2.png").convert()

        tile = pygame.image.load("src/タイル.png").convert()
        tile_rect = tile.get_rect()

        treasure = pygame.image.load("src/iwai.png")
        treasure = pygame.transform.scale(treasure, (34, 39)) 
        treasure_rect = treasure.get_rect()

        surf_treasure = pygame.image.load("src/iwai.png")
        surf_treasure_rect = surf_treasure.get_rect()
        surf_treasure_rect.center = treasure_rect.center

        #player1
        iwai = pygame.image.load("src/iwai2.png").convert()
        iwai = pygame.transform.scale(iwai, (34, 34)) 
        iwai_rect = iwai.get_rect()
        iwai_rect.topleft = (tile_w * px1, tile_h * px1)

        surf_iwai = pygame.image.load("src/iwai2.png")
        surf_iwai = pygame.transform.scale(surf_iwai, (170, 220)) 
        surf_iwai_rect = surf_iwai.get_rect()
        surf_iwai_rect.center = iwai_rect.center

        #player2
        iwai2 = pygame.image.load("src/iwai3.png").convert()
        iwai2 = pygame.transform.scale(iwai2, (34, 34)) 
        iwai2_rect = iwai2.get_rect()
        iwai2_rect.topleft = (tile_w * px2, tile_h * px2)

        surf_iwai2 = pygame.image.load("src/iwai3.png")
        surf_iwai2 = pygame.transform.scale(surf_iwai2, (170, 220)) 
        surf_iwai2_rect = surf_iwai.get_rect()
        surf_iwai2_rect.center = iwai_rect.center

        while loop:
            
            self.screen.fill(white)
            self.screen.blit(tile, tile_rect)
            
            for y in range(0, maze_h):
                for x in range(0, maze_w):
                    v = maze[y][x]
                    xx = tile_w * x
                    yy = tile_w * y
                    if v == 1:
                        self.screen.blit(wall, (xx, yy - 10)) 
                        if y + 1 <= 18:
                            if maze[y + 1][x] == 1:
                                self.screen.blit(wall2, (xx, yy - 10)) 

                    if v == 2:
                        treasure_rect.topleft = (xx, yy - 5)
                        self.screen.blit(treasure, treasure_rect) 
        
            # イベントを処理する --- (*5)
            for event in pygame.event.get():
                if event.type == QUIT:
                    counter = -1
                    loop = False

                if event.type == KEYDOWN: 
                    self.moveSound.play()
                    if event.key == K_0:
                        counter = 3
                        loop = False
                    else:
                        if event.key == K_LEFT:
                            if self.player == 1:
                                old_x1, old_y1 = px1, py1
                                px1 -= 1

                            elif self.player == 2:
                                old_x2, old_y2 = px2, py2
                                px2 -= 1

                            self.c2s(self.address,self.port,"left")

                        elif event.key == K_RIGHT:
                            if self.player == 1:
                                old_x1, old_y1 = px1, py1
                                px1 += 1

                            elif self.player == 2:
                                old_x2, old_y2 = px2, py2
                                px2 += 1
                                
                            self.c2s(self.address,self.port,"right")

                        elif event.key == K_UP:
                            if self.player == 1:
                                old_x1, old_y1 = px1, py1
                                py1 -= 1

                            elif self.player == 2:
                                old_x2, old_y2 = px2, py2
                                py2 -= 1

                            self.c2s(self.address,self.port,"up")

                        elif event.key == K_DOWN:
                            if self.player == 1:
                                old_x1, old_y1 = px1, py1
                                py1 += 1

                            elif self.player == 2:
                                old_x2, old_y2 = px2, py2
                                py2 += 1

                            self.c2s(self.address,self.port,"down")
            
            
                if self.player == 1:
                    if maze[py1][px1] == 2:
                        Goal1 = True
                        self.c2s(self.address,self.port,"goal1")
                
                elif self.player == 2:
                    if maze[py2][px2] == 2:
                        Goal2 = True
                        self.c2s(self.address,self.port,"goal2")

            if self.q.empty() == False: 
                dir = self.q.get().decode()
                if dir == 'left':
                    if self.player == 1:
                        old_x2, old_y2 = px2, py2
                        px2 -= 1

                    elif self.player == 2:
                        old_x1, old_y1 = px1, py1
                        px1 -= 1
                
                elif dir == 'right':
                    if self.player == 1:
                        old_x2, old_y2 = px2, py2
                        px2 += 1

                    elif self.player == 2:
                        old_x1, old_y1 = px1, py1
                        px1 += 1
                
                elif dir == 'up':
                    if self.player == 1:
                        old_x2, old_y2 = px2, py2
                        py2 -= 1

                    elif self.player == 2:
                        old_x1, old_y1 = px1, py1
                        py1 -= 1
                
                elif dir == 'down':
                    if self.player == 1:
                        old_x2, old_y2 = px2, py2
                        py2 += 1

                    elif self.player == 2:
                        old_x1, old_y1 = px1, py1
                        py1 += 1

                if dir == "goal1":
                    Goal1 = True

                elif dir == "goal2":
                    Goal2 = True

            if maze[py1][px1] == 1:
                px1, py1 = old_x1, old_y1

            if maze[py2][px2] == 1:
                px2, py2 = old_x2, old_y2

            #player1
            iwai_rect.topleft = (px1 * tile_w, py1 * tile_h)
            surf_iwai_rect.center = iwai_rect.center
            surf_iwai_rect.y -= 20

            #self.screen.blit(iwai, iwai_rect)
            self.screen.blit(surf_iwai, surf_iwai_rect)
        
            #player2
            iwai2_rect.topleft = (px2 * tile_w, py2 * tile_h)
            surf_iwai2_rect.center = iwai2_rect.center
            surf_iwai2_rect.y -= 20

            #self.screen.blit(iwai2, iwai2_rect)
            self.screen.blit(surf_iwai2, surf_iwai2_rect)

            pygame.display.flip()

            if Goal1 == True or Goal2 == True:
                j = 0
                
                self.decisionSound.play()

                self.bgm.fadeout(500)
                pygame.time.wait(1500)
                #self.bombSound.play()
                
                if self.player == 1:
                    if Goal1 == True:
                        loseWin = pygame.image.load("src/youwin.png")
                        self.winSound.play()

                    elif Goal2 == True:
                        loseWin = pygame.image.load("src/gameover.png")
                        self.loseSound.set_volume(0.5)
                        self.loseSound.play()
                
                elif self.player == 2:
                    if Goal1 == True:
                        loseWin = pygame.image.load("src/gameover.png")
                        self.loseSound.play()

                    elif Goal2 == True:
                        loseWin = pygame.image.load("src/youwin.png")
                        self.winSound.set_volume(0.5)
                        self.winSound.play()

                loseWin = pygame.transform.scale(loseWin, (WIDTH, HEIGHT + 5)) 
                loseWin_rect = loseWin.get_rect()

                while j < HEIGHT + 5:
                    self.screen.fill(white)
                    self.screen.blit(tile, tile_rect)
                    
                    for y in range(0, maze_h):
                        for x in range(0, maze_w):
                            v = maze[y][x]
                            xx = tile_w * x
                            yy = tile_w * y
                            if v == 1:
                                self.screen.blit(wall, (xx, yy - 10)) 
                                if y + 1 <= 18:
                                    if maze[y + 1][x] == 1:
                                        self.screen.blit(wall2, (xx, yy - 10)) 

                            if v == 2:
                                treasure_rect.topleft = (xx, yy - 5)
                                self.screen.blit(treasure, treasure_rect) 

                    self.screen.blit(surf_iwai, surf_iwai_rect)
                    self.screen.blit(surf_iwai2, surf_iwai2_rect)

                    loseWin_rect.center = (WIDTH/2, j - loseWin_rect.height/2)
                    self.screen.blit(loseWin, loseWin_rect)
                    pygame.display.flip()
                    # pygame.time.wait(10)

                    j += 1

                self.loseSound.fadeout(5000)
                self.winSound.fadeout(5000)
                pygame.time.wait(5000)
                
                counter = 2
                # self.bgm.stop()
                loop = False
                break

            elif Goal2 == True:
                pass

            pygame.display.update()

def main():
    q = queue.Queue()
    # server = Server(q,"localhost",8080)
    # Maze(q,"localhost",2222, 1).draw()

    server = Server(q,"localhost",2222)
    Race(q,"localhost",8080, 1).draw()

if __name__ == '__main__':
    main()