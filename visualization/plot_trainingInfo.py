import pandas as pd
from utils.plot_utils import plot_training_progress

path = "/Users/noppa/Documents/AI_logs/multi_train/18.04.24-1254/infoLogs/progress.csv"
df = pd.read_csv(path)

plot_training_progress(df)