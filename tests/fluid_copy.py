import numpy as np
import math
def create_fluid_sim(screen_w, screen_h):
    density = 1000

    sim_height = 1.1 #meters
    screen_scale = screen_h / sim_height  #pixels per simulation unit, screenh/simheight, make the sim height smaller than screen
    sim_width = screen_w / screen_scale #ratio in meters

    domain_height = 1 #smaller than sim height, meters
    domain_width = domain_height / sim_height * sim_width #meters, keep width ratio to new domain height
    res = 50
    h = domain_height / res #cell size, meters
    num_X = math.floor(domain_width / h)
    num_Y = math.floor(domain_height / h)

    return fluid.Fluid(density, num_X, num_Y, h)

class Fluid:
    def __init__(self, density, x, y, h):
        self.density = density
        self.num_x = x+2 #add boundaires   [b][x][b]
        self.num_y = y+2
        self.num_cells = self.num_x * self.num_y
        self.h = h #resolution of grid
        self.u = np.empty(self.num_cells, dtype=np.float32) 
        self.v = np.empty(self.num_cells, dtype=np.float32) 
        self.new_u = np.empty(self.num_cells, dtype=np.float32) 
        self.new_v = np.empty(self.num_cells, dtype=np.float32) 
        self.p = np.empty(self.num_cells, dtype=np.float32) 
        self.s = np.empty(self.num_cells, dtype=np.float32) 
        self.m = np.ones(self.num_cells, dtype=np.float32) 
        self.new_M = np.empty(self.num_cells, dtype=np.float32) 
        self.over_relaxation = 1.9
        self.U_FIELD = 0
        self.V_FIELD = 1
        self.S_FIELD = 2


    def integrate(self, dt, gravity):
        cols = self.num_x
        #ignore left boundaries , index 0 and last row/cool
        for y in range(1, self.num_y-1): 
            for x in range(1, self.num_x): 
                if self.s[y*cols + x] != 0.0 and self.s[y*cols + x] != 0.0:
                    self.v[y*cols + x] += gravity * dt  # Update velocity

    def solve_incompressibility(self, num_iters, dt):
        cp = self.density * self.h / dt
        cols = self.num_x

        for it in range(num_iters):
            for y in range(1, self.num_y - 1):  
                for x in range(1, self.num_x - 1):  
                    if self.s[y * cols + x] == 0.0:
                        continue

                    sx0 = self.s[y * cols + (x - 1)]  
                    sx1 = self.s[y * cols + (x + 1)]  
                    sy0 = self.s[(y - 1) * cols + x]  
                    sy1 = self.s[(y + 1) * cols + x]  
                    s = sx0 + sx1 + sy0 + sy1

                    if s == 0.0:
                        continue

                    div = self.u[y * cols + (x + 1)] - self.u[y * cols + x] + \
                        self.v[(y + 1) * cols + x] - self.v[y * cols + x]

                    p = -div / s
                    p *= self.over_relaxation
                    self.p[y * cols + x] += cp * p

                    self.u[y * cols + x] -= sx0 * p
                    self.u[y * cols + (x + 1)] += sx1 * p
                    self.v[y * cols + x] -= sy0 * p
                    self.v[(y + 1) * cols + x] += sy1 * p

    def extrapolate(self):
        cols = self.num_x
        for y in range(self.num_y):  # Iterating rows (Y-axis)
            self.v[y*cols + 0] = self.v[y*cols + 1]
            self.v[y*cols + (self.num_x - 1)] = self.v[y*cols + (self.num_x - 2)]
            
        for x in range(self.num_x):  # Iterating columns (X-axis)
            self.u[0*cols + x] = self.u[1*cols + x]
            self.u[(self.num_y - 1)*cols + x] = self.u[(self.num_y - 2)*cols + x]

    def sample_field(self, x, y, field):
        cols = self.num_x
        h = self.h
        h1 = 1.0 / h
        h2 = 0.5 * h

        x = max(min(x, self.num_x * h), h)
        y = max(min(y, self.num_y * h), h)

        dx = 0
        dy = 0.0

        if field == self.U_FIELD:
            f = self.u
            dy = h2
        elif field == self.V_FIELD:
            f = self.v
            dx = h2
        elif field == self.S_FIELD:
            f = self.m
            dx = h2
            dy = h2
        if math.isnan(x) or math.isnan(dx) or math.isnan(h1):
            print(f"x: {x}, dx: {dx}, h1: {h1}")
            raise ValueError("NaN detected in calculation.")
        x0 = min(int((x - dx) * h1), self.num_x - 1)
        tx = ((x - dx) - x0 * h) * h1
        x1 = min(x0 + 1, self.num_x - 1)

        y0 = min(int((y - dy) * h1), self.num_y - 1)
        ty = ((y - dy) - y0 * h) * h1
        y1 = min(y0 + 1, self.num_y - 1)

        sx = 1.0 - tx
        sy = 1.0 - ty

        val = (sx * sy * f[y0 * cols + x0] +
            tx * sy * f[y0 * cols + x1] +
            tx * ty * f[y1 * cols + x1] +
            sx * ty * f[y1 * cols + x0])
        
        return val

    def avg_v(self, x, y):
        cols = self.num_x
        v = (self.v[(y-1) * cols + x] + self.v[y * cols + x] +
            self.v[(y-1) * cols + (x+1)] + self.v[y * cols + (x+1)]) * 0.25
        return v
    def avg_u(self, x, y):
        cols = self.num_x
        u = (self.u[y * cols + (x-1)] + self.u[y * cols + x] +
            self.u[(y+1) * cols + (x-1)] + self.u[(y+1) * cols + x]) * 0.25
        return u
    def advect_vel(self, dt):
        self.new_u[:] = self.u[:]
        self.new_v[:] = self.v[:]

        cols = self.num_x
        h = self.h
        h2 = 0.5 * h

        for y in range(1, self.num_y):
            for x in range(1, self.num_x):
                if self.s[y * cols + x] != 0.0 and self.s[(y - 1) * cols + x] != 0.0 and y < self.num_x - 1:
                    x_coord = x * h
                    y_coord = y * h + h2
                    u = self.u[y * cols + x]
                    v = self.avg_v(x, y)
                    x_coord -= dt * u
                    y_coord -= dt * v
                    print(x_coord)
                    u = self.sample_field(x_coord, y_coord, self.U_FIELD)
                    self.new_u[y * cols + x] = u

                if self.s[y * cols + x] != 0.0 and self.s[y * cols + (x - 1)] != 0.0 and y < self.num_y - 1:
                    x_coord = x * h + h2
                    y_coord = y * h
                    u = self.avg_u(x, y)
                    v = self.v[y * cols + x]
                    x_coord -= dt * u
                    y_coord -= dt * v
                    print(x_coord)
                    v = self.sample_field(x_coord, y_coord, self.V_FIELD)
                    self.new_v[y * cols + x] = v

        self.u[:] = self.new_u[:]
        self.v[:] = self.new_v[:]

    def advect_smoke(self, dt):
        self.new_m[:] = self.m[:]  # Copy the current smoke density field
        
        cols = self.num_x
        h = self.h
        h2 = 0.5 * h

        for y in range(1, self.num_y - 1):
            for x in range(1, self.num_x - 1):
                
                if self.s[y * cols + x] != 0.0:  # Check if this cell is not empty
                    u = (self.u[y * cols + x] + self.u[y * cols + (x + 1)]) * 0.5
                    v = (self.v[y * cols + x] + self.v[(y + 1) * cols + x]) * 0.5
                    x_coord = x * h + h2 - dt * u
                    y_coord = y * h + h2 - dt * v

                    self.new_m[y * cols + x] = self.sample_field(x_coord, y_coord, self.S_FIELD)
        
        self.m[:] = self.new_m[:]  # Update the smoke density field

    def simulate(self, dt, gravity, numIter):
        self.integrate(dt, gravity)
        self.p = np.zeros_like(self.p)
        self.solve_incompressibility(numIter, dt)

        self.extrapolate()
        self.advect_vel(dt)
        self.advect_smoke(dt)

    def create(self):
        n = self.num_x
        for i in range(0,self.num_x):
            for j in range(0,self.num_y):
                s = 1.0;	
                if (i == 0 or i == self.num_x-1 or j == 0): #or j == self.num_y-1):
                    s = 0.0;	
                self.s[j*n + i] = s









































    