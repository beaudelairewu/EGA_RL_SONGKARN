import numpy as np
import matplotlib.pyplot as plt
import ast

def read_data(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    data = []
    for line in content.split('\n'):
        if line.strip():
            data_dict = ast.literal_eval(line)
            data.append(data_dict)

    return data

def plot_3D(points: list, start_goal: list):
    num_points = len(points)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    x = [p[0] for p in points]
    y = [p[1] for p in points]
    z = [p[2] for p in points]

    ax.scatter(x, y, z, marker='o', c=y, cmap='viridis')

    #plot start
    ax.scatter(start_goal[0][0], start_goal[0][1], start_goal[0][2], marker="^", color='orange', s=100)
    #plot goal
    ax.scatter(start_goal[1][0], start_goal[1][1], start_goal[1][2], marker="s", color='orange', s=100)

    for i in range(num_points - 1):
        ax.plot([x[i], x[i+1]],
                [y[i], y[i+1]],
                [z[i], z[i+1]], 
                color='0.5')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Interactive 3D Plot')

    ax.set_xlim(-40, 40) 
    ax.set_ylim(-40, 40) 
    ax.set_zlim(-40, 40) 
    ax.invert_zaxis()

    plt.show()


file_path = "/Users/noppa/Documents/AI_logs/multi_train/17.04.24-1115/episodeLogs/episodeLog_Drone0.txt"
dat = read_data(file_path)
points = dat[-1]['current_position']
start_goal = dat[-1]['start_goal']
print(points)
plot_3D(points, start_goal)