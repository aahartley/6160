import pygame
from scripts.utils import load_image, load_images, sprite_frame_dict, load_sprite_sheet

#index 0 = idle_bow, index 1 = walk_forward_bow, index 2 = attack_bow, index 3 = death_bow
class Animation:
    def __init__(self, player_path, player_shadow_path, frame_set, fps, scale, factor):
        self.player_path = player_path
        self.player_shadow_path = player_shadow_path
        self.fps = fps
        self.frame_time = 1/fps
        self.time = 0
        self.sheets = load_sprite_sheet(player_path, scale, factor)
        self.shadow_sheets = load_sprite_sheet(player_shadow_path, scale, factor)
        self.frame_set = frame_set
        self.frame = 0
        self.active_sheet = self.sheets[0]
        self.active_sheet.set_clip(pygame.Rect(self.frame_set[0]))
        self.active_shadow_sheet = self.shadow_sheets[0]
        self.active_shadow_sheet.set_clip(pygame.Rect(self.frame_set[0]))
        self.loop = False
        self.active = True

    def angle_distance(self, a, b):
            return min(abs(a - b), 360 - abs(a - b))

    def closest_angle_to_target(self, available_angles, target_angle):
        target_angle = target_angle % 360
        return min(available_angles, key=lambda x: self.angle_distance(x, target_angle))

    def update(self, dt, angle):
        self.time += dt
        available_angles = list(self.sheets.keys())
        closest_angle = self.closest_angle_to_target(available_angles, angle)
        #print(closest_angle)
        self.active_sheet = self.sheets[closest_angle]
        self.active_shadow_sheet = self.shadow_sheets[closest_angle]
        frame_in_frame_set = self.get_frame()
        self.active_sheet.set_clip(pygame.Rect(frame_in_frame_set))


    def get_frame(self):
        if(self.time >= self.frame_time and self.active ):
            if self.frame+1 > (len(self.frame_set) - 1):
                self.frame = 0
            else:
                self.frame += 1
                self.time = 0
                if(self.frame == len(self.frame_set)-1):
                    self.loop = True
        elif(not self.active):
            self.frame = len(self.frame_set)-1
        return self.frame_set[self.frame]

    def get_current_frames(self):
        return self.active_sheet.subsurface(self.active_sheet.get_clip()).convert_alpha(), self.active_shadow_sheet.subsurface(self.active_sheet.get_clip()).convert_alpha()

    def check_loop(self):
        return self.loop
        
    def reset(self):
        self.frame = 0
        self.time = 0
        self.loop = False
        self.active = True


    def copy(self):
        copied_animation = Animation.__new__(Animation) 
        
        copied_animation.sheets = self.sheets  
        copied_animation.shadow_sheets = self.shadow_sheets  
        copied_animation.frame_set = self.frame_set
        copied_animation.frame_time = self.frame_time
        copied_animation.time = self.time
        copied_animation.frame = self.frame
        copied_animation.active_sheet = self.active_sheet  
        copied_animation.active_shadow_sheet = self.active_shadow_sheet  
        copied_animation.loop = self.loop
        copied_animation.active = self.active
        
        return copied_animation
