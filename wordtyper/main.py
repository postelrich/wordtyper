import random

import pygame
import pygame.locals

# pygame setup
pygame.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
GAME_FONT = pygame.freetype.SysFont(pygame.font.get_default_font(), 42)


def random_word():
    words = ['hi', 'top', 'bed', 'hair', 'boy', 'girl', 'eye']
    return random.choice(words)


class Text(pygame.sprite.Sprite):
    def __init__(self, text, size, color, width, height):
        # Call the parent class (Sprite) constructor  
        pygame.sprite.Sprite.__init__(self)
    
        self.font = pygame.font.SysFont("Arial", size)
        self.textSurf = self.font.render(text, 1, color)
        self.image = pygame.Surface((width, height))
        self.width = width
        self.height = height
        W = self.textSurf.get_width()
        H = self.textSurf.get_height()
        self.rect = self.image.get_rect()
        self.image.blit(self.textSurf, [self.width/2 - W/2, self.height/2 - H/2])


class Word:
    def __init__(self, word=None):
        self.word = word
        self.word_pos = 0

    def need_word(self):
        return self.word is None or len(self.word) == self.word_pos

    def set_word(self, w):
        self.word = w
        self.word_pos = 0

    def get_char_color(self, char_pos):
        if char_pos == self.word_pos:
            return "blue"
        elif char_pos < self.word_pos:
            return "green"
        else:
            return "gray"

    def draw(self, screen):
        all_sprites_list = pygame.sprite.Group() 
        for i, c in enumerate(self.word):
            t = Text(c.upper(), 30, self.get_char_color(i), 50, 50)
            t.rect.x = 50 * i
            all_sprites_list.add(t) 
        all_sprites_list.draw(screen)

    def handle_keypress(self, e):
        if e.unicode == self.word[self.word_pos]:
            self.word_pos += 1


word = Word()


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            word.handle_keypress(event)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # RENDER YOUR GAME HERE
    if word.need_word():
        word.set_word(random_word())
    keys = pygame.key.get_pressed()
    word.draw(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()