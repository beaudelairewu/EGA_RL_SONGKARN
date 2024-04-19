from stable_baselines3.common.env_checker import check_env
from ega_env import EgaEnv

import datetime
import os

base_dir = "/Users/noppa/Documents/AI_logs/multi_train"
now = datetime.datetime.now()
formatted_datetime = now.strftime("%d.%m.%y-%H%M") #02.04.24-1035 
dir = os.path.join(base_dir, formatted_datetime)


try:
    os.mkdir(dir)
    os.mkdir(os.path.join(dir, "episodeLogs"))
    os.mkdir(os.path.join(dir, "checkpoints"))
except:
    print('dir exists')

    
check_env(EgaEnv(0, dir))