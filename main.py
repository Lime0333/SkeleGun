import os
#os.system("pip install ursina")
from ursina import *
import random

def resumeGame():
    global background, game, menu
    game.enabled=True
    menu.enabled=False
    background.texture="graphics/backgrounds/stage.png"

def skelegun():
    global background, game, menu

    game.waves = [
        [
            {'name': 'necro', 'spawn': (2,3.5)},
            {'name': 'monster2', 'spawn': (2,2)}
        ],
        [
            {'name': 'monster1', 'spawn': (-2,-3.5)},
            {'name': 'monster2', 'spawn': (-1.5,2)}
        ],
        [
            {'name': 'monster1', 'spawn': (-1.5,2)},
            {'name': 'monster2', 'spawn': (0,-3)},
            {'name': 'monster2', 'spawn': (-4,3)}
            ]
    ]
    game.wave=0

    class Monster(Sprite):
        def necromancer(self):
            self.specialCooldown+=1
            if self.specialCooldown>=self.specialDelay:
                self.specialCooldown=0
                x = random.uniform(0.500, 1.000)
                y = random.uniform(0.500, 1.000)
                if random.randint(1,2) == 1:
                    x = self.x + 0.5 + x
                else:
                    x = self.x - 0.5 - x
                if random.randint(1,2) == 1:
                    y = self.y + 0.5 + y
                else:
                    y = self.y - 0.5 - y
                game.monsters.append(Monster('monster2', (x,y)))
                

        def __init__(self, name, position, id=len(game.monsters)-1):
            super().__init__()
            self.data = {
                'monster1' : {'health': 2, 'damage': 1, 'hitDelay': 100, 'animDelay': 4, 'speed': 3, 'animLength': 6, 'scale': 1},
                'monster2' : {'health': 1, 'damage': 1, 'hitDelay': 100, 'animDelay': 4, 'speed': 2, 'animLength': 8, 'scale': 0.75},
                'necro' : {'health': 4, 'damage': 1, 'hitDelay': 100, 'animDelay': 4, 'speed': 1.5, 'animLength': 10, 'scale': 1, 'special': self.necromancer, 'specialDelay': 200}
            }
            
            self.parent=game
            self.id = id
            self.destroyed=False
            self.name = name
            self.x, self.y = position
            self.scale = self.data[self.name]['scale']
            self.collider='box'
            self.texture = "graphics/monsters/" + self.name + "/1.png"

            self.health = self.data[self.name]['health']

            self.animStage = 0
            self.animCooldown = 0

            self.cooldown=self.data[self.name]['hitDelay']

            if 'special' in self.data[self.name]:
                self.specialCooldown = 0
                self.specialDelay = self.data[self.name]['specialDelay']
                match self.data[self.name]['special']:
                    case self.necromancer:
                        pass

        def hit(self,damage):
            print("lubudubu", self.health, damage)
            self.health -= damage
            if self.health <= 0:
                self.destroyed = True
                destroy(self)
                game.monsters = [monster for monster in game.monsters if not monster.destroyed]
                print(game.monsters)


        def playerUpdate(self, player):
            self.animCooldown+=1
            self.cooldown+=1
            if not self.name in self.data:
                print(self.name)
            if self.animCooldown > self.data[self.name]['animDelay']:
                self.animCooldown = 0
                self.animStage += 1
                if self.animStage > self.data[self.name]['animLength']:
                    self.animStage = 1
                self.texture = "graphics/monsters/"+self.name+"/"+str(self.animStage)+".png"

            diffX = abs(self.x - player.x)
            diffY = abs(self.y - player.y)
            if diffX > .5 or diffY > .5:
                if self.x > player.x:
                    dirX = -1
                else:
                    dirX = 1
                if self.y > player.y:
                    dirY = -1
                else:
                    dirY = 1
            else:
                dirY = 0
                dirX = 0
            
            moveX = self.data[self.name]['speed'] / (diffX+diffY) * diffX * dirX
            moveY = self.data[self.name]['speed'] / (diffX+diffY) * diffY * dirY

            #if 3 != abs(moveX)+abs(moveY):
                #print(abs(moveX)+abs(moveY), diffX, diffY, dirX, dirY)
            self.x += time.dt * moveX
            self.y += time.dt * moveY

            hitInfo = self.intersects()
            if hitInfo.hit and hitInfo.entity == player and self.data[self.name]['hitDelay'] < self.cooldown:
                self.cooldown = 0
                player.hit()
            
            if 'special' in self.data[self.name]:
                spec = self.data[self.name]['special']
                spec()


    class Player(Sprite):
        def __init__(self,game):
            super().__init__()

            self.animDelay=4
            self.weaponsData =  {
                'weapon1': {'bulletSpeed' : 20, 'delay': 50, 'texture': "graphics/weapons/1.png", 'bulletTexture':"graphics/bullets/1.png", 'scale' : 5, 'damage' : 1, 'capacity' : 10, 'reloadTime' : 10, 'spread' : 10}
            }


            self.parent=game
            self.skin=1
            self.texture="graphics/player/" + str(self.skin) + ".png"
            self.texture.filtering = None
            self.scale = (1, 1, 0)
            self.collider='box'

            self.healthBar = Sprite(texture="graphics/healthBar/5.png", scale=5, position=(window.top_left.x*8+38/25/2+.1, window.top_left.y*8-12/25/2-.1), parent=game)
            self.health=5
            
            self.position = (2, 0, 0)
            self.speed = 5
            self.animStage=1
            self.animCooldown=0
            self.animation='walking'
            self.flip=""
            self.origin=0

            self.weaponName = 'weapon1'
            self.weapon=Sprite(texture=self.weaponsData[self.weaponName]['texture'], scale=self.weaponsData[self.weaponName]['scale'])
            self.weapon.origin=self.position
            self.weapon.parent=game

            self.shootingCooldown=0

            self.weapon.bullets=[]

            self.clickCooldown = 0
            self.clickDelay = 50
        
        def ensureFlip(self, do):
            if do:
                if self.flip=="":
                    self.flip = "f"
                    
            else:
                if self.flip=="f":
                    self.flip = ""

        def shoot(self):
            global game
            if self.shootingCooldown>self.weaponsData[self.weaponName]['delay']:
                self.shootingCooldown=0
                self.weapon.bullets.append(Sprite(texture=self.weaponsData[self.weaponName]['bulletTexture'], scale=3, parent=game, position=self.weapon.position, origin_x=3, rotation_z=self.shootingAngle, delta_x = self.weaponsData[self.weaponName]['bulletSpeed'] * math.cos(math.radians(self.shootingAngle)), delta_y = self.weaponsData[self.weaponName]['bulletSpeed'] * math.sin(math.radians(self.shootingAngle)), collider="box"))
        
        def hit(self):
            self.health-=1
            self.healthBar.texture="graphics/healthBar/" + str(self.health) + ".png"
            if self.health<=0:
                self.kill()


        def kill(self):
            game.enabled=False
            menu.enabled=True

        def update(self):
            self.weapon.position=self.position
            self.weapon.origin_x=1.5

            #weapon rotation
            mx, my = mouse.x*8+10, mouse.y*8+10
            x, y = self.x+10, self.y+10
            angle=math.degrees(math.atan2(mx-x, my-y))
            self.shootingAngle = self.weapon.rotation_z = 90+angle

            self.shootingCooldown+=1
            self.animCooldown+=1
            self.clickCooldown+=1
            
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

            if (held_keys['e'] or held_keys['left mouse']) and self.clickCooldown > self.clickDelay:
                self.clickCooldown = 0
                if held_keys['left mouse']:
                    self.shoot()
                if held_keys['e']:
                    for enemy in game.waves[game.wave]:
                        game.monsters.append(Monster(enemy['name'], enemy['spawn']))
                    game.wave+=1

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
            
            for i in self.weapon.bullets:
                i.x -= time.dt * i.delta_x
                i.y += time.dt * i.delta_y
                hitInfo = i.intersects()
                hitMonster=False
                if hitInfo.hit:
                    for ii in game.monsters:
                        if ii == hitInfo.entity:
                            ii.hit(self.weaponsData[self.weaponName]['damage'])
                            hitMonster=True
                            break
                if hitMonster or i.x > window.bottom_right.x*8 or i.x < window.top_left.x*8 or i.y < window.bottom_right.y*8 or i.y > window.top_left.y*8:
                    destroy(i)
                    self.weapon.bullets.remove(i)
            
            for i in game.monsters:
                i.playerUpdate(self)


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
game=Entity(enabled=False, monsters=[])
menu=Entity(enabled=True)

def input(key):
    if key=='escape':
        game.enabled=False
        menu.enabled=True
        background.texture="graphics/backgrounds/intro.png"

print("SIZE: ",app.get_size())
skelegun()

app.run()