import os
#os.system("pip install ursina")
from PIL import Image
import PIL
from ursina import *
import random

def resumeGame():
    global background, game, menu
    game.enabled=True
    menu.enabled=False
    background.texture="graphics/backgrounds/stage.png"

def skelegun():
    global background, game, menu

    class Player(Sprite):
        def __init__(self,game):
            super().__init__()
            self.parent=game
            self.skin=1
            self.texture="graphics/player/" + str(self.skin) + ".png"
            self.texture.filtering = None
            self.scale = (1, 1, 0)
            
            self.position = (2, 0, 0)
            self.speed = 5
            self.animStage=1
            self.animDelay=4
            self.animCooldown=0
            self.animation='walking'
            self.flip=""
            self.origin=0

            self.weapon=Sprite(texture="graphics/weapons/1.png", scale=5)
            self.weapon.origin=self.position
            self.weapon.parent=game

            self.weapon.bullets=[]
        
        def ensureFlip(self, do):
            if do:
                if self.flip=="":
                    self.flip = "f"
                    
            else:
                if self.flip=="f":
                    self.flip = ""

        def shoot(key):
            

        def update(self):
            self.weapon.position=self.position
            self.weapon.origin_x=1.5

            #weapon rotation
            mx, my = mouse.x*8+10, mouse.y*8+10
            x, y = self.x+10, self.y+10
            angle=math.degrees(math.atan2(mx-x, my-y))
            self.shootingAngle = self.weapon.rotation_z = 90+angle


            self.animCooldown+=1
            if self.animCooldown>=self.animDelay:
                self.animStage+=1
                if self.animStage>=10:
                    self.animStage=1
                self.animCooldown = 0
                match self.animation:
                    case 'walking':
                        self.texture = "graphics/player/" + str(self.skin) + "/" + str(self.animStage) + self.flip + ".png"
                    case 'idle':
                        self.texture = "graphics/player/" + str(self.skin) + self.flip + ".png"

            if held_keys['w'] or held_keys['s'] or held_keys['a'] or held_keys['d']:
                self.animation='walking'
            else:
                self.animation='idle'
            
            if held_keys['mouse left up']:
                self.shoot()

            if held_keys['w']:
                self.y+=time.dt*self.speed
            elif held_keys['s']:
                self.y-=time.dt*self.speed
            if held_keys['a']:
                self.x-=time.dt*self.speed
                self.ensureFlip(False)
            elif held_keys['d']:
                self.x+=time.dt*self.speed
                self.ensureFlip(True)

    windowSizeX,windowSizeY = app.get_size()
    background=Entity(model="quad", texture="graphics/backgrounds/intro.png", scale=(windowSizeX/100,windowSizeY/100), position=(0,0,.1))
    skeleGunIcon=Sprite(texture="graphics/logo.png", position=(0,2), scale=5, parent=menu)

    startButton = Button(model="quad", texture="graphics/buttons/play.png",scale=(25/10,14/10), radius=0, position=(0, 0),color=color.rgb(1,1,1), tooltip=Tooltip("Start the game"), parent=menu)
    startButton.on_click=resumeGame 
    def buttonHover():
        startButton.color=color.gray
    startButton.on_mouse_enter=buttonHover
    def buttonUnhover():
        startButton.color=color.white
    startButton.on_mouse_exit=buttonUnhover

    player=Player(game)


app = Ursina()
game=Entity(enabled=False)
menu=Entity(enabled=True)

def input(key):
    if key=='escape':
        print("AAAA")
        game.enabled=False
        menu.enabled=True
        background.texture="graphics/backgrounds/intro.png"


print("SIZE: ",app.get_size())
skelegun()

app.run()