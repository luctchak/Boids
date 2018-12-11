from globals import *

class Environment:
    
    def __init__(self, list_of_boids):
        self.list_of_boids = list_of_boids
        self.grid_x = {x : set() for x in range(0, SIZE_X//MAX_RANGE + 1)}
        self.grid_y = {y : set() for y in range(0, SIZE_Y//MAX_RANGE + 1)}
        
    def evolve(self):
        ever_seen_identifier = set()
        list_of_births = []
        list_of_death = []
        for boid in self.list_of_boids:
            births, death = boid.special_action(self)
            list_of_births += births
            list_of_death += death
            boid.update_params(self)
            boid.move()
        for dead_boil in list_of_death:
            if dead_boil in self.list_of_boids:
                self.list_of_boids.remove(dead_boil)
        self.list_of_boids += list_of_births
        self.update_grid()

    def update_grid(self):
        self.grid_x = {x : set() for x in range(0, SIZE_X//MAX_RANGE + 1)}
        self.grid_y = {y : set() for y in range(0, SIZE_Y//MAX_RANGE + 1)}
        for boid in self.list_of_boids:
            self.grid_x[boid.x//MAX_RANGE].add(boid)
            self.grid_y[boid.y//MAX_RANGE].add(boid)

    def get_range(self, x, size):
        x_index = x//MAX_RANGE
        if x_index == 0:
            return [0, 1, size//MAX_RANGE]
        if x_index == size//MAX_RANGE:
            return [0, size//MAX_RANGE-1, size//MAX_RANGE]
        return [x_index-1, x_index, x_index+1]
    
    def print_stats(self):
        type_to_count = {}
        for b in self.list_of_boids:
            type_to_count[b.type] = type_to_count.get(b.type, 0) + 1
        print("Number of blue boids :", type_to_count.get(BLUE_TYPE, 0))
        print("Number of red boids :", type_to_count.get(RED_TYPE, 0))
        print("Number of green boids :", type_to_count.get(GREEN_TYPE, 0))
        print("Best Eater :")
        max_eaten = 0
        best_eater = None
        for b in self.list_of_boids:
            if b.eaten_boids >= max_eaten:
                best_eater = b
                max_eaten = b.eaten_boids
        print("params :", best_eater.params)
        print("speed :", best_eater.params)
        print("count :", max_eaten)
        

    def get_closest_boids(self, boid):
        set_x = set()
        for x in self.get_range(boid.x, SIZE_X):
            set_x = set_x.union(self.grid_x[x])
        set_y = set()
        for y in self.get_range(boid.y, SIZE_Y):
            set_y = set_y.union(self.grid_y[y])
        return set_x.intersection(set_y)
