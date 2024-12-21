import pygame

class Arrow:
    def __init__(self, direction, flyin_time, press_time):
        self.press_time = press_time
        self.direction = direction
        self.x = self.position_image()[0]
        self.y = 720
        self.aura_x = self.x-25
        self.aura_y = -5
        self.time = flyin_time*60
        self.v = (self.y-20)/self.time
        self.img_path = self.position_image()[1]
        self.img = pygame.image.load(self.img_path).convert_alpha()
        self.aura_img_path = "game_image\\aura.png"
        self.aura_img = pygame.image.load(self.aura_img_path).convert_alpha()
        self.is_alive = True
        self.for_check = True
        self.miss = False
        

    def position_image(self):
        if self.direction == 1:
            x = 340
            image_path = "game_image\\left.png"
        elif self.direction == 2:
            x = 490
            image_path = "game_image\\down.png"
        elif self.direction == 3:
            x = 640
            image_path = "game_image\\up.png"
        elif self.direction ==4:
            x = 790
            image_path = "game_image\\right.png"

        return (x, image_path)
        
    

    def update(self, time, miss_list, popup_list):
        self.y -= self.v
        if time - self.press_time > 0.2:
            self.for_check = False
            if self.miss == False:
                miss_list += [1]
                self.miss = True
                popup_list.append(Popup(self.direction, 4))

        if self.y < -150-5:
            self.is_alive = False
        

    def draw(self, screen, time):
        screen.blit(self.img, (self.x, self.y))
        if abs(self.press_time - time) <= 0.2:
            screen.blit(self.aura_img, (self.aura_x, self.aura_y))


class Gamemanager:
    def __init__(self):
        self.game_objects = []
        self.check_objects = []
        self.popups = []
        self.check_miss = []
        self.combo_list = []
        self.combo = 0
        self.score = 0
        self.miss = 0
        self.perfect = 0
        self.great = 0
        self.good = 0
        self.reset_combo = False
        self.max_combo = 0
    
    def keypress(self, key, time):
        
        if len(self.check_objects) >= 1:
            lag_time = abs(self.check_objects[0].press_time - time)
            if (key == self.check_objects[0].direction) and lag_time <= 0.2:
                self.check_objects[0].for_check = False
                self.check_objects[0].is_alive = False
                if lag_time <= 0.1:
                    self.perfect += 1
                    self.score += 30 + 5*self.combo
                    self.combo += 1
                    self.popups.append(Popup(key, 1))
                elif lag_time <= 0.15:
                    self.great += 1
                    self.score += 20 + 4*self.combo
                    self.combo += 1
                    self.popups.append(Popup(key, 2))
                else:
                    self.good += 1
                    self.score += 10 + 3*self.combo
                    self.combo += 1
                    self.popups.append(Popup(key, 3))
                self.reset_combo = False
            else:
                self.reset_combo = True

            if len(self.check_objects) >= 2 and self.reset_combo == True:
                lag_time = abs(self.check_objects[1].press_time - time)
                if key == self.check_objects[1].direction:
                    if lag_time <= 0.2:
                        self.reset_combo = False
                        self.check_objects[1].for_check = False
                        self.check_objects[1].is_alive = False
                        if lag_time <= 0.1:
                            self.perfect += 1
                            self.score += 30 + 5*self.combo
                            self.combo += 1
                            self.popups.append(Popup(key, 1))
                        elif lag_time <= 0.15:
                            self.great += 1
                            self.score += 20 + 4*self.combo
                            self.combo += 1
                            self.popups.append(Popup(key, 2))
                        else:
                            self.good += 1
                            self.score += 10 + 3*self.combo
                            self.combo += 1
                            self.popups.append(Popup(key, 3))
                    else:
                        self.reset_combo = True

        if self.combo > self.max_combo:
                self.max_combo = self.combo

        if self.reset_combo == True:
            self.combo = 0
        
    def update(self):
        miss = self.miss
        self.check_objects = [obj for obj in self.check_objects if obj.for_check == True]
        self.game_objects = [obj for obj in self.game_objects if obj.is_alive == True]
        self.popups = [obj for obj in self.popups if obj.is_alive == True]
        self.miss = len(self.check_miss)
        if self.miss > miss:
            self.combo = 0

class Popup:
    def __init__(self, direction, sign):
        self.direction = direction
        self.sign = sign
        self.is_alive = True
        self.disp_time = 8
        self.x = self.position()
        self.y = 20
        self.img_path = self.image()
        self.img = pygame.image.load(self.img_path).convert_alpha()
    
    def position(self):
        if self.direction == 1:
            x = 340
        elif self.direction == 2:
            x = 490
        elif self.direction == 3:
            x = 640
        elif self.direction == 4:
            x = 790
        return x
    
    def image(self):
        if self.sign == 1:
            path = "game_image\\perfect.png"
        elif self.sign == 2:
            path = "game_image\\great.png"
        elif self.sign == 3:
            path = "game_image\\good.png"
        elif self.sign == 4:
            path = "game_image\\miss.png"
        return path 

    def update(self):
        self.disp_time -= 1
        if self.disp_time <= 0:
            self.is_alive = False
    
    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))