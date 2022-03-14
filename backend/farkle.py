import pygame
import random

pygame.init()

max_players = 6
large_dice = True
play_to = 10000

Width = 1200
Height = 600
window = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Farkle")
icon = pygame.image.load("./dice_rolls/dice6.png")
pygame.display.set_icon(icon)

running = True
endgame = False
end_turn = 0

startbox = pygame.Rect((Width-200)/3,(Height-100)/2,200,100)

font1 = pygame.font.Font('./Roboto/DroidSans-Bold.ttf', 48)
start_text = font1.render("Start", 0, (0,0,0))
font2 = pygame.font.Font('./Roboto/DroidSans-Bold.ttf', 30)
add_text = font2.render("Add Player", 0, (0,0,0))

header_font = pygame.font.Font('./Roboto/DroidSans-Bold.ttf', 70)
title_text = header_font.render("Farkle", 0, (90,0,0))

add_box = pygame.Rect(2*(Width-200)/3,(Height-100)/2-50,200,100)
curr_player = 0

class Player:
    turns = []
    name = ""
    score = 0
    farkles = 0
    roll_total = 0
    previous_moves = []

    def __init__(self, name):
        self.name = name
        self.turns = []
    
    def take_turn(self, score):
        if score == 0:
            self.farkles += 1
        else:
            self.score += score
            self.turns.append(score)

text_box_text = "Click to type name"
text_input = font2.render(text_box_text, 0, (0,0,0))
text_box = pygame.Rect(2*(Width-200)/3,(Height-100)/2+70,300,50)
input_active = False

players_handle = font1.render("Players", 0, (0,0,0))

players = []
num_players = 0
term = False

while running and not term:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            term = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if startbox.collidepoint(pygame.mouse.get_pos()):
                if num_players > 0:
                    running = False
            if add_box.collidepoint(pygame.mouse.get_pos()):
                if input_active and num_players < max_players and text_box_text != "":
                    players.append(Player(text_box_text))
                    num_players += 1
                    text_box_text = "Click to type name"
                    input_active = False
            if text_box.collidepoint(pygame.mouse.get_pos()):
                text_box_text = ""
                input_active = True
        elif event.type == pygame.KEYDOWN:
            if input_active:
                if event.key == pygame.K_BACKSPACE:
                    text_box_text = text_box_text[:-1]
                elif event.key == pygame.K_RETURN:
                    if input_active and num_players < max_players and text_box_text != "":
                        players.append(Player(text_box_text))
                        num_players += 1
                        text_box_text = "Click to type name"
                        input_active = False
                else:
                    text_box_text += event.unicode

    text_input = font2.render(text_box_text, 0, (0,0,0))       
    window.fill((255,255,255))
    pygame.draw.rect(window, (10, 150, 70), ((Width-200)/3,(Height-100)/2,200,100))
    pygame.draw.rect(window, (75, 150, 250), (2*(Width-200)/3,(Height-100)/2-50,200,100))
    pygame.draw.rect(window, (200, 200, 200), (2*(Width-200)/3,(Height-100)/2+70,300,50))
    window.blit(start_text, ((Width-200)/3+40, (Height-100)/2+20))
    window.blit(add_text, (2*(Width-200)/3+25, (Height-100)/2-20))
    window.blit(text_input, (2*(Width-200)/3+10, (Height-100)/2+78))
    window.blit(players_handle, (50, 50))
    window.blit(title_text, (Width*.45, Height*.05))
    displace = 0
    for person in players:
        player_names = font2.render(person.name, 0, (0,0,0))
        window.blit(player_names, (50, 120+displace))
        displace += 50
    pygame.display.update()



dice_image_size = 64
if large_dice:
    dice_image_size = 128
dice_coord_x = Width-(dice_image_size*3+30)
dice_coord_y = Height-(dice_image_size*2+20)


dice1 = pygame.image.load("./dice_rolls/dice1.png")
dice2 = pygame.image.load("./dice_rolls/dice2.png")
dice3 = pygame.image.load("./dice_rolls/dice3.png")
dice4 = pygame.image.load("./dice_rolls/dice4.png")
dice5 = pygame.image.load("./dice_rolls/dice5.png")
dice6 = pygame.image.load("./dice_rolls/dice6.png")

