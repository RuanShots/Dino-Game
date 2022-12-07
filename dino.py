from tkinter import image_names
import pygame
from pygame.locals import *
from sys import exit
import os
from random import randrange, choice
import sqlite3



pygame.init()
pygame.mixer.init()

diretorio_principal = os.path.dirname(__file__)
diretorio_imagens = os.path.join(diretorio_principal, 'imagens')
diretorio_sons = os.path.join(diretorio_principal, 'sons')

LARGURA = 640
ALTURA = 480
SPEED = 10
PULO = 20
SCORE = 0

BRANCO = (255,255,255)

tela = pygame.display.set_mode((LARGURA, ALTURA))

pygame.display.set_caption('Dino Game')

sprite_sheet = pygame.image.load(os.path.join(diretorio_imagens, 'dinoSpritesheet.png')).convert_alpha()

som_collide = pygame.mixer.Sound(os.path.join(diretorio_sons, "death_sound.wav"))
som_collide.set_volume(1)
colidiu = False

som_score = pygame.mixer.Sound(os.path.join(diretorio_sons, "score_sound.wav"))
som_score.set_volume(1)

escolha_obs = choice([0, 1])



def msm(msm, tamanho, cor):
    fonte = pygame.font.SysFont("comicsansms", tamanho, True, False)
    mensagem = f"{msm}"
    texto = fonte.render(mensagem, True, cor)
    return texto

def reiniciar():
    global SCORE, SPEED, colidiu, escolha_obs
    SCORE = 0
    SPEED = 10
    colidiu = False
    dino_voador.rect.x = LARGURA
    cacto.rect.x = LARGURA
    escolha_obs = choice([0, 1])
    dino.rect.y = LARGURA - 64 - 96//2
    dino.pulo = False


