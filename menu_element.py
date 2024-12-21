import pygame
import math
pygame.font.init()
font_s = pygame.font.Font("game_image/Retro Gaming.ttf", 30)
font_m = pygame.font.Font("game_image/Retro Gaming.ttf", 60)
font_xl = pygame.font.Font("game_image/Retro Gaming.ttf", 120)

class Thumbnail:
    def __init__(self, index, song_dict):
        self.index = index
        self.img_show = True
        self.text_show = False
        self.size = self.get_size()
        self.des_size = self.get_size()
        self.pos = self.get_position()
        self.des_pos = self.get_position()
        
        self.text = font_s.render(song_dict["artist"]+" - "+song_dict["song"], True, (255, 255, 255))
        self.song_path = song_dict["song path"]
        self.beat_path = song_dict["beat path"]
        self.img_path = song_dict["img path"]

        self.img = pygame.image.load(song_dict["img path"])
        self.img_scaled = pygame.transform.scale(self.img, (self.size,self.size))

        
    def get_size(self):
        if self.index == 4:
            return 300
        else:
            return 200
            
    def get_position(self):
        if self.index == 4:
            return [1280/2-self.size/2, 280-self.size/2]
        elif self.index < 4:
            return [1280/2-320-280*(4-self.index-1)-self.size/2, 280-self.size/2]
        elif self.index > 4:
            return [1280/2+320+280*(self.index-4-1)-self.size/2, 280-self.size/2]
    
    def get_des_position(self):
        if self.index == 4:
            return [1280/2-self.des_size/2, 280-self.des_size/2]
        elif self.index < 4:
            return [1280/2-320-280*(4-self.index-1)-self.des_size/2, 280-self.des_size/2]
        elif self.index > 4:
            return [1280/2+320+280*(self.index-4-1)-self.des_size/2, 280-self.des_size/2]
    
    def scroll(self):
        self.des_size = self.get_size()
        self.des_pos = self.get_des_position()
        
    def update(self):
        v_x = 0.1 * (self.des_pos[0] - self.pos[0])
        v_y = 0.1 * (self.des_pos[1] - self.pos[1])

        v_z = 0.1 * (self.des_size - self.size)

        if abs(v_x) < 0.1:
            v_x = 0
        if abs(v_y) < 0.1:
            v_y = 0
        if abs(v_z) < 0.1:
            v_z = 0
        
        if self.index == 4 and abs(v_x) < 10:
            self.text_show = True
        else:
            self.text_show = False

        if self.index == 0:
            self.img_show = False
        elif self.index > 7:
            self.img_show = False
        else:
            self.img_show = True
        
        self.pos[0] += v_x
        self.pos[1] += v_y
        self.size += v_z
        self.img_scaled = pygame.transform.scale(self.img, (self.size,self.size))

    def draw(self, screen):
        if self.img_show == True:
            screen.blit(self.img_scaled, (self.pos[0], self.pos[1]))
        if self.text_show == True:
            screen.blit(self.text, (640-self.text.get_width()/2, 470))



class Scroller:
    def __init__(self, song_list):
        self.song_list = song_list
        self.len = len(song_list)
        self.selection = song_list[0]

    def scroll_left(self):
        # thinking of modifying the focussing index becuase of the computation cost and easy to change figure. 
        #However, that will be hard for transition. 
        for song in self.song_list:
            song.index += 1
            if song.index > self.len - 1:
                song.index = 0
            song.scroll()
            
    def scroll_right(self):
        # thinking of modifying the focussing index becuase of the computation cost and easy to change figure. 
        #However, that will be hard for transition. 
        for song in self.song_list:
            song.index -= 1
            if song.index < 0:
                song.index = self.len - 1
            song.scroll()

    def update(self):
        for song in self.song_list:
            song.update()
            if song.index == 4:
                self.selection = song

    def draw(self, screen):
        for song in self.song_list:
            song.draw(screen)

# class Thumbnail_demo:
#     def __init__(self, index):
#         self.index = index
#         self.show = True
#         self.size = self.get_size()
#         self.des_size = self.get_size()
#         self.pos = self.get_position()
#         self.des_pos = self.get_position()
#         self.self = pygame.Rect(self.pos[0], self.pos[1], self.size, self.size)
        
#     def get_size(self):
#         if self.index == 4:
#             return 300
#         else:
#             return 200
            
#     def get_position(self):
#         if self.index == 4:
#             return [1280/2-self.size/2, 280-self.size/2]
#         elif self.index < 4:
#             return [1280/2-320-280*(4-self.index-1)-self.size/2, 280-self.size/2]
#         elif self.index > 4:
#             return [1280/2+320+280*(self.index-4-1)-self.size/2, 280-self.size/2]
    
