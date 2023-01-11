import random
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

FPS = 30     # Frame per Second 毎秒のフレーム数

counter = 0

@dataclass
class Shot1:  # クライアント側(送信側の処理)
    def __init__(self, q, address, port):
        self.q = q
        pygame.init()
        pygame.display.set_caption("player1")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.font = pygame.font.Font(None, 55)
        self.address = address
        self.port = port
        self.bgm = pygame.mixer.Sound('src/shooting.mp3')
        self.shoot4 = pygame.mixer.Sound('src/shoot4.mp3')
        self.shoot5 = pygame.mixer.Sound('src/shoot5.mp3')
        self.win = pygame.mixer.Sound('src/win.mp3')
        self.lose = pygame.mixer.Sound('src/lose.mp3')
        self.shoot4.set_volume(0.3)
        self.shoot5.set_volume(0.3)
        self.bgm.play(-1)

    def c2s(self, ip, port, msg):  # サーバー側へ送信
        s =  socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        serv_address = (ip, port)
        s.sendto(msg.encode('utf-8'), serv_address)
    
    def getCount(self):
        return counter

    def draw(self):
        global counter

        Lose = False
        Win = False
        loop = True
        text1 = self.font.render("",True,WHITE)
        text2 = self.font.render("",True,WHITE)
        iwai_HP = 640
        player1_HP = 320
        player2_HP = 320
        enemy_speed1 = 3
        enemy_speed2 = 1
        image_enemy = pygame.image.load('src/iwai.png')
        enemy = image_enemy.get_rect()
        enemy.center = (WIDTH/2, 40)
        image_fighter1 = pygame.image.load('src/fighter1.png')
        image_fighter2 = pygame.image.load('src/fighter2.png')
        image_bullet1 = pygame.image.load('src/bullet1.png')
        image_bullet2 = pygame.image.load('src/bullet2.png')
        image_enemy_bullet1 = pygame.image.load('src/enemy_bullet1.png')
        image_enemy_bullet2 = pygame.image.load('src/enemy_bullet2.png')
        image_enemy_bullet3 = pygame.image.load('src/enemy_bullet3.png')
        fighter1 = image_fighter1.get_rect()
        fighter2 = image_fighter2.get_rect()
        bullet1_1 = image_bullet1.get_rect()
        bullet1_2 = image_bullet1.get_rect()
        bullet1_3 = image_bullet1.get_rect()
        bullet1_4 = image_bullet1.get_rect()
        bullet1_5 = image_bullet1.get_rect()
        bullet1_6 = image_bullet1.get_rect()
        bullet2_1 = image_bullet2.get_rect()
        bullet2_2 = image_bullet2.get_rect()
        bullet2_3 = image_bullet2.get_rect()
        bullet2_4 = image_bullet2.get_rect()
        bullet2_5 = image_bullet2.get_rect()
        bullet2_6 = image_bullet2.get_rect()
        enemy_bullet1_1 = image_enemy_bullet1.get_rect()
        enemy_bullet1_2 = image_enemy_bullet1.get_rect()
        enemy_bullet1_3 = image_enemy_bullet1.get_rect()
        enemy_bullet2_1 = image_enemy_bullet2.get_rect()
        enemy_bullet2_2 = image_enemy_bullet2.get_rect()
        enemy_bullet2_3 = image_enemy_bullet2.get_rect()
        enemy_bullet3_1 = image_enemy_bullet3.get_rect()
        enemy_bullet3_2 = image_enemy_bullet3.get_rect()
        enemy_bullet3_3 = image_enemy_bullet3.get_rect()
        enemy_bullet1_1.center = (enemy.centerx, enemy.bottom)
        enemy_bullet1_2.center = (enemy.centerx, enemy.bottom)
        enemy_bullet1_3.center = (enemy.centerx, enemy.bottom)
        enemy_bullet2_1.center = (enemy.centerx, enemy.bottom)
        enemy_bullet2_2.center = (enemy.centerx, enemy.bottom)
        enemy_bullet2_3.center = (enemy.centerx, enemy.bottom)
        enemy_bullet3_1.center = (enemy.centerx, enemy.bottom)
        enemy_bullet3_2.center = (enemy.centerx, enemy.bottom)
        enemy_bullet3_3.center = (enemy.centerx, enemy.bottom)

        fighter1.center = (200, 600)
        fighter2.center = (400, 600)
        font_result = pygame.font.Font(None, 55)

        enemy_bullet_speed1 = 10
        enemy_bullet_speed2_1 = 10
        enemy_bullet_speed2_2 = 10
        enemy_bullet_speed2_3 = 10
        enemy_bullet_speed3_1 = 10
        enemy_bullet_speed3_2 = 10
        enemy_bullet_speed3_3 = 10
        bullet_speed = 30
        bullet_num_1 = 1
        bullet_num_2 = 1
        boost1_1 = False
        boost1_2 = False
        boost1_3 = False
        boost1_4 = False
        boost1_5 = False
        boost1_6 = False
        boost2_1 = False
        boost2_2 = False
        boost2_3 = False
        boost2_4 = False
        boost2_5 = False
        boost2_6 = False


        enemy = image_enemy.get_rect()
        enemy.center = (WIDTH/2, 40)


        pygame.display.flip()
        while loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    counter = -1
                    loop = False
                if event.type == KEYDOWN:
                    if event.key == K_0:
                        counter = 2
                        loop = False

            pressed_key = pygame.key.get_pressed()
            if pressed_key[K_LEFT]:
                self.c2s(self.address,self.port,pygame.key.name(event.key))
                if fighter1.left > 0:
                    fighter1.move_ip(-10, 0)
            elif pressed_key[K_RIGHT]:
                self.c2s(self.address,self.port,pygame.key.name(event.key))
                if fighter1.right < WIDTH:
                    fighter1.move_ip(10, 0)

            elif pressed_key[K_UP]:
                self.c2s(self.address,self.port,pygame.key.name(event.key))
                if bullet_num_1 == 1 and boost1_1 == False:
                    bullet1_1.center = (fighter1.centerx, fighter1.top)
                    self.screen.blit(image_bullet1, bullet1_1)
                    bullet_num_1 = 2
                    boost1_1 = True
                    self.shoot4.play()
                elif bullet_num_1 == 2 and boost1_2 == False:
                    bullet1_2.center = (fighter1.centerx, fighter1.top)
                    self.screen.blit(image_bullet1, bullet1_2)
                    bullet_num_1 = 3
                    boost1_2 = True
                    self.shoot4.play()
                elif bullet_num_1 == 3 and boost1_3 == False:
                    bullet1_3.center = (fighter1.centerx, fighter1.top)
                    self.screen.blit(image_bullet1, bullet1_3)
                    bullet_num_1 = 4
                    boost1_3 = True
                    self.shoot4.play()
                elif bullet_num_1 == 4 and boost1_4 == False:
                    bullet1_4.center = (fighter1.centerx, fighter1.top)
                    self.screen.blit(image_bullet1, bullet1_4)
                    bullet_num_1 = 5
                    boost1_4 = True
                    self.shoot4.play()
                elif bullet_num_1 == 5 and boost1_5 == False:
                    bullet1_5.center = (fighter1.centerx, fighter1.top)
                    self.screen.blit(image_bullet1, bullet1_5)
                    bullet_num_1 = 6
                    boost1_5 = True
                    self.shoot4.play()
                elif bullet_num_1 == 6 and boost1_6 == False:
                    bullet1_6.center = (fighter1.centerx, fighter1.top)
                    self.screen.blit(image_bullet1, bullet1_6)
                    bullet_num_1 = 1
                    boost1_6 = True
                    self.shoot4.play()

            bullet1_1.move_ip(0, -bullet_speed)
            bullet1_2.move_ip(0, -bullet_speed)
            bullet1_3.move_ip(0, -bullet_speed)
            bullet1_4.move_ip(0, -bullet_speed)
            bullet1_5.move_ip(0, -bullet_speed)
            bullet1_6.move_ip(0, -bullet_speed)
            bullet2_1.move_ip(0, -bullet_speed)
            bullet2_2.move_ip(0, -bullet_speed)
            bullet2_3.move_ip(0, -bullet_speed)
            bullet2_4.move_ip(0, -bullet_speed)
            bullet2_5.move_ip(0, -bullet_speed)
            bullet2_6.move_ip(0, -bullet_speed)

            if bullet1_1.colliderect(enemy) or bullet1_2.colliderect(enemy) or bullet1_3.colliderect(enemy) or  bullet1_4.colliderect(enemy) or bullet1_5.colliderect(enemy) or bullet1_6.colliderect(enemy):
                iwai_HP -= 2
                self.shoot5.play()
            elif bullet2_1.colliderect(enemy) or bullet2_2.colliderect(enemy) or bullet2_3.colliderect(enemy) or  bullet2_4.colliderect(enemy) or bullet2_5.colliderect(enemy) or bullet2_6.colliderect(enemy):
                iwai_HP -= 2
                self.shoot5.play()

            if enemy_bullet1_1.colliderect(fighter1) or enemy_bullet1_2.colliderect(fighter1) or enemy_bullet1_3.colliderect(fighter1) or enemy_bullet2_1.colliderect(fighter1) or enemy_bullet2_2.colliderect(fighter1) or enemy_bullet2_3.colliderect(fighter1) or enemy_bullet3_1.colliderect(fighter1) or enemy_bullet3_2.colliderect(fighter1) or enemy_bullet3_3.colliderect(fighter1):
                player1_HP -= 2

            if enemy_bullet1_1.colliderect(fighter2) or enemy_bullet1_2.colliderect(fighter2) or enemy_bullet1_3.colliderect(fighter2) or enemy_bullet2_1.colliderect(fighter2) or enemy_bullet2_2.colliderect(fighter2) or enemy_bullet2_3.colliderect(fighter2) or enemy_bullet3_1.colliderect(fighter2) or enemy_bullet3_2.colliderect(fighter2) or enemy_bullet3_3.colliderect(fighter2):
                player2_HP -= 2

            enemy_bullet1_1.move_ip(0, enemy_bullet_speed1)
            enemy_bullet1_2.move_ip(0, enemy_bullet_speed1)
            enemy_bullet1_3.move_ip(0, enemy_bullet_speed1)
            enemy_bullet2_1.move_ip(enemy_bullet_speed2_1, enemy_bullet_speed1)
            enemy_bullet2_2.move_ip(enemy_bullet_speed2_2, enemy_bullet_speed1)
            enemy_bullet2_3.move_ip(enemy_bullet_speed2_3, enemy_bullet_speed1)
            enemy_bullet3_1.move_ip(-enemy_bullet_speed3_1, enemy_bullet_speed1)
            enemy_bullet3_2.move_ip(-enemy_bullet_speed3_2, enemy_bullet_speed1)
            enemy_bullet3_3.move_ip(-enemy_bullet_speed3_3, enemy_bullet_speed1)

            if enemy_bullet1_1.top >= HEIGHT:
                enemy_bullet1_1.center = (enemy.centerx, enemy.bottom)
            elif enemy_bullet1_2.top >= HEIGHT + 100:
                enemy_bullet1_2.center = (enemy.centerx, enemy.bottom)
            elif enemy_bullet1_3.top >= HEIGHT + 200:
                enemy_bullet1_3.center = (enemy.centerx, enemy.bottom)

            if enemy_bullet2_1.top >= HEIGHT:
                enemy_bullet2_1.center = (enemy.centerx, enemy.bottom)
                if enemy_bullet_speed2_1 <= 0:
                    enemy_bullet_speed2_1 *= -1
            elif enemy_bullet2_2.top >= HEIGHT + 100:
                enemy_bullet2_2.center = (enemy.centerx, enemy.bottom)
                if enemy_bullet_speed2_2 <= 0:
                    enemy_bullet_speed2_2 *= -1
            elif enemy_bullet2_3.top >= HEIGHT + 200:
                enemy_bullet2_3.center = (enemy.centerx, enemy.bottom)
                if enemy_bullet_speed2_3 <= 0:
                    enemy_bullet_speed2_3 *= -1

            if enemy_bullet3_1.top >= HEIGHT:
                enemy_bullet3_1.center = (enemy.centerx, enemy.bottom)
                if enemy_bullet_speed3_1 <= 0:
                    enemy_bullet_speed3_1 *= -1
            elif enemy_bullet3_2.top >= HEIGHT + 100:
                enemy_bullet3_2.center = (enemy.centerx, enemy.bottom)
                if enemy_bullet_speed3_2 <= 0:
                    enemy_bullet_speed3_2 *= -1
            elif enemy_bullet3_3.top >= HEIGHT + 200:
                enemy_bullet3_3.center = (enemy.centerx, enemy.bottom)
                if enemy_bullet_speed3_3 <= 0:
                    enemy_bullet_speed3_3 *= -1


            if iwai_HP <= 0 or Win == True:
                self.c2s(self.address,self.port,"win")

                text_win = font_result.render("YOU WIN!!", True, WHITE)
                enemy.center = (WIDTH/2 - 50, HEIGHT/2)
                self.screen.blit(text_win, [WIDTH/2,HEIGHT/2 - 10])
                pygame.display.update()
                self.bgm.stop()
                self.win.set_volume(0.5)
                self.win.play()
                pygame.time.wait(3000)
                counter = 2
                loop = False

            if player1_HP <= 0 and player2_HP <= 0 or Lose == True:
                self.c2s(self.address,self.port,"lose")
                text_lose = font_result.render("GAME OVER!!", True, WHITE)
                enemy.center = (WIDTH/2 - 50, HEIGHT/2)
                self.screen.blit(text_lose, [WIDTH/2,HEIGHT/2 - 10])
                pygame.display.update()
                self.bgm.stop()
                self.lose.set_volume(0.5)
                self.lose.play()
                pygame.time.wait(3000)
                counter = 2
                loop = False


            if enemy_bullet2_1.right >= WIDTH:
                enemy_bullet_speed2_1 *= -1
            elif enemy_bullet2_1.left <= 0:
                enemy_bullet_speed2_1 *= -1

            if enemy_bullet2_2.right >= WIDTH:
                enemy_bullet_speed2_2 *= -1
            elif enemy_bullet2_2.left <= 0:
                enemy_bullet_speed2_2 *= -1

            if enemy_bullet2_3.right >= WIDTH:
                enemy_bullet_speed2_3 *= -1
            elif enemy_bullet2_3.left <= 0:
                enemy_bullet_speed2_3 *= -1

            if enemy_bullet3_1.left <= 0:
                enemy_bullet_speed3_1 *= -1
            elif enemy_bullet3_1.right >= WIDTH:
                enemy_bullet_speed3_1 *= -1

            if enemy_bullet3_2.left <= 0:
                enemy_bullet_speed3_2 *= -1
            elif enemy_bullet3_2.right >= WIDTH:
                enemy_bullet_speed3_2 *= -1

            if enemy_bullet3_3.left <= 0:
                enemy_bullet_speed3_3 *= -1
            elif enemy_bullet3_2.right >= WIDTH:
                enemy_bullet_speed3_3 *= -1

            if enemy.left <= 0:
                enemy_speed1 *= -1
                enemy_speed2 *= -1
            elif enemy.right >= WIDTH:
                enemy_speed1 *= -1
                enemy_speed2 *= -1
            elif enemy.top <= 0:
                enemy_speed2 *= -1
            enemy.move_ip(enemy_speed1, enemy_speed2)

            if self.q.empty()==False:
                que = self.q.get().decode()
                if que == 'left':
                    if fighter2.left > 0:
                        fighter2.move_ip(-10, 0)
                elif que == 'right':
                    if fighter2.right < WIDTH:
                        fighter2.move_ip(10, 0)

                if que == 'up':
                    if bullet_num_2 == 1 and boost2_1 == False:
                        bullet2_1.center = (fighter2.centerx, fighter2.top)
                        self.screen.blit(image_bullet2, bullet2_1)
                        bullet_num_2 = 2
                        boost2_1 = True
                        self.shoot4.play()
                    elif bullet_num_2 == 2 and boost2_2 == False:
                        bullet2_2.center = (fighter2.centerx, fighter2.top)
                        self.screen.blit(image_bullet2, bullet2_2)
                        bullet_num_2 = 3
                        boost2_2 = True
                        self.shoot4.play()
                    elif bullet_num_2 == 3 and boost2_3 == False:
                        bullet2_3.center = (fighter2.centerx, fighter2.top)
                        self.screen.blit(image_bullet2, bullet2_3)
                        bullet_num_2 = 4
                        boost2_3 = True
                        self.shoot4.play()
                    elif bullet_num_2 == 4 and boost2_4 == False:
                        bullet2_4.center = (fighter2.centerx, fighter2.top)
                        self.screen.blit(image_bullet2, bullet2_4)
                        bullet_num_2 = 5
                        boost2_1 = True
                        self.shoot4.play()
                    elif bullet_num_2 == 5 and boost2_5 == False:
                        bullet2_5.center = (fighter2.centerx, fighter2.top)
                        self.screen.blit(image_bullet2, bullet2_5)
                        bullet_num_2 = 6
                        boost2_5 = True
                        self.shoot4.play()
                    elif bullet_num_2 == 6 and boost2_6 == False:
                        bullet2_6.center = (fighter2.centerx, fighter2.top)
                        self.screen.blit(image_bullet2, bullet2_6)
                        bullet_num_2 = 1
                        boost2_6 = True
                        self.shoot4.play()
                
                if que == "win":
                    Win = True
                    self.bgm.stop()
                    self.win.set_volume(0.5)
                    self.win.play()
                elif que == "lose":
                    Lose = True
                    self.bgm.stop()
                    self.win.set_volume(0.5)
                    self.win.play()

            if bullet1_1.top <= 0:
                boost1_1 = False
            if bullet1_2.top <= 0:
                boost1_2 = False
            if bullet1_3.top <= 0:
                boost1_3 = False
            if bullet1_4.top <= 0:
                boost1_4 = False
            if bullet1_5.top <= 0:
                boost1_5 = False
            if bullet1_6.top <= 0:
                boost1_6 = False
            if bullet2_1.top <= 0:
                boost2_1 = False
            if bullet2_2.top <= 0:
                boost2_2 = False
            if bullet2_3.top <= 0:
                boost2_3 = False
            if bullet2_4.top <= 0:
                boost2_4 = False
            if bullet2_5.top <= 0:
                boost2_5 = False
            if bullet2_6.top <= 0:
                boost2_6 = False

            pygame.display.update()
            pygame.time.wait(30)
            self.screen.fill(BK_COLOR)
            self.screen.blit(image_fighter1, fighter1)
            self.screen.blit(image_fighter2, fighter2)
            self.screen.blit(image_enemy, enemy)
            self.screen.blit(text2, [0,HEIGHT-40])
            self.screen.blit(text1, [0,10])
            self.screen.blit(image_bullet1, bullet1_1)
            self.screen.blit(image_bullet1, bullet1_2)
            self.screen.blit(image_bullet1, bullet1_3)
            self.screen.blit(image_bullet1, bullet1_4)
            self.screen.blit(image_bullet1, bullet1_5)
            self.screen.blit(image_bullet1, bullet1_6)
            self.screen.blit(image_bullet2, bullet2_1)
            self.screen.blit(image_bullet2, bullet2_2)
            self.screen.blit(image_bullet2, bullet2_3)
            self.screen.blit(image_bullet2, bullet2_4)
            self.screen.blit(image_bullet2, bullet2_5)
            self.screen.blit(image_bullet2, bullet2_6)
            self.screen.blit(image_enemy_bullet1, enemy_bullet1_1)
            self.screen.blit(image_enemy_bullet1, enemy_bullet1_2)
            self.screen.blit(image_enemy_bullet1, enemy_bullet1_3)
            self.screen.blit(image_enemy_bullet2, enemy_bullet2_1)
            self.screen.blit(image_enemy_bullet2, enemy_bullet2_2)
            self.screen.blit(image_enemy_bullet2, enemy_bullet2_3)
            self.screen.blit(image_enemy_bullet3, enemy_bullet3_1)
            self.screen.blit(image_enemy_bullet3, enemy_bullet3_2)
            self.screen.blit(image_enemy_bullet3, enemy_bullet3_3)
            pygame.draw.rect(self.screen, (0,255,0), (0,0,iwai_HP,10))
            pygame.draw.rect(self.screen, (255,0,0), (0,HEIGHT-10,player1_HP,10))
            pygame.draw.rect(self.screen, (0,0,255), (WIDTH / 2,HEIGHT-10,player2_HP,10))


def main():
    q = queue.Queue()
    server = Server(q, "localhost", 2222)
    Shot1(q, "localhost", 8080) .draw()                  # メインルーチン

if __name__=="__main__":
    main()