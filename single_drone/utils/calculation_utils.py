import random
import numpy as np
import math


def normalize(x, _from: tuple, _to=(-1, 1)):
    return ((x - _from[0]) / (_from[1] - _from[0])) * (_to[1] - _to[0]) + _to[0]

def normalize_action(action):
    action[0] = normalize(action[0], (-1,1), (0,1)) #yaw
    action[1] = normalize(action[1], (-1,1), (0,1)) #speed
    action[2] = normalize(action[2], (-1,1), (0,1)) #duration
    action[3] = normalize(action[3], (-1,1), (0,1)) #duration
    return action

def is_out_of_box(now: tuple, min: tuple, max: tuple) -> bool:
    x_min, y_min, z_min = min
    x_max, y_max, z_max = max
    now_x, now_y, now_z = now
    if (x_min < now_x < x_max) and (y_min < now_y < y_max) and  (z_min > now_z > z_max) :
        return False
    else:
        return True

def spawn_random_position_xy(min_pos: tuple, max_pos: tuple, max_distance: float) -> tuple:
    x_min, y_min, z_min = min_pos
    x_max, y_max, z_max = max_pos
    
    while True:
        start_x = random.uniform(x_min, x_max)
        start_y = random.uniform(y_min, y_max)
        goal_x = random.uniform(x_min, x_max)
        goal_y = random.uniform(y_min, y_max)
        
        distance = math.sqrt((start_x - goal_x)**2 + (start_y - goal_y)**2)
        rounded_distance = round(distance, 2)
        
        if rounded_distance == round(max_distance, 2):
            return ((start_x, start_y, -4.0), (goal_x, goal_y, -4.0))

def distance_2d(point1: tuple, point2: tuple) -> float:
    x1, y1 = point1
    x2, y2 = point2
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

def distance_3d(point1: tuple, point2: tuple) -> float:
    x1, y1, z1 = point1
    x2, y2, z2 = point2
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2) ** 0.5 

def distance_point_to_line(point1, point2, point):
    point1 = np.array(point1)
    point2 = np.array(point2)
    point = np.array(point)

    line_direction = point2 - point1
    to_point = point - point1
    projection = np.dot(to_point, line_direction) / np.dot(line_direction, line_direction) * line_direction
    closest_point = point1 + projection
    distance = np.linalg.norm(point - closest_point)

    return distance

def directional_angle(current: tuple, goal: tuple) -> float:
    cur_x, cur_y, cur_z = current
    gol_x, gol_y, gol_z = goal

    diff_x = gol_x - cur_x
    diff_y = gol_y - cur_y

    directional_yaw_radians = math.atan2(diff_y, diff_x)
    directional_yaw_degrees = math.degrees(directional_yaw_radians)

    return directional_yaw_degrees

#tested 12.04.24
def yaw_diff_nomalized(cur_yaw, desired_yaw): # eg. 300 deg to 60 deg
    angle = desired_yaw - cur_yaw
    if angle > 3.14:
        angle -= 6.28
    elif angle < -3.14:
        angle += 6.28
    return angle

def goal_direction_2d(goal, cur_pos, cur_pry): # returns radian
    pitch, roll, yaw = cur_pry
    x, y, z = cur_pos
    delta_x = goal[0] - x
    delta_y = goal[1] - y
    direction_rad = math.atan2(delta_y, delta_x)
    dx = math.cos(direction_rad)
    dy = math.sin(direction_rad)
    # a = airsim.Vector3r(x,y,z)
    # b = airsim.Vector3r(x+dx, y+dy, z)
    # client.simPlotArrows([a], [b], is_persistent=True)

    return direction_rad


def goal_direction_3d(goal, cur_pos, cur_pry): # returns degree
    pitch, roll, yaw = cur_pry
    cur_x, cur_y, cur_z = cur_pos
    yaw = math.degrees(yaw)

    delta_x = goal[0] - cur_x
    delta_y = goal[1] - cur_y
    delta_z = goal[2] - cur_z

    pos_angle = math.degrees(math.atan2(delta_y, delta_x))
    pos_angle = (pos_angle + 360) % 360

    # Calculate the 3D direction vector from the current position to the goal
    goal_direction = [delta_x, delta_y, delta_z]

    # Calculate the 3D angle between the current orientation and the goal direction
    track = math.degrees(math.acos(
        (goal_direction[0] * math.cos(math.radians(yaw)) +
        goal_direction[1] * math.sin(math.radians(yaw))) /
        (math.sqrt(delta_x ** 2 + delta_y ** 2 + delta_z ** 2))
    ))

    # Ensure the result is within the range [-180, 180)
    return ((track - 180) % 360) - 180
    