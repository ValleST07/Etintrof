import LoginScreen
import pygame
from pygame.time import delay
import math
import sendToServer
import ast

WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800
ZOOM_FACTOR=3

MAP_HEIGHT=WINDOW_HEIGHT*ZOOM_FACTOR
MAP_WIDTH=WINDOW_WIDTH*ZOOM_FACTOR

blocksizeX=int(MAP_WIDTH/50)
blocksizeY=int(MAP_HEIGHT/50)

playersize=blocksizeX/2-5
playerbarrelsizeX=30
playerbarrelsizeY=10

projectilesize=playersize/2

healthbarWidth=70
healthbarHeigth=10
healthbarDistFromPlayer=40

#server_ip=LoginScreen.get_IP()
server_ip='172.20.10.6'
server_addr=(server_ip, 4444)
Map=[]
PLAYER = -1 #-1=unassigned 0 = RED, 1=GREEN, 2=YELLOW, 3=BLACK

#               FLOOR           WALL        WATER
MAP_COLORS=[(237, 157, 108), (133,64,33), (29,152,221)]

#               RED         GREEN       YELLOW      BLACK
PLAYER_COLORS=[(255,0,0), (0,255,0), (255,255,0), (0,0,0)]

#                   RED     GREEN    YELLOW   BLACK
PLAYER_POSITIONS=[[500,500],[100,50],[100,100],[200,200]]
PROJECTILE_POSITIONS=[]
PLAYER_LIFES=[50,100,100,100]
#in RADIANT!!!!!!!!!!!!!!!!!
PLAYER_ANGLES=[0,0,0,0]

LMB=0
keys = {
    "W": False,
    "A": False,
    "S": False,
    "D": False,
}
dirTo8Way = {
    (1, 0): 2,    # Right
    (-1, 0): 6,   # Left
    (0, 1): 4,    # Down
    (0, -1): 0,   # Up
    (1, -1): 1,   # Up-Right
    (1, 1): 3,    # Down-Right
    (-1, 1): 5,   # Down-Left
    (-1, -1): 7,  # Up-Left
}

def drawGrid():
    for x in range(0, MAP_WIDTH, blocksizeX):
        for y in range(0, MAP_HEIGHT, blocksizeY):
            rect = pygame.Rect(x, y, blocksizeX, blocksizeY)
            i=Map[int(y/blocksizeY)][int(x/blocksizeX)]
            pygame.draw.rect(SURFACE, MAP_COLORS[i], rect)

