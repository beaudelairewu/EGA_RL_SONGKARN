import cv2
import numpy as np
import airsim

def getScreenDepth(client, vehicle_name):
        # Constants for visualization
        MIN_DEPTH_METERS = 0
        MAX_DEPTH_METERS = 100

        # Request DepthPerspective image as uncompressed float
        response, = client.simGetImages(
            [
                airsim.ImageRequest("front_center", airsim.ImageType.DepthPerspective, True, False),
            ],
            vehicle_name=vehicle_name
        )

        skip = False
        
        if len(response.image_data_float) == 0:
            skip = True
            return np.zeros((56, 100, 1)), skip
        elif response.width == 0:
            skip = True
            return np.zeros((56, 100, 1)), skip
        

        # Reshape to a 2d array with correct width and height
        depth_img_in_meters = airsim.list_to_2d_float_array(response.image_data_float, response.width, response.height)
        depth_img_in_meters = depth_img_in_meters.reshape(response.height, response.width, 1)

        # Calculate the new width while maintaining aspect ratio
        new_width = 100
        height, width, _ = depth_img_in_meters.shape
        if width == 0:
            width = 100
        new_height = int(height * (new_width / width))


        # Resize the depth image using OpenCV
        resized_depth_img = cv2.resize(depth_img_in_meters, (new_width, new_height))

        # Lerp 0..100m to 0..255 gray values on the resized image
        depth_8bit_lerped = np.interp(resized_depth_img, (MIN_DEPTH_METERS, MAX_DEPTH_METERS), (0, 255))
        depth_8bit_lerped = depth_8bit_lerped.reshape(56, 100, 1)
        depth_8bit_lerped = depth_8bit_lerped.astype(np.uint8)

        return depth_8bit_lerped, skip
   
# client = airsim.MultirotorClient()
# im, skip = getScreenDepth(client, "Drone0")
# print(im.dtype)
# print(im)
