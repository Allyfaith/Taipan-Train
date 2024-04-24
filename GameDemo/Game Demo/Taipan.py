import pygame,sys,random
from pygame.math import Vector2
from button import Button
from pygame.locals import *

#TaipanTrain

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
        NewTracks = pygame.image.load('TaipanTracks.png').convert()
        screen.blit(NewTracks, (0,0))         

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
        Game_over_image = pygame.image.load('GameOver.png').convert()
        sample = pygame.mixer.music.load('GameOverMusic.wav')
        pygame.mixer.music.play(-1, 0.0)
        pygame.mixer.music.set_volume(0.5)

        while True:
            game_over_text = game_over_font.render("GAME OVER", True, (200,200,200))
            game_score_text = game_score_font.render(f"SCORE: {score_text_2}", True, (200,200,200))
            play_again_text = play_again_font.render("CLICK ON SCREEN TO PLAY AGAIN", True, (200,200,200))
            back_button_text = back_button_font.render("PRESS [M] FOR MAIN MENU", True, (200,200,200))
            back_button_2Text = back_button_fontBM.render("PRESS [D] TO CHANGE DIFFICULTY", True, (200,200,200))
            screen.blit(Game_over_image,(0,0))
            screen.blit(game_over_text,(35,-27))
            screen.blit(game_score_text,(240,175))
            screen.blit(play_again_text,(25,340))
            screen.blit(back_button_text,(135, 600))
            screen.blit(back_button_2Text,(135, 700))
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
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_d:
                        difficulty_select()

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
track = pygame.image.load('TaipanTracks.png').convert_alpha()
game_font = pygame.font.Font('Pixeled.ttf', 25)
game_over_font = pygame.font.Font('Pixeled.ttf', 84)
game_score_font = pygame.font.Font('Pixeled.ttf', 44)
play_again_font = pygame.font.Font('Pixeled.ttf', 30)
back_button_font = pygame.font.Font('Pixeled.ttf', 23)
SCREEN_UPDATE = pygame.USEREVENT
SCREEN = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size),pygame.SCALED|HWSURFACE|DOUBLEBUF|RESIZABLE)
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.png")

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)


main_game = MAIN()


def TaipanGame():
    pygame.time.set_timer(SCREEN_UPDATE, 125) 

    TaipanBGM = pygame.mixer.music.load('TaipanMusic.wav')
    pygame.mixer.music.play(-1, 0.0)
    pygame.mixer.music.set_volume(0.1)

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



