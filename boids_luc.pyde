from boid import Boid
from environment import Environment
import time
from globals import *
from math import pi

list_of_boids = []
for type in [BLUE_TYPE, RED_TYPE, GREEN_TYPE]:
    list_of_boids += [
        Boid(
            x=random(0, SIZE_X),
            y=random(0, SIZE_Y),
            angle=random(-pi, pi),
            type=type, 
            inertia=5
        )
        for _ in range(20)
    ]
    
env = Environment(list_of_boids)

def setup():
  size(1500, 900)
  frameRate(24)
  
def draw():
  background(0)
  env.evolve()
  smooth()
