# import numpy as np

# from calculation_utils import (
#     spawn_random_position_xy,
#     distance_3d,
#     is_out_of_box,
#     goal_direction_2d,
#     yaw_diff_nomalized
# )
# from airsim_utils import (
#     get_current_position,
#     get_pitch_roll_yaw,
# )

# def reset_state(start, goal):
#     state = {
#             'depth_image' : np.zeros((56, 100, 1), dtype=np.uint8),  
#             'distance_from_goal' : distance_3d(start, goal),
#             "goal_position": goal, 
#             'current_position': start,
#             "current_yaw": 0.0, 
#             "goal_direction": goal_direction_2d(goal, start, 0)
#     }
#     return state

# def reset_episode_log(state, start):
#     episodeLog = {
#             'reward': [0],
#             'action': [[0.0, 0.0, 0.0, 0.0]],
#             'distance_from_goal': [state['distance_from_goal']],
#             "current_position": [start],
#             'current_yaw': [state['current_yaw']], #rad
#             "goal_direction": [state["goal_direction"]] #rad
#         }
#     return episodeLog

# def addToLog(key, value, episodeLog):
#         if key not in episodeLog:
#             episodeLog[key] = []
#         episodeLog[key].append(value)
        
# def reset_start(box_min, box_max):
#     a, b = spawn_random_position_xy(box_min, box_max)
#     c, d = spawn_random_position_xy(box_min, box_max)
#     start = (a, b, -4.0)
#     goal = (c, d, -4.0)
    
#     return start, goal