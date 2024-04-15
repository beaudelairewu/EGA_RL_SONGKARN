from stable_baselines3 import PPO
from stable_baselines3.common.logger import configure
from stable_baselines3.common.callbacks import CheckpointCallback

from ega_env import EgaEnv
from utils.log_utils import make_episodeLog_folder

import os

dir = make_episodeLog_folder() #'/Users/noppa/Documents/AI_logs/02.04.24-1035 '

tmp_path = os.path.join(dir, "infoLogs")
new_logger = configure(tmp_path, ["stdout", "csv", "tensorboard"])


# Save a checkpoint every 1000 steps
checkpoint_callback = CheckpointCallback(
  save_freq=5000,
  save_path="/Users/noppa/Documents/AI_logs/checkpoints",
  name_prefix="cur1_1304",
  save_replay_buffer=False,
  save_vecnormalize=False,
)

model = PPO("MultiInputPolicy", EgaEnv(dir), verbose=1, n_steps=2048, batch_size=64)#, tensorboard_log="/Users/noppa/Documents/AI_logs/tensorboard") #tensorboard_log="ppo_cur1_tensorboard"
# model = PPO.load("checkpoints/cur1_2603_32508_steps", env=EgaEnv_Cur1())
model.set_logger(new_logger)
model.learn(total_timesteps=1000000, progress_bar=True, callback=checkpoint_callback)

