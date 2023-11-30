import pygame
import os
from pygame.locals import*
from random import randint
from sys import exit
from OpenGL.GL import*
import requests

pygame.init()

# Arquivo e diretório de imagens
file_principal = os.path.dirname(__file__)
file_image = os.path.join(file_principal, 'image')
file_song = os.path.join(file_principal, 'song')

# Variáveis do jogo
largura = 1280
altura = 720
pontos = 0
velocidade = 5
died = False
missel_x = 200
missel_y = 300
nave_x = 200
nave_y = 300
alien_x = randint(10,1280)
alien_y = randint(10,720)
fonte = pygame.font.SysFont('ariel',40,True,True)
fundo = pygame.image.load(os.path.join(file_image, 'fundo1.jpg')) 
fundo = pygame.transform.scale(fundo, (largura,altura))
nave = pygame.image.load(os.path.join(file_image, 'nave.png'))
nave = pygame.transform.scale(nave, (60,60))
nave = pygame.transform.rotate(nave, -90)
nave_rect = nave.get_rect()
missel = pygame.image.load(os.path.join(file_image, 'missile.png'))
missel = pygame.transform.scale(missel, (20,20))
missel = pygame.transform.rotate(missel, -45)
missel_rect = missel.get_rect()
alien = pygame.image.load(os.path.join(file_image, 'alien.png'))
alien = pygame.transform.scale(alien, (70,70))
alien_rect = alien.get_rect()
musica = pygame.mixer.music.load(os.path.join(file_song, 'fundo.ogg'))
pygame.mixer.music.play(-1)
barulho = pygame.mixer.Sound(os.path.join(file_song, 'explosão.mp3'))
disparo = pygame.mixer.Sound(os.path.join(file_song, 'disparo.mp3'))
attack = False

saude_da_nave = 100  # Valor inicial da saúde
largura_da_barra_maxima = 200  # Largura máxima da barra de vida
barra_de_vida_cor = (0, 255, 0)  # Cor verde
barra_de_vida_rect = pygame.Rect(10, 10, largura_da_barra_maxima, 10)  # Posição e tamanho da barra de vid
 
# Display
screen = pygame.display.set_mode((largura,altura))
pygame.display.set_caption('navejoker')
relogio = pygame.time.Clock()

# Função para enviar pontuação para o servidor
def enviar_pontuacao(nome, pontuacao):
    data = {'name': nome, 'score': pontuacao}
    response = requests.post('http://127.0.0.1:5000/submit', data=data)
    if response.status_code == 200:
        print("Pontuação enviada com sucesso!")

# Função para reiniciar o jogo
def reiniciar():
    global nave_x,nave_y,alien_x,alien_y,pontos,died,pontos
    died = False
    nave_x = 200 
    nave_y = 300
    alien_x = randint(10,1280)
    alien_y = randint(10,720)
    pontos = 0
    saude_da_nave = 100  # Restaura a saúde da nave ao reiniciar

# Loop do jogo
jogando = True
while jogando:
    relogio.tick(60)
    mensagem = f'Pontuação : {pontos}'
    texto = fonte.render(mensagem,True,(255,255,255))
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jogando = False
       
    screen.blit(fundo, (0,0))
   
    # Movimentacao tela
    rel_x = largura % fundo.get_rect().width
    screen.blit(fundo, (rel_x -fundo.get_rect().width,0))
    if rel_x < 1280:
        screen.blit(fundo, (rel_x,0))
    # Velocidade tela
    largura -= 2
   
    screen.blit(texto, (30,30))
    screen.blit(missel,(missel_x,missel_y))
    screen.blit(alien,(alien_x,alien_y))
    screen.blit(nave, (nave_x,nave_y))
   
    comandos = pygame.key.get_pressed()
    if comandos[pygame.K_UP] and nave_y > 1:
        nave_y -= velocidade
        if not attack:
            missel_y -= velocidade
    if comandos[pygame.K_DOWN] and nave_y < 665:
        nave_y += velocidade
        if not attack:
            missel_y += velocidade
    if comandos[pygame.K_LEFT] and nave_x > 1:
        nave_x -= velocidade
        if not attack:
            missel_x -= velocidade
    if comandos[pygame.K_RIGHT] and nave_x < 1200:
        nave_x += velocidade
        if not attack:
            missel_x += velocidade 
    if comandos[pygame.K_SPACE]:
        attack = True
        missel_x = nave_x
        missel_y = nave_y
        disparo.play()
      
    
    alien_x -= 4
    missel_x += velocidade
   
    if alien_x < -2:
        alien_x = randint(10,1280) 
        alien_y = randint(10,720)
      
    nave_rect.x = nave_x
    nave_rect.y = nave_y 
    alien_rect.x = alien_x
    alien_rect.y = alien_y
    missel_rect.x = missel_x
    missel_rect.y = missel_y
   
    # Colisão do míssil com o alienígena
    if missel_rect.colliderect(alien_rect):
        barulho.play()
        pontos = pontos + 1
        alien_x = randint(10,1280) 
        alien_y = randint(10,720)
        enviar_pontuacao("Nome do Jogador", pontos)
       
    # Colisão da nave com o alienígena
    if nave_rect.colliderect(alien_rect):
        saude_da_nave -= 10  # Diminui a saúde da nave quando ocorre uma colisão
        barulho.play()
        if saude_da_nave <= 0:
            reiniciar()
            saude_da_nave = 100
            died = True
            while died:
                fonte2 = pygame.font.SysFont('ariel',90,True,True)
                mensagem = f'Aperte R para jogar novamente'
                texto = fonte2.render(mensagem,True,(255,255,255))
          
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == K_r:
                            reiniciar()
                            saude_da_nave = 100
                
                screen.fill((0,0,0))
                screen.blit(texto, (250,300))
                pygame.display.update()

    pygame.draw.rect(screen, barra_de_vida_cor, barra_de_vida_rect)
               
    pygame.display.flip()

pygame.quit()
exit()
   