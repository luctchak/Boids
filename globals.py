BLUE_TYPE = 0
RED_TYPE = 1
GREEN_TYPE = 2
EPS = 1e-15
SIZE_X = 500
SIZE_Y = 500
MAX_RANGE = 80
MAX_SPEED = 10

TYPE_TO_COLOR = {
  BLUE_TYPE: (0, 0 , 255),
  GREEN_TYPE: (0 , 255, 0),
  RED_TYPE: (255 , 0, 0)
}

radius = 5

# BLUE EATS RED
# RED EATS GREEN
# GREEN EATS BLUE

def hunts(type_hunter, type_prey):
    if type_hunter == type_prey:
        return False
    if type_hunter == BLUE_TYPE:
        return (type_prey == RED_TYPE)
    if type_hunter == RED_TYPE:
        return (type_prey == GREEN_TYPE)
    if type_hunter == GREEN_TYPE:
        return (type_prey == BLUE_TYPE)
    return False

def distance(b_1, b_2):
    vec = get_vector(b_1, b_2)
    return sqrt(vec[0]**2 + vec[1]**2)

def axis_diff(x_1, x_2, SIZE):
    diff = x_1 - x_2
    if diff < -SIZE/2:
        diff += SIZE
    if diff > SIZE/2:
        diff -= SIZE
    return diff
    
def get_vector(b_1, b_2):
    return [
        axis_diff(b_1.x, b_2.x, SIZE_X), 
        axis_diff(b_1.y, b_2.y, SIZE_Y)
    ]