if large_dice:
    dice1 = pygame.image.load("./dice_rolls/dice1L.png")
    dice2 = pygame.image.load("./dice_rolls/dice2L.png")
    dice3 = pygame.image.load("./dice_rolls/dice3L.png")
    dice4 = pygame.image.load("./dice_rolls/dice4L.png")
    dice5 = pygame.image.load("./dice_rolls/dice5L.png")
    dice6 = pygame.image.load("./dice_rolls/dice6L.png")

class Dice:
    x = 0
    y = 0
    image = dice1
    value = 1
    locked = False
    lockable = False


    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    
    def roll(self):
        if not self.locked:
            self.value = random.randint(1,6)
            # self.value = self.z
            if self.value == 1:
                self.image = dice1
            elif self.value == 2:
                self.image = dice2
            elif self.value == 3:
                self.image = dice3
            elif self.value == 4:
                self.image = dice4
            elif self.value == 5:
                self.image = dice5
            elif self.value == 6:
                self.image = dice6
            
    
    def lock_toggle(self):
        if self.lockable:
            count_of_curr = 0
            locked_count = 0
            for die in dice:
                if die.value == self.value:
                    if die.lockable:
                        count_of_curr += 1
                        if die.locked:
                            locked_count += 1
            what_to_add = 0
            if self.value == 1 or self.value == 5:
                self.locked = not self.locked
                if self.value == 1:
                    what_to_add = 100
                elif self.value == 5:
                    what_to_add = 50
                if self.locked and locked_count > 2:
                    if self.value == 1:
                        what_to_add = 1000
                        if locked_count == 2:
                            what_to_add -= 200
                    else:
                        what_to_add = 500
                        if locked_count == 2:
                            what_to_add -= 100
                elif locked_count >= 2:
                    if self.value == 1:
                        what_to_add = 1000
                        if locked_count == 2:
                            what_to_add -= 200
                    else:
                        what_to_add = 500
                        if locked_count == 2:
                            what_to_add -= 100
            elif count_of_curr >= 3:
                for die in dice:
                    if die.value == self.value:
                        die.locked = not die.locked
                    self.locked = not self.locked
                what_to_add = self.value*100*(count_of_curr-2)
            else:
                i = 1
                j = 1
                fixer = not self.locked
                for d in dice:
                    for die in dice:
                        if not die.locked and i == die.value:
                            i += 1
                        if die.locked and i == die.value:
                            j += 1
                if i == 7 or j == 7:
                    for die in dice:
                        die.locked = fixer
                        die.lockable = True
                    what_to_add = 1000
            if self.locked:
                players[curr_player].previous_moves.append(what_to_add)
                players[curr_player].roll_total += what_to_add
            elif self.lockable:
                if players[curr_player].previous_moves == []:
                    players[curr_player].previous_moves.append(0)
                
                players[curr_player].roll_total -= players[curr_player].previous_moves.pop()




highest_score = 0
display_dice = False
dice = []
cheater = 1
dice.append(Dice(dice_coord_x, dice_coord_y, 1))
dice.append(Dice(dice_coord_x+dice_image_size+10, dice_coord_y, 2))
dice.append(Dice(dice_coord_x+2*(dice_image_size+10), dice_coord_y, 3))
dice.append(Dice(dice_coord_x, dice_coord_y+dice_image_size+10, 4))
dice.append(Dice(dice_coord_x+dice_image_size+10, dice_coord_y+dice_image_size+10, 5))
dice.append(Dice(dice_coord_x+2*(dice_image_size+10), dice_coord_y+dice_image_size+10, 6))
d1 = pygame.Rect(dice_coord_x, dice_coord_y, dice_image_size, dice_image_size)
d2 = pygame.Rect(dice_coord_x+dice_image_size+10, dice_coord_y, dice_image_size, dice_image_size)
d3 = pygame.Rect(dice_coord_x+2*(dice_image_size+10), dice_coord_y, dice_image_size, dice_image_size)
d4 = pygame.Rect(dice_coord_x, dice_coord_y+dice_image_size+10, dice_image_size, dice_image_size)
d5 = pygame.Rect(dice_coord_x+dice_image_size+10, dice_coord_y+dice_image_size+10, dice_image_size, dice_image_size)
d6 = pygame.Rect(dice_coord_x+2*(dice_image_size+10), dice_coord_y+dice_image_size+10, dice_image_size, dice_image_size)

