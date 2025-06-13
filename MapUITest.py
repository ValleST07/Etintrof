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

IsSpectating=False
newGame=False
SPECTATING_INDEX=0

server_ip=LoginScreen.get_IP()
#server_ip='192.168.137.1'
server_addr=(server_ip, 4444)
Map=[]
PLAYER = -1 #-1=unassigned 0 = RED, 1=GREEN, 2=YELLOW, 3=BLACK

#               FLOOR           WALL        WATER
MAP_COLORS=[(237, 157, 108), (133,64,33), (29,152,221)]

#               RED         GREEN       YELLOW      BLACK
PLAYER_COLORS=[(255,0,0), (0,255,0), (255,255,0), (0,0,0)]

#                   RED     GREEN    YELLOW   BLACK
PLAYER_POSITIONS=[[10000,10000],[10000,10000],[10000,10000],[10000,10000]]
BULLET_POSITIONS=[]
PLAYER_HEALTH=[100,100,100,100]
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

def spectate():
    global PLAYER
    global SPECTATING_INDEX
    playersavailable = [i for i in range(len(PLAYER_POSITIONS)) if PLAYER_HEALTH[i] > 0]
    PLAYER=playersavailable[SPECTATING_INDEX]
    text=font.render(f"Spectating Player {PLAYER}", True, (255,255,255))
    SCREEN.blit(text, (10, 10))
    text2=font.render(f"Press SPACE to change Player", True, (255,255,255))
    SCREEN.blit(text2, (10, 50))
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if SPECTATING_INDEX<len(playersavailable)-1:
                    SPECTATING_INDEX+=1
                else:
                    SPECTATING_INDEX=0

def DeathScreen():
    global IsSpectating
    text=font.render(f"YOU DIED!", True, (255,50,50))
    text2=font.render(f"Press S to Spectate or Q to Quit", True, (255,255,255))
    SCREEN.blit(text, (370, 350))
    SCREEN.blit(text2, (220, 400))
    pygame.display.update()
    while True:
        if PLAYER_HEALTH.count(0)>=len(PLAYER_HEALTH) and not newGame:
            GameOverScreen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sendToServer.transmit(server_addr, "E")
                    pygame.quit()
                    exit()
                if event.key == pygame.K_s:
                    print("Spectating")
                    IsSpectating=True
                    return

def GameOverScreen():
    global Map
    global IsSpectating
    global newGame
    PLAYER_POSITIONS[PLAYER]=(1000000,1000000)
    drawPlayer()
    CamView()
    text=font.render(f"Game Over Player {PLAYER} WON!", True, (50,255,50))
    text2=font.render(f"Press N for new Game or Q to Quit", True, (255,255,255))
    SCREEN.blit(text2, (220, 400))
    SCREEN.blit(text, (300, 350))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sendToServer.transmit(server_addr, "E")
                    pygame.quit()
                    exit()
                if event.key == pygame.K_n:
                    print("New Game")
                    sendToServer.transmit(server_addr, "N")
                    #reset server and play again
                    Map=[]
                    IsSpectating=False
                    newGame=True
                    return
    #new game possible

def drawUI():
    PlayersDead=PLAYER_HEALTH.count(0)
    text=font.render(f"{len(PLAYER_POSITIONS)-PlayersDead}/{len(PLAYER_POSITIONS)} Players Alive", True, (255,255,255))
    SCREEN.blit(text, (600, 10))

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
        life=PLAYER_HEALTH[i]
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
    for i in range(len(BULLET_POSITIONS)):
        pygame.draw.circle(SURFACE, (90,90,90), BULLET_POSITIONS[i], projectilesize)

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
    global BULLET_POSITIONS
    global PLAYER_HEALTH
    global Map
    
    data=sendToServer.receive(10000)
    
    if (data[0]=='M'):
        Map=ast.literal_eval(data[1:])
        print(f"Map RECEIVED")
        return
    elif (data[0]=='P'):
        PLAYER=int(data[1])
        print(f"PlayerNum={PLAYER}")
        return
    dataList=data.split('*')
    PLAYER_POSITIONS=ast.literal_eval(dataList[0])
    #wenn nicht spectating, dann nur eigene angle
    if not IsSpectating:
        for i,_ in enumerate(PLAYER_POSITIONS):
            if i != PLAYER:
                PLAYER_ANGLES[i]=ast.literal_eval(dataList[1])[i]
    else:
        PLAYER_ANGLES=ast.literal_eval(dataList[1])
    BULLET_POSITIONS=ast.literal_eval(dataList[2])
    PLAYER_HEALTH=ast.literal_eval(dataList[3])

pygame.init()
font=pygame.font.SysFont(None, 36)
pygame.display.set_caption('Etintrof')
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) #SCREEN = was man sieht; teil der Map; mit zoom
SURFACE = pygame.Surface((MAP_WIDTH, MAP_HEIGHT)) #SURFACE = gesamte Map ohne Zoom

is_running = True
while is_running:
    if not IsSpectating:
        sendInputs()
    handleReceivedData()
    if Map:
        drawGrid()
        drawPlayer()
        drawProjectile()
        CamView()
        drawUI()
    
    if PLAYER_HEALTH[PLAYER] == 0 and not IsSpectating and not newGame:
        DeathScreen()
    
    if IsSpectating and not newGame:
        spectate()
    
    if PLAYER_HEALTH.count(0)+1>=len(PLAYER_HEALTH) and not newGame:
        GameOverScreen()
        continue
    
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