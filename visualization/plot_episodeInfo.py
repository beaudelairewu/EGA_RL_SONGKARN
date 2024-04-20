from utils.data_filtering import filter_by_top_Nsteps, filter_by_top_reward, increment_sampling
from utils.plot_utils import plot_2D, plot_3D, read_data

file_path = "/Users/EGA/Documents/AI_logs/19.04.24-1914/episodeLogs/episodeLog_Drone0.txt"
dat = read_data(file_path)
samples = filter_by_top_Nsteps(dat, 16)
plot_2D(samples)

episodeN = -1
points = dat[episodeN]['current_position']
start_goal = dat[episodeN]['start_goal']

plot_3D(points, start_goal)
