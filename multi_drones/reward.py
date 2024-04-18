
import numpy as np
from utils.calculation_utils import yaw_diff_nomalized
from utils.airsim_plotting import draw_text
from utils.airsim_utils import to_vec3r
import math
from rich import print

# reward as a result of taking actions
def computeReward(client, episodeLog, distance_before, distance_now, goal_rad, cur_pry, bef_pry, cur_pos):
    r = 0
    distance_before = episodeLog['distance_from_goal'][-1]

    before_track_diff = abs(yaw_diff_nomalized(bef_pry[2], goal_rad)) # track_diff [0, pi]
    after_track_diff = abs(yaw_diff_nomalized(cur_pry[2], goal_rad)) # track_diff [0, pi]

    distance_diff = distance_before - distance_now # if closer + , further -

    yaw_rew = yaw_reward(before_track_diff,after_track_diff)
    distance_rew = 10 * distance_diff - distance_now

    # dis_rew = distance_reward(distance_diff, 10, distance_now)

    r +=  yaw_rew
    r +=  distance_rew

    if abs(distance_now - distance_before) < 0.001:
        r = r - 1.0
        print("not moving  -1  ")

    return r 


def yaw_reward(before_track_diff, after_track_diff):
    #sub-reward from getting closer to 0 degree
    before = -5*before_track_diff**2+10
    after = -5*after_track_diff**2+10
    #see for improvement
    return after+0.5*(after-before)