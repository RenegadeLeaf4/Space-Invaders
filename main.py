import pygame 
import random 
import os 
pygame.init()

SCREEN_WIDTH = 540 
SCREEN_HEIGHT = 620
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

MAIN_FONT = pygame.font.Font(os.path.join("assets", "kenvector_future_thin.ttf"), 30)

# Background
BG_IMG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (SCREEN_WIDTH, SCREEN_HEIGHT))

# Shhip(Player)
YELLOW_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png")).convert_alpha()

# Ship(Enemy)
GREEN_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png")).convert_alpha()
BLUE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png")).convert_alpha()
RED_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png")).convert_alpha()

# Laser
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png")).convert_alpha()
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png")).convert_alpha()
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png")).convert_alpha()
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png")).convert_alpha()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (0, 255, 255)
GREEN = (0,255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

clock = pygame.time.Clock()

class Laser(): 
	def __init__(self, x, y, img): 
		pass

	def draw(self, screen): 
		pass

class Ship(): 
	def __init__(self, x, y): 
		pass

	def draw(self, screen): 
		pass

class Player(Ship): 
	def __init__(self, x, y): 
		# super().__init__(x, y)
		pass

class Enemy(Ship):
	def __init__(self, x, y, color):
		# super().__init__(x, y)
		pass

def main(screen): 
	run = True 

	def redraw_game_win(screen): 
		screen.blit(BG_IMG, (0, 0))

		pygame.display.update()

	while run: 
		clock.tick(FPS)
		for event in pygame.event.get(): 
			if event.type == pygame.QUIT: 
				run = False

		redraw_game_win(screen)

main(screen)