def drawPlayer():
    for i in range(len(PLAYER_POSITIONS)):
        pygame.draw.circle(SURFACE, PLAYER_COLORS[i], PLAYER_POSITIONS[i],playersize)
        angle_rad = PLAYER_ANGLES[i]
        x=PLAYER_POSITIONS[i][0]
        y=PLAYER_POSITIONS[i][1]
        # Define rectangle corners relative to (x, y)
        barrel_x1 = x + math.cos(angle_rad) * -5  # Move inside the circle
        barrel_y1 = y + math.sin(angle_rad) * -5

        # Barrel ending point (outside)
        barrel_x2 = x + math.cos(angle_rad) * (playerbarrelsizeX - 5)
        barrel_y2 = y + math.sin(angle_rad) * (playerbarrelsizeX - 5)

        # Find perpendicular direction to create thickness
        perp_x = -math.sin(angle_rad) * (playerbarrelsizeY // 2)
        perp_y = math.cos(angle_rad) * (playerbarrelsizeY // 2)

        # Define rectangle corners
        points = [
            (barrel_x1 + perp_x, barrel_y1 + perp_y),  # Top-left
            (barrel_x1 - perp_x, barrel_y1 - perp_y),  # Bottom-left
            (barrel_x2 - perp_x, barrel_y2 - perp_y),  # Bottom-right
            (barrel_x2 + perp_x, barrel_y2 + perp_y)  # Top-right
        ]

        pygame.draw.polygon(SURFACE, PLAYER_COLORS[i], points)
        drawHealthbar()

def drawHealthbar():
    for i in range(len(PLAYER_POSITIONS)):
        life=PLAYER_LIFES[i]
        backgroundRect = pygame.Rect(PLAYER_POSITIONS[i][0] - healthbarWidth/2, PLAYER_POSITIONS[i][1] - healthbarDistFromPlayer-healthbarHeigth/2, healthbarWidth, healthbarHeigth)
        pygame.draw.rect(SURFACE, (150,150,150), backgroundRect)

        foregroundRect = pygame.Rect(PLAYER_POSITIONS[i][0] - healthbarWidth / 2,
                                     PLAYER_POSITIONS[i][1] - healthbarDistFromPlayer - healthbarHeigth / 2,
                                     healthbarWidth*life/100, healthbarHeigth)

        if (life>=80): color=(0, 153, 51)
        elif (life>=60): color=(153, 255, 102)
        elif (life>=40): color=(255, 255, 0)
        elif (life>=20): color=(255, 0, 0)
        else: color=(204,0,0)
        pygame.draw.rect(SURFACE, color, foregroundRect)

def drawProjectile():
    for i in range(len(PROJECTILE_POSITIONS)):
        pygame.draw.circle(SURFACE, (90,90,90), PROJECTILE_POSITIONS[i], projectilesize)

def CamView():
    cam_x=PLAYER_POSITIONS[PLAYER][0]-WINDOW_WIDTH/2
    cam_y=PLAYER_POSITIONS[PLAYER][1] - WINDOW_HEIGHT / 2
    camera_view = pygame.Rect(cam_x, cam_y, WINDOW_WIDTH, WINDOW_HEIGHT)
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(SURFACE, (0, 0), camera_view)

def sendInputs():
    x = keys["D"] - keys["A"]
    y = keys["S"] - keys["W"]
    mov_direction = dirTo8Way.get((x, y), 8) #8=keine bewegung
    angle=PLAYER_ANGLES[PLAYER]
    mouse=LMB
    sendToServer.transmit(server_addr, f"{PLAYER};{mov_direction};{angle};{mouse}")

def handleReceivedData():
    global PLAYER
    global PLAYER_POSITIONS
    global PLAYER_ANGLES
    global Map

    if not Map:#first frame (map frame):
        data=sendToServer.receive(10000)
    else:
        data=sendToServer.receive(1024)
    
    if (data[0]=='M'):
        Map=ast.literal_eval(data[1:])
        return
    elif (data[0]=='P'):
        PLAYER=int(data[1])
        print(f"PlayerNum={PLAYER}")
        return
    dataList=data.split('*')
    PLAYER_POSITIONS=ast.literal_eval(dataList[0])
    #PLAYER_ANGLES=ast.literal_eval(dataList[1])
    for i in range(4):
        if i != PLAYER:
            PLAYER_ANGLES[i]=ast.literal_eval(dataList[1])[i]

pygame.init()

pygame.display.set_caption('Etintrof')
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) #SCREEN = was man sieht; teil der Map; mit zoom
SURFACE = pygame.Surface((MAP_WIDTH, MAP_HEIGHT)) #SURFACE = gesamte Map ohne Zoom

is_running = True

count=0
while is_running:
    count+=1
    sendInputs()
    handleReceivedData()
    if Map:
        drawGrid()
        drawPlayer()
        drawProjectile()
        CamView()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.MOUSEMOTION:
            mousex, mousey = event.pos
            # build a vector between player position and mouse position
            delta = (mousex - WINDOW_WIDTH/2, mousey - WINDOW_HEIGHT/2)
            PLAYER_ANGLES[PLAYER] =  math.atan2(delta[1],delta[0])
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                keys["W"] = True
            if event.key == pygame.K_a:
                keys["A"] = True
            if event.key == pygame.K_s:
                keys["S"] = True
            if event.key == pygame.K_d:
                keys["D"] = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                keys["W"] = False
            if event.key == pygame.K_a:
                keys["A"] = False
            if event.key == pygame.K_s:
                keys["S"] = False
            if event.key == pygame.K_d:
                keys["D"] = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                LMB = 1

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                LMB = 0
    pygame.display.update()