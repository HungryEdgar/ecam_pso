import random
import math

class Particle:
    def __init__(self, x0):
        self.position_i = []          # particle position
        self.velocity_i = []          # particle velocity
        self.pos_best_i = []          # best position individual
        self.err_best_i = -1          # best error individual
        self.err_i = -1               # error individual
   
        for i in range(0, num_dimensions):
            self.velocity_i.append(random.uniform(-1, 1))
            self.position_i.append(x0[i])

    # update the particle position based off new velocity updates
    def update_position(self):
        for i in range(0, num_dimensions):
            self.position_i[i] = self.position_i[i] + self.velocity_i[i]

    # update new particle velocity
    def update_velocity(self, pos_best_g):
        w = 0.5       # constant inertia weight (how much to weigh the previous velocity), determines the contribution rate of a particle's previous velocity to its velocity at the current time step
        c1 = 1        # cognative constant = how much confidence a particle has in itself
        c2 = 2        # social constant = in others

        for i in range(0, num_dimensions):
            r1 = random.random()
            r2 = random.random()

            vel_cognitive = c1 * r1 * (self.pos_best_i[i] - self.position_i[i])
            vel_social = c2 * r2 * (pos_best_g[i] - self.position_i[i])
            self.velocity_i[i] = w * self.velocity_i[i] + vel_cognitive + vel_social

    #evaluate current fitness = the best solution (fitness) it has achieved so far
    def evaluate(self, costFunc):
        self.err_i = costFunc(self.position_i)

        # check to see if the current position is an individual best
        if self.err_i < self.err_best_i or self.err_best_i == -1:
            self.pos_best_i = self.position_i
            self.err_best_i = self.err_i

class PSO:
    def __init__(self, costFunc, x0, num_particles, maxiter, verbose=False):
        global num_dimensions
        num_dimensions = len(x0)
        err_best_g = -1                   # best error for group
        pos_best_g = []                   # best position for group

        # establish the swarm
        swarm = []

        for i in range(0, num_particles):
            swarm.append(Particle(x0))
        
        # begin optimization loop
        i = 0
        while i < maxiter:
            if verbose: print(f"Iteration {i:>2}: {err_best_g:>10.6f}")
            
            # cycle through particles in swarm and evaluate fitness
            for j in range(0, num_particles):
                swarm[j].evaluate(costFunc)
                
                # determine if current particle is the best (globally)
                if swarm[j].err_i < err_best_g or err_best_g == -1:
                    pos_best_g = list(swarm[j].position_i)
                    err_best_g = float(swarm[j].err_i)
        
            # cycle through swarm and update velocities and position
            for j in range(0, num_particles):
                swarm[j].update_velocity(pos_best_g)
                swarm[j].update_position()
            
            i += 1
        
         # print final results
        if verbose:
            print(f"\nSolution: {pos_best_g}")
            print(f"Error: {err_best_g}")

        self.result = pos_best_g
        self.error = err_best_g

def func1(x):
    return x[0]**2 + x[1]**2 + x[2]**2 + x[3]**2

#main
initial = [5, 5, 5, 5] # initial starting location [x1,x2,...,xn]
maximum_iterations = 10 # max number of iterations
num_particles = 10 # number of particles in the swarm

#perform optimization
optimization = PSO(func1, initial, num_particles, maximum_iterations, verbose=True)
print(f"\nFinal solution: {optimization.result}")
print(f"Final error: {optimization.error}")