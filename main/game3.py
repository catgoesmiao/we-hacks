#----------------------------------------------------------------------

import os
import pygame, sys, random
import soundfile as sf

from pygame.locals import *
from pygame import mixer

has_won = False
#----------------------------------------------------------------------

# Initialize pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Beautiful and Wonderful Fish Snatcher")
#----------------------------------------------------------------------

# Win CG
# Load the win BG CG
win = pygame.image.load("youWin.png")
win = pygame.transform.scale(win, (800, 600))  # Resize to fit the screen

# BG CG
background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (800, 600))
landlord = pygame.image.load("landlord.png")
landlord = pygame.transform.scale(landlord, (800, 600))
title = pygame.image.load("title.png")
title = pygame.transform.scale(title, (800, 600))
#----------------------------------------------------------------------

# BGM
pygame.mixer.music.load("piccadilly.wav")
pygame.mixer.music.play(-1)

# SFX
awesome = pygame.mixer.Sound("awesome.mp3")
fail = pygame.mixer.Sound("fail.mp3")
sale = pygame.mixer.Sound("sale.mp3")
splash = pygame.mixer.Sound("splash.mp3")
winsound = pygame.mixer.Sound("winsound.wav")
#----------------------------------------------------------------------

# Colors
b_color = (0, 0, 0)        # Black
g_color = (0, 255, 0)      # Green
r_color = (255, 0, 0)      # Red
w_color = (255, 255, 255)  # White

button_light = (170, 170, 170)
button_dark = (100, 100, 100)
#----------------------------------------------------------------------

# Font
font = pygame.font.SysFont("Impact", 25)
#----------------------------------------------------------------------

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
#----------------------------------------------------------------------

# Menu loop
menu = True
while menu:
    screen.blit(title, (0, 0))
    start_button.draw(screen)
    exit_button.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()
        if event.type == pygame.MOUSEBUTTONDOWN:
            start_button.check_click(event.pos)
            exit_button.check_click(event.pos)

    pygame.display.update()

# When start game, show a wall of text as a popup
# The player must click to continue -> popup goes away -> game begins
popup = True
popup_text = (
    "You big brokie!\n"
    "Your landlord just raised the rent...\n"
    "if you can't cough up a thousand bucks in a minute... \n"
    "you're gonna be HOMELESS!\n"
    "Quick, hurry up and catch some fish!\n"
    "Maybe if you sell them fast enough, you'll still have a place to crash!\n"
    "\n"
    "(Click to continue)"
)
# Split the text into lines based on newline characters
lines = popup_text.splitlines()

while popup:
    # Blit the background image
    screen.blit(landlord, (0, 0))
    
    y_offset = 100  # Initial y offset to position the text
    for line in lines:
        for dx in range(-2, 3):  
            for dy in range(-2, 3):  
                if dx != 0 or dy != 0:  # Skip the center
                    border_text = font.render(line, True, (0, 0, 0))  # Black border
                    border_rect = border_text.get_rect(center=(400 + dx * 2, y_offset + dy * 2))  # Offset the text
                    screen.blit(border_text, border_rect)

        rendered_line = font.render(line, True, w_color)  # White text
        line_rect = rendered_line.get_rect(center=(400, y_offset))
        screen.blit(rendered_line, line_rect)

        y_offset += font.get_linesize() + 5 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()
        if event.type == pygame.MOUSEBUTTONDOWN:
            popup = False  # Exit popup on any click

    pygame.display.update()
#----------------------------------------------------------------------

# Fish data
FISHIES = [
    {"name": "Blobette", "rarity": "R", "cost": 100, "weight": 1},  # Low chance
    {"name": "Chef", "rarity": "R", "cost": 50, "weight": 2},  # Slightly higher chance
    {"name": "Gerald", "rarity": "R", "cost": 50, "weight": 3},  # Medium chance
    {"name": "Goldfish", "rarity": "C", "cost": 5, "weight": 8},  # High chance
    {"name": "Largemouth", "rarity": "U", "cost": 25, "weight": 5},  # High chance
    {"name": "Mackerel", "rarity": "C", "cost": 5, "weight": 6},  # Medium-high chance
    {"name": "Magical Carp", "rarity": "L", "cost": 1000, "weight": 0.0001},  # 1 in 10,000 chance
    {"name": "Rainbow Trout", "rarity": "U", "cost": 25, "weight": 7},  # High chance
    {"name": "Shrimp", "rarity": "C", "cost": 5, "weight": 6},  # Medium-high chance
    {"name": "Yellow Perch", "rarity": "C", "cost": 5, "weight": 5},  # Medium chance
]

