
from ega_env import EgaEnv
# from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.vec_env import SubprocVecEnv
from stable_baselines3.ppo import PPO
from stable_baselines3.common.callbacks import CheckpointCallback
from stable_baselines3.common.logger import configure
from stable_baselines3.common.vec_env import VecMonitor 

import datetime
import os
import sys



base_dir = "/Users/noppa/Documents/AI_logs/multi_train"
now = datetime.datetime.now()
formatted_datetime = now.strftime("%d.%m.%y-%H%M") #02.04.24-1035 
dir = os.path.join(base_dir, formatted_datetime)

try:
    os.mkdir(dir)
    os.mkdir(os.path.join(dir, "episodeLogs"))
    os.mkdir(os.path.join(dir, "checkpoints"))
    os.mkdir(os.path.join(dir, "infoLogs"))
except:
    print('dir exists')

tmp_path = os.path.join(dir, "infoLogs")
new_logger = configure(tmp_path, ["stdout", "csv", "tensorboard"])

checkpoint_callback = CheckpointCallback(
    save_freq=400,
    save_path= os.path.join(dir, "checkpoints"),
    name_prefix=f"{formatted_datetime}",
    save_replay_buffer=False,
    save_vecnormalize=False
)

if __name__ == "__main__":
    envs = SubprocVecEnv([
        lambda: EgaEnv(0, formatted_datetime), 
        lambda: EgaEnv(1, formatted_datetime), 
        lambda: EgaEnv(2, formatted_datetime), 
        lambda: EgaEnv(3, formatted_datetime), 
        lambda: EgaEnv(4, formatted_datetime), 
        lambda: EgaEnv(5, formatted_datetime), 
        lambda: EgaEnv(6, formatted_datetime), 
        lambda: EgaEnv(7, formatted_datetime),
        lambda: EgaEnv(8, formatted_datetime), 
        lambda: EgaEnv(9, formatted_datetime)
        ])
    envs = VecMonitor(envs, os.path.join(dir, "infoLogs"))
    model = PPO("MultiInputPolicy", envs, n_steps=2048, batch_size=64, ent_coef=0.01) #n_steps=2048, batch_size=64)
    model.set_logger(new_logger)
    model.learn(total_timesteps=1500000, progress_bar=True, callback=checkpoint_callback, reset_num_timesteps=False)