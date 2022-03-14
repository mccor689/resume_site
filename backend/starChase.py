import pygame
import random

pygame.init()

f = open("scores.txt", "r")
text = f.read()
highscore = 0
if not text == "":
    highscore = int(text)
f.close()

squareSize = 75
playerSize = 32
moveSpeed = .5
hard = True
numBad = 0
tolerance = 10

Width = 1200
Height = 600
window = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Star Chase")
icon = pygame.image.load("./images/kiwi.png")
pygame.display.set_icon(icon)

playerImg = pygame.image.load("./images/star.png")
playerX = 200
playerY = 250

def player(X, Y):
    window.blit(playerImg, (X, Y))

def playerIsIn(a,b):
    return (a+playerSize-tolerance >= b and a <= (b+squareSize-tolerance))

def blockIsIn(a,b):
    return (a >= b-squareSize and a <= (b+squareSize))

# highscore = 0
font = pygame.font.Font('./Roboto/DroidSans-Bold.ttf', 48)
start_text = font.render("Start", 0, (0,0,0))
startbox = pygame.Rect((Width-200)/3,(Height-100)/2,200,100)
score_text = font.render("High Score:", 0, (0,0,0))


w = squareSize
h = squareSize
goodx = 0
goody = 0

badx = []
bady = []

def set_bad():
    badx.clear()
    bady.clear()
    for i in range(0, numBad):
        tempx = random.randint(0, Width-w)
        tempy = random.randint(0, Height-h)
        while (blockIsIn(tempx, goodx) and blockIsIn(tempy, goody)) or (blockIsIn(playerX, tempx) and blockIsIn(playerY, tempy)):
            tempx = random.randint(0, Width-w)
            tempy = random.randint(0, Height-h)
        badx.append(tempx)
        bady.append(tempy)

def disp_bad():
    for i in range(numBad):
        pygame.draw.rect(window, (200, 0, 0), (badx[i],bady[i],w,h))

moveX = 0
moveY = 0

score = 0


running = True
playing = False
reset = True

while running:
    while not playing and running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.MOUSEBUTTONUP:
                if startbox.collidepoint(pygame.mouse.get_pos()):
                    playing = True
        high_score = font.render(str(highscore), 0, (0,0,0))
        window.fill((255,255,255))
        pygame.draw.rect(window, (10, 150, 70), ((Width-200)/3,(Height-100)/2,200,100))
        window.blit(start_text, ((Width-200)/3+40, (Height-100)/2+20))
        window.blit(score_text, (2*(Width-200)/3+25, (Height-100)/2-20))
        window.blit(high_score, (Width*.65, Height*.48))
        pygame.display.update()
    numBad = 0
    moveX = 0
    moveY = 0
    score = 0
    while playing and running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                playing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    moveX -= moveSpeed
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    moveX += moveSpeed
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    moveY -= moveSpeed
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    moveY += moveSpeed
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    moveX = 0
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    moveX = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    moveY = 0
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    moveY = 0
        
        playerX += moveX
        playerY += moveY

        window.fill((0,0,0))
        curr_score = font.render(str(score), 0, (255,255,0))
        if (playerIsIn(playerX, goodx) and playerIsIn(playerY, goody)):
            # Successful score
            score += 1
            if score > highscore:
                highscore = score
            goodx = random.randint(0, Width-w)
            goody = random.randint(0, Height-h)
            if hard:
                numBad += 1
            reset = True
        
        if reset:
            set_bad()
            reset = False

        for i in range(0, numBad):
            if (playerIsIn(playerX, badx[i]) and playerIsIn(playerY, bady[i])):
                playing = False
        
        pygame.draw.rect(window, (10, 200, 100), (goodx,goody,w,h))
        disp_bad()
        window.blit(curr_score, (Width*.9, Height*.05))
        if playerX < 0:
            playerX = 0
        elif playerX > Width-playerSize:
            playerX = Width-playerSize
        if playerY < 0:
            playerY = 0
        elif playerY > Height-playerSize:
            playerY = Height-playerSize
        player(playerX, playerY)
        pygame.display.update()
        if not playing and running:
            i = 0
            while i < 1000:
                window.fill((255,255,255))
                pygame.draw.rect(window, (10, 150, 70), (goodx,goody,w,h))
                disp_bad()
                player(playerX, playerY)
                pygame.display.update()
                i += 1
            # running = False


print("Final score: ", highscore)
f = open("scores.txt", "w")
f.write(str(highscore))
f.close()