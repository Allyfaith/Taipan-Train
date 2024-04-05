import pygame,sys,random
from pygame.math import Vector2
from button import Button
from pygame.locals import *


class STEAM:
    def __init__(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(1,0)
        self.new_cart = False

        self.head_up = pygame.image.load('Steam/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Steam/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Steam/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Steam/head_left.png').convert_alpha()
		
        self.tail_up = pygame.image.load('Steam/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Steam/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Steam/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Steam/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Steam/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Steam/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Steam/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Steam/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Steam/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Steam/body_bl.png').convert_alpha()

        self.train_sound = pygame.mixer.Sound('horn.wav')
        self.train_sound.set_volume(0.7)

    def draw_steam(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index,cart in enumerate(self.body):
            x_pos = int(cart.x * cell_size)
            y_pos = int(cart.y * cell_size)
            cart_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, cart_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, cart_rect)
            else:
                previous_cart = self.body[index + 1] - cart
                next_cart = self.body[index - 1] - cart
                if previous_cart.x == next_cart.x:
                    screen.blit(self.body_vertical,cart_rect)
                elif previous_cart.y == next_cart.y:
                    screen.blit(self.body_horizontal,cart_rect)
                else:
                    if previous_cart.x == -1 and next_cart.y == -1 or previous_cart.y == -1 and next_cart.x == -1: 
                        screen.blit(self.body_tl, cart_rect)
                    elif previous_cart.x == -1 and next_cart.y == 1 or previous_cart.y == 1 and next_cart.x == -1:
                        screen.blit(self.body_bl, cart_rect)
                    elif previous_cart.x == 1 and next_cart.y == -1 or previous_cart.y == -1 and next_cart.x == 1:
                        screen.blit(self.body_tr, cart_rect)
                    elif previous_cart.x == 1 and next_cart.y == 1 or previous_cart.y == 1 and next_cart.x == 1:
                        screen.blit(self.body_br, cart_rect)

    def update_head_graphics(self):
        head_direction = self.body[1] - self.body[0]
        if head_direction == Vector2(1,0): self.head = self.head_left
        elif head_direction == Vector2(-1,0): self.head = self.head_right
        elif head_direction == Vector2(0,1): self.head = self.head_up
        elif head_direction == Vector2(0,-1): self.head = self.head_down

    def update_tail_graphics(self):
        tail_direction = self.body[-2] - self.body[-1]
        if tail_direction == Vector2(1,0): self.tail = self.tail_left
        elif tail_direction == Vector2(-1,0): self.tail = self.tail_right
        elif tail_direction == Vector2(0,1): self.tail = self.tail_up
        elif tail_direction == Vector2(0,-1): self.tail = self.tail_down

    def move_steam(self):
        if self.new_cart == True:
            body_copy = self.body[:]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_cart = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_cart(self):
        self.new_cart = True     

    def play_train_sound(self):
        self.train_sound.play()

    def reset(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(1,0)

class PASSENGER:
    def __init__(self):
        self.randomize()

    def draw_passenger(self):
        passenger_rect = pygame.Rect(int(self.pos.x * cell_size),int (self.pos.y * cell_size),cell_size, cell_size)
        screen.blit(passenger, passenger_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

class MAIN:
    def __init__(self):
        self.steam = STEAM()
        self.passenger = PASSENGER()

    def update(self):
        self.steam.move_steam()
        self.collision()
        self.fail_collision()

    def draw_elements(self):
        self.grass_background()
        self.passenger.draw_passenger()
        self.steam.draw_steam()
        self.score()

    def collision(self):
        if self.passenger.pos == self.steam.body[0]:
            self.passenger.randomize()
            self.steam.add_cart()
            self.steam.play_train_sound()

        for cart in self.steam.body[1:]:
            if cart == self.passenger.pos:
                self.passenger.randomize()
    
    def fail_collision(self):
        if not 0 <= self.steam.body[0].x < cell_number or not 0 <= self.steam.body[0].y < cell_number:
            pygame.mixer.music.stop()
            self.game_over()

        for cart in self.steam.body[1:]:
            if cart == self.steam.body[0]:
                pygame.mixer.music.stop()
                self.game_over()

    def grass_background(self):
        for row in range(cell_number):
            for col in range(cell_number):
                grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                screen.blit(track, grass_rect)

    def score(self):
        score_text = str(len(self.steam.body) - 3)
        score_surface = game_font.render(score_text, False, (56,74,12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center = (score_x, score_y))
        passenger_rect = passenger.get_rect(midright = (score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(passenger_rect.left - 2, passenger_rect.top - 2, passenger_rect.width + score_rect.width + 6, passenger_rect.height + 10)

        pygame.draw.rect(screen, (164, 209, 61), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(passenger, passenger_rect)
        pygame.draw.rect(screen, (56,74,12), bg_rect, 2)

    def game_over(self):
        score_text_2 = str(len(self.steam.body)-3)
        sample = pygame.mixer.music.load('GameOverMusic.wav')
        pygame.mixer.music.play(-1, 0.0)
        pygame.mixer.music.set_volume(0.5)

        while True:
            game_over_text = game_over_font.render("GAME OVER", True, (200,200,200))
            game_score_text = game_score_font.render(f"SCORE: {score_text_2}", True, (200,200,200))
            play_again_text = play_again_font.render("CLICK ON SCREEN TO PLAY AGAIN", True, (200,200,200))
            back_button_text = back_button_font.render("PRESS [M] TO GO BACK TO THE MAIN MENU", True, (200,200,200))
            screen.fill((0,100,36))
            screen.blit(game_over_text,(35,-27))
            screen.blit(game_score_text,(240,175))
            screen.blit(play_again_text,(25,340))
            screen.blit(back_button_text,(29.5, 600))

            self.steam.reset()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.mixer.music.stop()
                    SteamGame()

            pygame.display.update()
        



pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size),pygame.SCALED|HWSURFACE|DOUBLEBUF|RESIZABLE)
clock = pygame.time.Clock()
passenger = pygame.image.load('Passengers/passengerS.png').convert_alpha()
track = pygame.image.load('track.png').convert_alpha()
game_font = pygame.font.Font('Pixeled.ttf', 25)
game_over_font = pygame.font.Font('Pixeled.ttf', 84)
game_score_font = pygame.font.Font('Pixeled.ttf', 44)
play_again_font = pygame.font.Font('Pixeled.ttf', 30)
back_button_font = pygame.font.Font('Pixeled.ttf', 23)
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = MAIN()

def SteamGame():

    sample = pygame.mixer.music.load('SampleMusic.wav')
    pygame.mixer.music.play(-1, 0.0)
    pygame.mixer.music.set_volume(0.3)

    while True:
        GAME_MOUSE_POS = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if main_game.steam.direction.y != 1:
                        main_game.steam.direction = Vector2(0,-1)
                if event.key == pygame.K_DOWN:
                    if main_game.steam.direction.y != -1:
                        main_game.steam.direction = Vector2(0,1)
                if event.key == pygame.K_RIGHT:
                    if main_game.steam.direction.x != -1:
                        main_game.steam.direction = Vector2(1,0)
                if event.key == pygame.K_LEFT:
                    if main_game.steam.direction.x != 1:
                        main_game.steam.direction = Vector2(-1,0)


        screen.fill((175,215,70))
        main_game.draw_elements()
        pygame.display.update()
        clock.tick(60)



