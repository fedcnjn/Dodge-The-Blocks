import pygame
import random
import sys
import time

print("--------------------------------------------------")
print('~Dodge The Blocks')
print('~Version v1.1.0')
print('~Created by Joseph Morrison')
print('~Licensed Under MIT License')
print("--------------------------------------------------")


pygame.init()

# Setup
WIDTH, HEIGHT = 600, 400
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Blocks - V2")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Player
player = pygame.Rect(WIDTH//2, HEIGHT - 40, 50, 10)
player_speed = 5

# Blocks and powerups
blocks = []
block_speed = 3
spawn_timer = 0
score = 0
highscore = 0

# Powerups
powerups = []
powerup_timer = 0
powerup_effect_end = 0
flashing = False

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (160, 32, 240)
ORANGE = (255, 165, 0)

# Load highscore
try:
    with open("highscore.txt", "r") as f:
        highscore = int(f.read())
except:
    highscore = 0

def reset_game():
    global blocks, powerups, spawn_timer, powerup_timer, powerup_effect_end
    global score, player, flashing, block_speed
    blocks = []
    powerups = []
    spawn_timer = 0
    powerup_timer = 0
    powerup_effect_end = 0
    score = 0
    player = pygame.Rect(WIDTH//2, HEIGHT - 40, 50, 10)
    flashing = False
    block_speed = 3

def draw_text(text, x, y, color=WHITE):
    txt = font.render(text, True, color)
    win.blit(txt, (x, y))

# Main loop
running = True
while running:
    win.fill((0, 0, 0))
    spawn_timer += 1
    powerup_timer += 1

    if spawn_timer > 30:
        blocks.append(pygame.Rect(random.randint(0, WIDTH-20), 0, 20, 20))
        spawn_timer = 0

    if powerup_timer > 150:
        powerups.append(pygame.Rect(random.randint(0, WIDTH-20), 0, 20, 20))
        powerup_timer = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > 0:
        player.move_ip(-player_speed, 0)
    if keys[pygame.K_RIGHT] and player.right < WIDTH:
        player.move_ip(player_speed, 0)

    for block in blocks[:]:
        block.move_ip(0, block_speed)
        if block.colliderect(player):
            if score > highscore:
                with open("highscore.txt", "w") as f:
                    f.write(str(score))
            draw_text("GAME OVER - Press R to Restart", 150, HEIGHT//2, RED)
            pygame.display.flip()
            waiting = True
            while waiting:
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if e.type == pygame.KEYDOWN and e.key == pygame.K_r:
                        reset_game()
                        waiting = False
            break
        color = RED if flashing else WHITE
        pygame.draw.rect(win, color, block)

    for powerup in powerups[:]:
        powerup.move_ip(0, 3)
        if powerup.colliderect(player):
            powerups.remove(powerup)
            kind = random.choice(["good1", "good2", "good3", "good4", "bad"])
            if kind == "good1":
                score += 50
            elif kind == "good2":
                block_speed = max(1, block_speed - 1)
            elif kind == "good3":
                player.inflate_ip(10, 0)
            elif kind == "good4":
                player_speed += 1
            elif kind == "bad":
                flashing = True
                powerup_effect_end = pygame.time.get_ticks() + 20000
        pygame.draw.rect(win, ORANGE, powerup)

    if flashing and pygame.time.get_ticks() > powerup_effect_end:
        flashing = False

    pygame.draw.rect(win, GREEN, player)
    score += 1

    draw_text(f"Score: {score}", 10, 10)
    draw_text(f"High Score: {highscore}", 10, 40)

    pygame.display.flip()
    clock.tick(30)
