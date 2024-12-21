from ursina import *
import random

def ifCollidesList(a,b):
    for i in b:
        if i!=a and ifCollides(a,i):
            return i
    return False

def ifCollides(a,b):
    Jleft=a.x-0.5
    Jright=a.x+0.5
    Jtop=a.y-0.5
    Jbottom=a.y+0.5
    left=b.x-0.5
    right=b.x+0.5
    top=b.y-0.5
    bottom=b.y+0.5

    if Jright >= left and Jleft <= right and Jtop <= bottom and Jbottom >= top:
        return True
    else:
        return False

def kulaUpdate(i, move=0.1):
    global kule
    global kuleKierunki
    ball = kule[i]
    ball.rotation_x+=move*50
    ball.rotation_z+=move*50
    ball.rotation_y+=move*50

    ball.x+=move*kuleKierunki[i][0]
    ball.y+=move*kuleKierunki[i][1]

    if i==0 and (ball.y>3 or ball.x>4 or ball.y<-3 or ball.x<-4):
        lista=["circle", "sphere", "cube", "quad"]
        textureList = ["freaky.png", "freaky2.png", "freaky3.png", "freaky4.png", "pingwin.png", "freaky6.png", "freaky10.png", "freaky8.png", "freaky9.png"]
        kule.append(Entity(model=random.choice(lista), color=color.rgb(random.random(),random.random(),random.random()), texture=random.choice(textureList)))
        got = False
        for m in range(10):
            kule[-1].y=random.uniform(-2.99999,2.99999)
            kule[-1].x=random.uniform(-3.99999,3.99999)
            if ifCollidesList(kule[-1],kule)==False:
                got=True
                break
        if not got:
            kule.pop()
        

        k=random.random()*2
        k1=k-1
        k2=2-k
        if(random.randint(1,2)==1):
            k1*=-1
        if(random.randint(1,2)==1):
            k2*=-1

        kuleKierunki.append([k1,k2])
        

    if ball.y>3:
        kuleKierunki[i][1]=0-kuleKierunki[i][1]
    if ball.y<-3:
        kuleKierunki[i][1]=0-kuleKierunki[i][1]

    if ball.x>4 or ball.x<-4:
        kuleKierunki[i][0]=0-kuleKierunki[i][0] 

    collider = ifCollidesList(ball,kule)

    if collider!=False:
        diffrenceX=abs(collider.x-ball.x)
        diffrenceY=abs(collider.y-ball.y)
        if(diffrenceX>diffrenceY):
            kuleKierunki[i][0]=0-kuleKierunki[i][0]
        else:
            kuleKierunki[i][1]=0-kuleKierunki[i][1]
                



#os.system("pip install ursina")

def update():
    global speed
    global acceleration
    global kule
    global camMoveX
    global camMoveY
    global camMoveZ
    global camMoveZup

    r=random.random()
    g=random.random()
    b=random.random()
    kule[0].color=color.rgb(r,g,b)

    for i in range(len(kule)):
        kulaUpdate(i, time.dt*speed)

    camMoveX+=time.dt*(1-random.random()*2)*speed
    camMoveY+=time.dt*(1-random.random()*2)*speed

    if camMoveZup:
        camMoveZ+=time.dt*speed*9
    else:
        camMoveZ-=time.dt*speed*9
    
    if camMoveZ>10:
        camMoveZup=False
    elif camMoveZ<-10:
        camMoveZup=True

    if camMoveX>10 or camMoveX<-10:
        camMoveX=0
    if camMoveY>10 or camMoveY<-10:
        camMoveY=0

    camVec = camera.position_getter()
    #camX = camVec.getX() + camMoveX
    #camY = camVec.getY() + camMoveY

    camera.position = (0, 0, -25+camMoveZ)

app=Ursina()

speed=3
acceleration = 1.001
camMoveX = 0
camMoveY = 0
camMoveZ = 0
camMoveZup=True;

#test=Entity(model="circle")
#test.

kule=[Entity(model="cube", color=color.red, texture="freaky.png"), Entity(model="circle", color=color.blue, texture="pingwin.png")]
kuleKierunki=[[1,1],[-1.25,-0.75]]


app.run()