import math
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

def plot_2D(samples):
    n_cols = 4
    n_rows = math.ceil(len(samples)/n_cols)
    print(n_rows)
    fig, axes = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=(10, 10))
    axes = axes.flatten()  

    for ax, sample in zip(axes, samples):
        x = [p[0] for p in sample['current_position']]
        y = [p[1] for p in sample['current_position']]
        ax.plot(x, y)
        ax.plot(sample['start_goal'][0][0], sample['start_goal'][0][1], marker='^', markersize=6, markerfacecolor='orange')
        ax.plot(sample['start_goal'][1][0], sample['start_goal'][1][1], marker='s', markersize=6, markerfacecolor='orange')

        ax.set_title(f"reward: {sum(sample['reward'])}".title())
        ax.set_xlim(-40, 40) 
        ax.set_ylim(-40, 40) 
        
    plt.subplots_adjust(hspace=0.5, wspace=1)
    plt.show()

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

def plot_training_progress(df):
    for index, row in df.iterrows():
        df.loc[index, 'time/total_timesteps'] = row['time/total_timesteps']/1000

    eject = ["time/fps", "time/total_timesteps", "time/time_elapsed", "time/iterations"]
    columns_to_plot = set(df.columns) ^ set(eject)
    print(columns_to_plot)
    n_cols = 3
    n_rows = math.ceil(len(columns_to_plot)/n_cols)

    print(n_rows)
    fig, axes = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=(10, 20))
    axes = axes.flatten()  

    for ax, col in zip(axes, columns_to_plot):
        ax.plot(df['time/total_timesteps'], df[col])
        ax.set_title(col.title())
        ax.set_xlabel('steps*10e-3')
        # ax.set_ylabel(col.title())

    # Adjust the spacing between subplots
    plt.subplots_adjust(hspace=1, wspace=0.5)

    # Display the plots
    plt.show()