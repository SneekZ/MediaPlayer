import pygame
from C import *
import sys
from V import *


class Camera(object):
    global lvl

    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l+WIN_WIDTH / 2, -t+WIN_HEIGHT / 2

    l = min(0, l)
    l = max(-(camera.width-WIN_WIDTH), l)
    t = max(-(camera.height-WIN_HEIGHT), t)
    t = min(0, t)
    return Rect(l, t, w, h) 


def loadLevel(lv):
    global playerX, playerY

    levelFile = open(f'%s/levels/{lv}.txt' % FILE_DIR)
    line = " "
    commands = []
    while line[0] != "/":
        line = levelFile.readline()
        if line[0] == "[":
            while line[0] != "]":
                line = levelFile.readline()
                if line[0] != "]":
                    endLine = line.find("|")
                    level.append(line[0: endLine])
                    
        if line[0] != "":
         commands = line.split()
         if len(commands) > 1:
            if commands[0] == "player":
                playerX = int(commands[1])
                playerY = int(commands[2])


def main():
    lvl = input()
    try:
        loadLevel(lvl)
    except Exception as e:
        print('Такого файла не сущствует')
        print('Запускается уровнь по умолчанию...')
        loadLevel(1)

    pygame.init()
    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption("Mario")
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))
    bg.fill(Color(BACKGROUND_COLOR))
        
    left = right = False
    up = False
    running = False
     
    hero = Player(playerX,playerY)
    entities.add(hero)
           
    timer = pygame.time.Clock()
    x = y = 0
    f = pygame.font.Font(None, 36)
    cash = f.render(f'Score: {hero.score} ', 1, (0, 255, 0))
    health = f.render(f'HP: {hero.hp} ', 1, (255, 0, 0))

    for row in level:
        for col in row:
            if col == "-":
                pf = Platform(x,y)
                entities.add(pf)
                platforms.append(pf)
            if col == "*":
                bd = BlockDie(x,y)
                entities.add(bd)
                platforms.append(bd)
            if col == "P":
                pr = Princess(x,y)
                entities.add(pr)
                platforms.append(pr)
                animatedEntities.add(pr)
            if col == 'M':
                m = Money(x, y)
                entities.add(m)
                platforms.append(m)
                animatedEntities.add(m)
   
            x += PLATFORM_WIDTH
        y += PLATFORM_HEIGHT
        x = 0
    
    total_level_width  = len(level[0])*PLATFORM_WIDTH
    total_level_height = len(level)*PLATFORM_HEIGHT
    
    camera = Camera(camera_configure, total_level_width, total_level_height) 
    
    while not hero.winner:
        timer.tick(60)
        for e in pygame.event.get():
            if e.type == QUIT:
                sys.exit()
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYDOWN and e.key == K_LSHIFT:
                running = True

            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
            if e.type == KEYUP and e.key == K_LSHIFT:
                running = False
        if hero.hp == 0:
            screen.blit(gameover, (0, 0))
            pygame.display.update()
            pygame.time.delay(3000)
            pygame.quit()

        screen.blit(bg, (0, 0))

        animatedEntities.update()
        camera.update(hero)
        hero.update(left, right, up, running, platforms)
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        cash = f.render(f'Score: {hero.score} ', 1, (0, 0, 255))
        health = f.render(f'HP: {hero.hp} ', 1, (0, 255, 0))
        screen.blit(cash, (100, 10))
        screen.blit(health, (10, 10))
        pygame.display.update()
    screen.fill((0, 0, 0))
    screen.blit(winimg, (0, 0))
    pygame.display.update()
    pygame.time.delay(3000)


level = []
entities = pygame.sprite.Group()
animatedEntities = pygame.sprite.Group()
platforms = []
if __name__ == "__main__":
    main()
