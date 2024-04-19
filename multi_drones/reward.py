
import numpy as np
from utils.calculation_utils import yaw_diff_nomalized
from utils.airsim_plotting import draw_text
from utils.airsim_utils import to_vec3r
import math
from rich import print
import os
import datetime
now = datetime.datetime.now()
formatted_datetime = now.strftime("%d.%m.%y-%H%M")

# reward as a result of taking actions
def computeReward(client, distance_before, distance_now, goal_rad, cur_pry, cur_pos, client_id):
    #r = -2.0 # for doing nothing
    r = 0
    
    track_diff = abs(yaw_diff_nomalized(cur_pry[2], goal_rad)) # track_diff [0, pi]

    distance_diff = distance_before - distance_now # if closer + , further -

    yaw_rew = yaw_reward_2(track_diff)
    # dis_rew = distance_reward(distance_diff, 10, distance_now)

    color = {
        0: "red",
        1: "green",
        2: "blue",
        3: "yellow",
        4: "cyan",
        5: "magenta",
        6: "blue3",
        7: "blue_violet",
        8: "light_slate_grey",
        9: "deep_pink4" 
    }
    
    rew_breakdown = f"[{color[client_id]}]  track_diff:  {track_diff} yaw_reward: {yaw_rew} dis_diff : {distance_diff} [/{color[client_id]}]]"

    # print("track_diff:  ", track_diff, "yaw_reward: ", yaw_rew)
    print(rew_breakdown)

    r +=  yaw_rew
    r +=  10*distance_diff

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
   

    if abs(distance_now - distance_before) < 0.001:
        r = r - 1.0
        print(str(client_id)+"not moving  -1  ")
    folder_path = r"C:\Users\noppa\Documents\GitHub\AI_logs\rewLogs\\" + formatted_datetime + "\\"

    """ # Create the folder if it doesn't exist
    try:
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created successfully.")
    except FileExistsError:
        print(f"Folder '{folder_path}' already exists.")

    # Define the data dictionary
    data = {
        "distance_diff": [distance_diff],
        "before_track_diff": [before_track_diff],
        "after_track_diff": [after_track_diff],
        "distance_reward": [distance_rew],
        "yaw_reward": [yaw_rew],
        "reward": [r]
    }

    # Construct the file path
    log_dir = folder_path + "data" + str(client_id) + ".xlsx"

    # Check if the file exists
    if not os.path.exists(log_dir):
        # Create a new DataFrame with the data
        df = pd.DataFrame(data)
        # Write the DataFrame to an Excel file
        df.to_excel(log_dir, index=False)
        print(f"Excel file '{log_dir}' created successfully.")
    else:
        # Read the existing Excel file into a DataFrame
        existing_df = pd.read_excel(log_dir)
        print(f"Excel file '{log_dir}' already exists.")
        # Create a new DataFrame with the data
        new_df = pd.DataFrame(data)
        # Concatenate the existing DataFrame and the new DataFrame
        df = pd.concat([existing_df, new_df], ignore_index=True)

        # Write the concatenated DataFrame back to the Excel file
        df.to_excel(log_dir, index=False)
        print(f"Data appended to '{log_dir}' successfully.") """
    return r 


def yaw_reward(diff):
    return (-20/np.pi)*diff +10

def yaw_reward_2(diff):
    return -5*(diff**2)+10
