import numpy as np
import math
class Fluid:
    def __init__(self, density, x, y, h):
        self.density = density
        self.numX = x+2 #add boundaires   [b][x][b]
        self.numY = y+2
        self.num_cells = self.numX * self.numY
        self.h = h #resolution of grid
        self.u = np.zeros(self.num_cells, dtype=np.float32) 
        self.v = np.zeros(self.num_cells, dtype=np.float32) 
        self.newU = np.zeros(self.num_cells, dtype=np.float32) 
        self.newV = np.zeros(self.num_cells, dtype=np.float32) 
        self.p = np.zeros(self.num_cells, dtype=np.float32) 
        self.s = np.zeros(self.num_cells, dtype=np.float32) 
        self.m = np.ones(self.num_cells, dtype=np.float32) 
        self.newM = np.zeros(self.num_cells, dtype=np.float32) 
        self.overRelaxation = 1.9
        self.U_FIELD = 0
        self.V_FIELD = 1
        self.S_FIELD = 2

    def integrate(self, dt, gravity):
        n = self.numY
        for i in range(1, self.numX):
            for j in range(1, self.numY - 1):
                if self.s[i * n + j] != 0.0 and self.s[i * n + j - 1] != 0.0:
                    self.v[i * n + j] += gravity * dt

    def solve_incompressibility(self, numIters, dt):
        n = self.numY
        cp = self.density * self.h / dt

        for iter in range(numIters):
            for i in range(1, self.numX - 1):
                for j in range(1, self.numY - 1):
                    if self.s[i * n + j] == 0.0:
                        continue

                    s = self.s[i * n + j]
                    sx0 = self.s[(i - 1) * n + j]
                    sx1 = self.s[(i + 1) * n + j]
                    sy0 = self.s[i * n + j - 1]
                    sy1 = self.s[i * n + j + 1]
                    s = sx0 + sx1 + sy0 + sy1
                    if s == 0.0:
                        continue

                    div = self.u[(i + 1) * n + j] - self.u[i * n + j] + \
                          self.v[i * n + j + 1] - self.v[i * n + j]

                    p = -div / s
                    p *= self.overRelaxation
                    self.p[i * n + j] += cp * p

                    self.u[i * n + j] -= sx0 * p
                    self.u[(i + 1) * n + j] += sx1 * p
                    self.v[i * n + j] -= sy0 * p
                    self.v[i * n + j + 1] += sy1 * p

    def extrapolate(self):
        n = self.numY
        for i in range(self.numX):
            self.u[i * n + 0] = self.u[i * n + 1]
            self.u[i * n + self.numY - 1] = self.u[i * n + self.numY - 2]

        for j in range(self.numY):
            self.v[0 * n + j] = self.v[1 * n + j]
            self.v[(self.numX - 1) * n + j] = self.v[(self.numX - 2) * n + j]

    def sample_field(self, x, y, field):
        n = self.numY
        h = self.h
        h1 = 1.0 / h
        h2 = 0.5 * h

        x = max(min(x, self.numX * h), h)
        y = max(min(y, self.numY * h), h)

        dx = 0.0
        dy = 0.0

        f = None

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

        x0 = min(int((x - dx) * h1), self.numX - 1)
        tx = ((x - dx) - x0 * h) * h1
        x1 = min(x0 + 1, self.numX - 1)

        y0 = min(int((y - dy) * h1), self.numY - 1)
        ty = ((y - dy) - y0 * h) * h1
        y1 = min(y0 + 1, self.numY - 1)

        sx = 1.0 - tx
        sy = 1.0 - ty

        val = sx * sy * f[x0 * n + y0] + \
              tx * sy * f[x1 * n + y0] + \
              tx * ty * f[x1 * n + y1] + \
              sx * ty * f[x0 * n + y1]

        return val

    def avgU(self, i, j):
        n = self.numY
        u = (self.u[i * n + j - 1] + self.u[i * n + j] +
              self.u[(i + 1) * n + j - 1] + self.u[(i + 1) * n + j]) * 0.25
        return u

    def avgV(self, i, j):
        n = self.numY
        v = (self.v[(i - 1) * n + j] + self.v[i * n + j] +
              self.v[(i - 1) * n + j + 1] + self.v[i * n + j + 1]) * 0.25
        return v

    def advectVel(self, dt):
        self.newU[:] = self.u
        self.newV[:] = self.v

        n = self.numY
        h = self.h
        h2 = 0.5 * h

        for i in range(1, self.numX):
            for j in range(1, self.numY):
                # u component
                if self.s[i * n + j] != 0.0 and self.s[(i - 1) * n + j] != 0.0 and j < self.numY - 1:
                    x = i * h
                    y = j * h + h2
                    u = self.u[i * n + j]
                    v = self.avgV(i, j)
                    x -= dt * u
                    y -= dt * v
                    u = self.sample_field(x, y, self.U_FIELD)
                    self.newU[i * n + j] = u

                # v component
                if self.s[i * n + j] != 0.0 and self.s[i * n + j - 1] != 0.0 and i < self.numX - 1:
                    x = i * h + h2
                    y = j * h
                    u = self.avgU(i, j)
                    v = self.v[i * n + j]
                    x -= dt * u
                    y -= dt * v
                    v = self.sample_field(x, y, self.V_FIELD)
                    self.newV[i * n + j] = v

        self.u[:] = self.newU
        self.v[:] = self.newV

    def advectSmoke(self, dt):
        self.newM[:] = self.m

        n = self.numY
        h = self.h
        h2 = 0.5 * h

        for i in range(1, self.numX - 1):
            for j in range(1, self.numY - 1):
                if self.s[i * n + j] != 0.0:
                    u = (self.u[i * n + j] + self.u[(i + 1) * n + j]) * 0.5
                    v = (self.v[i * n + j] + self.v[i * n + j + 1]) * 0.5
                    x = i * h + h2 - dt * u
                    y = j * h + h2 - dt * v

                    self.newM[i * n + j] = self.sample_field(x, y, self.S_FIELD)

        self.m[:] = self.newM
    def simulate(self, dt, gravity, numIter):
        self.integrate(dt, gravity)
        self.p = np.zeros_like(self.p)
        self.solve_incompressibility(numIter, dt)

        self.extrapolate()
        self.advectVel(dt)
        self.advectSmoke(dt)

    def create(self):
        n = self.numY
        for i in range(0,self.numX):
            for j in range(0,self.numY):
                s = 1.0;	
                if (i == 0 or i == self.numX-1 or j == 0): #or j == self.num_y-1):
                    s = 0.0;	
                self.s[i*n + j] = s
