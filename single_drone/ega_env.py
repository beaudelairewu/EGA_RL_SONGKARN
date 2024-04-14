import gymnasium as gym
from gymnasium import spaces
import numpy as np
import airsim
from rich import print

from utils.get_depth_image import getScreenDepth
from reward import computeReward

from utils.airsim_utils import (
    airsim_init,
    direction_based_navigation_2D,
    get_current_position,
    get_pitch_roll_yaw, 
    airsim_setpose
)
from utils.calculation_utils import (
    is_out_of_box,
    goal_direction_2d,
    distance_3d, 
    spawn_random_position_xy,
    normalize_action
)
from utils.log_utils import episodeLog_to_file
from utils.airsim_plotting import draw_actionRad_goalRad_2D, draw_direction_arrow_2D


class EgaEnv(gym.Env):
    def __init__(self, log_dir):

        #configurations
        self.log_dir = log_dir
        self.vehicle_name = "Drone0"
        self.client = airsim.MultirotorClient()
        airsim_init(self.vehicle_name)
        self.box_min = (-39.5, -39.5, 1.6)
        self.box_max = (39.5, 39.5, -40)
        self.start, self.goal = self.reset_start(self.box_min, self.box_max)
        
        self.observation_space = spaces.Dict({
            "depth_image": spaces.Box(low=0, high=255, shape=(56, 100, 1), dtype=np.uint8), 
            "distance_from_goal": spaces.Box(low=0, high=np.inf, shape=(1,), dtype=np.float32),
            # "goal_position":  spaces.Box(low=-np.inf, high=np.inf, shape=(3,), dtype=np.float32), 
            "current_position": spaces.Box(low=-np.inf, high=np.inf, shape=(3,), dtype=np.float32), 
            "current_yaw": spaces.Box(low=-3.14, high=3.14, shape=(1,), dtype=np.float32), #radian get_pitch_roll_yaw
            "goal_direction" : spaces.Box(low=-3.14, high=3.14, shape=(1,), dtype=np.float32) # yaw angle that points to goal (radian) goal_direction_2d
        })
        
        self.action_space = spaces.Box( 
            low=np.array([-1, -1, -1]),  # low=np.array([-3.14, 3, 1]) vx, vy, duration
            high=np.array([1, 1, 1])    # high=np.array([3.14, 5, 3]) 
        )
        
        self.state = {}
        self.episodeLog = {}
        self.episodeN = 0
        self.stepN = 0
        self.log_ep = 0 
        self.reset_state(self.start, self.goal)
        self.reset_episode_log(self.state, self.start)
        
        
    def reset(self, seed=None):
        print(f"resetting env ------------------------ {self.vehicle_name}----------------------------")
        airsim_setpose(self.client, self.start, self.vehicle_name)
        self.reset_state(self.start, self.goal)
        episodeLog_to_file(f"{self.episodeLog}", self.log_dir, self.vehicle_name, self.log_ep, self.episodeN)
        self.reset_episode_log(self.state, self.start)
        self.log_ep += 1
        self.episodeN += 1
        
        return self.state, self.state
    
    def step(self, action):
        # turn [-1,1] to real range
        action = normalize_action(action)

        #get distance before taking action
        cur_pos1 = get_current_position(self.client, self.vehicle_name)
        distance1 = distance_3d(cur_pos1, self.goal)

        #take action
        collisionInfo = direction_based_navigation_2D(self.client, self.vehicle_name, action) #observation as a result of taking an action
                
        #get observations after taking action
        depth_im, skip = getScreenDepth(self.client, self.vehicle_name)
        cur_pos = get_current_position(self.client, self.vehicle_name)
        cur_pry = get_pitch_roll_yaw(self.client, self.vehicle_name)
        goal_rad = goal_direction_2d(self.goal, cur_pos, cur_pry)
        distance2 = distance_3d(cur_pos, self.goal)
        
        #draw current yaw and goal's direction
        draw_direction_arrow_2D(self.client, cur_pry, goal_rad, cur_pos)

        #check if drone is out of training area
        out_of_box = is_out_of_box(cur_pos, self.box_min, self.box_max)
        
        #compute reward as a result of taking action
        if collisionInfo.has_collided:
            done = True
            reward = -200.0
            print(f"collided")
            print(f"object:     {collisionInfo.object_name}")
        elif out_of_box:
            print("out of box")
            done = True
            reward = -0
        else:
            done = False
            #compute reward here
            reward = computeReward(self.client, distance1, distance2, goal_rad, cur_pry, cur_pos)
            # print(f"distance_from_goal:  {distance}     ")
            # print(f"reward_step:  {reward}      ")
            # print(f"step  {self.stepN}")

        if distance2 < 3:
            print("Yehhhhhhhhhh you've done it!")
            done = True
            reward = 1200
        
            
        self.addToLog('reward', float(reward))
        self.addToLog('action', list(action))
        self.addToLog('distance_from_goal', float(distance2))
        self.addToLog('current_position', list(cur_pos))
        self.addToLog('current_pry', list(cur_pry))
        self.addToLog('goal_direction', float(goal_rad))

        
        self.state = {
            'depth_image' : depth_im, #np array float32
            "distance_from_goal": np.array([distance2], dtype=np.float32),
            # "goal_position": np.array(self.goal, dtype=np.float32),
            "current_position": np.array(cur_pos, dtype=np.float32),
            "current_yaw": np.array([cur_pry[2]], dtype=np.float32),
            "goal_direction": np.array([goal_rad], dtype=np.float32)
        }
        
               
        return self.state, float(reward), done, False, self.state
            
    def reset_state(self, start, goal):
        self.state = {
                'depth_image' : np.zeros((56, 100, 1), dtype=np.uint8),  
                'distance_from_goal' : np.array([distance_3d(start, goal)], dtype=np.float32),
                # "goal_position": np.array(goal, dtype=np.float32), 
                'current_position': np.array(start, dtype=np.float32),
                "current_yaw": np.array([0.0], dtype=np.float32), 
                "goal_direction": np.array([goal_direction_2d(goal, start, (0,0,0))], dtype=np.float32)
        }

    def reset_episode_log(self, state, start):
        self.episodeLog = {
            "episodeN": self.episodeN,
            "reward": [0],
            "action": [[0.0, 0.0, 0.0, 0.0]],
            "distance_from_goal": [float(state['distance_from_goal'])],
            "current_position": [list(start)],
            "current_pry": [[0,0,0]], #rad rad rad
            "goal_direction": [list(state["goal_direction"])], #rad
            "start_goal": [list(self.start), list(self.goal)]
        }

    def addToLog(self, key, value):
            if key not in self.episodeLog:
                self.episodeLog[key] = []
            self.episodeLog[key].append(value)
            
    def reset_start(self, box_min, box_max):
        a, b = spawn_random_position_xy(box_min, box_max)
        c, d = spawn_random_position_xy(box_min, box_max)
        start = (0, 0, -4.0)
        goal = (38, 38, -4.0)
        
        return start, goal