#     def get_des_position(self):
#         if self.index == 4:
#             return [1280/2-self.des_size/2, 280-self.des_size/2]
#         elif self.index < 4:
#             return [1280/2-320-280*(4-self.index-1)-self.des_size/2, 280-self.des_size/2]
#         elif self.index > 4:
#             return [1280/2+320+280*(self.index-4-1)-self.des_size/2, 280-self.des_size/2]
    
#     def scroll(self):
#         self.des_size = self.get_size()
#         self.des_pos = self.get_des_position()
        
#     def update(self):
#         v_x = 0.1 * (self.des_pos[0] - self.pos[0])
#         v_y = 0.1 * (self.des_pos[1] - self.pos[1])

#         v_z = 0.1 * (self.des_size - self.size)

#         if abs(v_x) < 0.1:
#             v_x = 0
#         if abs(v_y) < 0.1:
#             v_y = 0
#         if abs(v_z) < 0.1:
#             v_z = 0

#         if self.index == 0:
#             self.show = False
#         elif self.index > 7:
#             self.show = False
#         else:
#             self.show = True
        
#         self.pos[0] += v_x
#         self.pos[1] += v_y
#         self.size += v_z
#         self.self = pygame.Rect(self.pos[0], self.pos[1], self.size, self.size)

#     def draw(self, screen):
#         if self.show == True:
#             pygame.draw.rect(screen, "White", self.self)

class Score_board:
    def __init__(self, perfect, great, good, miss, score, max_combo):
        self.total = perfect+great+good+miss
        self.perfect = 0
        self.great = 0
        self.good = 0
        self.des_perfect =  (perfect/self.total)*360
        self.des_great = ((perfect+great)/self.total)*360
        self.des_good = ((perfect+great+good)/self.total)*360
        self.rating = self.get_rating()
        self.rating_text = font_xl.render(self.rating, True, (255, 255, 255))
        self.score_texth = font_s.render("Score", True, (255, 255, 255))
        self.des_score = score
        self.score = 0
        self.score_text = font_m.render(str(self.score), True, (255, 255, 255))
        self.combo_texth = font_s.render("Max Combo", True, (255, 255, 255))
        self.des_combo = max_combo
        self.combo = 0
        self.combo_text = font_m.render(str(self.combo), True, (255, 255, 255))

    def get_rating(self):
        if self.perfect/360 > 0.90:
            return "S"
        elif self.perfect/360 > 0.80:
            return "A"
        elif self.perfect/360 > 0.70:
            return "B"
        elif self.perfect/360 > 0.60:
            return "C"
        else:
            return "D"

    def update(self):
    
        v_perfect = 0.03*(self.des_perfect-self.perfect)
        v_great = 0.03*(self.des_great-self.great)
        v_good = 0.03*(self.des_good-self.good)

        self.perfect += v_perfect
        self.great += v_great
        self.good += v_good

        if self.score < self.des_score:
            if math.floor((self.des_score-self.score)*0.04) > 1:
                self.score += math.floor((self.des_score-self.score)*0.04)
            else:
                self.score += 1
        
        if self.combo < self.des_combo:
            if math.floor((self.des_combo-self.combo)*0.04) > 1:
                self.combo += math.floor((self.des_combo-self.combo)*0.04)
            else:
                self.combo += 1

        self.rating = self.get_rating()
        self.rating_text = font_xl.render(self.rating, True, (255, 255, 255))
        self.score_text = font_m.render(str(self.score), True, (255, 255, 255))
        self.combo_text = font_m.render(str(self.combo), True, (255, 255, 255))

    def draw(self, screen):
        screen.blit(self.rating_text, (480-self.rating_text.get_width()/2, 360-self.rating_text.get_height()/2))
        screen.blit(self.score_texth, (750, 180))
        screen.blit(self.score_text, (750, 220))
        screen.blit(self.combo_texth, (750, 380))
        screen.blit(self.combo_text, (750, 420))
        for angle in range(0, 360, 4):
            if angle < self.perfect:
                color = (30,165,135)
            elif angle < self.great:
                color = (140, 195, 135)
            elif angle < self.good:
                color = (240, 240, 135)
            else:
                color = (200,0,0)
            for radius in range(140, 210, 15):
                pygame.draw.circle(screen, color, (480-radius*math.cos(math.radians(angle-90)), 360+radius*math.sin(math.radians(angle-90))), 4)
        
        
            

