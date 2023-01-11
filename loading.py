import sys
sys.path.append('/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages')

from curses.ascii import STX
import socket
from typing import Text
import pygame
from dataclasses import dataclass, field
import threading
import queue
from pygame.constants import *
import pygame
from pygame.locals import *
import sys, random
from Server_game import Server

WIDTH = 640
HEIGHT = 400

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BK_COLOR = WHITE   # 背景色の設定

FPS = 60     # Frame per Second 毎秒のフレーム数

tw = 640
th = 400

guru = True

matching = 0
counter = 0
player = 0

class Loading():
    def __init__(self, q, address, port):
        self.q = q
        pygame.init()
        pygame.display.set_caption("loading")

        self.address = address
        self.port = port

        self.screen = pygame.display.set_mode((tw, th))
        self.font = pygame.font.Font(None, 55)
        self.thread = threading.Thread(target = self.guru2, daemon = True)
        self.thread.start()

        self.decisionSound = pygame.mixer.Sound("src/カーソル移動11.mp3")
        self.bgm = pygame.mixer.Sound("src/loading.mp3")
        self.bgm.set_volume(0.4)
        self.bgm.play(-1)

    def load(self):
        global guru
        global matching
        global counter
        global player

        load_sc = pygame.image.load("src/loading.png")
        rect_load_sc = load_sc.get_rect()

        player = 0
        matching = 0

        loop = True
        bx = tw/2
        by = th/2

        return_b = pygame.image.load("src/return.png").convert()
        return_b = pygame.transform.scale(return_b, (50, 50)) 
        rect_return = return_b.get_rect()
        return_pos = (WIDTH - rect_return.width - 10, 10)

        self.screen.fill(BK_COLOR)
        pygame.display.flip()

        while loop:
            
            self.c2s(self.address, self.port, "player")
            self.c2s(self.address, self.port, "matching")

            guru = True
            self.screen.blit(load_sc, rect_load_sc)
            self.screen.blit(return_b, return_pos)
            if matching >= 2:
                self.decisionSound.play()
                self.screen.fill(BK_COLOR)
                

                load_sc = pygame.image.load("src/matching.png")
                self.screen.blit(load_sc, rect_load_sc)
                self.screen.blit(return_b, return_pos)
                guru = False
                pygame.display.flip()
    
                loop = False
                self.bgm.fadeout(3000)
                pygame.time.wait(3000)
                self.bgm.stop()
                
                
                counter = 2

            for event in pygame.event.get():
                    # 「閉じる」ボタンを処理する
                if event.type == pygame.QUIT: 
                    loop = False
                    counter = -1
                    
                if event.type == KEYDOWN:
                    if event.key == K_0:
                        counter = 2
                        guru = False
                        loop = False
                        self.bgm.stop()

                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos
                    if WIDTH - rect_return.width - 10 <= x and x <= WIDTH - 10 and 10 <= y and y <= 10 + rect_return.height:
                        self.decisionSound.play()
                        counter = 0
                        guru = False
                        loop = False
                        self.bgm.stop()

            if self.q.empty() == False: 
                self.screen.fill(BK_COLOR)
                match = self.q.get().decode()
                if match == "matching":
                    matching = 2
                if match == "player":
                    if player != 1:
                        player = 2

            if player != 2:
                player = 1

            pygame.display.flip()
    
    def c2s(self, ip, port, msg):  # サーバー側へ送信
        s =  socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        serv_address = (ip, port)
        s.sendto(msg.encode('utf-8'), serv_address)

    def getCount(self):
        return counter

    def getPlayer(self):
        return player

    def guru2(self):
        global guru

        guru = True
        x = 20
        count = 0
        bx = tw/2
        by = th/2
        bw = 16 

        while guru:
            if count % 8 ==  0:
                bw = 20
                pygame.draw.ellipse(self.screen,(0,0,0),(bx - bw/2 ,by - bw/2 + 50 - x,bw,bw))
                bw = 16
            else:
                pygame.draw.ellipse(self.screen,(255,255,255),(bx - 20/2 ,by - 20/2 + 50 - x,20,20))
                pygame.draw.ellipse(self.screen,(0,0,0),(bx - bw/2 ,by - bw/2 + 50 - x,bw,bw))
    
            if count % 8 ==  1:
                bw = 20
                pygame.draw.ellipse(self.screen,(0,0,0),(bx - bw/2 + 35,by - bw/2 + 65 - x,bw,bw))
                bw = 16
            else:
                pygame.draw.ellipse(self.screen,(255,255,255),(bx - 20/2 + 35,by - 20/2 + 65 - x,20,20))
                pygame.draw.ellipse(self.screen,(0,0,0),(bx - bw/2 + 35,by - bw/2 + 65 - x,bw,bw))

            if count % 8 ==  2:
                bw = 20
                pygame.draw.ellipse(self.screen,(0,0,0),(bx - bw/2 + 50 ,by - bw/2 + 100 - x,bw,bw))
                bw = 16
            else:
                pygame.draw.ellipse(self.screen,(255,255,255),(bx - 20/2 + 50 ,by - 20/2 + 100 - x,20,20))
                pygame.draw.ellipse(self.screen,(0,0,0),(bx - bw/2 + 50 ,by - bw/2 + 100 - x,bw,bw))

            if count % 8 ==  3:
                bw = 20
                pygame.draw.ellipse(self.screen,(0,0,0),(bx - bw/2 + 35,by - bw/2 + 135 - x,bw,bw))
                bw = 16
            else:
                pygame.draw.ellipse(self.screen,(255,255,255),(bx - 20/2 + 35,by - 20/2 + 135 - x,20,20))
                pygame.draw.ellipse(self.screen,(0,0,0),(bx - bw/2 + 35,by - bw/2 + 135 - x,bw,bw))

            if count % 8 ==  4:
                bw = 20
                pygame.draw.ellipse(self.screen,(0,0,0),(bx - bw/2 ,by - bw/2 + 150 - x,bw,bw))
                bw = 16
            else:
                pygame.draw.ellipse(self.screen,(255,255,255),(bx - 20/2 ,by - 20/2 + 150 - x,20,20))
                pygame.draw.ellipse(self.screen,(0,0,0),(bx - bw/2 ,by - bw/2 + 150 - x,bw,bw))

            if count % 8 ==  5:
                bw = 20
                pygame.draw.ellipse(self.screen,(0,0,0),(bx - bw/2 - 35,by - bw/2 + 135 - x,bw,bw))
                bw = 16
            else:
                pygame.draw.ellipse(self.screen,(255,255,255),(bx - 20/2 - 35,by - 20/2 + 135 - x,20,20))
                pygame.draw.ellipse(self.screen,(0,0,0),(bx - bw/2 - 35,by - bw/2 + 135 - x,bw,bw))

            if count % 8 ==  6:
                bw = 20
                pygame.draw.ellipse(self.screen,(0,0,0),(bx - bw/2 - 50,by - bw/2 + 100 - x,bw,bw))
                bw = 16
            else:
                pygame.draw.ellipse(self.screen,(255,255,255),(bx - 20/2 - 50,by - 20/2 + 100 - x,20,20))
                pygame.draw.ellipse(self.screen,(0,0,0),(bx - bw/2 - 50,by - bw/2 + 100 - x,bw,bw))

            if count % 8 ==  7:
                bw = 20
                pygame.draw.ellipse(self.screen,(0,0,0),(bx - bw/2 - 35,by - bw/2 + 65 - x,bw,bw))
                bw = 16
            else:
                pygame.draw.ellipse(self.screen,(255,255,255),(bx - 20/2 - 35,by - 20/2 + 65 - x,20,20))
                pygame.draw.ellipse(self.screen,(0,0,0),(bx - bw/2 - 35,by - bw/2 + 65 - x,bw,bw))

            count += 1
            pygame.time.wait(100)
        
        self.screen.fill(BK_COLOR)
        

def main():
    q = queue.Queue()
    server = Server(q, "localhost", 2222)
    Loading(q, "localhost", 8080).load()

if __name__=="__main__":
    main()
