

class Environment:
    
    def __init__(self, list_of_boids):
        self.list_of_boids = list_of_boids
        
    def evolve(self):
        ever_seen_identifier = set()
        list_of_births = []
        list_of_death = []
        for boid in self.list_of_boids:
            births, death = boid.special_action(self.list_of_boids)
            list_of_births += births
            list_of_death += death
            boid.update_params(self)
            boid.move()
        for dead_boil in list_of_death:
            if dead_boil in self.list_of_boids:
                self.list_of_boids.remove(dead_boil)
        self.list_of_boids += list_of_births
