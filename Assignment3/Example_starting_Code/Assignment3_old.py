import pygame
import sys

pygame.init()
clock = pygame.time.Clock()



# Size of Background layer(sky)
ORIGINAL_WIDTH, ORIGINAL_HEIGHT = 3508, 1964

layer_widths = [3508, 2770, 3508, 3508, 3508, 3508, 3508]
max_layer_width = 3508

# y position of each layer from photoshop
original_y_positions = [0, 807, 624, 805, 831, 951, 1684]

screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
pygame.display.set_caption("Assignment3")
#import parallax
#para = parallax.Parallax(screen,"parallax_IMGS/Background_IMGS/", 7, 0, [(0,0), (0,807), (0,624), 
#																  (0,805), (0,831), (0,951), (0,1684)])

# Load all the layer images
layers = []
for i in range(1, 8):
    l = pygame.image.load(f"parallax_IMGS/Background_IMGS/Layer{i}.png").convert_alpha()
    layers.append(l)


# keep aspect ratio of each layer in relation to layer1(sky)
def resize_layers(screen_width, screen_height):
	# based off of layer1
	scale_factor = min(screen_width / ORIGINAL_WIDTH, screen_height / ORIGINAL_HEIGHT)

	# Resized layers and positions
	resized_layers = []
	new_positions = []

	# Calculate the scaled height of each layer
	scaled_heights = [int(layer.get_height() * scale_factor) for layer in layers]

	# Calculate the total height of all layers combined (based on their positions)
	total_height = scaled_heights[-1] + (original_y_positions[-1] - original_y_positions[0]) * scale_factor
	total_height = ORIGINAL_HEIGHT*scale_factor
	# Calculate the Y offset to vertically center the group of layers
	if total_height < screen_height:
		y_offset = (screen_height - total_height) // 2
	else:
		y_offset = 0  # No offset needed if it fills the height

	for i, layer in enumerate(layers):
		# Resize layer based on the scale factor
		new_width = int(layer_widths[i] * scale_factor)
		new_height = int(layer.get_height() * scale_factor)
		resized_layer = pygame.transform.scale(layer, (new_width, new_height))
		resized_layers.append(resized_layer)

		# Calculate new X and Y positions proportionally
		x_pos = (screen_width - new_width) // 2 + int((layer_widths[i] - ORIGINAL_WIDTH) * scale_factor / 2)
		y_pos = int(original_y_positions[i] * scale_factor) + y_offset
		new_positions.append((x_pos, y_pos))

	return resized_layers, new_positions, scale_factor

# init resizing
resized_layers, new_positions, scale_factor = resize_layers(screen.get_width(), screen.get_height())
#para.resize_layers()
# parallax variables
starts = [0] * len(layers) 
speed = 5  
speed_modifiers = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]  

# Main loop
run = True
while run:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()

        if event.type == pygame.VIDEORESIZE:
            new_width, new_height = event.w, event.h
            resized_layers, new_positions, scale_factor = resize_layers(new_width, new_height)
            #para.resize_layers()
    #para.handle_event(event)

    # Handle key input for moving left or right
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        for i in range(len(starts)):
            starts[i] += speed * speed_modifiers[i]

    if key[pygame.K_RIGHT]:
        for i in range(len(starts)):
            starts[i] -= speed * speed_modifiers[i]

    # Ensure the image starts over when fully off-screen
    for i in range(len(resized_layers)):
        new_image_width = resized_layers[i].get_width()
        if abs(starts[i]) >= new_image_width:
            starts[i] = 0

    screen.fill((0, 0, 0))
    #para.draw()
    max_layer_width = max(layer.get_width() for layer in resized_layers)
    # Draw each layer with parallax effect
    for i, (layer, (x_pos, y_pos)) in enumerate(zip(resized_layers, new_positions)):
        # Adjust position for parallax scrolling
        scroll_x = x_pos + starts[i]
        # Draw the image within screen bounds, repeating it if necessary
        if layer.get_width() < screen.get_width() and layer.get_width() == max_layer_width :
            render_start = scroll_x
            new_image_width = layer.get_width()
            
            screen.blit(layer, (render_start, y_pos))
            screen.blit(layer, (render_start - new_image_width, y_pos))
            screen.blit(layer, (render_start + new_image_width, y_pos))
            
            # Draw black rectangles to cover any empty space
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, x_pos, screen.get_height()))
            pygame.draw.rect(screen, (0, 0, 0), (x_pos + new_image_width, 0, screen.get_width() - new_image_width, screen.get_height()))
        else:
            # Regular parallax rendering for wider images
            screen.blit(layer, (scroll_x, y_pos))
            screen.blit(layer, (scroll_x - layer.get_width(), y_pos))
            screen.blit(layer, (scroll_x + layer.get_width(), y_pos))

    # Update the display
    pygame.display.flip()

pygame.quit()