import pygame
import game_element as game
import menu_element as menu
import csv
from csv import DictReader

pygame.init()
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

def init_song_selection():
    with open("Song Directory.csv", 'r') as f:
        song_reader = DictReader(f)
        song_list = list(song_reader)

    thumbnail_list = []
    for i in range(len(song_list)):
        thumbnail_list.append(menu.Thumbnail(i ,song_list[i]))

    scroller = menu.Scroller(thumbnail_list)
    return scroller

def song_selection(scroller):
    while True:
        time = (pygame.mixer.music.get_pos()/1000)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    scroller.scroll_left()
                if event.key == pygame.K_RIGHT:
                    scroller.scroll_right()
                if event.key == pygame.K_RETURN:
                    fade(1)
                    main(scroller.selection)
                    
                    
        scroller.update()
        screen.fill("black")
        scroller.draw(screen)
        pygame.display.flip()
        clock.tick(60)  # limits FPS to 60

def main(song):
    with open(song.beat_path, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
        data = data[1:]
    beat = 0
    flyin_time = 2.5 

    pygame.init()
    pygame.mixer.init() 
    pygame.font.init()
    font_s = pygame.font.Font("game_image/Retro Gaming.ttf", 35)
    font_m = pygame.font.Font("game_image/Retro Gaming.ttf", 50)
    font_xl = pygame.font.Font("game_image/Retro Gaming.ttf", 90)

    screen = pygame.display.set_mode((1280,720))
    cover = pygame.Surface((screen_width, screen_height))
    cover.fill((0,0,0))
    cover_alpha = 300

    clock = pygame.time.Clock()

    left_img = pygame.image.load("game_image\\left_s.png").convert_alpha()
    down_img = pygame.image.load("game_image\\down_s.png").convert_alpha()
    up_img = pygame.image.load("game_image\\up_s.png").convert_alpha()
    right_img = pygame.image.load("game_image\\right_s.png").convert_alpha()
    filter_img = pygame.image.load("game_image\\filter.png").convert_alpha()

    combo_text_h = font_m.render("Combo", True, (255, 255, 255))
    perfect_text_h = font_s.render("Perfect", True, (255, 255, 255))
    great_text_h = font_s.render("Great", True, (255, 255, 255))
    good_text_h = font_s.render("Good", True, (255, 255, 255))
    miss_text_h = font_s.render("Miss", True, (255, 255, 255))

    manager = game.Gamemanager()
    pygame.mixer.music.load(song.song_path) 
    pygame.mixer.music.set_volume(0.7) 
    pygame.mixer.music.play() 

    while True:
        # Process player inputs.
        time = (pygame.mixer.music.get_pos()/1000)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    manager.keypress(1, time)
                if event.key == pygame.K_DOWN:
                    manager.keypress(2, time)
                if event.key == pygame.K_UP:
                    manager.keypress(3, time)
                if event.key == pygame.K_RIGHT:
                    manager.keypress(4, time)
                if event.key == pygame.K_RETURN:
                    pygame.mixer.music.fadeout(700) 
                    fade(5)
                    if (manager.perfect+manager.great+manager.good+manager.miss) == 0:
                        song_selection(scroller)
                    else:
                        score(manager.perfect, manager.great, manager.good, manager.miss, manager.score, manager.max_combo)

        
        press_time = float(data[beat][0])
        if time+flyin_time >= press_time:
            if beat < len(data)-1:
                for i in range(1,5):
                    if int(data[beat][i]) != 0:
                        a = game.Arrow(i, flyin_time, press_time)
                        manager.game_objects.append(a)
                        manager.check_objects.append(a)
                beat += 1

        # Do logical updates here.
        for obj in manager.game_objects:
            obj.update(time, manager.check_miss, manager.popups)

        for obj in manager.popups:
            obj.update()

        manager.update()
        combo_text = font_xl.render(str(manager.combo), True, (255, 255, 255))
        perfect_text = font_s.render(str(manager.perfect), True, (255, 255, 255))
        great_text = font_s.render(str(manager.great), True, (255, 255, 255))
        good_text = font_s.render(str(manager.good), True, (255, 255, 255))
        miss_text = font_s.render(str(manager.miss), True, (255, 255, 255))

        screen.fill("black")
        screen.blit(filter_img, (0, 0))
        for obj in manager.game_objects:
            obj.draw(screen, time)

        screen.blit(left_img, (340, 20))
        screen.blit(down_img, (490, 20))
        screen.blit(up_img, (640, 20))
        screen.blit(right_img, (790, 20))
        screen.blit(combo_text_h, (70,150))
        screen.blit(combo_text, (170-combo_text.get_width()/2,210))

        screen.blit(perfect_text_h, (1040,150))
        screen.blit(perfect_text, (1210-perfect_text.get_width(),200))
        screen.blit(great_text_h, (1090,290))
        screen.blit(great_text, (1210-great_text.get_width(),340))
        screen.blit(good_text_h, (1100,430))
        screen.blit(good_text, (1210-good_text.get_width(),480))
        screen.blit(miss_text_h, (1120,570))
        screen.blit(miss_text, (1210-miss_text.get_width(),620))

        if pygame.mixer.music.get_busy() == False:
            fade(5)
            score(manager.perfect, manager.great, manager.good, manager.miss, manager.score, manager.max_combo)
        
        if cover_alpha > 0:
            cover_alpha -= 1    
        cover.set_alpha(cover_alpha)
        screen.blit(cover, (0,0))

        if cover_alpha > 230:
            screen.blit(song.text, (640-song.text.get_width()/2, 300))


        for pop in manager.popups:
            pop.draw(screen)
        pygame.display.flip()  # Refresh on-screen display
        clock.tick(60)         # wait until next frame (at 60 FPS)

def fade(delay):
    cover = pygame.Surface((screen_width, screen_height))
    cover.fill((0,0,0))
    for alpha in range(0, 150):
        cover.set_alpha(alpha)
        screen.blit(cover, (0,0))
        pygame.display.update()
        pygame.time.delay(delay)

def score(perfect, great, good, miss, score, max_combo):
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    score_board = menu.Score_board(perfect, great, good, miss, score, max_combo)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: 
                    fade(5)
                    song_selection(scroller)


        screen.fill("black")
        score_board.update()
        score_board.draw(screen)
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

scroller = init_song_selection()
song_selection(scroller)