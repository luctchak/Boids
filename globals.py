BLUE_TYPE = 0
RED_TYPE = 1
GREEN_TYPE = 2

SIZE_X = 500
SIZE_Y = 500

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

def dist_axis(x_1, x_2, SIZE):
    return min((x_1 - x_2)**2, (x_1 - x_2 + SIZE_X)**2, (x_1 - x_2 - SIZE)**2)

def distance(b_1, b_2):
    x_d = dist_axis(b_1.x, b_2.x, SIZE_X)
    y_d = dist_axis(b_1.y, b_2.y, SIZE_Y)
    return sqrt(x_d + y_d)

def compute_relative_angle(x_s, y_s, x_t, y_t):
    if abs(x_s - x_t) > SIZE_X/2:
        if x_s < x_t:
            x_s += SIZE_X
        else:
            x_t += SIZE_X
    if abs(y_s - y_t) > SIZE_Y/2:
        if y_s < y_t:
            y_s += SIZE_Y
        else:
            y_t += SIZE_Y
    if abs(y_t - y_s) < 1e-15:
        return 0
    return atan((x_t - x_s)/(y_s - y_t))
