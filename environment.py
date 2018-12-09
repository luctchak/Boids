

class Environment:
    
    def __init__(self, list_of_boids):
        self.list_of_boids = list_of_boids
        
    def evolve(self):
        for boid in self.list_of_boids:
            boid.special_action(self)
            boid.update_params(self)
            boid.move()