class BULLET:
    def __init__(self):
        self.bodyBM = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.directionBM = Vector2(1,0)
        self.new_cartBM = False

        self.head_upBM = pygame.image.load('Bullet/head_up.png').convert_alpha()
        self.head_downBM = pygame.image.load('Bullet/head_down.png').convert_alpha()
        self.head_rightBM = pygame.image.load('Bullet/head_right.png').convert_alpha()
        self.head_leftBM = pygame.image.load('Bullet/head_left.png').convert_alpha()
		
        self.tail_upBM = pygame.image.load('Bullet/tail_up.png').convert_alpha()
        self.tail_downBM = pygame.image.load('Bullet/tail_down.png').convert_alpha()
        self.tail_rightBM = pygame.image.load('Bullet/tail_right.png').convert_alpha()
        self.tail_leftBM = pygame.image.load('Bullet/tail_left.png').convert_alpha()

        self.body_verticalBM = pygame.image.load('Bullet/body_vertical.png').convert_alpha()
        self.body_horizontalBM = pygame.image.load('Bullet/body_horizontal.png').convert_alpha()

        self.body_trBM = pygame.image.load('Bullet/body_tr.png').convert_alpha()
        self.body_tlBM = pygame.image.load('Bullet/body_tl.png').convert_alpha()
        self.body_brBM = pygame.image.load('Bullet/body_br.png').convert_alpha()
        self.body_blBM = pygame.image.load('Bullet/body_bl.png').convert_alpha()

        self.train_soundBM = pygame.mixer.Sound('horn.wav')
        self.train_soundBM.set_volume(0.7)

    def draw_bullet(self):
        self.update_head_graphicsBM()
        self.update_tail_graphicsBM()

        for indexBM,cartBM in enumerate(self.bodyBM):
            x_posBM = int(cartBM.x * cell_sizeBM)
            y_posBM = int(cartBM.y * cell_sizeBM)
            cart_rectBM = pygame.Rect(x_posBM, y_posBM, cell_sizeBM, cell_sizeBM)

            if indexBM == 0:
                screenBM.blit(self.headBM, cart_rectBM)
            elif indexBM == len(self.bodyBM) - 1:
                screenBM.blit(self.tailBM, cart_rectBM)
            else:
                previous_cartBM = self.bodyBM[indexBM + 1] - cartBM
                next_cartBM = self.bodyBM[indexBM - 1] - cartBM
                if previous_cartBM.x == next_cartBM.x:
                    screenBM.blit(self.body_verticalBM,cart_rectBM)
                elif previous_cartBM.y == next_cartBM.y:
                    screenBM.blit(self.body_horizontalBM,cart_rectBM)
                else:
                    if previous_cartBM.x == -1 and next_cartBM.y == -1 or previous_cartBM.y == -1 and next_cartBM.x == -1: 
                        screenBM.blit(self.body_tlBM, cart_rectBM)
                    elif previous_cartBM.x == -1 and next_cartBM.y == 1 or previous_cartBM.y == 1 and next_cartBM.x == -1:
                        screenBM.blit(self.body_blBM, cart_rectBM)
                    elif previous_cartBM.x == 1 and next_cartBM.y == -1 or previous_cartBM.y == -1 and next_cartBM.x == 1:
                        screenBM.blit(self.body_trBM, cart_rectBM)
                    elif previous_cartBM.x == 1 and next_cartBM.y == 1 or previous_cartBM.y == 1 and next_cartBM.x == 1:
                        screenBM.blit(self.body_brBM, cart_rectBM)

    def update_head_graphicsBM(self):
        head_directionBM = self.bodyBM[1] - self.bodyBM[0]
        if head_directionBM == Vector2(1,0): self.headBM = self.head_leftBM
        elif head_directionBM == Vector2(-1,0): self.headBM = self.head_rightBM
        elif head_directionBM == Vector2(0,1): self.headBM = self.head_upBM
        elif head_directionBM == Vector2(0,-1): self.headBM = self.head_downBM

    def update_tail_graphicsBM(self):
        tail_directionBM = self.bodyBM[-2] - self.bodyBM[-1]
        if tail_directionBM == Vector2(1,0): self.tailBM = self.tail_leftBM
        elif tail_directionBM == Vector2(-1,0): self.tailBM = self.tail_rightBM
        elif tail_directionBM == Vector2(0,1): self.tailBM = self.tail_upBM
        elif tail_directionBM == Vector2(0,-1): self.tailBM = self.tail_downBM

    def move_bulletBM(self):
        if self.new_cartBM == True:
            body_copyBM = self.bodyBM[:]
            body_copyBM.insert(0,body_copyBM[0] + self.directionBM)
            self.bodyBM = body_copyBM[:]
            self.new_cartBM = False
        else:
            body_copyBM = self.bodyBM[:-1]
            body_copyBM.insert(0,body_copyBM[0] + self.directionBM)
            self.bodyBM = body_copyBM[:]

    def add_cartBM(self):
        self.new_cartBM = True     

    def play_train_soundBM(self):
        self.train_soundBM.play()

    def resetBM(self):
        self.bodyBM = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.directionBM = Vector2(1,0)

class PASSENGERBM:
    def __init__(self):
        self.randomizeBM()

    def draw_passengerBM(self):
        passenger_rectBM = pygame.Rect(int(self.posBM.x * cell_sizeBM),int (self.posBM.y * cell_sizeBM),cell_sizeBM, cell_sizeBM)
        screenBM.blit(passengerBM, passenger_rectBM)

    def randomizeBM(self):
        self.xBM = random.randint(0, cell_numberBM - 1)
        self.yBM = random.randint(0, cell_numberBM - 1)
        self.posBM = Vector2(self.xBM, self.yBM)

