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

# UI 
PLAYER_LIVES = pygame.transform.scale(pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png")).convert_alpha(), (30, 30))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (0, 255, 255)
GREEN = (0,255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

clock = pygame.time.Clock()

class Laser(): 
	def __init__(self, x, y, img): 
		self.x = x 
		self.y = y 

		self.img = img

		self.mask = pygame.mask.from_surface(self.img)

	def move(self, vel): 
		self.y -= vel

	def collide(self, obj): 
		return collide(self, obj)

	def draw(self, screen): 
		screen.blit(self.img, (self.x, self.y))

class Ship(): 
	VEL = 8
	COOLDOWN = 20

	def __init__(self, x, y): 
		self.x = x 
		self.y = y 

		self.img = None
		self.laser_img = None 
		self.lasers = []

		self.health = 100
		self.cooldown_counter = 0

	def get_width(self): 
		return self.img.get_width()

	def get_height(self): 
		return self.img.get_height()

	def cooldown(self): 
		if self.cooldown_counter > 0: 
			self.cooldown_counter += 1
		if self.cooldown_counter >= self.COOLDOWN: 
			self.cooldown_counter = 0

	def move_lasers(self, vel, obj): 
		self.cooldown()
		for laser in self.lasers[:]: 
			laser.move(vel)
			if laser.y + self.laser_img.get_height() <= 0: 
				self.lasers.remove(laser)
			if laser.collide(obj):
				obj.health -= 10
				self.lasers.remove(laser)

	def shoot(self): 
		if self.cooldown_counter == 0:
			laser = Laser(self.x + self.img.get_width() / 2 - self.laser_img.get_width() / 2, self.y -  50, self.laser_img)
			self.lasers.append(laser)
			self.cooldown_counter = 1

	def draw(self, screen): 
		screen.blit(self.img, (self.x, self.y)) 
		for laser in self.lasers: 
			laser.draw(screen)

class Player(Ship): 
	def __init__(self, x, y): 
		super().__init__(x, y)
		self.img = YELLOW_SHIP
		self.laser_img = YELLOW_LASER

		self.mask = pygame.mask.from_surface(self.img)

		self.lives = 5 
		self.lives_img = PLAYER_LIVES

	def move_lasers(self, laser_vel, objs, obj):
		self.cooldown()
		for laser in self.lasers:
			laser.move(laser_vel)
			if laser.y + self.laser_img.get_height() <= 0:
				self.lasers.remove(laser)
			else:
				for obj in objs:
					if laser.collide(obj):
						objs.remove(obj)
						if laser in self.lasers:
							self.lasers.remove(laser)

	def draw_lives(self, screen): 
		for i in range(self.lives):
			self.lives_x = 300 + 45 * i
			self.lives_y = 50 - self.lives_img.get_height() / 2
			screen.blit(self.lives_img, (self.lives_x, self.lives_y))
	
	def draw_healthbar(self, screen, pct): 
		BAR_LENGHT = 200
		BAR_HEIGHT = 15

		if pct <0: 
			pct = 0
		else: 
			pygame.draw.rect(screen, GREEN, (25, 50 - BAR_HEIGHT / 2, ((pct / 100) * BAR_LENGHT), BAR_HEIGHT))
        
		pygame.draw.rect(screen, WHITE, (25, 50 - BAR_HEIGHT / 2, BAR_LENGHT, BAR_HEIGHT), 2)


class Enemy(Ship):
	VEL = 6

	COLOR_MAP = {
        "green": (GREEN_SHIP, GREEN_LASER),
        "blue":(BLUE_SHIP, BLUE_LASER),
        "red": (RED_SHIP, RED_LASER)
    }

	def __init__(self, x, y, color):
		super().__init__(x, y)
		self.img, self.laser_img = self.COLOR_MAP[color]

		self.mask = pygame.mask.from_surface(self.img)

	def move(self): 
		self.y += self.VEL

	def shoot(self): 
		if self.cooldown_counter == 0: 
			laser = Laser(self.x + self.img.get_width() / 2 - self.laser_img.get_width() / 2, self.y + 20, self.laser_img)
			self.lasers.append(laser)
			self.cooldown_counter = 1

def collide(obj1, obj2): 
	offset_x = round(obj2.x - obj1.x)
	offset_y = round(obj2.y - obj1.y)

	return obj1.mask.overlap(obj2.mask, (offset_x, offset_y))

def main_menu(screen): 
	screen.blit(BG_IMG, (0, 0))
	start_text = MAIN_FONT.render("Press mouse to start", 1, WHITE)
	start_text_rect = start_text.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
	screen.blit(start_text, start_text_rect)

	pygame.display.flip()
	run = True 
	while run: 
		clock.tick(FPS)
		for event in pygame.event.get(): 
			if event.type == pygame.QUIT: 
				run = False

			if event.type == pygame.MOUSEBUTTONDOWN: 
				main(screen)
				run = False

def game_over_screen(screen): 
	screen.blit(BG_IMG, (0, 0))
	go_text = MAIN_FONT.render("You lost!", 1, WHITE)
	go_text_rect = go_text.get_rect(center= (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100))
	screen.blit(go_text, go_text_rect)

	restart_text = MAIN_FONT.render("Press mouse to restart", 1, WHITE)
	restart_text_rect = restart_text.get_rect(center= (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 100))
	screen.blit(restart_text, restart_text_rect)

	pygame.display.flip()
	run = True 
	while run: 
		clock.tick(FPS)
		for event in pygame.event.get(): 
			if event.type == pygame.QUIT: 
				run = False

			if event.type == pygame.MOUSEBUTTONDOWN: 
				main(screen)
				run = False

def main(screen): 
	run = True 
	player = Player(SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT - 100)

	enemies = []
	wave_length = 5

	score = 0
	lost = False 

	def redraw_game_win(screen): 
		screen.blit(BG_IMG, (0, 0))
		player.draw(screen)

		for enemy in enemies: 
			enemy.draw(screen)

		player.draw_lives(screen)
		player.draw_healthbar(screen, player.health)

		score_text = MAIN_FONT.render(str(round(score)), 1, WHITE)
		screen.blit(score_text, (25, SCREEN_HEIGHT - 60))

		pygame.display.update()

	while run: 
		clock.tick(FPS)
		for event in pygame.event.get(): 
			if event.type == pygame.QUIT: 
				pygame.quit()

		if not lost:
			if len(enemies) == 0:
				wave_length += 2
				for i in range(wave_length):
					enemy = Enemy(random.randrange(50, SCREEN_WIDTH - 100), random.randrange(-1500, -100), random.choice(["green", "red", "blue"]))
					enemies.append(enemy)

			player.move_lasers(8, enemies, enemy)

			if player.health <= 0 and player.lives >= 1: 
				player.lives -= 1
				player.health = 100

			if player.lives == 0: 
				lost = True
				break

			keys = pygame.key.get_pressed()

			if keys[pygame.K_LEFT] and player.x + 10 >= 0: 
				player.x -= player.VEL
			if keys[pygame.K_RIGHT] and player.x - 10 <= SCREEN_WIDTH - player.get_width(): 
				player.x += player.VEL
			if keys[pygame.K_SPACE]: 
				player.shoot()

			for enemy in enemies[:]:
				enemy.move()
				enemy.move_lasers(-8, player)

				if random.randrange(100) == 50:
					enemy.shoot()

				if collide(enemy, player):
					player.health -= 5
					enemies.remove(enemy)

				if enemy.y + enemy.get_height() > SCREEN_HEIGHT:
					player.lives -= 1
					enemies.remove(enemy)

			score += 0.2

		redraw_game_win(screen)

	game_over_screen(screen)

main_menu(screen)