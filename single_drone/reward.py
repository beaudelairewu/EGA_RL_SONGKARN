
import numpy as np
from utils.calculation_utils import yaw_diff_nomalized
from utils.airsim_plotting import draw_text
from utils.airsim_utils import to_vec3r
import math

def computeReward(client, episodeLog, distance_now, goal_rad, cur_pry, cur_pos):
    r = -2.0 # for doing nothing

    distance_before = episodeLog['distance_from_goal'][-1]
    
    track_diff = abs(yaw_diff_nomalized(cur_pry[2], goal_rad))

    distance_diff = distance_before - distance_now # if closer + , further -

    yaw_rew = yo(track_diff)
    # dis_rew = distance_reward(distance_diff, 10, distance_now)

    rew_breakdown = {
        "yaw_diff": yaw_rew,
        "dis_diff": 5*distance_diff
    }

    r +=  yaw_rew
    r +=  5*distance_diff

    draw_text(
        client,
        [
            f"deg_diff: {math.degrees(track_diff)}", 
            f"rew:  {yaw_rew}",
            # f"dis_diff: {distance_diff}",
            # f"dis_rew:  {dis_rew}"
        ],
        [
            to_vec3r(cur_pos), 
            to_vec3r((cur_pos[0], cur_pos[1], cur_pos[2]+0.2)),
            # to_vec3r((cur_pos[0], cur_pos[1], cur_pos[2]+0.4)),
            # to_vec3r((cur_pos[0], cur_pos[1], cur_pos[2]+0.6)),

        ]
    )
   

    print(rew_breakdown)

    if abs(distance_now - distance_before) < 0.001:
        r = r - 1.0
        print("not moving  -1  ")

    return r 

# def yaw_reward(cur_pry, goal_rad):
#     # track_diff = (cur_pry[2] - goal_rad)
#     # if track_diff < -np.pi:
#     #     track_diff += 2 * np.pi  # Adjust for negative values 
#     #     track_diff = abs(track_diff)
#     # print(f"track_diff  {track_diff}")
#     track_diff = yaw_diff_nomalized(cur_pry[2], goal_rad)
    
#     print(linear_decrease(track_diff, 10, 0.5))
    

def linear_decrease(difference, max_rew, threshold=0.1):

    if difference <= threshold:
        reward = max_rew # Maximum reward if difference is very low
    else:
        # Linear decrease: Adjust the slope (1/threshold) for steeper/shallower decline
        reward =  max_rew - (difference - threshold) / threshold 

    return reward 

def yo(diff):
    return (-10/(0.5*np.pi))*diff + 10


def distance_reward(distance_diff, max_reward, distance_now):

    if distance_diff > 0:  # Moving closer to the goal
        reward = max_reward * (distance_diff / distance_now)  # Reward proportional to change
    else:  # Moving away or no change
        penalty_factor = 1
        reward = - penalty_factor * max_reward * abs(distance_diff) / distance_now

    return reward  # Ensure non-negative reward