import pygame
from sprites import *
from config import *
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sys

from Batalla import ejecutar_batalla,game_over

enemy_defeat=0 
class Game:
    def __init__(self):
        pygame.init()  
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption("Juego Principal")
        self.clock = pygame.time.Clock()
        self.running = True
        self.character_spritesheet = Spritesheet('img/heroe.png')
        self.terrain_spritesheet = Spritesheet('img/terreno-roca.png')
        self.enemy_spritesheet = Spritesheet('img/enemy.png')
        self.attack_spritesheet = Spritesheet('img/attack.png')
        self.font = pygame.font.Font('img/Ruritania.ttf', 32)
        self.go_background = pygame.image.load('img/gameover.png')

    def new(self):
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attack = pygame.sprite.LayeredUpdates()
        self.TileMap()

    def TileMap(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == "B":
                    Block(self, j, i)
                if column == "P":
                    self.player = Player(self, j, i)
                if column == 'E':
                    enemy = Enemy(self, j, i)
                    self.enemies.add(enemy)
                if column == "O":
                    Obstacle(self, j, i)

    def events(self):
        global enemy_defeat
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Calcular la posición de ataque
                    dx, dy = 0, 0
                    if self.player.facing == 'up':
                        dy = -TILESIZE
                    elif self.player.facing == 'down':
                        dy = TILESIZE
                    elif self.player.facing == 'right':
                        dx = TILESIZE
                    elif self.player.facing == 'left':
                        dx = -TILESIZE
                    
                    attack_rect = self.player.rect.move(dx, dy)
                    Attack(self, attack_rect.x, attack_rect.y)

                    #  Detectar colisión con enemigo para activar batalla
                    for enemy in self.enemies:
                        if enemy.rect.colliderect(attack_rect):
                            # Guardar tamaño original
                            old_screen = self.screen
                            old_size = self.screen.get_size()

                            # Cambiar temporalmente la pantalla a 800x600 para la batalla
                            self.screen = pygame.display.set_mode((800, 600))
                            resultado = ejecutar_batalla(self.screen)
                            if game_over==1:
                                res=1
                            elif game_over==-1:
                                res=0    
                            # Restaurar pantalla principal
                            self.screen = pygame.display.set_mode(old_size)
                            pygame.display.set_caption("Juego Principal")
                            
                            if resultado == 1:
                                print("¡Victoria detectada! Eliminando enemigo...")
                                enemy.kill()  # Eliminar enemigo si pierde batalla 
                                enemy_defeat+=1
                                if enemy_defeat:
                                    print(f"contador de enemigos muertos:",enemy_defeat)
                                if enemy_defeat == 3:
                                    print("¡Has ganado el juego!")
                                    pygame.quit()
                                    self.running = False
                                    self.playing = False
                                    Victoria()  # Mostrar pantalla de victoria
                                    return
                            elif resultado == 0:
                                self.playing = False  # Juego termina si pierde batalla
                            break  # Solo luchar con un enemigo a la vez
        
    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        pygame.display.update()
        self.clock.tick(FPS)

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def game_over(self):
        text = self.font.render('GAME OVER', True, WHITE)
        text_rect = text.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 2))
        restartbutton = Button(10, WIN_HEIGHT - 60, 120, 50, WHITE, BLACK, 'Restart', 32)

        for sprite in self.all_sprites:
            sprite.kill()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if restartbutton.pulsado(mouse_pos, mouse_pressed):
                self.new()
                self.main()

            self.screen.blit(self.go_background, (0, 0))
            self.screen.blit(text, text_rect)
            self.screen.blit(restartbutton.image, restartbutton.rect)
            self.clock.tick(FPS)
            pygame.display.update()
class Victoria():                                                                                            
    def __init__(self):
        
        self.vic=tk.Tk()
        self.vic.title("VICTORY")
        self.vic.geometry("640x480")
        self.vic.resizable(False,False)
        vimage = Image.open('img/V.png')                     
        vimage = vimage.resize((640, 480))
        self.vphoto = ImageTk.PhotoImage(vimage)
        self.victory_label = tk.Label(self.vic, image=self.vphoto)
        self.victory_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.endbutton=tk.Button(self.vic,text="salir",font=('Times New Roman',14), bg="#cc3333",fg="white",command=self.End)
        self.endbutton.place(x=230, y=420, width=180, height=40)
        self.vic.mainloop()
    def End(self):
        self.vic.destroy()
        sys.exit()       
class Intro():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GAME")
        self.root.geometry("640x480")
        self.root.resizable(False, False)
        bgimage = Image.open('img/bgi.jpg')                     
        bgimage = bgimage.resize((640, 480))
        self.bgphoto = ImageTk.PhotoImage(bgimage)
        self.background_label = tk.Label(self.root, image=self.bgphoto)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.startbutton = tk.Button(self.root, text="Iniciar Juego", font=("Times New Roman", 14), bg="#007acc", fg="white", command=self.start_game)
        self.startbutton.place(x=230, y=360, width=180, height=40)

        self.quitbutton = tk.Button(self.root, text="Salir", font=("Times New Roman", 14), bg="#cc3333", fg="white", command=self.quit)
        self.quitbutton.place(x=230, y=420, width=180, height=40)

        self.root.mainloop()

    def start_game(self):
        self.root.destroy()
        g = Game()
        g.new()
        while g.running:
            g.main()
            g.game_over()

    def quit(self):
        self.root.destroy()
        sys.exit()

if __name__ == '__main__':
    Intro()
#if enemy_defeat==3:
    #print("si funciono xd")
    #Victoria() 
pygame.quit()
sys.exit()
