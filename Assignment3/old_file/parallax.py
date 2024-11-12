import pygame
class Parallax:
    def __init__(self, screen, path, num_layers, main_index, offsets):
        self.screen = screen
        self.path = path
        self.num_layers = num_layers
        self.main_index = main_index
        self.layers = []
        for i in range(1, num_layers+1):
            l = pygame.image.load(f"parallax_IMGS/Background_IMGS/Layer{i}.png").convert_alpha()
            self.layers.append(l)
        self.og_main_width = self.layers[main_index].get_width()
        self.og_main_height = self.layers[main_index].get_height()
        self.offsets = offsets
        self.resized_layers = []
        self.resized_pos = []
        self.speed = 100
        self.speed_modifiers = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]  
        self.starts = [0] * len(self.layers) 
        self.left = False
        self.right = False

        
    # keep aspect ratio of layer1, size rest to fit
    def resize_layers(self):
        screen_width, screen_height = self.screen.get_width(), self.screen.get_height()
        # based off of layer1
        scale_factor = min(screen_width / self.og_main_width, screen_height / self.og_main_height)

        self.resized_layers.clear()
        self.resized_pos.clear()

        # last layer is the bottom: scaled_ground + proportion to sky= new height
        total_height = self.og_main_height*scale_factor
        # center image if cant fill screen
        if total_height < screen_height:
            y_offset = (screen_height - total_height) // 2
        else:
            y_offset = 0  #fills screen
 
        #smoothscale
        for i, layer in enumerate(self.layers):
            new_width = int(layer.get_width() * scale_factor)
            new_height = int(layer.get_height() * scale_factor)
            resized_layer = pygame.transform.scale(layer, (new_width, new_height))
            self.resized_layers.append(resized_layer)

            #(since layer2 is not same width, when its centered it has an x offset
            # empty space on one side of layer width (to center)+ new proportion on image/2 (offset from size diff on one side) align on left again
            x_pos = (screen_width - new_width) // 2 + int((self.layers[i].get_width() - self.og_main_width) * scale_factor / 2)

            #proportion to sky + center
            y_pos = int(self.offsets[i][1] * scale_factor) + y_offset
            self.resized_pos.append((x_pos, y_pos))
    
    def handle_event(self, event, dt):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.left = True
        
            if event.key == pygame.K_RIGHT:
                self.right = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.left = False
        
            if event.key == pygame.K_RIGHT:
                self.right = False


    def update(self,dt):
        if self.left and not self.right:
            for i in range(len(self.starts)):
                self.starts[i] += self.speed * self.speed_modifiers[i] * dt
        elif self.right and not self.left:
            for i in range(len(self.starts)):
                self.starts[i] -= self.speed * self.speed_modifiers[i] * dt
        # reset start when img is scrolled through
        for i in range(len(self.resized_layers)):
            new_image_width = self.resized_layers[i].get_width()
            if abs(self.starts[i]) >= new_image_width:
                self.starts[i] = 0       


    def draw(self):
        max_layer_width = max(layer.get_width() for layer in self.resized_layers)
        for i in range(len(self.resized_layers)):
            layer = self.resized_layers[i]
            x_pos, y_pos = self.resized_pos[i]          
            scroll_x = x_pos + self.starts[i]
            layer_width = layer.get_width()
            self.screen.blit(layer, (scroll_x, y_pos))
            self.screen.blit(layer, (scroll_x - layer_width, y_pos))
            self.screen.blit(layer, (scroll_x + layer_width, y_pos))
            if(layer_width == max_layer_width):
                # Draw black rectangles to cover any the images loaded beside (image has border to fit screen)
                pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, x_pos, self.screen.get_height()))
                pygame.draw.rect(self.screen, (0, 0, 0), (x_pos + layer_width, 0, self.screen.get_width() - layer_width, self.screen.get_height()))
    