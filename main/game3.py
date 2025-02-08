import os
import pygame, sys, random
import soundfile as sf

from pygame.locals import *
from pygame import mixer

# Initialize pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Beautiful and Wonderful Fish Snatcher")

# BGM
pygame.mixer.music.load("piccadilly.wav")
pygame.mixer.music.play(-1)

# SFX
awesome = pygame.mixer.Sound("awesome.mp3")
fail = pygame.mixer.Sound("fail.mp3")
sale = pygame.mixer.Sound("sale.mp3")
splash = pygame.mixer.Sound("splash.mp3")

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
start_button = Button("Go Fish", 300, 250, 200, 60, start_game)
exit_button = Button("Go Home", 300, 350, 200, 60, quit_game)

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
    {"name": "Blobette", "rarity": "R", "cost": 100},
    {"name": "Chef", "rarity": "R", "cost": 85},
    {"name": "Gerald", "rarity": "R", "cost": 90},
    {"name": "Goldfish", "rarity": "C", "cost": 5},
    {"name": "Largemouth", "rarity": "U", "cost": 22},
    {"name": "Mackerel", "rarity": "C", "cost": 9},
    {"name": "Magical Carp", "rarity": "L", "cost": 10000},
    {"name": "Rainbow Trout", "rarity": "U", "cost": 25},
    {"name": "Shrimp", "rarity": "C", "cost": 8},
    {"name": "Yellow Perch", "rarity": "C", "cost": 10},
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
        sale.play()

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
                awesome.play()
                return self.fish_lst.pop(random.randint(0, len(self.fish_lst) - 1))
            else:
                fail.play()
            return None

# Game setup
player = Player()
lake = Lake()

# Load and scale the hand image once (adjust the size as needed)
open_hand = pygame.image.load("hand.png")
open_hand = pygame.transform.scale(open_hand, (500, 300))
grab = pygame.image.load("grab.png")
grab = pygame.transform.scale(grab, (500, 300))

hand = open_hand

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

        # On click
        if event.type == pygame.MOUSEBUTTONDOWN:
            sold = False
            hand = grab
            splash.play()
            
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

        elif event.type == pygame.MOUSEBUTTONUP:
            hand = open_hand
    pygame.display.update()

pygame.quit()
sys.exit()
