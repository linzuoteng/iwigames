import sys
sys.path.append('/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages')
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

WIDTH = 720
HEIGHT = 495

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BK_COLOR = WHITE   # 背景色の設定

FPS = 60     # Frame per Second 毎秒のフレーム数

counter = 0

bgms = ["src/GB-Fighting-B05-1(Stage1).mp3", "src/GB-Fighting-B06-1(Stage2).mp3", "src/GB-Fighting-B07-1(Stage3).mp3", "src/GB-Fighting-B08-1(Stage4).mp3"]

@dataclass
class Fight:  # クライアント側(送信側の処理)
    def __init__(self,q,address,port,player):
        self.q = q
        pygame.init()
        pygame.display.set_caption("main")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.font = pygame.font.Font(None, 55)
        self.address = address
        self.port = port
        self.player = player

        self.wall_pos = []
        # 水平ブロック
        self.horizontal_blocks = pygame.sprite.Group()
        # 垂直方向のブロック
        self.vertical_blocks = pygame.sprite.Group()

        for y, row in enumerate(stage()):
            for x, item in enumerate(row):
                if item == 1:
                    self.wall_pos.append([x * 48, y * 45])

        self.moveSound = pygame.mixer.Sound("src/カーソル移動1.mp3")
        self.moveSound.set_volume(0.5)
        self.shotSound = pygame.mixer.Sound("src/キャンセル5.mp3")
        self.bombSound = pygame.mixer.Sound("src/爆発1.mp3")
        self.crashSound = pygame.mixer.Sound("src/小パンチ.mp3")
        self.winSound = pygame.mixer.Sound("src/win2.mp3")
        self.loseSound = pygame.mixer.Sound("src/lose.mp3")
        self.bgm = pygame.mixer.Sound(bgms[random.randint(0,3)])
        
        self.bgm.set_volume(0.8)
        self.bgm.play(-1)
        self.bgm.play(-1)

    def c2s(self, ip, port, msg):  # サーバー側へ送信
        s =  socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        serv_address = (ip, port)
        s.sendto(msg.encode('utf-8'), serv_address)

    def draw(self):
        global counter

        Lose1 = False
        Win1 = False

        Lose2 = False
        Win2 = False

        loop = True

        walls = []
        boms = ["src/bom1.png","src/bom2.png","src/bom3.png","src/bom4.png","src/bom5.png","src/bom6.png"]

        dir = "RIGHT"
        dir_i = ""

        dir2 = "LEFT"
        dir2_i = ""

        for y in range(4):
            for x in range(5):
                # 画像の大きさを設定
                wall = pygame.Surface([48 * 3, 45 * 2])
                # 指定した色で描画
                wall.fill(BLACK)
                # 画像を囲む四角形
                wall_rect = wall.get_rect()
                # 四角形の左上すみの座標を設定
                wall_rect.topleft = (x * 192 - 48 * 2, y * 135)

                walls.append(wall_rect)

        #岩井1P
        iwai = pygame.image.load("src/iwai2.png").convert()
        iwai = pygame.transform.scale(iwai, (48, 45)) 
        iwai_rect = iwai.get_rect()
        iwai_rect.topleft = (48, 90)

        surf_iwai = pygame.image.load("src/iwai2.png")
        surf_iwai_rect = surf_iwai.get_rect()
        surf_iwai_rect.center = iwai_rect.center

        surfiwai_R = surf_iwai
        surfiwai_L =  pygame.transform.flip(surf_iwai, True, False)

        change_x = 0
        change_y = 0

        #岩井2P
        iwai2 = pygame.image.load("src/iwai2.png")
        iwai2 = pygame.transform.scale(iwai2, (48, 45)) 
        iwai_rect2 = iwai2.get_rect()
        iwai_rect2.topleft = (624, 360)

        surf_iwai2 = pygame.image.load("src/iwai3.png")
        surf_iwai_rect2 = surf_iwai2.get_rect()
        surf_iwai_rect2.center = iwai_rect2.center

        surfiwai2_L = surf_iwai2
        surfiwai2_R =  pygame.transform.flip(surf_iwai2, True, False)

        change_x2 = 0
        change_y2 = 0

        #弾player1
        balet = pygame.image.load("src/iwai.png")
        balet = pygame.transform.scale(balet, (32, 32)) 
        balet_rect = balet.get_rect()
        balet_rect.top = HEIGHT
        boost = False

        #弾player2
        balet2 = pygame.image.load("src/iwai.png")
        balet2 = pygame.transform.scale(balet2, (32, 32)) 
        balet_rect2 = balet2.get_rect()
        balet_rect2.top = HEIGHT
        boost2 = False

        self.screen.fill(BK_COLOR)
        pygame.display.flip()

        while loop:
            
            for event in pygame.event.get():
                    # 「閉じる」ボタンを処理する
                if event.type == pygame.QUIT: 
                    loop = False
                    counter = -1
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        if self.player == 1:
                            if boost == False:
                                self.shotSound.play()
                                boost = True
                                balet_rect.center = iwai_rect.center
                        
                        if self.player == 2:
                            if boost2 == False:
                                self.shotSound.play()
                                boost2 = True
                                balet_rect2.center = iwai_rect2.center
                        
                        self.c2s(self.address,self.port,"shot")
                    
                    if self.player == 1:
                        if dir_i != "left":
                            if event.key == K_LEFT:
                                self.moveSound.play()
                        if dir_i != "right":
                            if event.key == K_RIGHT:
                                self.moveSound.play()
                        if dir_i != "up":
                            if event.key == K_UP:
                                self.moveSound.play()
                        if dir_i != "down":
                            if event.key == K_DOWN:
                                self.moveSound.play()

                    if self.player == 2:
                        if dir2_i != "left":
                            if event.key == K_LEFT:
                                self.moveSound.play()
                        if dir2_i != "right":
                            if event.key == K_RIGHT:
                                self.moveSound.play()
                        if dir2_i != "up":
                            if event.key == K_UP:
                                self.moveSound.play()
                        if dir2_i != "down":
                            if event.key == K_DOWN:
                                self.moveSound.play()

            pressed_key = pygame.key.get_pressed()
            if pressed_key[K_LEFT]:
                self.c2s(self.address,self.port,"left")

                if self.player == 1:
                    change_x = -3
                    change_y = 0
                    dir_i = "left"
                    surf_iwai = surfiwai_L

                if self.player == 2:
                    change_x2 = -3
                    change_y2 = 0
                    dir2_i = "left"
                    surf_iwai2 = surfiwai2_L

            elif pressed_key[K_RIGHT]:
                self.c2s(self.address,self.port,"right")

                if self.player == 1:
                    change_x = 3
                    change_y = 0
                    dir_i = "right"
                    surf_iwai = surfiwai_R

                if self.player == 2:
                    change_x2 = 3
                    change_y2 = 0
                    dir2_i = "right"
                    surf_iwai2 = surfiwai2_R

            elif pressed_key[K_DOWN]:
                self.c2s(self.address,self.port,"down")

                if self.player == 1:
                    change_x = 0
                    change_y = 3
                    dir_i = "down"

                if self.player == 2:
                    change_x2 = 0
                    change_y2 = 3
                    dir2_i = "down"

            elif pressed_key[K_UP]:
                self.c2s(self.address,self.port,"up")

                if self.player == 1:
                    change_x = 0
                    change_y = -3
                    dir_i = "up"

                if self.player == 2:
                    change_x2 = 0
                    change_y2 = -3
                    dir2_i = "up"

            #岩井player1
            if iwai_rect.right < 0:
                    iwai_rect.left = WIDTH
            if iwai_rect.left > WIDTH:
                iwai_rect.right = 0
            if iwai_rect.top > HEIGHT:
                iwai_rect.bottom = 0
            if iwai_rect.bottom < 0:
                iwai_rect.top = HEIGHT

            if boost == False:
                if dir_i == "left":
                    dir = "LEFT"
                elif dir_i == "right":
                    dir = "RIGHT"
                elif dir_i == "down":
                    dir = "DOWN"
                elif dir_i == "up":
                    dir = "UP"

            #岩井player2
            if iwai_rect2.right < 0:
                    iwai_rect2.left = WIDTH
            if iwai_rect2.left > WIDTH:
                iwai_rect2.right = 0
            if iwai_rect2.top > HEIGHT:
                iwai_rect2.bottom = 0
            if iwai_rect2.bottom < 0:
                iwai_rect2.top = HEIGHT

            if boost2 == False:
                if dir2_i == "left":
                    dir2 = "LEFT"
                elif dir2_i == "right":
                    dir2 = "RIGHT"
                elif dir2_i == "down":
                    dir2 = "DOWN"
                elif dir2_i == "up":
                    dir2 = "UP"


            #壁の判定player1
            for i in range(len(walls)):

                #右の判定
                if walls[i].bottom - 45 < iwai_rect.top and iwai_rect.top < walls[i].bottom and walls[i].left < iwai_rect.right and iwai_rect.right < walls[i].left + 48:
                    if dir_i == "right":
                        iwai_rect.top = walls[i].bottom
                    elif dir_i == "up":
                        iwai_rect.right = walls[i].left
                if walls[i].top <= iwai_rect.top and iwai_rect.top <= walls[i].bottom - 45 and walls[i].left < iwai_rect.right and iwai_rect.right < walls[i].left + 48:
                    iwai_rect.right = walls[i].left
                if walls[i].top + 45 <= iwai_rect.bottom and iwai_rect.bottom <= walls[i].bottom and walls[i].left < iwai_rect.right and iwai_rect.right < walls[i].left + 48:
                    iwai_rect.right = walls[i].left
                if walls[i].top < iwai_rect.bottom and iwai_rect.bottom < walls[i].top + 45 and walls[i].left < iwai_rect.right and iwai_rect.right <= walls[i].left + 48:
                    if dir_i == "right":
                        iwai_rect.bottom = walls[i].top
                    elif dir_i == "down":
                        iwai_rect.right = walls[i].left

                #左の判定
                if walls[i].bottom - 45 < iwai_rect.top and iwai_rect.top < walls[i].bottom and walls[i].right -48 < iwai_rect.left and iwai_rect.left < walls[i].right:
                    if dir_i == "left":
                        iwai_rect.top = walls[i].bottom
                    elif dir_i == "up":
                        iwai_rect.left = walls[i].right
                if walls[i].top <= iwai_rect.top and iwai_rect.top <= walls[i].bottom - 45 and walls[i].right -48 < iwai_rect.left and iwai_rect.left < walls[i].right:
                    iwai_rect.left = walls[i].right
                if walls[i].top + 45 <= iwai_rect.bottom and iwai_rect.bottom <= walls[i].bottom and walls[i].right -48 < iwai_rect.left and iwai_rect.left < walls[i].right:
                    iwai_rect.left = walls[i].right
                if walls[i].top < iwai_rect.bottom and iwai_rect.bottom < walls[i].top + 45 and walls[i].right -48 <= iwai_rect.left and iwai_rect.left < walls[i].right:
                    if dir_i == "left":
                        iwai_rect.bottom = walls[i].top
                    elif dir_i == "down":
                        iwai_rect.left = walls[i].right

                #上の判定
                if walls[i].left <= iwai_rect.left and iwai_rect.right <= walls[i].right and walls[i].top <= iwai_rect.bottom and iwai_rect.bottom <= walls[i].bottom:
                    iwai_rect.bottom = walls[i].top

                #下の判定
                if walls[i].left <= iwai_rect.left and iwai_rect.right <= walls[i].right and walls[i].top <= iwai_rect.top and iwai_rect.top <= walls[i].bottom:
                    iwai_rect.top = walls[i].bottom
            
            #壁の判定player2
            for i in range(len(walls)):
                #print(walls[i])
                #右の判定
                if walls[i].bottom - 45 < iwai_rect2.top and iwai_rect2.top < walls[i].bottom and walls[i].left < iwai_rect2.right and iwai_rect2.right < walls[i].left + 48:
                    if dir2_i == "right":
                        iwai_rect2.top = walls[i].bottom
                    elif dir2_i == "up":
                        iwai_rect2.right = walls[i].left
                if walls[i].top <= iwai_rect2.top and iwai_rect2.top <= walls[i].bottom - 45 and walls[i].left < iwai_rect2.right and iwai_rect2.right < walls[i].left + 48:
                    iwai_rect2.right = walls[i].left
                if walls[i].top + 45 <= iwai_rect2.bottom and iwai_rect2.bottom <= walls[i].bottom and walls[i].left < iwai_rect2.right and iwai_rect2.right < walls[i].left + 48:
                    iwai_rect2.right = walls[i].left
                if walls[i].top < iwai_rect2.bottom and iwai_rect2.bottom < walls[i].top + 45 and walls[i].left <= iwai_rect2.right and iwai_rect2.right <= walls[i].left + 48:
                    if dir2_i == "right":
                        iwai_rect2.bottom = walls[i].top
                    elif dir2_i == "down":
                        iwai_rect2.right = walls[i].left

                #左の判定
                if walls[i].bottom - 45 < iwai_rect2.top and iwai_rect2.top < walls[i].bottom and walls[i].right -48 <= iwai_rect2.left and iwai_rect2.left <= walls[i].right:
                    if dir2_i == "left":
                        iwai_rect2.top = walls[i].bottom
                    elif dir2_i == "up":
                        iwai_rect2.left = walls[i].right
                if walls[i].top <= iwai_rect2.top and iwai_rect2.top <= walls[i].bottom - 45 and walls[i].right -48 < iwai_rect2.left and iwai_rect2.left < walls[i].right:
                    iwai_rect2.left = walls[i].right
                if walls[i].top + 45 <= iwai_rect2.bottom and iwai_rect2.bottom <= walls[i].bottom and walls[i].right -48 < iwai_rect2.left and iwai_rect2.left < walls[i].right:
                    iwai_rect2.left = walls[i].right
                if walls[i].top < iwai_rect2.bottom and iwai_rect2.bottom < walls[i].top + 45 and walls[i].right -48 <= iwai_rect2.left and iwai_rect2.left <= walls[i].right:
                    if dir2_i == "left":
                        iwai_rect2.bottom = walls[i].top
                    elif dir2_i == "down":
                        iwai_rect2.left = walls[i].right

                #上の判定
                if walls[i].left <= iwai_rect2.left and iwai_rect2.right < walls[i].right and walls[i].top <= iwai_rect2.bottom and iwai_rect2.bottom <= walls[i].bottom:
                    iwai_rect2.bottom = walls[i].top

                #下の判定
                if walls[i].left <= iwai_rect2.left and iwai_rect2.right < walls[i].right and walls[i].top <= iwai_rect2.top and iwai_rect2.top <= walls[i].bottom:
                    iwai_rect2.top = walls[i].bottom
            
            #player1
            if boost:
                if dir == "RIGHT":
                    if 0 < balet_rect.y + balet_rect.height/2 and balet_rect.y + balet_rect.height/2 < 90:
                        balet_rect.top = HEIGHT
                        boost = False
                    elif 135 < balet_rect.y + balet_rect.height/2 and balet_rect.y + balet_rect.height/2 < 225:
                        balet_rect.top = HEIGHT
                        boost = False
                    elif 270 < balet_rect.y + balet_rect.height/2 and balet_rect.y + balet_rect.height/2 < 360:
                        balet_rect.top = HEIGHT
                        boost = False
                    elif 405 < balet_rect.y + balet_rect.height/2 and balet_rect.y + balet_rect.height/2 < 495:
                        balet_rect.top = HEIGHT
                        boost = False
                    else:
                        balet_rect.move_ip(8, 0)
                elif dir == "LEFT":
                    if 0 < balet_rect.y + balet_rect.height/2 and balet_rect.y + balet_rect.height/2 < 90:
                        balet_rect.top = HEIGHT
                        boost = False
                    elif 135 < balet_rect.y + balet_rect.height/2 and balet_rect.y + balet_rect.height/2 < 225:
                        balet_rect.top = HEIGHT
                        boost = False
                    elif 270 < balet_rect.y + balet_rect.height/2 and balet_rect.y + balet_rect.height/2 < 360:
                        balet_rect.top = HEIGHT
                        boost = False
                    elif 405 < balet_rect.y + balet_rect.height/2 and balet_rect.y + balet_rect.height/2 < 495:
                        balet_rect.top = HEIGHT
                        boost = False
                    else:
                        balet_rect.move_ip(-8, 0)
                elif dir == "UP":
                    if 0 < balet_rect.x + balet_rect.width/2 and balet_rect.x + balet_rect.width/2 < 48:
                        balet_rect.top = HEIGHT
                        boost = False
                    elif 96 < balet_rect.x + balet_rect.width/2 and balet_rect.x + balet_rect.width/2 < 48 * 5:
                        balet_rect.top = HEIGHT
                        boost = False
                    elif 48 * 6 < balet_rect.x + balet_rect.width/2 and balet_rect.x + balet_rect.width/2 < 48 * 9:
                        balet_rect.top = HEIGHT
                        boost = False
                    elif 48 * 10 < balet_rect.x + balet_rect.width/2 and balet_rect.x + balet_rect.width/2 < 48 * 13:
                        balet_rect.top = HEIGHT
                        boost = False
                    elif 48 * 14 < balet_rect.x + balet_rect.width/2 and balet_rect.x + balet_rect.width/2 < 720:
                        balet_rect.top = HEIGHT
                        boost = False
                    else:
                        balet_rect.move_ip(0, -8)

                elif dir == "DOWN":
                    if 0 < balet_rect.x + balet_rect.width/2 and balet_rect.x + balet_rect.width/2 < 48:
                        balet_rect.top = HEIGHT
                        boost = False
                    elif 96 < balet_rect.x + balet_rect.width/2 and balet_rect.x + balet_rect.width/2 < 48 * 5:
                        balet_rect.top = HEIGHT
                        boost = False
                    elif 48 * 6 < balet_rect.x + balet_rect.width/2 and balet_rect.x + balet_rect.width/2 < 48 * 9:
                        balet_rect.top = HEIGHT
                        boost = False
                    elif 48 * 10 < balet_rect.x + balet_rect.width/2 and balet_rect.x + balet_rect.width/2 < 48 * 13:
                        balet_rect.top = HEIGHT
                        boost = False
                    elif 48 * 14 < balet_rect.x + balet_rect.width/2 and balet_rect.x + balet_rect.width/2 < 720:
                        balet_rect.top = HEIGHT
                        boost = False
                    else:
                        balet_rect.move_ip(0, 8)

                if balet_rect.right < 0 or balet_rect.left > WIDTH or balet_rect.top > HEIGHT or balet_rect.bottom < 0:
                    balet_rect.top = HEIGHT
                    boost = False
            
            #player2
            if boost2:
                if dir2 == "RIGHT":
                    if 0 < balet_rect2.y + balet_rect2.height/2 and balet_rect2.y + balet_rect2.height/2 < 90:
                        balet_rect2.top = HEIGHT
                        boost2 = False
                    elif 135 < balet_rect2.y + balet_rect2.height/2 and balet_rect2.y + balet_rect2.height/2 < 225:
                        balet_rect2.top = HEIGHT
                        boost2 = False
                    elif 270 < balet_rect2.y + balet_rect2.height/2 and balet_rect2.y + balet_rect2.height/2 < 360:
                        balet_rect2.top = HEIGHT
                        boost2 = False
                    elif 405 < balet_rect2.y + balet_rect2.height/2 and balet_rect2.y + balet_rect2.height/2 < 495:
                        balet_rect2.top = HEIGHT
                        boost2 = False
                    else:
                        balet_rect2.move_ip(8, 0)

                elif dir2 == "LEFT":
                    if 0 < balet_rect2.y + balet_rect2.height/2 and balet_rect2.y + balet_rect2.height/2 < 90:
                        balet_rect2.top = HEIGHT
                        boost2 = False
                    elif 135 < balet_rect2.y + balet_rect2.height/2 and balet_rect2.y + balet_rect2.height/2 < 225:
                        balet_rect2.top = HEIGHT
                        boost2 = False
                    elif 270 < balet_rect2.y + balet_rect2.height/2 and balet_rect2.y + balet_rect2.height/2 < 360:
                        balet_rect2.top = HEIGHT
                        boost2 = False
                    elif 405 < balet_rect2.y + balet_rect2.height/2 and balet_rect2.y + balet_rect2.height/2 < 495:
                        balet_rect2.top = HEIGHT
                        boost2 = False
                    else:
                        balet_rect2.move_ip(-8, 0)

                elif dir2 == "UP":
                    if 0 < balet_rect2.x + balet_rect2.width/2 and balet_rect2.x + balet_rect2.width/2 < 48:
                        balet_rect2.top = HEIGHT
                        boost2 = False
                    elif 96 < balet_rect2.x + balet_rect2.width/2 and balet_rect2.x + balet_rect2.width/2 < 48 * 5:
                        balet_rect2.top = HEIGHT
                        boost2 = False
                    elif 48 * 6 < balet_rect2.x + balet_rect2.width/2 and balet_rect2.x + balet_rect2.width/2 < 48 * 9:
                        balet_rect2.top = HEIGHT
                        boost2 = False
                    elif 48 * 10 < balet_rect2.x + balet_rect2.width/2 and balet_rect2.x + balet_rect2.width/2 < 48 * 13:
                        balet_rect2.top = HEIGHT
                        boost2 = False
                    elif 48 * 14 < balet_rect2.x + balet_rect2.width/2 and balet_rect2.x + balet_rect2.width/2 < 720:
                        balet_rect2.top = HEIGHT
                        boost2 = False
                    else:
                        balet_rect2.move_ip(0, -8)

                elif dir2 == "DOWN":
                    if 0 < balet_rect2.x + balet_rect2.width/2 and balet_rect2.x + balet_rect2.width/2 < 48:
                        balet_rect2.top = HEIGHT
                        boost2 = False
                    elif 96 < balet_rect2.x + balet_rect2.width/2 and balet_rect2.x + balet_rect2.width/2 < 48 * 5:
                        balet_rect2.top = HEIGHT
                        boost2 = False
                    elif 48 * 6 < balet_rect2.x + balet_rect2.width/2 and balet_rect2.x + balet_rect2.width/2 < 48 * 9:
                        balet_rect.top = HEIGHT
                        boost2 = False
                    elif 48 * 10 < balet_rect2.x + balet_rect2.width/2 and balet_rect2.x + balet_rect2.width/2 < 48 * 13:
                        balet_rect2.top = HEIGHT
                        boost2 = False
                    elif 48 * 14 < balet_rect2.x + balet_rect2.width/2 and balet_rect2.x + balet_rect2.width/2 < 720:
                        balet_rect2.top = HEIGHT
                        boost2 = False
                    else:
                        balet_rect2.move_ip(0, 8)

                if balet_rect2.right < 0 or balet_rect2.left > WIDTH or balet_rect2.top > HEIGHT or balet_rect2.bottom < 0:
                    balet_rect2.top = HEIGHT
                    boost2 = False

            if self.q.empty() == False: 
                self.screen.fill(BK_COLOR)
                d = self.q.get().decode()
                if d == "shot":
                    self.shotSound.play()
                    if self.player == 1:
                        if boost2 == False:
                            boost2 = True
                            balet_rect2.center = iwai_rect2.center
                    
                    if self.player == 2:
                        if boost == False:
                            boost = True
                            balet_rect.center = iwai_rect.center

                if d == 'left':
                    if self.player == 1:
                        change_x2 = -3
                        change_y2 = 0
                        dir2_i = "left"
                        surf_iwai2 = surfiwai2_L

                    if self.player == 2:    
                        change_x = -3
                        change_y = 0
                        dir_i = "left"
                        surf_iwai = surfiwai_L

                elif d == "right":
                    if self.player == 1:
                        change_x2 = 3
                        change_y2 = 0
                        dir2_i = "right"
                        surf_iwai2 = surfiwai2_R

                    if self.player == 2:
                        change_x = 3
                        change_y = 0
                        dir_i = "right"
                        surf_iwai = surfiwai_R

                elif d == "down":
                    if self.player == 1:
                        change_x2 = 0
                        change_y2 = 3
                        dir2_i = "down"

                    if self.player == 2:
                        change_x = 0
                        change_y = 3
                        dir_i = "down"

                elif d == "up":
                    if self.player == 1:
                        change_x2 = 0
                        change_y2 = -3
                        dir2_i = "up"

                    if self.player == 2:
                        change_x = 0
                        change_y = -3
                        dir_i = "up"

                if d == "lose1":
                    Win2 == True
                elif d == "win1":
                    Lose2 = True
                elif d == "lose2":
                    Win1 = True
                elif d == "win2":
                    Lose1 = True

            #player1に当たったら
            if iwai_rect.left < balet_rect2.left and balet_rect2.right < iwai_rect.right and iwai_rect.top < balet_rect2.top and balet_rect2.bottom < iwai_rect.bottom:
                if self.player == 1:
                    Lose1 = True
                    self.c2s(self.address,self.port,"lose1")
                if self.player == 2:
                    Win2 = True
                    self.c2s(self.address,self.port,"win2")

            #player2に当たったら
            if iwai_rect2.left < balet_rect.left and balet_rect.right < iwai_rect2.right and iwai_rect2.top < balet_rect.top and balet_rect.bottom < iwai_rect2.bottom:
                if self.player == 2:
                    Lose2 = True
                    self.c2s(self.address,self.port,"lose2")
                if self.player == 1:
                    Win1 = True
                    self.c2s(self.address,self.port,"win1")

            if Lose1 == True or Win2 == True:
                i = 0
                j = 0
                self.crashSound.play()
                self.bgm.fadeout(500)
                pygame.time.wait(1500)
                self.bombSound.play()
                while i < 7:
                    self.screen.fill(BK_COLOR)
                    draw_stage(self)
                    self.screen.blit(surf_iwai2, surf_iwai_rect2)
                    if i < 3:
                        self.screen.blit(surf_iwai, surf_iwai_rect)
                    if i < 6:
                        bom = pygame.image.load(boms[i])
                        bom = pygame.transform.scale(bom, (96, 90)) 
                        bom_rect = bom.get_rect()
                        bom_rect.center = iwai_rect.center
                        self.screen.blit(bom, bom_rect)
                    pygame.display.flip()

                    pygame.time.wait(100)
                    i += 1
                
                pygame.time.wait(1700)
                
                if Lose1 == True:
                    loseWin = pygame.image.load("src/gameover.png")
                    self.loseSound.play()
                    

                elif Win2 == True:
                    loseWin = pygame.image.load("src/youwin.png")
                    self.winSound.set_volume(0.5)
                    self.winSound.play()

                loseWin = pygame.transform.scale(loseWin, (WIDTH, HEIGHT + 5)) 
                loseWin_rect = loseWin.get_rect()

                while j < HEIGHT + 5:
                    self.screen.fill(BK_COLOR)
                    draw_stage(self)
                    self.screen.blit(surf_iwai2, surf_iwai_rect2)
                    loseWin_rect.center = (WIDTH/2, j - loseWin_rect.height/2)
                    self.screen.blit(loseWin, loseWin_rect)
                    pygame.display.flip()

                    j += 7

                self.loseSound.fadeout(7000)
                self.winSound.fadeout(7000)
                pygame.time.wait(7000)
                
                counter = 2
                self.bgm.stop()
                break

            #player2に当たったら
            if Lose2 == True or Win1 == True:
                i = 0
                j = 0
                self.crashSound.play()
                self.bgm.fadeout(500)
                pygame.time.wait(1500)
                self.bombSound.play()
                while i < 7:
                    self.screen.fill(BK_COLOR)
                    draw_stage(self)
                    self.screen.blit(surf_iwai, surf_iwai_rect)
                    if i < 3:
                        self.screen.blit(surf_iwai2, surf_iwai_rect2)
                    if i < 6:
                        bom = pygame.image.load(boms[i])
                        bom = pygame.transform.scale(bom, (96, 90)) 
                        bom_rect = bom.get_rect()
                        bom_rect.center = iwai_rect2.center
                        self.screen.blit(bom, bom_rect)
                    pygame.display.flip()

                    pygame.time.wait(100)
                    i += 1
                
                pygame.time.wait(1700)

                if Lose2 == True:
                    loseWin = pygame.image.load("src/gameover.png")
                    self.loseSound.play()
                elif Win1 == True:
                    loseWin = pygame.image.load("src/youwin.png")
                    self.winSound.play()
                    self.winSound.set_volume(0.5)

                loseWin = pygame.transform.scale(loseWin, (WIDTH, HEIGHT + 5)) 
                loseWin_rect = loseWin.get_rect()

                while j < HEIGHT + 5:
                    self.screen.fill(BK_COLOR)
                    draw_stage(self)
                    self.screen.blit(surf_iwai, surf_iwai_rect)
                    loseWin_rect.center = (WIDTH/2, j - loseWin_rect.height/2)
                    self.screen.blit(loseWin, loseWin_rect)
                    pygame.display.flip()

                    j += 7

                self.loseSound.fadeout(7000)
                self.winSound.fadeout(7000)
                pygame.time.wait(7000)
                counter = 2
                self.bgm.stop()
                break

            #player1
            iwai_rect.x += change_x
            iwai_rect.y += change_y

            #player2
            iwai_rect2.x += change_x2
            iwai_rect2.y += change_y2

            self.screen.fill(BK_COLOR)
            draw_stage(self)

            surf_iwai_rect.center = iwai_rect.center
            surf_iwai_rect2.center = iwai_rect2.center

            #player1
            self.screen.blit(balet, balet_rect)
            #player2
            self.screen.blit(balet2, balet_rect2)

            #player1
            self.screen.blit(surf_iwai, surf_iwai_rect)
            #player2
            self.screen.blit(surf_iwai2, surf_iwai_rect2)

            pygame.display.flip()
    
    def getCount(self):
        return counter
         

