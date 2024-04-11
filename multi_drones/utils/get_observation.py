# from airsim_utils import (
#     get_current_position,
#     get_current_orientation
# )

# from calculation_utils import (
#     goal_direction_2d,
#     distance_3d
# )

# def get_observations(client, vehicle_name, goal):
#     cur_pos = get_current_position(client, vehicle_name)
#     cur_pry = get_current_orientation(client, vehicle_name)
#     goal_rad = goal_direction_2d(goal, cur_pos, cur_pry)
#     distance = distance_3d(cur_pos, goal)
#     return distance, cur_pos, cur_pry, goal_rad