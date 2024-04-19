from utils.data_filtering import filter_by_top_Nsteps, filter_by_top_reward, increment_sampling
from utils.plot_utils import plot_2D, plot_3D, read_data
for i in range(6):
    file_path = f"/Users/noppa/Documents/AI_logs/multi_train/19.04.24-1622/episodeLogs/episodeLog_Drone{i}.txt"
    dat = read_data(file_path)
    # samples = filter_by_top_reward(dat, 16)
    # samples = increment_sampling(dat, 16)
    samples = dat[-16:]
    plot_2D(samples)

episodeN = -1
points = dat[episodeN]['current_position']
start_goal = dat[episodeN]['start_goal']

# plot_3D(points, start_goal)