class MAINBM:
    def __init__(self):
        self.bullet = BULLET()
        self.passengerBM = PASSENGERBM()

    def updateBM(self):
        self.bullet.move_bulletBM()
        self.collisionBM()
        self.fail_collisionBM()

    def draw_elementsBM(self):
        self.grass_backgroundBM()
        self.passengerBM.draw_passengerBM()
        self.bullet.draw_bullet()
        self.scoreBM()

    def collisionBM(self):
        if self.passengerBM.posBM == self.bullet.bodyBM[0]:
            self.passengerBM.randomizeBM()
            self.bullet.add_cartBM()
            self.bullet.play_train_soundBM()

        for cart in self.bullet.bodyBM[1:]:
            if cart == self.passengerBM.posBM:
                self.passengerBM.randomizeBM()
    
    def fail_collisionBM(self):
        if not 0 <= self.bullet.bodyBM[0].x < cell_numberBM or not 0 <= self.bullet.bodyBM[0].y < cell_numberBM:
            self.game_overBM()

        for cartBM in self.bullet.bodyBM[1:]:
            if cartBM == self.bullet.bodyBM[0]:
                self.game_overBM()


    def grass_backgroundBM(self):
       NewTracksBM = pygame.image.load('BulletTracks.png').convert()
       screen.blit(NewTracksBM, (0,0))

    def scoreBM(self):
        score_textBM = str(len(self.bullet.bodyBM) - 3)
        score_surfaceBM = game_fontBM.render(score_textBM, False, (56,74,12))
        score_xBM = int(cell_sizeBM * cell_numberBM - 60)
        score_yBM = int(cell_sizeBM * cell_numberBM - 40)
        score_rectBM = score_surfaceBM.get_rect(center = (score_xBM, score_yBM))
        passenger_rectBM = passengerBM.get_rect(midright = (score_rectBM.left, score_rectBM.centery))
        bg_rectBM = pygame.Rect(passenger_rectBM.left - 2, passenger_rectBM.top - 2, passenger_rectBM.width + score_rectBM.width + 6, passenger_rectBM.height + 10)

        pygame.draw.rect(screenBM, (164, 209, 61), bg_rectBM)
        screenBM.blit(score_surfaceBM, score_rectBM)
        screenBM.blit(passengerBM, passenger_rectBM)
        pygame.draw.rect(screenBM, (56,74,12), bg_rectBM, 2)

    def game_overBM(self):
        Game_over_imageBM = pygame.image.load('GameOver.png').convert()
        score_text_2BM = str(len(self.bullet.bodyBM)-3)
        sampleBM = pygame.mixer.music.load('GameOverMusic.wav')
        pygame.mixer.music.play(-1, 0.0)
        pygame.mixer.music.set_volume(0.5)

        while True:
            game_over_textBM = game_over_fontBM.render("GAME OVER", True, (200,200,200))
            game_score_textBM = game_score_fontBM.render(f"SCORE: {score_text_2BM}", True, (200,200,200))
            play_again_textBM = play_again_fontBM.render("CLICK ON SCREEN TO PLAY AGAIN", True, (200,200,200))
            back_button_textBM = back_button_fontBM.render("PRESS [M] FOR MAIN MENU", True, (200,200,200))
            back_button_2TextBM = back_button_fontBM.render("PRESS [D] TO CHANGE DIFFICULTY", True, (200,200,200))
            screen.blit(Game_over_imageBM,(0,0))
            screenBM.blit(game_over_textBM,(35,-27))
            screenBM.blit(game_score_textBM,(240,175))
            screenBM.blit(play_again_textBM,(25,340))
            screenBM.blit(back_button_textBM,(135, 600))
            screenBM.blit(back_button_2TextBM,(135, 700))

            self.bullet.resetBM()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.mixer.music.stop()
                    BulletGame()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_m:
                        main_menu()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_d:
                        difficulty_select()
            pygame.display.update()



pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
cell_sizeBM = 40
cell_numberBM = 20
screenBM = pygame.display.set_mode((cell_numberBM * cell_sizeBM, cell_numberBM * cell_sizeBM),pygame.SCALED|HWSURFACE|DOUBLEBUF|RESIZABLE)
clockBM = pygame.time.Clock()
passengerBM = pygame.image.load('Passengers/passengerB.png').convert_alpha()
trackBM = pygame.image.load('BulletTracks.png').convert_alpha()
game_fontBM = pygame.font.Font('Pixeled.ttf', 25)
game_over_fontBM = pygame.font.Font('Pixeled.ttf', 84)
game_score_fontBM = pygame.font.Font('Pixeled.ttf', 44)
play_again_fontBM = pygame.font.Font('Pixeled.ttf', 30)
back_button_fontBM = pygame.font.Font('Pixeled.ttf', 23)
SCREEN_UPDATEBM = pygame.USEREVENT

main_gameBM = MAINBM()

