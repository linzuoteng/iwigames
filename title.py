import sys
sys.path.append('/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages')
from curses.ascii import STX
import socket
from typing import Text
from dataclasses import dataclass, field
from pygame.constants import *
import pygame
from pygame.locals import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BK_COLOR = WHITE   # 背景色の設定

FPS = 60     # Frame per Second 毎秒のフレーム数

tw = 640
th = 400

counter = 0

class Title():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("title")
        self.screen = pygame.display.set_mode((tw, th))
        self.font = pygame.font.Font(None, 55)
        self.decisionSound = pygame.mixer.Sound("src/カーソル移動11.mp3")

        self.bgm = pygame.mixer.Sound("src/タイトル.mp3")
        self.bgm.set_volume(0.5)
        self.bgm.play(-1)

    def start(self):
        global counter
        global matching

        Tenmetsu = True
        tenmetsuC = 1

        loop = True

        logo1 = pygame.image.load("src/タイトル1.png").convert()
        logo2 = pygame.image.load("src/タイトル2.png").convert()
        logo_rect = logo1.get_rect()

        self.screen.fill(BK_COLOR)
        pygame.display.flip()

        while loop:
            if Tenmetsu == True:
                self.screen.blit(logo1, logo_rect)
            else:
                self.screen.blit(logo2, logo_rect)

            for event in pygame.event.get():
                    # 「閉じる」ボタンを処理する
                if event.type == pygame.QUIT: 
                    loop = False
                    counter = -1
                    self.bgm.stop()

                if event.type == pygame.KEYDOWN:
                    counter = 1
                    loop = False
                    self.decisionSound.play()
                    self.bgm.fadeout(1000)
                    pygame.time.wait(1000)


                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos
                    if 0 <= x and x <= tw and 0 <= y and y <= th:
                        counter = 1
                        loop = False
                        self.decisionSound.play()
                        self.bgm.fadeout(1000)
                        pygame.time.wait(1000)
            
            if tenmetsuC % 500 == 0:
                if Tenmetsu:
                    Tenmetsu = False
                else:
                    Tenmetsu = True
                    
            tenmetsuC += 1

            pygame.display.flip()

        self.bgm.stop()
    
    def c2s(self, ip, port, msg):  # サーバー側へ送信
        s =  socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        serv_address = (ip, port)
        s.sendto(msg.encode('utf-8'), serv_address)

    def getCount(self):
        return counter

def main():
    Title().start()

if __name__=="__main__":
    main()