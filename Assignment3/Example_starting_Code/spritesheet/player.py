#Imports the pygame library, which is used to create games and multimedia applications in Python
import pygame


#Defines a class Character that inherits from pygame.sprite.Sprite, 
#which is a built-in class in pygame for creating and managing 2D game objects (sprites)
class Character(pygame.sprite.Sprite):
    
#This is the constructor method, which initializes a new Character object. 
#It takes position as an argument to determine where the character will be placed on the screen   
    def __init__(self, position):
    
        #Loads an image called caveman.png, which contains a 
        #sprite sheet (a collection of multiple character images in a single file)
        #load the image
        self.sheet = pygame.image.load('caveman.png')
        
        #Defines a rectangular clipping area for the sprite sheet 
        #The rectangle starts at coordinates (0, 0)
        #and has a width of 131 pixels and a height of 135 pixels 
        #This is the size of one sprite in the sheet.
        #defines area of a single sprite of an image
        self.sheet.set_clip(pygame.Rect(0, 0, 131, 135))
        
        #Extracts the clipped sprite from the sprite sheet and assigns it to self.image 
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        
        #self.rect defines the rectangular area around this sprite, 
        #which is useful for positioning and collision detection
        self.rect = self.image.get_rect()
        
        #position image in the screen surface
        #Sets the position of the top-left corner of the sprite 
        #rectangle to the given position   
        self.rect.topleft = position
        
        #variable for looping the frame sequence
        #Initializes a frame counter that will be 
        #used to animate the sprite by cycling through frames.
        self.frame = 0
        
        
        #Sets the width and height of each sprite in 
        #the sprite sheet, making it easier to reference in the animation sequences.
        self.rectWidth = 131
        self.rectHeight = 135


        #This defines the frames for the "down" movement. 
        #The dictionary contains keys (0 to 3) that correspond to different frames in the down animation. 
        #Each value is a tuple that defines the clipping rectangle for each frame.
        self.down_states = { 0: (0, 0, self.rectWidth,  self.rectHeight), 1: (131, 0, self.rectWidth,  self.rectHeight), 2: (261, 0, self.rectWidth,  self.rectHeight), 3:(390, 0, self.rectWidth,  self.rectHeight) }     
            
        #Similar to down_states, these dictionaries define the frames for 
        #the "up," "left," and "right" movement animation                       
        self.up_states = { 0: (0, 264, self.rectWidth,  self.rectHeight), 1: (131, 264, self.rectWidth,  self.rectHeight), 2: (261, 264, self.rectWidth,  self.rectHeight), 3: (390, 264, self.rectWidth,  self.rectHeight)  }                    
        self.left_states = { 0: (0, 133, self.rectWidth,  self.rectHeight), 1: (131, 133, self.rectWidth,  self.rectHeight), 2: (261, 133, self.rectWidth,  self.rectHeight),3: (390, 133, self.rectWidth,  self.rectHeight) }
        self.right_states = { 0: (0, 396, self.rectWidth,  self.rectHeight), 1: (131, 396, self.rectWidth,  self.rectHeight), 2: (261, 396, self.rectWidth,  self.rectHeight), 3: (390, 396, self.rectWidth,  self.rectHeight) }

    #This method selects and returns the next frame from a given 
    #frame set (such as down_states or left_states)
    def get_frame(self, frame_set):
        #looping the sprite sequences
        self.frame += 1
        
        #Increments the frame counter and loops back to the first frame
        #if the end of the frame set is reached
        if self.frame > (len(frame_set) - 1):
            self.frame = 0
        #print(frame_set[self.frame])
        return frame_set[self.frame]


        
    #Clips the sprite sheet to the specified rectangle, effectively selecting the current frame
    def clip(self, clipped_rect):
        #If clipped_rect is a dictionary (a frame set),
        #it uses get_frame to clip the sprite sheet. Otherwise, it directly uses clipped_rect
        if type(clipped_rect) is dict:
            self.sheet.set_clip(pygame.Rect(self.get_frame(clipped_rect)))
        else:
            self.sheet.set_clip(pygame.Rect(clipped_rect))
        #Returns the clipped rectangle, which defines the current frame of the sprite
        return clipped_rect
    
    #Updates the character's position and animation based on the direction of movement
    def update(self, direction):
        #If the character is moving left, the method updates the frame by 
        #clipping from left_states and moves the sprite 5 pixels to the left
        if direction == 'left':
            self.clip(self.left_states)
            #animate rect coordinates
            self.rect.x -= 5
        if direction == 'right':
            self.clip(self.right_states)
            self.rect.x += 5
        if direction == 'up':
            self.clip(self.up_states)
            self.rect.y -= 5
        if direction == 'down':
            self.clip(self.down_states)
            self.rect.y += 5

        #If the character is standing still, 
        #the corresponding first frame of each state (0) is used to show the "standing" sprite
        if direction == 'stand_left':
            self.clip(self.left_states[0])
        if direction == 'stand_right':
            self.clip(self.right_states[0])
        if direction == 'stand_up':
            self.clip(self.up_states[0])
        if direction == 'stand_down':
            self.clip(self.down_states[0])
        #Updates self.image with the newly clipped frame from the sprite sheet.
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        print(self.frame)


    #User events handling
    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:
            #Moves the character left if the left arrow key is pressed.
            if event.key == pygame.K_LEFT:
                self.update('left')
            if event.key == pygame.K_RIGHT:
                self.update('right')
            if event.key == pygame.K_UP:
                self.update('up')
            if event.key == pygame.K_DOWN:
                self.update('down')

        if event.type == pygame.KEYUP:
            #When a key is released, the character stops moving and transitions to 
            #the corresponding "standing" frame.
            if event.key == pygame.K_LEFT:
                self.update('stand_left')
            if event.key == pygame.K_RIGHT:
                self.update('stand_right')
            if event.key == pygame.K_UP:
                self.update('stand_up')
            if event.key == pygame.K_DOWN:
                self.update('stand_down')