# Fish images
FISH_PICS = {
    "Blobette": pygame.image.load(os.path.join("assets", "blobette.png")),
    "Chef": pygame.image.load(os.path.join("assets", "chef.png")),
    "Gerald": pygame.image.load(os.path.join("assets", "gerald.png")),
    "Goldfish": pygame.image.load(os.path.join("assets", "goldfish.png")),
    "Largemouth": pygame.image.load(os.path.join("assets", "largemouth.png")),
    "Mackerel": pygame.image.load(os.path.join("assets", "mackerel.png")),
    "Magical Carp": pygame.image.load(os.path.join("assets", "magical_carp.png")),
    "Rainbow Trout": pygame.image.load(os.path.join("assets", "rainbow_trout.png")),
    "Shrimp": pygame.image.load(os.path.join("assets", "shrimp.png")),
    "Yellow Perch": pygame.image.load(os.path.join("assets", "yellow_perch.png"))
}

# Scale
for key in FISH_PICS:
    FISH_PICS[key] = pygame.transform.scale(FISH_PICS[key], (25, 25))
#----------------------------------------------------------------------
    
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
#----------------------------------------------------------------------
        
# Fish class
class Fish:
    def __init__(self, name, rarity, cost):
        self.name = name
        self.rarity = rarity
        self.cost = cost
#----------------------------------------------------------------------
        
# Lake class
class Lake:
    def __init__(self):
        self.fish_lst = []
        self.max_fish = 12
        self.spawn_fish()

    def spawn_fish(self):
        while len(self.fish_lst) < self.max_fish:
            fish_data = self.get_random_fish()  # Get a random fish
            new_fish = Fish(fish_data["name"], fish_data["rarity"], fish_data["cost"])
            self.fish_lst.append(new_fish)

    def get_random_fish(self):
        # Create a list of fish based on their weight
        weighted_fish = []
        for fish in FISHIES:
            weighted_fish.extend([fish] * int(fish["weight"] * 10000))  # Scale by 10,000 for precision

        # Pick a random fish from the weighted list
        return random.choice(weighted_fish)

    def catch_fish(self):
        if self.fish_lst:
            success = random.randint(1, 10)
            if success > 3:  # 70% success rate
                awesome.play()
                return self.fish_lst.pop(random.randint(0, len(self.fish_lst) - 1))
            else:
                fail.play()
            return None
#----------------------------------------------------------------------
        
# Game setup
player = Player()
lake = Lake()

# Load and scale the hand image once (adjust the size as needed)
open_hand = pygame.image.load("hand.png")
open_hand = pygame.transform.scale(open_hand, (500, 300))
grab = pygame.image.load("grab.png")
grab = pygame.transform.scale(grab, (500, 300))

hand = open_hand
#----------------------------------------------------------------------

# Main game loop
play_winsound = True
running = True
while running:
    screen.blit(background, (0, 0))  # Background first

    # Check for win condition (before any UI)
    if player.money >= 1000:
        screen.blit(win, (0, 0))  # Win screen
        
        if play_winsound:
            play_winsound = False
            winsound.play()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()
        continue  # Skip the rest of the game loop to keep the win screen on display

    # Process events: Mouse click, quit, etc.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Handle fish selling or catching
            hand = grab  # Show the hand image when the player clicks
            splash.play()
            
            # Check if the player clicked on a fish in the inventory to sell it
            sold = False
            for idx, fish in enumerate(player.inventory):
                fish_rect = pygame.Rect(560, 90 + idx * 30, 180, 25)
                if fish_rect.collidepoint(event.pos):
                    player.sell_fish(fish)
                    sold = True
                    break
                
            # If the player didn't sell a fish, try to catch a fish
            if not sold:
                caught_fish = lake.catch_fish()
                if caught_fish:
                    player.add_fish(caught_fish)
                    player.leveling(caught_fish.cost // 5)
                    lake.spawn_fish()

        elif event.type == pygame.MOUSEBUTTONUP:
            hand = open_hand  # Reset the hand image when the click is released

    # Draw the inventory area and fish inside it
    pygame.draw.rect(screen, b_color, (550, 50, 200, 400))
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

        # Display fish graphics
        if fish.name in FISH_PICS:
            screen.blit(FISH_PICS[fish.name], (520, 90 + idx * 30))

    # Draw the hand image based on the mouse position
    hand_rect = hand.get_rect(center=(mouse_x, mouse_y))
    screen.blit(hand, hand_rect)

    # Display player level and EXP info
    level_text = font.render(f"Level: {player.lvl} | EXP: {player.exp}/{player.exp_needed}", True, b_color)
    screen.blit(level_text, (20, 20))

    # Display player money count 
    money_text = font.render(f"Money: ${player.money}", True, b_color)
    screen.blit(money_text, (20, screen.get_height() - 40)) 

    # Display fish available in the lake
    for idx, fish in enumerate(lake.fish_lst):
        fish_text = font.render(fish.name, True, b_color)
        screen.blit(fish_text, (50, 60 + idx * 30))

        if fish.name in FISH_PICS:
            screen.blit(FISH_PICS[fish.name], (20, 60 + idx * 30))

    pygame.display.update()

pygame.quit()
sys.exit()
