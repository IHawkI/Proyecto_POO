import pygame
from config import *
import math
import random
class Spritesheet:
    def __init__(self,file):
        self.sheet=pygame.image.load(file).convert()
    def get_sprite(self,x,y,width,height):
        sprite=pygame.Surface([width,height])
        sprite.blit(self.sheet, (0,0), (x,y,width,height))
        sprite.set_colorkey(BLACK)
        return sprite    
class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game=game
        self.x=x*TILESIZE
        self.y=y*TILESIZE
        self.start_x=x
        self.start_y=y
        self.width=TILESIZE
        self.height=TILESIZE
        self.x_change=0 
        self.y_change=0
        self._layer=PLAYER_LAYER
        self.groups=self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = self.game.character_spritesheet.get_sprite(3, 2, 32, 32)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.facing='down' 
        self.animation_loop=1
    def respawn(self):
        self.x = self.start_x * TILESIZE
        self.y = self.start_y * TILESIZE
        self.rect.x = self.x
        self.rect.y = self.y
    
    def update(self):
        self.movement()
        self.animate()
        self.collide_enemy()
        self.rect.x+=self.x_change
        self.collide_b('x')
        self.rect.y+=self.y_change
        self.collide_b('y')
        self.x_change=0
        self.y_change=0
    def movement(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x_change -= PLAYER_SPEED #en archivo de config para cambiar la velocidad tanto del enemigo como el player ~-~
            self.facing='left'
        if keys[pygame.K_RIGHT]:
            self.x_change += PLAYER_SPEED 
            self.facing='right'        
        if keys[pygame.K_UP]:
            self.y_change -= PLAYER_SPEED 
            self.facing='up'
        if keys[pygame.K_DOWN]:
            self.y_change += PLAYER_SPEED 
            self.facing='down'   
    def collide_enemy(self):                    
          hits=pygame.sprite.spritecollide(self,self.game.enemies, False)
          if hits:
                self.kill()
                self.game.playing=False                 
              
    def collide_b(self,direction):
        if direction=="x":
            hits=pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change>0:
                    self.rect.x=hits[0].rect.left-self.rect.width
                if self.x_change<0:
                    self.rect.x=hits[0].rect.right
        if direction=="y":
            hits=pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change>0:
                    self.rect.y=hits[0].rect.top - self.rect.height
                if self.y_change<0:
                    self.rect.y=hits[0].rect.bottom 
    def animate(self):
        down_animations = [self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(35, 2, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(68, 2, self.width, self.height)]
        up_animations = [self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(35, 34, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(68, 34, self.width, self.height)]
        left_animations = [self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(35, 98, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(68, 98, self.width, self.height)]
        right_animations = [self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(35, 66, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(68, 66, self.width, self.height)]
        if self.facing=='down':
            if self.y_change==0:
                self.image=self.game.character_spritesheet.get_sprite(3,2,self.width,self.height)
            else:
                self.image=down_animations[math.floor(self.animation_loop)]
                self.animation_loop+=0.1
                if self.animation_loop >=3:
                    self.animation_loop=1
        if self.facing=='up':
            if self.y_change==0:
                self.image=self.game.character_spritesheet.get_sprite(3,34,self.width,self.height)
            else:
                self.image=up_animations[math.floor(self.animation_loop)]
                self.animation_loop+=0.1
                if self.animation_loop >=3:
                    self.animation_loop=1
        if self.facing=='right':
            if self.x_change==0:
                self.image=self.game.character_spritesheet.get_sprite(3,66,self.width,self.height)
            else:
                self.image=right_animations[math.floor(self.animation_loop)]
                self.animation_loop+=0.1
                if self.animation_loop >=3:
                    self.animation_loop=1
        if self.facing=='left':
            if self.x_change==0:
                self.image=self.game.character_spritesheet.get_sprite(3,98,self.width,self.height)
            else:
                self.image=left_animations[math.floor(self.animation_loop)]
                self.animation_loop+=0.1
                if self.animation_loop >=3:
                    self.animation_loop=1   
class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game=game
        self._layer=ENEMY_LAYER
        self.groups=self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.x=x*TILESIZE
        self.y=y*TILESIZE
        self.width=TILESIZE
        self.height=TILESIZE
        self.x_change=0
        self.y_change=0
        self.image=self.game.enemy_spritesheet.get_sprite(3,2,self.width,self.height)
        self.image.set_colorkey(BLACK)
        self.rect=self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y
        self.facing=random.choice(['left','right'])
        self.animation_loop=1
        self.movement_loop=0
        self.max_travel=random.randint(20,30)
    def update(self):
        self.movement()
        self.animate()
        self.rect.x+=self.x_change
        #self.collide_b('x')
        self.rect.y+=self.y_change
        #self.collide_b('y')
        self.x_change=0
        self.y_change=0
    def movement(self):
        if self.facing=='left':
            self.x_change -= ENEMY_SPEED
            self.movement_loop-=1
            if self.movement_loop <= -self.max_travel:
                self.facing='right'
        if self.facing=='right':
            self.x_change += ENEMY_SPEED
            self.movement_loop+=1                                                                              
            if self.movement_loop>=self.max_travel:
                self.facing='left'
        #if self.facing=='up':
            #self.y_change-=ENEMY_SPEED
            #self.movement_loop-=1
            #if self.movement_loop<=-self.max_travel:
                #self.facing="down"
        #if self.facing=='down':
            #self.y_change+=ENEMY_SPEED
            #self.movement_loop+=1
            #if self.movement_loop>=self.max_travel:
                #self.facing="up"                
                        
    def animate(self):
        left_animations = [self.game.enemy_spritesheet.get_sprite(3, 98, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(35, 98, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(68, 98, self.width, self.height)]
        right_animations = [self.game.enemy_spritesheet.get_sprite(3, 66, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(35, 66, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(68, 66, self.width, self.height)]
        if self.facing=='right':
            if self.x_change==0:
                self.image=self.game.enemy_spritesheet.get_sprite(3,66,self.width,self.height)
            else:
                self.image=right_animations[math.floor(self.animation_loop)]
                self.animation_loop+=0.1
                if self.animation_loop >=3:
                    self.animation_loop=1
        if self.facing=='left':
            if self.x_change==0:
                self.image=self.game.enemy_spritesheet.get_sprite(3,98,self.width,self.height)
            else:
                self.image=left_animations[math.floor(self.animation_loop)]
                self.animation_loop+=0.1
                if self.animation_loop >=3:
                    self.animation_loop=1           
class Block(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game=game
        self._layer=BLOCK_LAYER
        self.groups=self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x=x*TILESIZE
        self.y=y*TILESIZE
        self.width=TILESIZE
        self.height=TILESIZE      
        self.image=self.game.terrain_spritesheet.get_sprite(390,280,35,35) #bloque verde de marco 390,280,40,40
        self.rect=self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y
class Obstacle(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game=game
        self._layer=BLOCK_LAYER
        self.groups=self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x=x*TILESIZE
        self.y=y*TILESIZE
        self.width=TILESIZE
        self.height=TILESIZE      
        self.image=self.game.terrain_spritesheet.get_sprite(960,448,self.width,self.height) 
        self.rect=self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y
class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x , y):
        self.game=game
        self._layer=GROUND_LAYER
        self.groups=self.game.all_sprites
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.x=x*TILESIZE
        self.y=y*TILESIZE
        self.width=TILESIZE    
        self.height=TILESIZE
        self.image=self.game.terrain_spritesheet.get_sprite(64, 352, self.width, self.height)
        self.rect=self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y
class Button():
    def __init__(self,x,y,width,height, fg,bg,content,font_size):
        self.font=pygame.font.Font('img/ruritania.ttf',font_size)
        self.content=content
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.fg=fg
        self.bg=bg
        self.image=pygame.Surface((self.width,self.height))
        self.image.fill(self.bg)
        self.rect=self.image.get_rect()
        self.rect.x=self.x  
        self.rect.y=self.y
        self.text=self.font.render(self.content,True,self.fg)
        self.text_rect=self.text.get_rect(center=(self.width/2, self.height/2))
        self.image.blit(self.text,self.text_rect)
    def pulsado(self,pos,pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False
class Attack(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game=game
        self._layer=PLAYER_LAYER
        self.groups=self.game.all_sprites, self.game.attack
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.x=x
        self.y=y 
        self.width=TILESIZE
        self.height=TILESIZE
        self.animation_loop=0
        self.image=self.game.attack_spritesheet.get_sprite(0,0,self.width,self.height)
        self.rect=self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y
    def update(self):
        self.animate()
        #self.collide()
    #def collide(self):
        #hits=pygame.sprite.spritecollide(self,self.game.enemies, True) #ese true mata instantaneamente al enemigo es de prueba, aca implementaremos el combate por turnos
    def animate(self):
        direction=self.game.player.facing
        right_animations = [self.game.attack_spritesheet.get_sprite(0, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 64, self.width, self.height)]

        down_animations = [self.game.attack_spritesheet.get_sprite(0, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 32, self.width, self.height)]

        left_animations = [self.game.attack_spritesheet.get_sprite(0, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 96, self.width, self.height)]

        up_animations = [self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(32, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(64, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(96, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(128, 0, self.width, self.height)]
        if direction=='up':
            self.image=up_animations[math.floor(self.animation_loop)]
            self.animation_loop+=0.5
            if self.animation_loop>=5:
                self.kill()
        if direction=='down':
            self.image=up_animations[math.floor(self.animation_loop)]
            self.animation_loop+=0.5
            if self.animation_loop>=5:
                self.kill()        
        if direction=='right':
            self.image=up_animations[math.floor(self.animation_loop)]
            self.animation_loop+=0.5
            if self.animation_loop>=5:
                self.kill() 
        if direction=='left':
            self.image=up_animations[math.floor(self.animation_loop)]
            self.animation_loop+=0.5
            if self.animation_loop>=5:
                self.kill()                       
                    
                            
   
         
                