def BulletGame():
    pygame.time.set_timer(SCREEN_UPDATEBM, 90) 

    BulletBGM = pygame.mixer.music.load('BulletMusic.wav')
    pygame.mixer.music.play(-1, 0.0)
    pygame.mixer.music.set_volume(0.2)

    while True:
        GAME_MOUSE_POSBM = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATEBM:
                main_gameBM.updateBM()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if main_gameBM.bullet.directionBM.y != 1:
                        main_gameBM.bullet.directionBM = Vector2(0,-1)
                if event.key == pygame.K_DOWN:
                    if main_gameBM.bullet.directionBM.y != -1:
                        main_gameBM.bullet.directionBM = Vector2(0,1)
                if event.key == pygame.K_RIGHT:
                    if main_gameBM.bullet.directionBM.x != -1:
                        main_gameBM.bullet.directionBM = Vector2(1,0)
                if event.key == pygame.K_LEFT:
                    if main_gameBM.bullet.directionBM.x != 1:
                        main_gameBM.bullet.directionBM = Vector2(-1,0)


        screenBM.fill((175,215,70))
        main_gameBM.draw_elementsBM()
        pygame.display.update()
        clockBM.tick(60)

class STEAM:
    def __init__(self):
        self.bodyT = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.directionT = Vector2(1,0)
        self.new_cartT = False

        self.head_upT = pygame.image.load('Steam/head_up.png').convert_alpha()
        self.head_downT = pygame.image.load('Steam/head_down.png').convert_alpha()
        self.head_rightT = pygame.image.load('Steam/head_right.png').convert_alpha()
        self.head_leftT = pygame.image.load('Steam/head_left.png').convert_alpha()
		
        self.tail_upT = pygame.image.load('Steam/tail_up.png').convert_alpha()
        self.tail_downT = pygame.image.load('Steam/tail_down.png').convert_alpha()
        self.tail_rightT = pygame.image.load('Steam/tail_right.png').convert_alpha()
        self.tail_leftT = pygame.image.load('Steam/tail_left.png').convert_alpha()

        self.body_verticalT = pygame.image.load('Steam/body_vertical.png').convert_alpha()
        self.body_horizontalT = pygame.image.load('Steam/body_horizontal.png').convert_alpha()

        self.body_trT = pygame.image.load('Steam/body_tr.png').convert_alpha()
        self.body_tlT = pygame.image.load('Steam/body_tl.png').convert_alpha()
        self.body_brT = pygame.image.load('Steam/body_br.png').convert_alpha()
        self.body_blT = pygame.image.load('Steam/body_bl.png').convert_alpha()

        self.train_soundT = pygame.mixer.Sound('horn.wav')
        self.train_soundT.set_volume(0.7)

    def draw_steam(self):
        self.update_head_graphicsT()
        self.update_tail_graphicsT()

        for indexT,cartT in enumerate(self.bodyT):
            x_posT = int(cartT.x * cell_sizeT)
            y_posT = int(cartT.y * cell_sizeT)
            cart_rectT = pygame.Rect(x_posT, y_posT, cell_sizeT, cell_sizeT)

            if indexT == 0:
                screenT.blit(self.headT, cart_rectT)
            elif indexT == len(self.bodyT) - 1:
                screenT.blit(self.tailT, cart_rectT)
            else:
                previous_cartT = self.bodyT[indexT + 1] - cartT
                next_cartT = self.bodyT[indexT - 1] - cartT
                if previous_cartT.x == next_cartT.x:
                    screenT.blit(self.body_verticalT,cart_rectT)
                elif previous_cartT.y == next_cartT.y:
                    screenT.blit(self.body_horizontalT,cart_rectT)
                else:
                    if previous_cartT.x == -1 and next_cartT.y == -1 or previous_cartT.y == -1 and next_cartT.x == -1: 
                        screenT.blit(self.body_tlT, cart_rectT)
                    elif previous_cartT.x == -1 and next_cartT.y == 1 or previous_cartT.y == 1 and next_cartT.x == -1:
                        screenT.blit(self.body_blT, cart_rectT)
                    elif previous_cartT.x == 1 and next_cartT.y == -1 or previous_cartT.y == -1 and next_cartT.x == 1:
                        screenT.blit(self.body_trT, cart_rectT)
                    elif previous_cartT.x == 1 and next_cartT.y == 1 or previous_cartT.y == 1 and next_cartT.x == 1:
                        screenT.blit(self.body_brT, cart_rectT)

    def update_head_graphicsT(self):
        head_directionT = self.bodyT[1] - self.bodyT[0]
        if head_directionT == Vector2(1,0): self.headT = self.head_leftT
        elif head_directionT == Vector2(-1,0): self.headT = self.head_rightT
        elif head_directionT == Vector2(0,1): self.headT = self.head_upT
        elif head_directionT == Vector2(0,-1): self.headT = self.head_downT

    def update_tail_graphicsT(self):
        tail_directionT = self.bodyT[-2] - self.bodyT[-1]
        if tail_directionT == Vector2(1,0): self.tailT = self.tail_leftT
        elif tail_directionT == Vector2(-1,0): self.tailT = self.tail_rightT
        elif tail_directionT == Vector2(0,1): self.tailT = self.tail_upT
        elif tail_directionT == Vector2(0,-1): self.tailT = self.tail_downT

    def move_steam(self):
        if self.new_cartT == True:
            body_copyT = self.bodyT[:]
            body_copyT.insert(0,body_copyT[0] + self.directionT)
            self.bodyT = body_copyT[:]
            self.new_cartT = False
        else:
            body_copyT = self.bodyT[:-1]
            body_copyT.insert(0,body_copyT[0] + self.directionT)
            self.bodyT = body_copyT[:]

    def add_cartT(self):
        self.new_cartT = True     

    def play_train_soundT(self):
        self.train_soundT.play()

    def resetT(self):
        self.bodyT = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.directionT = Vector2(1,0)

