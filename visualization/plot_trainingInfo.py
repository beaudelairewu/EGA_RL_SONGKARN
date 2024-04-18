import pandas as pd
from utils.plot_utils import plot_training_progress

path = "/Users/EGA/Documents/AI_logs/multi_train/17.04.24-1115/infoLogs/progress.csv"
df = pd.read_csv(path)

plot_training_progress(df)