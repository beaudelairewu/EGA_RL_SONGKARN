
import numpy as np
from utils.calculation_utils import yaw_diff_nomalized
from utils.airsim_plotting import draw_text
from utils.airsim_utils import to_vec3r
import math
from rich import print

def computeReward(client, episodeLog, distance_now, goal_rad, cur_pry, cur_pos, client_id):
    r = -2.0 # for doing nothing

    distance_before = episodeLog['distance_from_goal'][-1]
    
    track_diff = abs(yaw_diff_nomalized(cur_pry[2], goal_rad))

    distance_diff = distance_before - distance_now # if closer + , further -

    yaw_rew = linear_decrease(track_diff)
    # dis_rew = distance_reward(distance_diff, 10, distance_now)

    rew_breakdown = {
        "yaw_diff": yaw_rew,
        "dis_diff": distance_diff
    }
    color = {
        0: "red",
        1: "green",
        2: "blue"
    }
    
    rew_breakdown = f"[{color[client_id]}]  yaw_diff: {yaw_rew}, dis_diff : {distance_diff} [/{color[client_id]}]]"

    r +=  yaw_rew
    r +=  distance_diff

    # draw_text(
    #     client,
    #     [
    #         f"deg_diff: {math.degrees(track_diff)}", 
    #         f"rew:  {yaw_rew}",
    #         # f"dis_diff: {distance_diff}",
    #         # f"dis_rew:  {dis_rew}"
    #     ],
    #     [
    #         to_vec3r(cur_pos), 
    #         to_vec3r((cur_pos[0], cur_pos[1], cur_pos[2]+0.2)),
    #         # to_vec3r((cur_pos[0], cur_pos[1], cur_pos[2]+0.4)),
    #         # to_vec3r((cur_pos[0], cur_pos[1], cur_pos[2]+0.6)),
    #     ]
    # )
   

    print(rew_breakdown)

    if abs(distance_now - distance_before) < 0.001:
        r = r - 1.0
        print("not moving  -1  ")

    return r 



def linear_decrease(diff):
    return (-10/(0.5*np.pi))*diff + 10
