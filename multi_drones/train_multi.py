
from ega_env import EgaEnv
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.vec_env import SubprocVecEnv, DummyVecEnv
from stable_baselines3.ppo import PPO
from stable_baselines3.common.callbacks import CheckpointCallback
from stable_baselines3.common.logger import configure

import datetime
import os
import sys
import argparse

def config_new_train():
    now = datetime.datetime.now()
    formatted_datetime = now.strftime("%d.%m.%y-%H%M") #02.04.24-10:35 
    try:
        os.mkdir(f'train/{formatted_datetime}')  
        os.mkdir(f'train/{formatted_datetime}/logs{formatted_datetime}')
        os.mkdir(f'train/{formatted_datetime}/checkpoints')
    except FileExistsError:
        print("Directory already exists")
        sys.exit()
        
    tmp_path = f"train/{formatted_datetime}/logs{formatted_datetime}"
    new_logger = configure(tmp_path, ["stdout", "csv", "tensorboard"])
    
    checkpoint_callback = CheckpointCallback(
        save_freq=50,
        save_path=f"./train/{formatted_datetime}/checkpoints",
        name_prefix=f"{formatted_datetime}",
        save_replay_buffer=False,
        save_vecnormalize=False
    )
    envs = SubprocVecEnv([lambda: EgaEnv(0, formatted_datetime), lambda: EgaEnv(1, formatted_datetime), lambda: EgaEnv(2, formatted_datetime)])
    model = PPO("MultiInputPolicy", envs, n_steps=2048, batch_size=64)
    model.set_logger(new_logger)
        
    return model, checkpoint_callback

def config_continue_train(date_time, envs):
    try:
        os.mkdir(f'train/{date_time}/logs{date_time}')
    except FileExistsError:
        print("Directory already exists")
        
    tmp_path = f"train/{date_time}/logs{date_time}"
    files = os.listdir(f"train/{date_time}/checkpoints")
    model_path = f"train/{date_time}/checkpoints/{files[-1]}" #select the last model
    try:
        model = PPO.load(model_path, envs, n_steps=2048, batch_size=64) #n_step=2048 64
    except:
        "date time incorrect"
        sys.exit()
        
    new_logger = configure(tmp_path, ["stdout", "csv", "tensorboard"])

    checkpoint_callback = CheckpointCallback(
    save_freq=5000,
    save_path=f"./train/{date_time}/checkpoints",
    name_prefix=f"{date_time}",
    save_replay_buffer=False,
    save_vecnormalize=False
    )
    
    model.set_logger(new_logger)
    
    return model, checkpoint_callback
 
# check_env(EgaEnv(0))

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--con_train", type=str, help="Continue Training")
args = parser.parse_args()

if __name__ == "__main__":
    date_time = args.con_train
    if date_time != None:
        envs = SubprocVecEnv([lambda: EgaEnv(0, date_time), lambda: EgaEnv(1, date_time), lambda: EgaEnv(2, date_time)])
        model, checkpoint_callback = config_continue_train(date_time, envs)
    else:
        model, checkpoint_callback = config_new_train()

    model.learn(total_timesteps=1500000, progress_bar=True, callback=checkpoint_callback, reset_num_timesteps=False)