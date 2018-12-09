BLUE_TYPE = 0
RED_TYPE = 1
GREEN_TYPE = 2

SIZE_X = 1500
SIZE_Y = 900

TYPE_TO_COLOR = {
  BLUE_TYPE: (0, 0 , 255),
  GREEN_TYPE: (0 , 255, 0),
  RED_TYPE: (255 , 0, 0)
}

radius = 5

def is_hunted(type_hunter, type_prey):
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
	return sqrt((b_1.x - b_2.x)**2 + (b_1.y - b_2.y)**2)

def compute_relative_angle(x_s, y_s, x_t, y_t, angle):
    if abs(y_t - y_s) < 1e-15:
        return - angle
    return atan((x_t - x_s)/(y_t - y_s)) - angle
