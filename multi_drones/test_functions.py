import airsim
from utils.airsim_utils import direction_based_navigation_2D, get_current_position, get_pitch_roll_yaw
from utils.airsim_plotting import draw_direction_arrow_2D, draw_actionRad_goalRad_2D
from utils.calculation_utils import normalize_action, directional_angle

client = airsim.MultirotorClient()
client.enableApiControl(True)
client.takeoffAsync().join()

goal = (-10,10,-4)

cur_pry = get_pitch_roll_yaw(client, "")
cur_pos = get_current_position(client, "")

action = [0.5,-1,1]
action = normalize_action(action)
print(f"normalized {action}")
goal_rad = directional_angle(cur_pos, goal)
draw_actionRad_goalRad_2D(client, cur_pos, action[0], goal_rad)
direction_based_navigation_2D(client, "", action)
