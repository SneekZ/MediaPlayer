import os
import pygame
WIN_WIDTH = 800
WIN_HEIGHT = 640
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BACKGROUND_COLOR = "#000000"

FILE_DIR = os.path.dirname(__file__)

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#000000"
ICON_DIR = os.path.dirname(__file__)

ANIMATION_BLOCKTELEPORT = [
    ('%s/data/portal2.png' % ICON_DIR),
    ('%s/data/portal1.png' % ICON_DIR)]

ANIMATION_PRINCESS = [
    ('%s/data/princess_l.png' % ICON_DIR),
    ('%s/data/princess_r.png' % ICON_DIR)]



MOVE_SPEED = 7
MOVE_EXTRA_SPEED = 2.5
WIDTH = 22
HEIGHT = 32
COLOR =  "#888888"
JUMP_POWER = 10
JUMP_EXTRA_POWER = 1
GRAVITY = 0.35
ANIMATION_DELAY = 0.1
ANIMATION_SUPER_SPEED_DELAY = 0.05
ICON_DIR = os.path.dirname(__file__)

ANIMATION_RIGHT = [('%s/data/r1.png' % ICON_DIR),
            ('%s/data/r2.png' % ICON_DIR),
            ('%s/data/r3.png' % ICON_DIR),
            ('%s/data/r4.png' % ICON_DIR),
            ('%s/data/r5.png' % ICON_DIR)]
ANIMATION_LEFT = [('%s/data/l1.png' % ICON_DIR),
            ('%s/data/l2.png' % ICON_DIR),
            ('%s/data/l3.png' % ICON_DIR),
            ('%s/data/l4.png' % ICON_DIR),
            ('%s/data/l5.png' % ICON_DIR)]
ANIMATION_JUMP_LEFT = [('%s/data/jl.png' % ICON_DIR, 0.1)]
ANIMATION_JUMP_RIGHT = [('%s/data/jr.png' % ICON_DIR, 0.1)]
ANIMATION_JUMP = [('%s/data/j.png' % ICON_DIR, 0.1)]
ANIMATION_STAY = [('%s/data/0.png' % ICON_DIR, 0.1)]

lvl = 1

winimg = pygame.image.load('data//win.jpg')
rub = pygame.image.load('data//money.png')
gameover = pygame.image.load('data//gameover.png')