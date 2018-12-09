from math import sin, cos, pi
from globals import *

def generate_random_params():
    return {
        "range": random(20, 50),
        "n_max_neighbors": int(random(1, 5)),
        "fear_factor": random(0, 1),
        "hunter_factor": random(0, 1),
        "inertia_factor": random(0, 2)
    }

class Boid:
    
    def __init__(self, x, y, angle, type, params=generate_random_params() ,inertia=0):
        self.x = x
        self.y = y
        self.type = type
        self.angle = angle
        self.inertia = inertia
        self.pregnant = False
        self._col = TYPE_TO_COLOR[self.type]
        self.params = params
        
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
        x_diff = self.inertia*sin(self.angle)
        y_diff = -self.inertia*cos(self.angle)
        self.x += x_diff
        self.y += y_diff
        self.stay_in_range()
        pushMatrix()
        translate(self.x, self.y)
        fill(self._col[0], self._col[1], self._col[2])
        rotate(self.angle)    
        beginShape(TRIANGLES)
        vertex(0, -radius*2)
        vertex(-radius, radius*2)
        vertex(radius, radius*2)
        endShape();
        popMatrix()
        
    def give_birth(self):
        assert(self.pregnant)
        babies = []
        if random(0, 2) < 1:
            params = self.params
            inertia = self.inertia
        else:
            params = generate_random_params()
            inertia = random(1, 10)
        baby_boid = Boid(self.x,
                        self.y,
                        random(-pi, pi),
                        self.type,
                        params,
                        inertia)
        self.pregnant = False
        return [baby_boid]

    def special_action(self, other_boids):
        births = []
        death = []
        if self.pregnant and random(0, 10) < 1:
            births = self.give_birth()
            
        #TODO : optimize this with a KDTree
        for boid in other_boids:
            if all([distance(boid, self) < radius,
                    is_hunted(self.type, boid.type)]):
                self.pregnant = True
                death += [boid]
        return births, death
        
    def update_params(self, environment):
        if self.angle > pi or self.angle < -pi:
            print('error', self.angle)
        # Get features from the neighbors hunters and preys
        # Features are composed of distances and angles
        hunters = [
            boid for boid in environment.list_of_boids
            if distance(boid, self) < self.params["range"] and is_hunted(boid.type, self.type)
        ]
        preys = [
            boid for boid in environment.list_of_boids
            if distance(boid, self) < self.params["range"] and is_hunted(self.type, boid.type)
        ]
        hunters_distances_and_angles = [
            (distance(boid, self), compute_relative_angle(boid.x, boid.y, self.x, self.y))
             for boid in hunters
        ]
        preys_distances_and_angles = [
            (distance(boid, self), compute_relative_angle(self.x, self.y, boid.x, boid.y))
             for boid in preys
        ]
        # Only consider the n_max_neighbors closest ones
        hunters_distances_and_angles = sorted(hunters_distances_and_angles, key=lambda x:x[0])[:self.params["n_max_neighbors"]]
        preys_distances_and_angles = sorted(preys_distances_and_angles, key=lambda x:x[0])[:self.params["n_max_neighbors"]]
        # Easy function for begining :
        barycenter_fear = None
        barycenter_hunt = None
        if len(hunters) > 0:
            barycenter_fear = sum([item[1]*(self.params["range"]-item[0]) for item in hunters_distances_and_angles])
            barycenter_fear /= sum([self.params["range"]-item[0] for item in hunters_distances_and_angles])
        if len(preys) > 0:
            barycenter_hunt = sum([item[1]*(self.params["range"]-item[0]) for item in preys_distances_and_angles])
            barycenter_hunt /= sum([self.params["range"]-item[0] for item in preys_distances_and_angles])
        h_f = self.params["hunter_factor"]
        f_f = self.params["fear_factor"]
        i_f = self.params["inertia_factor"]
        new_angle = self.angle
        if barycenter_fear and barycenter_hunt and f_f*h_f > 0:
            new_angle = (barycenter_hunt*h_f + barycenter_fear*f_f)/(h_f + f_f)
        elif barycenter_fear and f_f > 0:
            new_angle = barycenter_fear
        elif barycenter_hunt and h_f > 0:
            new_angle = barycenter_hunt
        assert(-pi<new_angle<pi)
        assert(-pi<self.angle<pi)
        self.angle = (new_angle + self.angle*self.params["inertia_factor"])/(1 + self.params["inertia_factor"])
