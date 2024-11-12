import pygame



class Character(pygame.sprite.Sprite):
    
 
    def __init__(self, position):
    
        super().__init__()
        self.sheet = pygame.image.load('Spritesheets_IMGS/moo_deng_test5.png').convert_alpha()
        self.sheet.set_clip(pygame.Rect(0, 126, 77, 63)) #init with idle left
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = self.image.get_rect() 
        self.position = [position[0], position[1]]
        self.rect.topleft = position
        self.frame = 0
        self.rectWidth = 122.25
        self.rectHeight = 63
        self.idle_rect_width = 76.9348#77 
        self.idle_x_offset =  45.3152#45.25 by 77,
        self.left_states = { 0: (0, 0, self.rectWidth,  self.rectHeight), 1: (self.rectWidth, 0, self.rectWidth,  self.rectHeight), 2: (self.rectWidth*2, 0, self.rectWidth,  self.rectHeight), 3: (self.rectWidth*3, 0, self.rectWidth,  self.rectHeight)}         
        self.right_states = { 3: (0, self.rectHeight, self.rectWidth,  self.rectHeight), 2: (self.rectWidth, self.rectHeight, self.rectWidth,  self.rectHeight), 1: (self.rectWidth*2, self.rectHeight, self.rectWidth,  self.rectHeight),0: (self.rectWidth*3, self.rectHeight, self.rectWidth,  self.rectHeight)}
        self.idle_left = { 0:(0, self.rectHeight*2, self.idle_rect_width,  self.rectHeight)}
        #self.idle_right = {0:(self.idle_rect_width, self.rectHeight*2+self.idle_rect_height_offset, self.rectWidth,  self.idle_rect_height)}
        self.idle_right = {0:(self.rectWidth*3+self.idle_x_offset, self.rectHeight*2, self.idle_rect_width,  self.rectHeight)}

        self.speed = 100
        self.time = 0
        self.left = False
        self.right = False
        self.idle = True
        self.initial_position=[1754, 1675]
        self.original_position = list(self.initial_position)
        self.last_direction = "left"

    def get_frame(self, frame_set):
        if(self.time >= 1/4 ):
            if self.frame+1 > (len(frame_set) - 1):
                self.frame = 0
            else:
                self.frame += 1
            self.time = 0

       
        return frame_set[self.frame]


        
    def clip(self, clipped_rect):
        #If clipped_rect is a dictionary (a frame set),
        if type(clipped_rect) is dict:
            self.sheet.set_clip(pygame.Rect(self.get_frame(clipped_rect)))
        else:
            self.sheet.set_clip(pygame.Rect(clipped_rect))
        return clipped_rect
    
    def update(self, dt, para):
        if (self.left and self.right) or (not self.left and not self.right):
            direction = self.last_direction
            self.frame=0
            self.idle =True
            self.time = 0
            if direction == "right":
                self.clip(self.idle_right[0])
            elif direction == "left":
                self.clip(self.idle_left[0])
        else:
            if self.left:
                if not self.right:
                    self.time += dt
                    self.clip(self.left_states)
                    self.position[0] -= self.speed * dt
                    self.update_original_position(-dt*self.speed,0,para)
                    self.last_direction = "left"
                self.idle =False
            if self.right:
                if not self.left:
                    self.time += dt
                    self.clip(self.right_states)
                    self.position[0] +=  self.speed * dt
                    self.update_original_position(dt*self.speed,0,para)
                    self.last_direction ="right"
                self.idle =False

        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = self.image.get_rect()
      
        if self.last_direction == "left":
            new_pos = (self.position[0]-self.idle_x_offset, self.position[1])
            self.rect.topleft = new_pos 
        elif self.last_direction == "right":
            new_pos = (self.position[0]+self.idle_x_offset, self.position[1])
            self.rect.topright = new_pos
    



    def handle_event(self, event, dt, para):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                #print("Left pressed")
                self.left = True
            if event.key == pygame.K_RIGHT:
                #print("Right pressed")
                self.right = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                #print("Left released")
                self.left = False
            if event.key == pygame.K_RIGHT:
                #print("Right released")
                self.right = False
            
           

    def update_original_position(self, move_x, move_y, para):
        o_w = 3508
        o_h = 1964
        # Calculate the position in the original reference space (the unscaled background)
        scale_x = para.resized_layers[0].get_width() / o_w
        scale_y = para.resized_layers[0].get_height() / o_h

        # Save position relative to original size
        self.original_position[0] += move_x/scale_x
        self.original_position[1] += move_y/scale_y


    def reposition(self, old_w, old_h, new_w, new_h):
        # Calculate the scale factor based on the original reference dimensions
        scale_factor = min(new_w / old_w, new_h / old_h)
        
        # Calculate the total scaled dimensions of the main layer
        scaled_main_width = old_w * scale_factor
        scaled_main_height = old_h * scale_factor
        
        # Determine the offsets used to center the main layer within the screen dimensions
        x_offset = (new_w - scaled_main_width) // 2 if scaled_main_width < new_w else 0
        y_offset = (new_h - scaled_main_height) // 2 if scaled_main_height < new_h else 0

        # # Print debug information
        # print("\n--- Debug Info ---")
        # print(f"Original Width, Height: {old_w}, {old_h}")
        # print(f"New Width, Height: {new_w}, {new_h}")
        # print(f"Scale Factor: {scale_factor}")
        # print(f"Scaled Main Layer Dimensions: {scaled_main_width}, {scaled_main_height}")
        # print(f"Offset (x, y): {x_offset}, {y_offset}")
        
        # # Print character's initial position before resize
        # print(f"Initial Position: {self.initial_position}")
        # print(f"Previous Position: {self.position}")

        # Calculate the new position relative to the initial position
        self.position[0] = int((self.initial_position[0] / old_w) * scaled_main_width) + x_offset
        self.position[1] = int((self.initial_position[1] / old_h) * scaled_main_height) + y_offset - self.image.get_height() // 2
        self.position[0] = int((self.original_position[0] / old_w) * scaled_main_width) + x_offset
        self.position[1] = int((self.original_position[1] / old_h) * scaled_main_height) + y_offset - self.image.get_height() // 2
        # Update the character's rectangle position based on the new calculated position
        if self.last_direction =="left":
            new_pos = (self.position[0]-self.idle_x_offset, self.position[1])
            self.rect.topleft = new_pos 
        elif self.last_direction == "right":
            new_pos = (self.position[0]+self.idle_x_offset, self.position[1])
            self.rect.topright = new_pos
        # Print character's new position after resizing
        # print(f"New Position After Resize: {self.position}")
        # print(f"Character Rect: {self.rect}")
        # print("--- End Debug Info ---\n")
