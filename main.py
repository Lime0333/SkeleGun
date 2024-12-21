import os
#os.system("pip install ursina")
from ursina import *
import random

def welcomeScreen():

    def skelegun():
        destroy(startButton)
        destroy(skeleGunIcon)
        
        class Player(Entity):
            def __init__(self):
                super().__init__()
                self.model = 'quad'
                self.color = color.random_color()
                self.scale = (1, 1, 1)
                self.position = (2, 0, 0)
                self.speed = 5

            def update(self):
                if held_keys['w']:
                    self.y+=time.dt*self.speed
                elif held_keys['s']:
                    self.y-=time.dt*self.speed
                if held_keys['a']:
                    self.x-=time.dt*self.speed
                elif held_keys['d']:
                    self.x+=time.dt*self.speed

        player=Player()
        background.texture="graphics/backgrounds/stage.png"

    windowSizeX,windowSizeY = app.get_size()
    background=Entity(model="quad", texture="graphics/backgrounds/intro.png", scale=(windowSizeX/100,windowSizeY/100), position=(0,0,.1))
    skeleGunIcon=Sprite(texture="graphics/logo.png", position=(0,2), scale=5)

    startButton = Button(model="quad", texture="graphics/buttons/play.png",scale=(25/70,14/70), radius=0, position=(0, 0),color=color.rgb(1,1,1), tooltip=Tooltip("Start the game"))
    startButton.on_click=skelegun
    def buttonHover():
        startButton.color=color.gray
    startButton.on_mouse_enter=buttonHover
    def buttonUnhover():
        startButton.color=color.white
    startButton.on_mouse_exit=buttonUnhover


    #b=Button(mode)

app = Ursina()
print("SIZE: ",app.get_size())
welcomeScreen()

app.run()