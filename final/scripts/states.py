from scripts.utils import load_image, load_images, scale_image
class SmokeState:
    def __init__(self):
        self.positions = []
        self.velocities = []
        self.colors = []
        self.radi = []
        self.lives = []
        self.ages = []
        self.img_sizes =[]
        self.alpha_decays =[]
        self.inactive_particles = []
        self.inactive_count = 0
        self.default_radius = 2
        self.default_age = 10
        self.default_radius_decrement = 2
        self.default_alpha_decay = 3
        self.default_size = 0.1
        self.surfaces = []
        self.img = None
    
    def get_nb(self):
        return len(self.positions) 

    def get_active_nb(self):
        return len(self.positions) - self.inactive_count

    
    def update_state(self, dt):
        for i in range(self.get_nb()):
            if(self.lives[i] == True):
                self.colors[i][3] -= self.alpha_decays[i] 
                self.img_sizes[i] += 0.05 * dt
                if(self.colors[i][3] <= 0):
                    self.colors[i][3] = 0
                self.alpha_decays[i] -= 50*dt
                if self.alpha_decays[i] < 50 * dt:
                    self.alpha_decays[i] = 50 *dt

                self.surfaces[i] = scale_image(self.img, self.img_sizes[i])
                self.surfaces[i].set_alpha(self.colors[i][3])
                self.radi[i] += self.default_radius_decrement * dt
                self.ages[i]+=dt
                if(self.ages[i] > self.default_age or self.colors[i][3] == 0):
                    self.lives[i] = False
                    self.inactive_particles.append(i)
                    self.inactive_count += 1
    
    
    def add_particle(self, P, V ,C, img):
        if self.img == None:
            self.img = img
        if(self.inactive_count > 0):
            index = self.inactive_particles.pop()
            self.inactive_count -= 1
            self.positions[index]= P
            self.velocities[index]= V
            self.colors[index] =C
            self.alpha_decays[index]=self.default_alpha_decay
            self.lives[index]= True
            self.ages[index] =0
            self.radi[index] = self.default_radius
            self.img_sizes[index] = self.default_size
            self.surfaces[index] = scale_image(img,self.default_size)
        else:
            self.positions.append(P)
            self.velocities.append(V)
            self.colors.append(C)
            self.alpha_decays.append(self.default_alpha_decay)
            self.lives.append(True)
            self.ages.append(0)
            self.radi.append(self.default_radius)
            self.img_sizes.append(self.default_size)
            self.surfaces.append(scale_image(img, self.default_size))

