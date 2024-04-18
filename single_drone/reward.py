
import numpy as np
from utils.calculation_utils import yaw_diff_nomalized
from utils.airsim_plotting import draw_text
from utils.airsim_utils import to_vec3r
import math

# reward as a result of taking actions
def computeReward(client, distance_before, distance_now, goal_rad, cur_pry, cur_pos):
    #r = -2.0 # for doing nothing
    r = 0
    
    track_diff = abs(yaw_diff_nomalized(cur_pry[2], goal_rad)) # track_diff [0, pi]

    distance_diff = distance_before - distance_now # if closer + , further -

    yaw_rew = yaw_reward(track_diff)
    # dis_rew = distance_reward(distance_diff, 10, distance_now)

    print("track_diff:  ", track_diff)

    r += yaw_rew*2
    r +=  10*distance_diff

    if abs(distance_now - distance_before) < 0.001:
        r = r - 1.0
        print("not moving  -1  ")

    return r 


def yaw_reward(diff):
    return (-20/np.pi)*diff +10
