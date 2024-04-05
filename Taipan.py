import pygame,sys,random
from pygame.math import Vector2
from button import Button
from pygame.locals import *
from Titanoboa import SteamGame
from BlackMamba import BulletGame


class TAIPAN:
    def __init__(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(1,0)
        self.new_cart = False

        self.head_up = pygame.image.load('Train/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Train/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Train/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Train/head_left.png').convert_alpha()
		
        self.tail_up = pygame.image.load('Train/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Train/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Train/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Train/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Train/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Train/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Train/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Train/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Train/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Train/body_bl.png').convert_alpha()

        self.train_sound = pygame.mixer.Sound('horn.wav')
        self.train_sound.set_volume(0.7)

    def draw_taipan(self):
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

    def move_taipan(self):
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
        self.taipan = TAIPAN()
        self.passenger = PASSENGER()

    def update(self):
        self.taipan.move_taipan()
        self.collision()
        self.fail_collision()
        self.game_over

    def draw_elements(self):
        self.grass_background()
        self.passenger.draw_passenger()
        self.taipan.draw_taipan()
        self.score()

    def collision(self):
        if self.passenger.pos == self.taipan.body[0]:
            self.passenger.randomize()
            self.taipan.add_cart()
            self.taipan.play_train_sound()

        for cart in self.taipan.body[1:]:
            if cart == self.passenger.pos:
                self.passenger.randomize()
    
    def fail_collision(self):
        if not 0 <= self.taipan.body[0].x < cell_number or not 0 <= self.taipan.body[0].y < cell_number:
            pygame.mixer.music.stop()
            self.game_over()

        for cart in self.taipan.body[1:]:
            if cart == self.taipan.body[0]:
                pygame.mixer.music.stop()
                self.game_over()

    def grass_background(self):
        for row in range(cell_number):
            for col in range(cell_number):
                grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                screen.blit(track, grass_rect)            

    def score(self):
        score_text = str(len(self.taipan.body) - 3)
        score_surface = game_font.render(score_text, False, (56,74,12))
        score_x = int(cell_size * cell_number - 50)
        score_y = int(cell_size * cell_number - 80)
        score_rect = score_surface.get_rect(center = (score_x, score_y))
        passenger_rect = passenger.get_rect(midright = (score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(passenger_rect.left - 2, passenger_rect.top - 2, passenger_rect.width + score_rect.width + 6, passenger_rect.height + 10)

        pygame.draw.rect(screen, (164, 209, 61), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(passenger, passenger_rect)
        pygame.draw.rect(screen, (56,74,12), bg_rect, 2)
        
    def game_over(self):
        score_text_2 = str(len(self.taipan.body)-3)
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

            self.taipan.reset()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.mixer.music.stop()
                    TaipanGame()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_m:
                        main_menu()

            pygame.display.update()
        
           
class Slider:
    def __init__(self, pos: tuple, size: tuple, initial_val: float, min: int, max: int) -> None:
        self.pos = pos
        self.size = size
        self.hovered = False
        self.grabbed = False

        self.slider_left_pos = self.pos[0] - (size[0]//2)
        self.slider_right_pos = self.pos[0] + (size[0]//2)
        self.slider_top_pos = self.pos[1] - (size[1]//2)

        self.min = min
        self.max = max
        self.initial_val = (self.slider_right_pos-self.slider_left_pos)*initial_val

        self.container_rect = pygame.Rect(self.slider_left_pos, self.slider_top_pos, self.size[0], self.size[1])
        self.button_rect = pygame.Rect(self.slider_left_pos + self.initial_val - 5, self.slider_top_pos, 10, self.size[1])

        
        self.text = game_font['m'].render(str(int(self.get_value())), True, "white", None)
        self.label_rect = self.text.get_rect(center = (self.pos[0], self.slider_top_pos - 15))
        
    def move_slider(self, mouse_pos):
        pos = mouse_pos[0]
        if pos < self.slider_left_pos:
            pos = self.slider_left_pos
        if pos > self.slider_right_pos:
            pos = self.slider_right_pos
        self.button_rect.centerx = pos
    def hover(self):
        self.hovered = True
    def render(self, app):
        pygame.draw.rect(app.screen, "darkgray", self.container_rect)
        pygame.draw.rect(app.screen, Button[self.hovered], self.button_rect)
    def get_value(self):
        val_range = self.slider_right_pos - self.slider_left_pos - 1
        button_val = self.button_rect.centerx - self.slider_left_pos

        return (button_val/val_range)*(self.max-self.min)+self.min
    def display_value(self, app):
        self.text = game_font['m'].render(str(int(self.get_value())), True, "white", None)
        app.screen.blit(self.text, self.label_rect)




pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size),pygame.SCALED|HWSURFACE|DOUBLEBUF|RESIZABLE)
clock = pygame.time.Clock()
passenger = pygame.image.load('Passengers/passengerT.png').convert_alpha()
track = pygame.image.load('track.png').convert_alpha()
game_font = pygame.font.Font('Pixeled.ttf', 25)
game_over_font = pygame.font.Font('Pixeled.ttf', 84)
game_score_font = pygame.font.Font('Pixeled.ttf', 44)
play_again_font = pygame.font.Font('Pixeled.ttf', 30)
back_button_font = pygame.font.Font('Pixeled.ttf', 23)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 125)
SCREEN = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size),pygame.SCALED|HWSURFACE|DOUBLEBUF|RESIZABLE)
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.png")

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)


main_game = MAIN()


def TaipanGame():

    sample = pygame.mixer.music.load('SampleMusic.wav')
    pygame.mixer.music.play(-1, 0.0)
    pygame.mixer.music.set_volume(0.3)

    while True:
        GAME_MOUSE_POS = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if GAME_BACK.checkForInput(GAME_MOUSE_POS):
                    main_menu()
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if main_game.taipan.direction.y != 1:
                        main_game.taipan.direction = Vector2(0,-1)
                if event.key == pygame.K_DOWN:
                    if main_game.taipan.direction.y != -1:
                        main_game.taipan.direction = Vector2(0,1)
                if event.key == pygame.K_RIGHT:
                    if main_game.taipan.direction.x != -1:
                        main_game.taipan.direction = Vector2(1,0)
                if event.key == pygame.K_LEFT:
                    if main_game.taipan.direction.x != 1:
                        main_game.taipan.direction = Vector2(-1,0)
        GAME_BACK = Button(image=None, pos=(20,20), 
                        text_input="BACK", font=get_font(35), base_color="Black", hovering_color="Green")
        GAME_BACK.changeColor(GAME_MOUSE_POS)
        GAME_BACK.update(screen)
        main_game.draw_elements()
        pygame.display.update()
        clock.tick(60)

def difficulty_select():
    while True:
        DIFFICULTY_SELECT_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("Gray")

        DIFFICULTY_SELECT_TEXT = get_font(45).render("SELECT DIFFICULTY", True, "Black")
        DIFFICULTY_SELECT_RECT = DIFFICULTY_SELECT_TEXT.get_rect(center=(400, 100))
        SCREEN.blit(DIFFICULTY_SELECT_TEXT, DIFFICULTY_SELECT_RECT)

        DIFFICULTY_SELECT_BACK = Button(image=None, pos=(400, 750), 
                            text_input="BACK", font=get_font(35), base_color="Black", hovering_color="Green")

        DIFFICULTY_SELECT_BACK.changeColor(DIFFICULTY_SELECT_MOUSE_POS)
        DIFFICULTY_SELECT_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if DIFFICULTY_SELECT_BACK.checkForInput(DIFFICULTY_SELECT_MOUSE_POS):
                    main_menu()
        TAIPAN_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(400, 250), 
                            text_input="TAIPAN", font=get_font(60), base_color="#d7fcd4", hovering_color="White")
        STEAM_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(400, 400), 
                            text_input="STEAM", font=get_font(60), base_color="#d7fcd4", hovering_color="White")
        BULLET_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(400, 550), 
                            text_input="BULLET", font=get_font(60), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(DIFFICULTY_SELECT_TEXT, DIFFICULTY_SELECT_RECT)

        for button in [TAIPAN_BUTTON, STEAM_BUTTON, BULLET_BUTTON]:
            button.changeColor(DIFFICULTY_SELECT_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if TAIPAN_BUTTON.checkForInput(DIFFICULTY_SELECT_MOUSE_POS):
                    pygame.mixer.music.fadeout(1000)
                    TaipanGame()
                if STEAM_BUTTON.checkForInput(DIFFICULTY_SELECT_MOUSE_POS):
                    pygame.mixer.music.fadeout(1000)
                    SteamGame()
                if BULLET_BUTTON.checkForInput(DIFFICULTY_SELECT_MOUSE_POS):
                    pygame.mixer.music.fadeout(1000)
                    BulletGame()
        pygame.display.update()
def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("Gray")

        OPTIONS_TEXT = get_font(45).render("Change Volume", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(400, 100))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(400, 300), 
                            text_input="BACK", font=get_font(35), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():

    music = pygame.mixer.music.load('MenuMusic.wav')
    pygame.mixer.music.play(-1, 0.0)
    pygame.mixer.music.set_volume(0.7)

    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(60).render("TAIPAN TRAIN", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 75))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(400, 250), 
                            text_input="PLAY", font=get_font(60), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(400, 400), 
                            text_input="OPTIONS", font=get_font(60), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(400, 550), 
                            text_input="QUIT", font=get_font(60), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.mixer.music.fadeout(1000)
                    difficulty_select()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()



