from math import sin, cos
from globals import *

def generate_random_params():
    n_max_neighbors = int(random(5, 21))
    return {
        "range": random(20, 100),
        "n_max_neighbors": n_max_neighbors,
        "fear_factor": random(0, 1),
        "hunter_factor": random(0, 1)
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
        n_babies = int(random(1, 4))
        babies = []
        for _ in range(n_babies):
            if random(0, 10) < 9:
                son_decision_function = self.decision_function
            else:
                son_decision_function = generate_random_params()
            baby_boid = Boid(self.x,
                             self.y,
                             random(0, 2*pi),
                             self.type,
                             random_decision_func_generator(),
                             random(0, 1))
            babies.append(baby_boid)
        self.pregnant = False
        return babies

    def special_action(self, environment):
        if self.pregnant and random(0, 10) < 1:
            environment.list_of_boids += self.give_birth()
        #TODO : optimize this with a KDTree
        new_list_of_boids = []
        for boid in environment.list_of_boids:
            if all([distance(boid, self) < radius,
                    is_hunted(self.type, boid.type)]):
                print('eated')
                boid.pregnant = True
                print(len(environment.list_of_boids))
                continue
            new_list_of_boids.append(boid)
        environment.list_of_boids = new_list_of_boids
        
    def update_params(self, environment):
        # Get features from the neighbors hunters and preys
        # Features are composed of distances and angles
        hunters = [
            boid for boid in environment.list_of_boids
            if distance(boid, self) < self.params["range"] and is_hunted(self.type, boid.type)
        ]
        preys = [
            boid for boid in environment.list_of_boids
            if distance(boid, self) < self.params["range"] and is_hunted(boid.type, self.type)
        ]
        hunters_distances_and_angles = [
            (distance(boid, self), compute_relative_angle(boid.x, boid.y, self.x, self.y, self.angle))
             for boid in hunters
        ]
        preys_distances_and_angles = [
            (distance(boid, self), compute_relative_angle(boid.x, boid.y, self.x, self.y, self.angle))
             for boid in preys
        ]
        # Only consider the n_max_neighbors closest ones
        hunters_distances_and_angles = sorted(hunters_distances_and_angles, key=lambda x:x[0])[:self.params["n_max_neighbors"]]
        preys_distances_and_angles = sorted(hunters_distances_and_angles, key=lambda x:x[0])[:self.params["n_max_neighbors"]]
        # Easy function for begining :
        barycenter_fear = None
        barycenter_hunt = None
        if len(hunters) > 0:
            barycenter_fear = sum([item[0]*(self.params["range"]-item[1]) for item in hunters_distances_and_angles])
            barycenter_fear /= sum([self.params["range"]-item[1] for item in hunters_distances_and_angles])
        if len(preys) > 0:
            print(len(preys))
            print(len(preys_distances_and_angles))
            print(preys_distances_and_angles)
            barycenter_hunt = sum([item[1]*(self.params["range"]-item[0]) for item in preys_distances_and_angles])
            barycenter_hunt /= sum([self.params["range"]-item[0] for item in preys_distances_and_angles])
        h_f = self.params["hunter_factor"]
        f_f = self.params["fear_factor"]
        if barycenter_fear and barycenter_hunt:
            self.angle = barycenter_hunt*h_f + barycenter_fear*f_f/(h_f + f_f)
        elif barycenter_fear:
            self.angle = barycenter_fear
        elif barycenter_hunt:
            self.angle = barycenter_hunt
