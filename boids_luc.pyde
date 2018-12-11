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
            type=type
        )
        for _ in range(50)
    ]
    
env = Environment(list_of_boids)

def setup():
  size(SIZE_X, SIZE_Y)
  frameRate(24)
  
def draw():
  background(0)
  env.evolve()
  smooth()
  
def keyPressed():
    if (key == 'p'):
        env.print_stats()
    if (key == 'r'):
        env.list_of_boids+= [Boid(
            x=mouseX,
            y=mouseY,
            angle=random(-pi, pi),
            type=RED_TYPE
        )]
    if (key == 'g'):
        env.list_of_boids+= [Boid(
            x=mouseX,
            y=mouseY,
            angle=random(-pi, pi),
            type=GREEN_TYPE
        )]
    if (key == 'b'):
        env.list_of_boids+= [Boid(
            x=mouseX,
            y=mouseY,
            angle=random(-pi, pi),
            type=BLUE_TYPE
        )]