def allow_locking(val):
    for die in dice:
        if die.value == val:
            die.lockable = True

def calc_score():
        roll_score = 0
        roll_new = []
        roll_size = 0
        ones = 0
        twos = 0
        threes = 0
        fours = 0
        fives = 0
        sixes = 0
        for die in dice:
            roll_size += 1
            if not die.locked:
                die.lockable = False
                roll_new.append(die.value)
                roll_size += 1
                if die.value == 1:
                    die.lockable = True
                    ones += 1
                elif die.value == 2:
                    allow_locking(die.value)
                    twos += 1
                elif die.value == 3:
                    allow_locking(die.value)
                    threes += 1
                elif die.value == 4:
                    allow_locking(die.value)
                    fours += 1
                elif die.value == 5:
                    die.lockable = True
                    fives += 1
                elif die.value == 6:
                    allow_locking(die.value)
                    sixes += 1
        if roll_size == 0:
            return 1   # hot dice
        if ones >= 3:
            roll_score += 1000*(ones-2)
        else:
            roll_score += 100*ones
        if twos >= 3:
            roll_score += 200*(twos-2)
        if threes >= 3:
            roll_score += 300*(threes-2)
        if fours >= 3:
            roll_score += 400*(fours-2)
        if fives >= 3:
            roll_score += 500*(fives-2)
        else:
            roll_score += 50*fives
        if sixes >= 3:
            roll_score += 600*(sixes-2)
        
        if roll_size == 6 and ones == 1 and twos == 1 and threes == 1 and fours == 1 and fives == 1 and sixes == 1:
            for die in dice:
                die.lockable = True
            roll_score += 850

        return roll_score

for die in dice:
    die.roll()


turn_active = False
active_score = 0
curr_player = random.randint(0,num_players-1)

def advance_turn(player_num):
    # if num_players > 1:
    curr_player = (player_num+1) % num_players

bank_text = font1.render("Bank", 0, (0,0,0))
bank_box = pygame.Rect((Width-200)/3+30,(Height)/2+160,200,100)

roll_text = font1.render("Roll", 0, (0,0,0))
roll_box = pygame.Rect((Width-200)/3+30,(Height)/2+40,200,100)
score_adder = 0
text_box = pygame.Rect(Width*.05, Height*.8, 200, 50)
text_box_text = "Manual score"
text_input = font2.render(text_box_text, 0, (0,0,0))