class PASSENGERT:
    def __init__(self):
        self.randomizeT()

    def draw_passengerT(self):
        passenger_rect = pygame.Rect(int(self.posT.x * cell_sizeT),int (self.posT.y * cell_sizeT),cell_sizeT, cell_sizeT)
        screenT.blit(passengerT, passenger_rect)

    def randomizeT(self):
        self.xT = random.randint(0, cell_numberT - 1)
        self.yT = random.randint(0, cell_numberT - 1)
        self.posT = Vector2(self.xT, self.yT)

class MAIN:
    def __init__(self):
        self.steam = STEAM()
        self.passengerT = PASSENGERT()

    def updateT(self):
        self.steam.move_steam()
        self.collisionT()
        self.fail_collisionT()

    def draw_elementsT(self):
        self.grass_backgroundT()
        self.passengerT.draw_passengerT()
        self.steam.draw_steam()
        self.scoreT()

    def collisionT(self):
        if self.passengerT.posT == self.steam.bodyT[0]:
            self.passengerT.randomizeT()
            self.steam.add_cartT()
            self.steam.play_train_soundT()

        for cartT in self.steam.bodyT[1:]:
            if cartT == self.passengerT.posT:
                self.passengerT.randomizeT()
    
    def fail_collisionT(self):
        if not 0 <= self.steam.bodyT[0].x < cell_numberT or not 0 <= self.steam.bodyT[0].y < cell_numberT:
            pygame.mixer.music.stop()
            self.game_overT()

        for cartT in self.steam.bodyT[1:]:
            if cartT == self.steam.bodyT[0]:
                pygame.mixer.music.stop()
                self.game_overT()

    def grass_backgroundT(self):
        NewTracksT = pygame.image.load('SteamTracks.png').convert()
        screen.blit(NewTracksT, (0,0))

    def scoreT(self):
        score_textT = str(len(self.steam.bodyT) - 3)
        score_surfaceT = game_fontT.render(score_textT, False, (56,74,12))
        score_xT = int(cell_sizeT * cell_numberT - 60)
        score_yT = int(cell_sizeT * cell_numberT - 40)
        score_rectT = score_surfaceT.get_rect(center = (score_xT, score_yT))
        passenger_rectT = passengerT.get_rect(midright = (score_rectT.left, score_rectT.centery))
        bg_rectT = pygame.Rect(passenger_rectT.left - 2, passenger_rectT.top - 2, passenger_rectT.width + score_rectT.width + 6, passenger_rectT.height + 10)

        pygame.draw.rect(screenT, (164, 209, 61), bg_rectT)
        screenT.blit(score_surfaceT, score_rectT)
        screenT.blit(passengerT, passenger_rectT)
        pygame.draw.rect(screenT, (56,74,12), bg_rectT, 2)

    def game_overT(self):
        score_text_2T = str(len(self.steam.bodyT)-3)
        Game_over_imageT = pygame.image.load('GameOver.png').convert()
        sampleT = pygame.mixer.music.load('GameOverMusic.wav')
        pygame.mixer.music.play(-1, 0.0)
        pygame.mixer.music.set_volume(0.5)

        while True:
            game_over_textT = game_over_fontT.render("GAME OVER", True, (200,200,200))
            game_score_textT = game_score_fontT.render(f"SCORE: {score_text_2T}", True, (200,200,200))
            play_again_textT = play_again_fontT.render("CLICK ON SCREEN TO PLAY AGAIN", True, (200,200,200))
            back_button_textT = back_button_fontT.render("PRESS [M] FOR MAIN MENU", True, (200,200,200))
            back_button_text2T = back_button_fontT.render("PRESS [D] TO CHANGE DIFFICULTY", True, (200,200,200))
            screen.blit(Game_over_imageT,(0,0))
            screenT.blit(game_over_textT,(35,-27))
            screenT.blit(game_score_textT,(240,175))
            screenT.blit(play_again_textT,(25,340))
            screenT.blit(back_button_textT,(135, 600))
            screenT.blit(back_button_text2T,(135, 700))

            self.steam.resetT()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.mixer.music.stop()
                    SteamGame()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_m:
                        main_menu()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_d:
                        difficulty_select()
            pygame.display.update()
        



pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
cell_sizeT = 40
cell_numberT = 20
screenT = pygame.display.set_mode((cell_numberT * cell_sizeT, cell_numberT * cell_sizeT),pygame.SCALED|HWSURFACE|DOUBLEBUF|RESIZABLE)
clockT = pygame.time.Clock()
passengerT = pygame.image.load('Passengers/passengerS.png').convert_alpha()
trackT = pygame.image.load('SteamTracks.png').convert_alpha()
game_fontT = pygame.font.Font('Pixeled.ttf', 25)
game_over_fontT = pygame.font.Font('Pixeled.ttf', 84)
game_score_fontT = pygame.font.Font('Pixeled.ttf', 44)
play_again_fontT = pygame.font.Font('Pixeled.ttf', 30)
back_button_fontT = pygame.font.Font('Pixeled.ttf', 23)
SCREEN_UPDATET = pygame.USEREVENT

main_gameT = MAIN()

def SteamGame():
    
    pygame.time.set_timer(SCREEN_UPDATET, 150) 

    SteamBGM = pygame.mixer.music.load('SteamMusic.wav')
    pygame.mixer.music.play(-1, 0.0)
    pygame.mixer.music.set_volume(0.2)

    while True:
        GAME_MOUSE_POST = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATET:
                main_gameT.updateT()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if main_gameT.steam.directionT.y != 1:
                        main_gameT.steam.directionT = Vector2(0,-1)
                if event.key == pygame.K_DOWN:
                    if main_gameT.steam.directionT.y != -1:
                        main_gameT.steam.directionT = Vector2(0,1)
                if event.key == pygame.K_RIGHT:
                    if main_gameT.steam.directionT.x != -1:
                        main_gameT.steam.directionT = Vector2(1,0)
                if event.key == pygame.K_LEFT:
                    if main_gameT.steam.directionT.x != 1:
                        main_gameT.steam.directionT = Vector2(-1,0)


        screenT.fill((175,215,70))
        main_gameT.draw_elementsT()
        pygame.display.update()
        clockT.tick(60)


def difficulty_select():
    Difficulty_music = pygame.mixer.music.load('DifficultySelectMusic.wav')
    pygame.mixer.music.play(-1, 0.0)
    pygame.mixer.music.set_volume(0.4)

    Difficulty_image = pygame.image.load('Difficulty.png').convert()
    screen.blit(Difficulty_image,(0,0))
    
    while True:
        
        DIFFICULTY_SELECT_MOUSE_POS = pygame.mouse.get_pos()

        #SCREEN.fill("Gray")

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
        TAIPAN_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(200, 250), 
                            text_input="TAIPAN", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        STEAM_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(200, 400), 
                            text_input="TITANOBOA", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        BULLET_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(200, 550), 
                            text_input="BLACKMAMBA", font=get_font(36), base_color="#d7fcd4", hovering_color="White")

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
                    pygame.mixer.music.stop()
                    TaipanGame()
                if STEAM_BUTTON.checkForInput(DIFFICULTY_SELECT_MOUSE_POS):
                    pygame.mixer.music.stop()
                    SteamGame()
                if BULLET_BUTTON.checkForInput(DIFFICULTY_SELECT_MOUSE_POS):
                    pygame.mixer.music.stop()
                    BulletGame()
        pygame.display.update()
        
def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        options_image = pygame.image.load('OptionsImage.png').convert()
        screen.blit(options_image,(0,0))

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
                    pygame.mixer.music.stop()
                    difficulty_select()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()
