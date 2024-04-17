import math

def increment_sampling(dat, n_samples):
    d = math.floor(len(dat)/n_samples+1)
    i = 0
    samples = []
    while i <= len(dat):
        samples.append(dat[i])
        i += d
    return samples

def filter_by_top_reward(data, n):
    sorted_objects = sorted(data, key=lambda obj: sum(obj['reward']), reverse=True)
    return sorted_objects[:n]
    
def filter_by_top_Nsteps(data, n):
    sorted_objects = sorted(data, key=lambda obj: len(obj['action']), reverse=True)
    return sorted_objects[:n]
    