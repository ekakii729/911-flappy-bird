import pygame
import random

screen: pygame.Surface
clock: pygame.time.Clock
background_song: pygame.mixer.Sound
font: pygame.font.Font
white: pygame.Color
screen_height: int
screen_width: int


class Plane:

    def __init__(self):
        self.x_position = 100
        self.y_position = screen_height / 2
        self.image_size = (151, 53)  # aspect ratio of the image
        self.image = pygame.transform.scale(pygame.image.load('images/plane.png'), self.image_size)
        self.velocity_down = -5
        self.velocity_up = 0

    def update(self):
        if self.velocity_up != 0:
            self.velocity_up -= 1
        self.velocity_down *= 1.04  # plane accelerates as it falls
        self.y_position -= (self.velocity_up + self.velocity_down)

    def jump(self):
        self.velocity_down = -5
        self.velocity_up = 20

    def draw(self):
        self.update()
        screen.blit(self.image, (self.x_position, self.y_position))

    def get_rect(self):
        return pygame.Rect(self.x_position, self.y_position, self.image_size[0], self.image_size[1])


class Towers:

    def __init__(self):
        self.x_position = screen_width + 1
        self.top_tower_y_position = -50
        self.top_tower = pygame.transform.flip(pygame.image.load('images/tower.png').convert_alpha(), 0, 1)
        self.bottom_tower = pygame.image.load('images/tower.png').convert_alpha()
        self.height = 425
        self.gap = 175

    def set_top_tower_y_position(self):
        self.top_tower_y_position = random.randint(-400, -50)

    def move(self):
        if self.x_position < -50:
            self.x_position = screen_width + 50
            self.set_top_tower_y_position()
        self.x_position -= 10

    def draw(self):
        screen.blit(self.top_tower, (self.x_position, self.top_tower_y_position))
        screen.blit(self.bottom_tower, (self.x_position, self.top_tower_y_position + self.gap + self.height))

    def get_top_tower_rect(self):
        return pygame.Rect(self.x_position, self.top_tower_y_position, self.top_tower.get_width(),
                           self.top_tower.get_height())

    def get_bottom_tower_rect(self):
        bottom_tower_y = self.top_tower_y_position + self.gap + self.height
        return pygame.Rect(self.x_position, bottom_tower_y, self.bottom_tower.get_width(),
                           self.bottom_tower.get_height())


def draw_background():
    screen.blit(pygame.image.load('images/background.png'), (0, 0))


def init():
    global screen_height, screen_width, screen, clock, background_song, font, white
    pygame.init()
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    background_song = pygame.mixer.Sound("sounds/background_music.mp3")
    font = pygame.font.SysFont("Comic Sans MS", 50)
    white = (255, 255, 255)
    pygame.display.set_caption('911 Flappy Bird')
    # pygame.mixer.Sound.play(background_song, -1)
    draw_background()


def start_screen():
    button = pygame.Rect(290, 255, 200, 70)  # centers the button
    title = font.render('911 Flappy Bird', True, white)
    button_text = font.render('Start', True, white)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button.collidepoint(event.pos):
                    return True
        pygame.draw.rect(screen, (0, 0, 200), button)  # button is blue
        screen.blit(title, (225, 100))  # draws title in center
        screen.blit(button_text, (320, 250))  # draws text in button
        pygame.display.flip()


def run():
    plane = Plane()
    towers = Towers()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_SPACE]:
            plane.jump()
        draw_background()
        plane_rect = plane.get_rect()
        tower_rects = [towers.get_top_tower_rect(), towers.get_bottom_tower_rect()]
        if plane_rect.collidelist(tower_rects) != -1:
            print('x')
        plane.draw()
        towers.draw()
        towers.move()
        pygame.display.flip()
        clock.tick(60)


def main():
    init()
    if start_screen():
        run()


if __name__ == '__main__':
    main()
