import airsim
from utils.airsim_plotting import draw_direction_arrow_2D
from utils.calculation_utils import goal_direction_2d
from utils.airsim_utils import get_pitch_roll_yaw, get_current_position
import math

client = airsim.MultirotorClient()
client.enableApiControl(True)
client.takeoffAsync().join()
vehicle_name = "Drone0"

cur_pry = get_pitch_roll_yaw(client, vehicle_name)
cur_pos = get_current_position(client, vehicle_name)

client.rotateToYawAsync(3.14).join()

goals = [
    (39.5, 39.5, -4),
    (39.5, -39.5, -4),
    (-39.5, -39.5, -4),
    (-39.5, 39.5, -4)
]
for goal in goals:
    goal_rad = goal_direction_2d(goal, cur_pos, cur_pry)
    client.rotateToYawAsync(math.degrees(goal_rad)).join()
    new_pry = get_pitch_roll_yaw(client, vehicle_name)
    print(goal_rad, "    ", math.degrees(goal_rad), "   new_pry: ", new_pry)

    
    draw_direction_arrow_2D(client, cur_pry, goal_rad, cur_pos)
