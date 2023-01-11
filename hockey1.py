import sys
sys.path.append('/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages')
import socket
from typing import Text
import pygame
from dataclasses import dataclass, field
import threading
import queue
from pygame.constants import *
from Server_game import Server

WIDTH = 640
HEIGHT = 640

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BK_COLOR = BLACK   # 背景色の設定

FPS = 60     # Frame per Second 毎秒のフレーム数

counter = 0

@dataclass
class Hockey:  # クライアント側(送信側の処理)
    def __init__(self, q, address, port):
        self.q = q
        pygame.init()
        pygame.display.set_caption("player1")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.font = pygame.font.Font(None, 55)
        self.bgm = pygame.mixer.Sound('src/hockey.mp3')
        self.win = pygame.mixer.Sound('src/win.mp3')
        self.lose = pygame.mixer.Sound('src/lose.mp3')
        self.bgm.play(-1)
        self.address = address
        self.port = port

    def c2s(self, ip, port, msg):  # サーバー側へ送信
        s =  socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        serv_address = (ip, port)
        s.sendto(msg.encode('utf-8'), serv_address)

    def getCount(self):
        return counter

    def draw(self):
        global counter

        loop = True
        x1 = WIDTH/2
        x2 = WIDTH/2
        text1 = self.font.render("",True,WHITE)
        text2 = self.font.render("",True,WHITE)
        image_paddle = pygame.image.load('src/paddle.png').convert()
        rect1 = image_paddle.get_rect()
        rect2 = image_paddle.get_rect()
        rect1.center = (x1, 610)
        rect2.center = (x2, 30)
        speedx = 7
        speedy = 7
        image_ball = pygame.image.load('src/iwai.png').convert()
        ball = image_ball.get_rect()
        ball.center = (rect1.centerx,rect1.top)
        font_point = pygame.font.Font(None, 55)
        font_result = pygame.font.Font(None, 55)
        point_1 = 0
        point_2 = 0

        pygame.display.flip()
        while loop:
            ball.centerx += speedx
            ball.centery -= speedy

            if ball.right >= WIDTH and speedx > 0:
                speedx *= -1
            elif ball.left <= 0 and speedx < 0:
                speedx *= -1

            if ball.colliderect(rect1) and speedy < 0:
                speedy *= -1.1
            elif ball.colliderect(rect2) and speedy > 0:
                speedy *= -1.1

            if ball.centery >= HEIGHT:
                ball.center = (rect1.centerx,rect1.top)
                point_1 += 1
                speedy = 7
            elif ball.centery <= 0:
                ball.center = (rect2.centerx,rect2.top)
                point_2 += 1
                speedy = 7

            text1 = font_point.render(str(point_1), True, (255,255,255))
            text2 = font_point.render(str(point_2), True, (255,255,255))

            if point_2 == 1:
                text_win = font_result.render("YOU WIN!!", True, WHITE)
                speedx = 0
                speedy = 0
                ball.center = (WIDTH/2 - 50, HEIGHT/2)
                self.screen.blit(text_win, [WIDTH/2,HEIGHT/2 - 10])
                pygame.display.update()
                self.bgm.stop()
                self.win.play()

                loop = False
                counter = 2
                pygame.time.wait(3000)

            elif point_1 == 1:
                speedx = 0
                speedy = 0
                text_lose = font_result.render("YOU LOSE", True, WHITE)
                ball.center = (WIDTH/2 - 50, HEIGHT/2)
                self.screen.blit(text_lose, [WIDTH/2,HEIGHT/2 - 10])
                self.bgm.stop()
                self.lose.play()

                pygame.display.update()
                loop = False
                counter = 2
                pygame.time.wait(3000)
                

            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    loop = False
                    counter = -1
                if event.type == KEYDOWN:
                    if event.key == K_0:
                        counter = 2
                        loop = False
            
            pressed_key = pygame.key.get_pressed()
            if pressed_key[K_LEFT]:
                self.c2s(self.address,self.port,pygame.key.name(event.key))
                if rect1.left > 0:
                    rect1.move_ip(-10, 0)
            elif pressed_key[K_RIGHT]:
                self.c2s(self.address,self.port,pygame.key.name(event.key))
                if rect1.right < WIDTH:
                    rect1.move_ip(10, 0)

            if self.q.empty()==False:
                que = self.q.get().decode()
                if que == 'right':
                    if rect2.left > 0:
                        rect2.move_ip(-10, 0)
                    elif rect2.left < 0:
                        rect2.move_ip(0,0)
                elif que == 'left':
                    if rect2.right < WIDTH:
                        rect2.move_ip(10, 0)

                position2 = text2.get_rect()
                position2.right = self.screen.get_rect().right
                
            
            pygame.time.wait(30)
            self.screen.fill(BK_COLOR)
            self.screen.blit(image_paddle,rect1)
            self.screen.blit(image_paddle,rect2)
            self.screen.blit(image_ball, ball)
            self.screen.blit(text2, [0,HEIGHT-40])
            self.screen.blit(text1, [0,10])

            pygame.display.update()

def main():
    q = queue.Queue()
    client = Hockey(q, "localhost", 2222) # 盤面の初期化
    server = Server(q,"localhost",1111)
    client.draw()                  # メインルーチン

if __name__=="__main__":
    main()
