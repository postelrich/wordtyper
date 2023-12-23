import itertools
import math
import pathlib
import random
import time
from io import BytesIO

import pygame
import pygame.locals
from gtts import gTTS
from mutagen.mp3 import MP3


# pygame setup
pygame.init()
pygame.mixer.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
GAME_FONT = pygame.freetype.SysFont(pygame.font.get_default_font(), 42)


def load_words(level):
    path = pathlib.Path(__file__).parent.joinpath('data', f'{level}.txt')
    with open(path) as f:
        return [w.strip() for w in f.readlines()]


_LEVEL_WORDS = load_words('kindergarten')


def random_word():
    random.shuffle(_LEVEL_WORDS)
    for w in itertools.cycle(_LEVEL_WORDS):
        yield w


WORDS = random_word()


def speak(text, language='en'):
    mp3_fo = BytesIO()
    tts = gTTS(text, lang=language, tld='com.au', slow=True)
    tts.write_to_fp(mp3_fo)
    mp3_fo.seek(0)
    audio = MP3(mp3_fo)
    length = audio.info.length
    mp3_fo.seek(0)
    pygame.mixer.music.load(mp3_fo, 'mp3')
    pygame.mixer.music.play()
    time.sleep(length)


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
    def __init__(self, word=None, font_size=60, char_height=80, char_width=70):
        self.word = word
        self.word_pos = 0
        self.font_size = font_size
        self.char_height = char_height
        self.char_width = char_width

    def need_word(self):
        return self.word is None or len(self.word) == self.word_pos

    def set_word(self, w):
        self.word = w
        self.word_pos = 0

    def get_char_color(self, char_pos, completed=False):
        if char_pos < self.word_pos or completed:
            return "green"
        elif char_pos == self.word_pos:
            return "blue"
        else:
            return "gray"

    def draw(self, screen, completed=False):
        all_sprites_list = pygame.sprite.Group() 
        word_mid = int(len(self.word) / 2)
        for i, c in enumerate(self.word):
            t = Text(c.upper(), self.font_size, self.get_char_color(i, completed=completed), self.char_width, self.char_height)
            x_multiplier = i - word_mid
            t.rect.x = (screen.get_width() / 2) + (self.char_width * x_multiplier + x_multiplier * 20)
            t.rect.y = (screen.get_height() / 2) - (self.char_height / 2)
            all_sprites_list.add(t) 
        all_sprites_list.draw(screen)

    def handle_keypress(self, e):
        if e.unicode == self.word[self.word_pos]:
            self.word_pos += 1

    def speak_word(self):
        speak(f"{' '.join(self.word)} spells {self.word}")


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
    screen.fill("grey13")

    # speak word on completion and get next word
    if word.need_word():
        if word.word is not None:
            word.draw(screen, completed=True)
            pygame.display.flip()
            word.speak_word()
        word.set_word(next(WORDS))

    # draw word
    word.draw(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
