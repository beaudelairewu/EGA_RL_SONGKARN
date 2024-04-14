
import airsim
import math
import numpy as np

def draw_direct_path(client, start: tuple, goal: tuple):
    start = np.array(start)
    start[2] = start[2] #- 3
    goal = np.array(goal)
    goal[2] = goal[2] #- 3
    line_points = [[round(x, 5) for x in start + (goal - start) * t] for t in np.linspace(0, 1, 10)]
    vect3r_line_points = []
    for point in line_points:
        vect3r_line_points.append(airsim.Vector3r(x_val=point[0], y_val=point[1], z_val=point[2]))
    client.simPlotLineStrip(vect3r_line_points, is_persistent=False, duration=20, color_rgba=[1.0, 1.0, 1.0], thickness=1.0)
    return vect3r_line_points
def draw_actionRad_goalRad_2D(client, cur_pos, action_rad, goal_rad):
    x,y,z = cur_pos
    dax = math.cos(action_rad)
    day = math.sin(action_rad)
    dgx = math.cos(goal_rad)
    dgy = math.sin(goal_rad)
    
    a = airsim.Vector3r(x, y, z)
    vec_goal = airsim.Vector3r(x + dgx, y + dgy, z)
    vec_action = airsim.Vector3r(x + dax, y + day, z)

    client.simPlotArrows([a], [vec_goal], color_rgba=[0,1,0], duration=10)
    client.simPlotArrows([a], [vec_action], duration=10)
    
#passed 25.03.24
def draw_direction_arrow_2D(client, cur_pry, goal_rad, cur_pos):
    pitch, roll, yaw = cur_pry
    x,y,z = cur_pos
    dcx = math.cos(yaw)
    dcy = math.sin(yaw)
    dgx = math.cos(goal_rad)
    dgy = math.sin(goal_rad)

    a = airsim.Vector3r(x, y, z)
    vec_goal = airsim.Vector3r(x + dgx, y + dgy, z)
    vec_cur_direc = airsim.Vector3r(x + dcx, y + dcy, z)

    client.simPlotArrows([a], [vec_goal], color_rgba=[0,1,0], duration=2)
    client.simPlotArrows([a], [vec_cur_direc], duration=2)

def draw_goal_position(client, goal_pos):
    vec = airsim.Vector3r(goal_pos[0], goal_pos[1], goal_pos[2])
    client.simPlotPoints([vec], color_rgba=[0.0, 1.0, 0.0, 1.0], size=20.0, duration=20.0, is_persistent=False)

def draw_text(client, texts: list, pos: list):
    client.simPlotStrings(texts, pos, color_rgba=[1.0,1.0,1.0,1.0], scale=1.2, duration=5)