class Block(pygame.sprite.Sprite):
    # ブロックの関数
    def __init__(self,x,y,color,width,height):
        pygame.sprite.Sprite.__init__(self)
        # 画像の大きさを設定
        self.image = pygame.Surface([width,height])
        # 指定した色で描画
        self.image.fill(color)
        # 画像を囲む四角形
        self.rect = self.image.get_rect()
        # 四角形の左上すみの座標を設定
        self.rect.topleft = (x,y)

def stage():

        glid = ((1,0,1,1,1,0,1,1,1,0,1,1,1,0,1),
                (1,0,1,1,1,0,1,1,1,0,1,1,1,0,1),
                (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
                (1,0,1,1,1,0,1,1,1,0,1,1,1,0,1),
                (1,0,1,1,1,0,1,1,1,0,1,1,1,0,1),
                (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
                (1,0,1,1,1,0,1,1,1,0,1,1,1,0,1),
                (1,0,1,1,1,0,1,1,1,0,1,1,1,0,1),
                (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
                (1,0,1,1,1,0,1,1,1,0,1,1,1,0,1),
                (1,0,1,1,1,0,1,1,1,0,1,1,1,0,1),
                (0,0,0,0,0,0,0,0,0,0,0,0,0,0,1))
        
        return glid

def draw_stage(screen):
    wall = pygame.image.load("src/wall.png")
    wall = pygame.transform.scale(wall, (48 * 3, 90)) 

    back = pygame.image.load("src/floor.png")
    screen.screen.blit(back, (0, 0))

    for y, row in enumerate(stage()):
        for x, item in enumerate(row):
            if item == 1:
                if y % 3 ==  0 and x  == 0:
                    screen.screen.blit(wall, (-96, y * 45 + 10))
                if y % 3 ==  0 and (x - 2) % 4 == 0:
                    screen.screen.blit(wall, (x * 48, y * 45 + 10)) 

def main():
    q = queue.Queue()
    server = Server(q,"localhost",2222)
    Fight(q,"localhost",8080, 2).draw()


if __name__=="__main__":
    main()