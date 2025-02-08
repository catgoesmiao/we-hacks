import os
import pygame, sys, random
import soundfile as sf
from pygame.locals import *
from pygame import mixer

# Initialize pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Beautiful and Wonderful Fish 鱻 Snatcher")

# BGM
pygame.mixer.music.load("piccadilly.wav")
pygame.mixer.music.play(-1)

# Colors
b_color = (0, 0, 0)        # Black
blu_color = (0, 150, 255)  # Blue
g_color = (0, 255, 0)      # Green
r_color = (255, 0, 0)      # Red
w_color = (255, 255, 255)  # White

button_light = (170, 170, 170)
button_dark = (100, 100, 100)

# Font
font = pygame.font.SysFont("Comic Sans", 25)

# Button Class
class Button:
    def __init__(self, text, x, y, w, h, action):
        self.text = font.render(text, True, w_color)
        self.rect = pygame.Rect(x, y, w, h)
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, button_dark, self.rect)
        text_rect = self.text.get_rect(center=self.rect.center)
        screen.blit(self.text, text_rect)

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.action()

# Start/Exit functions
def start_game():
    global menu
    menu = False  # Exit menu and start game

def quit_game():
    pygame.quit()
    sys.exit()

# Buttons for the menu
start_button = Button("Go Fish!", 300, 250, 200, 60, start_game)
exit_button = Button("Go Home!", 300, 350, 200, 60, quit_game)

# Menu loop
menu = True
while menu:
    screen.fill(b_color)
    start_button.draw(screen)
    exit_button.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()
        if event.type == pygame.MOUSEBUTTONDOWN:
            start_button.check_click(event.pos)
            exit_button.check_click(event.pos)

    pygame.display.update()

# Fish data
FISHIES = [
    {"name": "fish1", "rarity": "-", "cost": 5},
    {"name": "fish2", "rarity": "-", "cost": 5},
    {"name": "fish3", "rarity": "-", "cost": 5},
    {"name": "fish4", "rarity": "-", "cost": 5},
    {"name": "fish5", "rarity": "-", "cost": 5},
    {"name": "fish6", "rarity": "-", "cost": 5},
    {"name": "fish7", "rarity": "-", "cost": 5},
    {"name": "fish8", "rarity": "-", "cost": 5},
    {"name": "fish9", "rarity": "-", "cost": 5},
    {"name": "fish10", "rarity": "-", "cost": 5},
    {"name": "fish11", "rarity": "-", "cost": 5},
    {"name": "fish12", "rarity": "-", "cost": 5}
]

# Player class
class Player:
    def __init__(self):
        self.lvl = 1
        self.exp = 0
        self.exp_needed = 10
        self.money = 0
        self.inventory = []

    def leveling(self, exp_gained):
        self.exp += exp_gained
        if self.exp >= self.exp_needed:
            self.lvl_up()

    def lvl_up(self):
        self.lvl += 1
        self.exp = 0
        self.exp_needed += 5

    def add_fish(self, fish):
        if len(self.inventory) < 12:
            self.inventory.append(fish)

    def sell_fish(self, fish):
        self.money += fish.cost
        self.inventory.remove(fish)

# Fish class
class Fish:
    def __init__(self, name, rarity, cost):
        self.name = name
        self.rarity = rarity
        self.cost = cost

# Lake class
class Lake:
    def __init__(self):
        self.fish_lst = []
        self.max_fish = 12
        self.spawn_fish()

    def spawn_fish(self):
        while len(self.fish_lst) < self.max_fish:
            fish_data = random.choice(FISHIES)
            new_fish = Fish(fish_data["name"], fish_data["rarity"], fish_data["cost"])
            self.fish_lst.append(new_fish)

    def catch_fish(self):
        if self.fish_lst:
            success = random.randint(1, 10)
            if success > 3:  # 70% success rate
                return self.fish_lst.pop(random.randint(0, len(self.fish_lst) - 1))
        return None

# Game setup
player = Player()
lake = Lake()

# Load and scale the hand image once (adjust the size as needed)
hand = pygame.image.load("hand.png")
hand = pygame.transform.scale(hand, (500, 300))

# Main game loop
running = True
while running:
    screen.fill(blu_color)  # Game background

    # Draw the inventory area
    pygame.draw.rect(screen, button_dark, (550, 50, 200, 400))
    inventory_text = font.render(f"Inventory ({len(player.inventory)}/12)", True, w_color)
    screen.blit(inventory_text, (560, 60))

    # Get the current mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Display fish in the player's inventory with hover highlighting
    for idx, fish in enumerate(player.inventory):
        fish_rect = pygame.Rect(560, 90 + idx * 30, 180, 25)
        if fish_rect.collidepoint(mouse_x, mouse_y):
            fish_text = font.render(f"{fish.name} (${fish.cost})", True, r_color)  # Highlight in red
            
        else:
            fish_text = font.render(f"{fish.name} (${fish.cost})", True, g_color)
        screen.blit(fish_text, (560, 90 + idx * 30))

    # Draw the hand image 
    hand_rect = hand.get_rect(center=(mouse_x, mouse_y))
    screen.blit(hand, hand_rect)

    # Display player level and EXP info
    level_text = font.render(f"Level: {player.lvl} | EXP: {player.exp}/{player.exp_needed}", True, w_color)
    screen.blit(level_text, (20, 20))

    # Display fish available in the lake
    for idx, fish in enumerate(lake.fish_lst):
        fish_text = font.render(fish.name, True, w_color)
        screen.blit(fish_text, (50, 60 + idx * 30))

    # Process
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # On click, check if an inventory fish is clicked to sell it; otherwise, catch a fish
        if event.type == pygame.MOUSEBUTTONDOWN:
            sold = False
            
            for idx, fish in enumerate(player.inventory):
                fish_rect = pygame.Rect(560, 90 + idx * 30, 180, 25)
                if fish_rect.collidepoint(event.pos):
                    player.sell_fish(fish)
                    sold = True
                    break
                
            if not sold:
                caught_fish = lake.catch_fish()
                if caught_fish:
                    player.add_fish(caught_fish)
                    player.leveling(caught_fish.cost // 5)
                    lake.spawn_fish()

    pygame.display.update()

pygame.quit()
sys.exit()
