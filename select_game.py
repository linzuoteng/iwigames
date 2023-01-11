import sys
sys.path.append('/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages')
from curses.ascii import STX
import queue
import socket
import time
from typing import Text
from dataclasses import dataclass, field
from pygame.constants import *
import pygame
from pygame.locals import *
from Server_game import Server

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BK_COLOR = WHITE   # 背景色の設定

FPS = 60     # Frame per Second 毎秒のフレーム数

tw = 640
th = 400

counter = 0



class Select():
    def __init__(self,q,address,port,player):
        self.q = q
        self.address = address
        self.port = port
        self.player = player

        pygame.init()
        pygame.display.set_caption("selecting")
        self.screen = pygame.display.set_mode((tw, th))
        self.font = pygame.font.Font(None, 55)

        self.selectSound = pygame.mixer.Sound("src/カーソル移動1.mp3")
        self.decisionSound = pygame.mixer.Sound("src/カーソル移動11.mp3")
        self.bgm = pygame.mixer.Sound("src/selectS.mp3")
        self.bgm.set_volume(0.5)
        self.bgm.play(-1)

    def select(self):
        global counter

        sdx1 = 279
        sdy1 = 146
        sx1 = 81
        sy1 = 113

        sdx2 = 279
        sdy2 = 146
        sx2 = 281
        sy2 = 113

        games = [["FIGHT","HOKEY"],["SHOT","MAZE"]]
        game = "FIGHT"
        g_index1 = 0
        g_index2 = 0

        player1 = pygame.image.load("src/iwai2.png")
        rect_player1 = player1.get_rect()
        rect_player1.center = (sx1, sy1)

        player2 = pygame.image.load("src/iwai3.png")
        rect_player2 = player2.get_rect()
        rect_player2.center = (sx2, sy2)

        game_sc = pygame.image.load("src/選択画面.png").convert()
        rect_game_sc = game_sc.get_rect()

        loop = True
        self.screen.fill(BK_COLOR)
        pygame.display.flip()

        while loop:
            for event in pygame.event.get():
                    # 「閉じる」ボタンを処理する
                if event.type == pygame.QUIT: 
                    loop = False
                    counter = -1
                    
                if event.type == KEYDOWN:
                    if event.key == K_0:
                        counter = 3
                        loop = False
                    else:
                        if event.key == K_LEFT:
                            self.selectSound.play()
                            if self.player == 1:
                                sx1 -= sdx1
                                if sx1 < 81:
                                    sx1 = 81
                            
                            if self.player == 2:
                                sx2 -= sdx2
                                if sx2 < 281:
                                    sx2 = 281

                            g_index2 = 0
                            game = games[g_index1][g_index2]

                            self.screen.fill(BK_COLOR)

                            self.c2s(self.address, self.port, pygame.key.name(event.key))

                        elif event.key == K_RIGHT:
                            self.selectSound.play()
                            if self.player == 1:
                                sx1 += sdx1
                                if sx1 > 369:
                                    sx1 = 360

                            if self.player == 2:
                                sx2 += sdx2
                                if sx2 > 560:
                                    sx2 = 560

                            g_index2 = 1
                            game = games[g_index1][g_index2]

                            self.screen.fill(BK_COLOR)
                            self.c2s(self.address, self.port, pygame.key.name(event.key))

                        elif event.key == K_UP:
                            self.selectSound.play()
                            if self.player == 1:
                                sy1 -= sdy1
                                if sy1 < 113:
                                    sy1 = 113

                            if self.player == 2:
                                sy2 -= sdy2
                                if sy2 < 113:
                                    sy2 = 113

                            g_index1 = 0
                            game = games[g_index1][g_index2]

                            self.screen.fill(BK_COLOR)
                            self.c2s(self.address, self.port, pygame.key.name(event.key))

                        elif event.key == K_DOWN:
                            self.selectSound.play()
                            if self.player == 1:
                                sy1 += sdy1
                                if sy1 > 259:
                                    sy1 = 259
                                
                            if self.player == 2:
                                sy2 += sdy2
                                if sy2 > 259:
                                    sy2 = 259

                            g_index1 = 1
                            game = games[g_index1][g_index2]

                            self.screen.fill(BK_COLOR)
                            self.c2s(self.address, self.port, pygame.key.name(event.key))

                        elif event.key == K_RETURN or event.key == K_SPACE:
                            self.decisionSound.play()
                            pygame.time.wait(1000)
                            if game == "FIGHT":
                                counter = 3

                                self.c2s(self.address, self.port, "FIGHT")
                                
                                loop = False

                            elif game == "HOKEY":
                                counter = 4

                                self.c2s(self.address, self.port, "HOKEY")

                                loop = False

                            elif game == "SHOT":
                                counter = 5

                                self.c2s(self.address, self.port,"SHOT")

                                loop = False

                            elif game == "MAZE":
                                counter = 6

                                self.c2s(self.address, self.port,"MAZE") 

                                loop = False

                            self.bgm.stop()

            if self.q.empty() == False: 
                self.screen.fill(BK_COLOR)
                dir = self.q.get().decode()
                if dir == 'left':
                    if self.player == 2:
                        sx1 -= sdx1
                        if sx1 < 81:
                            sx1 = 81

                    if self.player == 1:
                        sx2 -= sdx2
                        if sx2 < 281:
                            sx2 = 281

                elif dir == 'right':
                    if self.player == 2:
                        sx1 += sdx1
                        if sx1 > 360:
                            sx1 = 360
                    
                    if self.player == 1:
                        sx2 += sdx2
                        if sx2 > 560:
                            sx2 = 560

                elif dir == "up":
                    if self.player == 2:
                        sy1 -= sdy1
                        if sy1 < 113:
                            sy1 = 113
                    
                    if self.player == 1:
                        sy2 -= sdy2
                        if sy2 < 113:
                            sy2 = 113

                elif dir == "down":
                    if self.player == 2:
                        sy1 += sdy1
                        if sy1 > 259:
                            sy1 = 259
                    
                    if self.player == 1:
                        sy2 += sdy2
                        if sy2 > 259:
                            sy2 = 259

                elif dir == "FIGHT":
                    counter = 3
                    loop = False
                    self.bgm.stop()

                elif dir == "HOKEY":
                    counter = 4
                    loop = False
                    self.bgm.stop()

                elif dir == "SHOT":
                    counter = 5
                    loop = False
                    self.bgm.stop()

                elif dir == "MAZE":
                    counter = 6
                    loop = False
                    self.bgm.stop()

            self.screen.blit(game_sc, rect_game_sc)

            rect_player1.center = (sx1, sy1)
            rect_player2.center = (sx2, sy2)

            self.screen.blit(player1, rect_player1)
            self.screen.blit(player2, rect_player2)
            
            pygame.display.flip()

    def c2s(self, ip, port, msg):  # サーバー側へ送信
        s =  socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        serv_address = (ip, port)
        s.sendto(msg.encode('utf-8'), serv_address)

    def getCount(self):
        return counter

def main():
    q = queue.Queue()
    server = Server(q, "localhost", 8080)
    Select(q, "localhost", 2222, 1).select()

if __name__=="__main__":
    main()