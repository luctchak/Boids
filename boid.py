from math import sin, cos, pi
from globals import *

def generate_random_params():
    return {
        "range": random(0, MAX_RANGE),
        "max_speed": random(0, MAX_SPEED),
        "n_max_neighbors": int(random(1, 5)),
        "fear_factor": random(0, 1),
        "hunter_factor": random(0, 1),
        "neutral_factor": 0
    }

class Boid:
    
    def __init__(self, x, y, angle, type, params=generate_random_params()):
        self.x = x
        self.y = y
        self.speed = params["max_speed"]
        self.type = type
        self.angle = angle
        self.pregnant = False
        self._col = TYPE_TO_COLOR[self.type]
        self.params = params
        self.eaten_boids = 0
        self.radius = radius
        
    def stay_in_range(self):
        if self.x < 0:
            self.x = SIZE_X
        if self.y < 0:
            self.y = SIZE_Y
        if self.x > SIZE_X:
            self.x = 0
        if self.y > SIZE_Y:
            self.y = 0
        
    def move(self):
        x_diff = self.speed*sin(self.angle)
        y_diff = -self.speed*cos(self.angle)
        self.x += x_diff
        self.y += y_diff
        self.stay_in_range()
        pushMatrix()
        translate(self.x, self.y)
        fill(self._col[0], self._col[1], self._col[2])
        rotate(self.angle)    
        beginShape(TRIANGLES)
        vertex(0, -self.radius*2)
        vertex(-self.radius, self.radius*2)
        vertex(self.radius, self.radius*2)
        endShape()
        popMatrix()
        
    def give_birth(self):
        assert(self.pregnant)
        babies = []
        if random(0, 2) < 1:
            params = self.params
        else:
            params = generate_random_params()
        baby_boid = Boid(self.x,
                         self.y,
                         random(-pi, pi),
                         self.type,
                         params)
        self.pregnant = False
        return [baby_boid]

    def special_action(self, environment):
        births = []
        death = []
        if self.pregnant and random(0, 10) < 1:
            births = self.give_birth()
            
        #TODO : optimize this with a KDTree
        for boid in  environment.get_closest_boids(self):
            if distance(boid, self) < 2*self.radius and hunts(self.type, boid.type):
                self.pregnant = True
                self.eaten_boids += 1
                self.radius = min(self.radius+1/2, 10)
                death += [boid]
        return births, death
    
        
    def update_params(self, environment):
        if self.angle > pi or self.angle < -pi:
            print('error', self.angle)
        # Get features from the neighbors hunters and preys
        # Features are composed of vectors and distances
        closest_boids = environment.get_closest_boids(self)
        if self in closest_boids:
            closest_boids.remove(self)
        hunters = [
            boid for boid in closest_boids if hunts(boid.type, self.type)
        ]
        preys = [
            boid for boid in closest_boids if hunts(self.type, boid.type)
        ]
        neutrals = [
            boid for boid in closest_boids if self.type == boid.type
        ]
        hunters_vector = [
            (get_vector(self, boid), distance(self, boid)) for boid in hunters
        ]
        hunters_vector = [
            item for item in hunters_vector 
            if item[1] < self.params["range"]
        ]
        preys_vector = [
            (get_vector(boid, self), distance(self, boid)) for boid in preys
        ]
        preys_vector = [
            item for item in preys_vector 
            if item[1] < self.params["range"]
        ]
        neutrals_vector = [
            (get_vector(self, boid), distance(self, boid)) for boid in neutrals
        ]
        neutrals_vector = [
            item for item in neutrals_vector 
            if item[1] < self.params["range"]
        ]
        # Only consider the n_max_neighbors closest ones
        sorted_hunters = sorted(hunters_vector, key=lambda x:x[1])[:self.params["n_max_neighbors"]]
        sorted_preys = sorted(preys_vector, key=lambda x:x[1])[:self.params["n_max_neighbors"]]
        sorted_neutrals = sorted(neutrals_vector, key=lambda x:x[1])[:self.params["n_max_neighbors"]]
        # Easy function for begining :
        vec_fear = [0, 0]
        vec_hunt = [0, 0]
        vec_neutral = [0, 0]
        if len(sorted_preys) > 0:
            norm_factor = sum([self.params["range"]-item[1] for item in sorted_preys]) + EPS
            assert(norm_factor>0)
            for index in [0, 1]:
                vec_hunt[index] = sum([item[0][index]*(self.params["range"]-item[1])/(item[1]+EPS) for item in sorted_preys])
                vec_hunt[index] /= norm_factor
        if len(sorted_hunters) > 0:
            norm_factor = sum([self.params["range"]-item[1] for item in sorted_hunters]) + EPS
            assert(norm_factor>0)
            for index in [0, 1]:
                vec_fear[index] = sum([item[0][index]*(self.params["range"]-item[1])/(item[1]+EPS) for item in sorted_hunters])
                vec_fear[index] /= norm_factor
        if len(sorted_neutrals) > 0:
            norm_factor = sum([self.params["range"]-item[1] for item in sorted_neutrals]) + EPS
            assert(norm_factor>0)
            for index in [0, 1]:
                vec_neutral[index] = sum([item[0][index]*(self.params["range"]-item[1])/(item[1]+EPS) for item in sorted_neutrals])
                vec_neutral[index] /= norm_factor
        
        h_f = self.params["hunter_factor"]
        f_f = self.params["fear_factor"]
        n_f = self.params["neutral_factor"]
        final_vec = [0, 0]
        for index in [0, 1]:
            final_vec[index] = (f_f*vec_fear[index] + h_f*vec_hunt[index] + n_f*vec_neutral[index])/ (f_f + h_f + n_f)
        if final_vec[0] == 0 and final_vec[1] == 0:
            return
        if abs(final_vec[1]) < 1e-15:
            if final_vec[0] > 0:
                self.angle = 0 
            else:
                self.angle = pi
        else:
            angle = atan(abs(final_vec[0])/abs(final_vec[1]))
            if final_vec[1] > 0:
                angle = pi - angle
            if final_vec[0] < 0:
                angle = -angle
            self.angle = angle