running = True
while running and not term:
    # score_adder = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            term = True
        # elif event.type == pygame.KEYUP:
            # for die in dice:
            #     die.roll()
        elif event.type == pygame.MOUSEBUTTONUP:
            if d1.collidepoint(pygame.mouse.get_pos()):
                if dice[0].lockable:
                    # players[curr_player].roll_total += dice[0].lock_toggle()
                    dice[0].lock_toggle()
            elif d2.collidepoint(pygame.mouse.get_pos()):
                if dice[1].lockable:
                    dice[1].lock_toggle()
                    # players[curr_player].roll_total += dice[1].lock_toggle()
            elif d3.collidepoint(pygame.mouse.get_pos()):
                if dice[2].lockable:
                    # players[curr_player].roll_total += dice[2].lock_toggle()
                    dice[2].lock_toggle()
            elif d4.collidepoint(pygame.mouse.get_pos()):
                if dice[3].lockable:
                    # players[curr_player].roll_total += dice[3].lock_toggle()
                    dice[3].lock_toggle()
            elif d5.collidepoint(pygame.mouse.get_pos()):
                if dice[4].lockable:
                    # players[curr_player].roll_total += dice[4].lock_toggle()
                    dice[4].lock_toggle()
            elif d6.collidepoint(pygame.mouse.get_pos()):
                if dice[5].lockable:
                    # players[curr_player].roll_total += dice[5].lock_toggle()
                    dice[5].lock_toggle()
            elif roll_box.collidepoint(pygame.mouse.get_pos()):
                lock_count = 0
                players[curr_player].previous_moves = []
                for die in dice:
                    if die.locked:
                        lock_count += 1
                        die.lockable = False
                    die.roll()
                if lock_count == 6:
                    for die in dice:
                        die.locked = False
                        die.roll()
                score_adder = calc_score()
                if score_adder == 0:
                    players[curr_player].roll_total = 0
            elif bank_box.collidepoint(pygame.mouse.get_pos()):
                players[curr_player].previous_moves = []
                if score_adder == 0:
                    players[curr_player].roll_score = 0
                if not text_box_text.isnumeric():
                    players[curr_player].take_turn(players[curr_player].roll_total)
                else:
                    players[curr_player].take_turn(int(text_box_text))
                text_box_text = "Manual score"
                # advance_turn(curr_player)
                players[curr_player].roll_total = 0
                if players[curr_player].score >= play_to:
                    endgame = True
                    end_turn = curr_player
                curr_player += 1
                curr_player = curr_player % num_players
                for die in dice:
                    die.locked = False
            elif text_box.collidepoint(pygame.mouse.get_pos()):
                text_box_text = ""
                input_active = True
        elif event.type == pygame.KEYDOWN:
            if input_active:
                if event.key == pygame.K_BACKSPACE:
                    text_box_text = text_box_text[:-1]
                elif event.key == pygame.K_RETURN:
                    if input_active and text_box_text != "":
                        text_box_text = "Manual score"
                        input_active = False
                else:
                    text_box_text += event.unicode
    text_input = font2.render(text_box_text, 0, (0,0,0))
                
    if (score_adder == 1):
        for die in dice:
            die.locked = False
    elif score_adder == 0:
        # players[curr_player].take_turn(score_adder)
        # advance_turn(curr_player)
        players[curr_player].roll_score = 0
    active_score = score_adder
    roll_total_text = "Total Score: " + str(players[curr_player].roll_total)
    roll_sum = "Roll Score: " + str(active_score)
    turn_score_text = font2.render((roll_total_text), 0, (0,0,0))
    active_score_text = font2.render((roll_sum), 0, (0,0,0))
    if turn_active:
        window.blit(active_score_text, ((Width-200)/3+180, (Height)/2))
    window.fill((255,255,255))
    for die in dice:
        if die.locked:
            pygame.draw.rect(window, (200, 195, 210), (die.x-5,die.y-5,dice_image_size+10,dice_image_size+10))
        # else:
        #     pygame.draw.rect(window, (255, 255, 200), (die.x-5,die.y-5,dice_image_size+10,dice_image_size+10))
        window.blit(die.image, (die.x, die.y))
    for i in range(num_players):
        player_disp = font2.render(players[i].name, 0, (0,0,0))
        player_score = font2.render(str(players[i].score), 0, (0,0,0))
        if i < 3:
            window.blit(player_disp, ((120*i)+20, 20))
            window.blit(player_score, ((120*i)+25, 55))
        else:
            window.blit(player_disp, ((120*(i%3))+20, 100))
            window.blit(player_score, ((120*(i%3))+25, 135))
    window.blit(turn_score_text, ((Width-200)/3+180, (Height)/2-50))
    window.blit(active_score_text, ((Width-200)/3+180, (Height)/2-10))
    the_player = font1.render(players[curr_player].name, 0, (0,0,0))
    window.blit(the_player, (Width*.75, Height*.3))
    pygame.draw.rect(window, (75, 200, 75), ((Width-200)/3+30,(Height)/2+40,200,100))
    window.blit(roll_text, ((Width-200)/3+90, (Height)/2+60))
    pygame.draw.rect(window, (200, 75, 75), ((Width-200)/3+30,(Height)/2+160,200,100))
    pygame.draw.rect(window, (200, 200, 200), (Width*.05, Height*.8, 200, 50))
    window.blit(text_input, (Width*.05+8, Height*.8+7))
    window.blit(bank_text, ((Width-200)/3+75, (Height)/2+180))
    if endgame:
        end_text = font2.render("Last Turn!", 0, (0,0,0))
        window.blit(end_text, (Width*.75, Height*.1))
        if end_turn == curr_player:
            running = False
    pygame.display.update()

running = True
while running and not term:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            term = True
    window.fill((255,255,255))
    wins = players[0]
    for player in players:
        if player.score > wins.score:
            wins = player
    winner = wins.name + " wins Farkle!"
    winning = header_font.render(winner, 0, (0,0,0))
    window.blit(winning, (Width*.2, Height*.25))
    pygame.display.update()