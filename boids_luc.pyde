from boid import Boid
from environment import Environment
import time
from globals import *
from math import pi

list_of_boids = []
for type in [BLUE_TYPE, RED_TYPE, GREEN_TYPE]:
    list_of_boids += [
        Boid(
            x=random(0, 1500),
            y=random(0, 900),
            angle=random(0, 2*pi),
            type=type, 
            inertia=random(0, 10)
        )
        for _ in range(100)
    ]
for b in list_of_boids:
    b.pregnant = False
    
env = Environment(list_of_boids)

def setup():
  size(1500, 900)
  frameRate(24)
  
def draw():
  background(0)
  env.evolve()
  smooth()