class Dino(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.som_pulo = pygame.mixer.Sound(os.path.join(diretorio_sons, "jump_sound.wav"))
        self.som_pulo.set_volume(1)
        
        self.imagens_dinossauro = []
        
        
        for i in range(3):
            img = sprite_sheet.subsurface((i*32,0), (32,32))
            img = pygame.transform.scale(img, (32*3, 32*3))
            self.imagens_dinossauro.append(img)
        
        
        self.index_lista = 0
        self.image = self.imagens_dinossauro[self.index_lista]
        self.rect = self.image.get_rect()
        self.rect.center = (100, ALTURA - 64)
        self.mask = pygame.mask.from_surface(self.image)
        self.pos_y = ALTURA - 64 - 96//2

        self.pulo = False

    def pular(self):
        self.pulo = True
        self.som_pulo.play()

    def update(self):

        if self.pulo == True:
            if self.rect.y <= 270:
                self.pulo = False
            self.rect.y -= PULO
        else:
            if self.rect.y < self.pos_y:
                self.rect.y += PULO - 10
            else:
                self.rect.y = self.pos_y


        if self.index_lista > 2:
            self.index_lista = 0
        self.index_lista += SPEED * 0.025
        self.image = self.imagens_dinossauro[int(self.index_lista)]
    



class Nuvens(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = sprite_sheet.subsurface((224, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (3 * 32, 3* 32))
        self.rect = self.image.get_rect()
        self.rect.y = randrange(50, 200, 50)
        self.rect.x = LARGURA - randrange(30, 300, 90)
    
    def update(self):
        if self.rect.topright[0] <  0:
            self.rect.y = randrange(50, 200, 50)
            self.rect.x = LARGURA - randrange(30, 300, 90)
            self.rect.x = LARGURA
        self.rect.x -= SPEED


class Chao(pygame.sprite.Sprite):
    def __init__(self, pos_x):
        pygame.sprite.Sprite.__init__(self)

        self.image = sprite_sheet.subsurface((6 * 32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (2 * 32, 2 * 32))
        self.rect = self.image.get_rect()
        self.rect.y = ALTURA - 64
        self.rect.x = pos_x * 64
    
    def update(self):
        if self.rect.topright[0] <  0:
            self.rect.x = LARGURA
        self.rect.x -= 10


class Cacto(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = sprite_sheet.subsurface((5 * 32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (2 * 32, 2 * 32))
        self.rect = self.image.get_rect()
        self.rect.center = (LARGURA, ALTURA - 64)
        self.mask = pygame.mask.from_surface(self.image)
        self.escolha = escolha_obs

    def update(self):

        if self.escolha == 0:
            if self.rect.topright[0] <  0:
                self.rect.x = LARGURA
            self.rect.x -= SPEED


class DinoVoador(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.imagens_dino = []
        for i in range(3, 5):
            img = sprite_sheet.subsurface((i * 32, 0), (32, 32))
            img = pygame.transform.scale(img, (32 * 3, 32 * 3))
            self.imagens_dino.append(img) 

        self.index = 0
        self.image = self.imagens_dino[self.index]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (LARGURA, 300)
        self.rect.x = LARGURA
        self.escolha = escolha_obs
    
    def update(self):
        if self.escolha == 1:
            if self.rect.topright[0] <  0:
                self.rect.x = LARGURA
            self.rect.x -= SPEED

            if self.index > 1:
                self.index = 0
            self.index += SPEED * 0.025
            self.image = self.imagens_dino[int(self.index)]

todas_as_sprites = pygame.sprite.Group()
dino = Dino()
todas_as_sprites.add(dino)

for i in range(4):
    nuvem = Nuvens()
    todas_as_sprites.add(nuvem)

for i in range(LARGURA * 2//64):
    chao = Chao(i)
    todas_as_sprites.add(chao)

cacto = Cacto()
todas_as_sprites.add(cacto)

dino_voador = DinoVoador()
todas_as_sprites.add(dino_voador)

obstaculos = pygame.sprite.Group()
obstaculos.add(cacto)
obstaculos.add(dino_voador)


relogio = pygame.time.Clock()

while True:
    relogio.tick(30)
    if SCORE >= 1000 and SCORE <= 1500:
        tela.fill((245,245,245))
        if SCORE > 1002:
            tela.fill((235,235,235))
            if SCORE > 1006:
                tela.fill((225,225,225))
    else:
        tela.fill((BRANCO))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if colidiu == True:
                    reiniciar()
                elif dino.rect.y != dino.pos_y:
                    pass
                else:
                    dino.pular()


    todas_as_sprites.draw(tela)
    
    colisoes = pygame.sprite.spritecollide(dino, obstaculos, False, pygame.sprite.collide_mask)

    if colisoes and colidiu == False:
        som_collide.play(1)
        colidiu = True
    
    if colidiu == True:
        if SCORE % 100 == 0:
            SCORE += 1


        
        g_o =msm("Game Over", 40, (0, 0, 0))
        scr = msm("Pontos", 40, (0, 0, 0))
        sub = msm("Aperte 'SPACE'", 20, (0, 0, 0))
        tela.blit(sub, (LARGURA//2 + 20, (ALTURA//2) + 60))
        tela.blit(scr, (LARGURA - 280, ALTURA - 430))
        tela.blit(g_o, (LARGURA//2, ALTURA//2))

    else:
        SCORE += 0.5
        todas_as_sprites.update()
        pontuador = msm(int(SCORE), 40, (0, 0, 0))
    
    if SCORE % 100 == 0:
        som_score.play()
        if SPEED >= 23:
            SPEED += 0
        else:
            SPEED += 1
    
    
    if cacto.rect.topright[0] <= 0 or dino_voador.rect.topright[0] <= 0:
        escolha_obs = choice([0, 1])
        cacto.rect.x = LARGURA
        dino_voador.rect.x = LARGURA
        cacto.escolha = escolha_obs
        dino_voador.escolha = escolha_obs

    tela.blit(pontuador, (LARGURA - 140, ALTURA - 430))
    pygame.display.flip()