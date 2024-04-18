import airsim
import time
import numpy as np
import math

def airsim_init(vehicle_name):
    client = airsim.MultirotorClient()
    # client.reset()
    client.confirmConnection()
    client.enableApiControl(True, vehicle_name=vehicle_name)
    client.armDisarm(True, vehicle_name=vehicle_name)
    client.takeoffAsync(vehicle_name=vehicle_name).join()
    return client

#test 19.03.24 passed
def airsim_setpose(client, pos: tuple, vehicle_name):
    x, y, z = pos
    print(f"setting pose: {x}, {y}, {z}")
    pose = airsim.Pose(airsim.Vector3r(x, y, z), airsim.to_quaternion(0, 0, 0))
    client.simSetVehiclePose(pose, ignore_collision=True, vehicle_name=vehicle_name)

# test 19.03.24 passed
def get_current_position(client, vehicle_name) -> tuple:
    pos = client.simGetGroundTruthKinematics(vehicle_name=vehicle_name).position
    return (pos.x_val, pos.y_val, pos.z_val)

def to_vec3r(point: tuple) -> airsim.Vector3r:
    return airsim.Vector3r(point[0], point[1], point[2])

def get_current_orientation(client, vehicle_name) -> tuple:
    ori = client.simGetGroundTruthKinematics(vehicle_name=vehicle_name).orientation
    return (ori.w_val, ori.x_val, ori.y_val, ori.z_val)

def get_pitch_roll_yaw(client, vehicle_name) -> tuple:
    ori = client.simGetGroundTruthKinematics(vehicle_name=vehicle_name).orientation
    return airsim.to_eularian_angles(ori) #pitch roll yaw (rad)

def take_action(client, action, vehicle_name):
    client.moveByVelocityZAsync(
        float(action[0]),
        float(action[1]),
        -7,
        float(action[2]),
        airsim.DrivetrainType.ForwardOnly,
        airsim.YawMode(False, 0),
        vehicle_name=vehicle_name
    )

def direction_based_navigation_2D(client, vehicle_name, action):
    #action[0] desired yaw_angle (radian) [-3.14, 3.14]
    #action[1] speed [5, 15]
    #action[2] duration [1,3]
    vx = math.cos(action[0]) * action[1]
    vy = math.sin(action[0]) * action[1]

    start_time = time.time()

    client.moveByVelocityZAsync(
        float(vx), float(vy), -4, float(action[2]),
        airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False, 0),
        vehicle_name=vehicle_name
    )
    while time.time() - start_time < action[2]:
        collisionInfo = client.simGetCollisionInfo()
    return collisionInfo