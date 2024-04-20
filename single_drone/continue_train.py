
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

continue_from = "cur1_1304_325000_steps"
pref = continue_from.split("_")[0]

base_dir = "/Users/EGA/Documents/AI_logs/"
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
  save_freq=5000,
  save_path="/Users/EGA/Documents/AI_logs/checkpoints",
  name_prefix="cur1_1304",
  save_replay_buffer=False,
  save_vecnormalize=False,
)


model_path = os.path.join(base_dir, "checkpoints",  continue_from)

if __name__ == "__main__":
        # model = PPO("MultiInputPolicy", envs, n_steps=1024, batch_size=64) #n_steps=2048, batch_size=64)
    model = PPO.load(model_path, EgaEnv(dir), verbose=1, n_steps=2048, batch_size=512)
    model.set_logger(new_logger)
    model.learn(total_timesteps=1500000, progress_bar=True, callback=checkpoint_callback, reset_num_timesteps=False)
