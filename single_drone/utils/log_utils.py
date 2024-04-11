import logging
import json
import os


def get_log_data(log_dir) -> list: 
    with open(f'{log_dir}/', 'r') as file:
        data = file.read()
        json_array_string = "[" + data.replace('\n', ',').rstrip(',') + "]"  # Remove trailing comma
        json_array = json.loads(json_array_string)
        json_array = [json.dumps(j) for j in json_array]
    return json_array

def episodeLog_to_file(episodeLog, logdir, vehicle_name, log_ep, episodeN):
    print(f"============================={log_ep}============================{episodeN}==========================================")    

    file_path = f'{logdir}/episodeLog_{vehicle_name}.txt'
    if not os.path.exists(file_path):
        # File doesn't exist, create it
        with open(file_path, 'w') as f:
            print('File created:', file_path)
    else:
        print('File already exists:', file_path)
    
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    
    # Remove any existing console handlers
    for handler in logger.handlers[:]: 
        if isinstance(handler, logging.StreamHandler):
            logger.removeHandler(handler)

    handler = logging.FileHandler(file_path)
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logger.info(episodeLog)

def write_txt(episodeLog, logdir, vehicle_name, log_ep, episodeN):
    print(f"============================={log_ep}============================{episodeN}==========================================")    

    file_path = f'{logdir}/episodeLog_{vehicle_name}.txt'
    if not os.path.exists(file_path):
        # File doesn't exist, create it
        with open(file_path, 'w') as f:
            print('File created:', file_path)
    else:
        print('File already exists:', file_path)
        with open(file_path, "a") as file:
            file.write(episodeLog)
    
    
    