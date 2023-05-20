start = 1/6
tilerange = 1/3
def mapoffset(x,y):
    map = []
    for i in range (6):
        temp = []
        for j in range(6):
            temp.append([start+tilerange*i,start+tilerange*j])
        map.append(temp)
    print(map)
    print("______________")
    for i in range(6):
        for j in range(6):
            map[i][j][0] = map[i][j][0] + x
            map[i][j][1] = map[i][j][1] + y
    return map

# print(mapoffset(1,2))
def euler_to_quaternion(roll, pitch, yaw):
    # Convert yaw from degrees to radians
    yaw_rad = math.radians(yaw)
    
    # Convert angles to half angles
    roll_half = roll / 2.0
    pitch_half = pitch / 2.0
    yaw_half = yaw_rad / 2.0
    
    # Calculate sin and cos values of the half angles
    sin_roll_half = math.sin(roll_half)
    cos_roll_half = math.cos(roll_half)
    sin_pitch_half = math.sin(pitch_half)
    cos_pitch_half = math.cos(pitch_half)
    sin_yaw_half = math.sin(yaw_half)
    cos_yaw_half = math.cos(yaw_half)
    
    # Calculate quaternion components
    x = sin_roll_half * cos_pitch_half * cos_yaw_half - cos_roll_half * sin_pitch_half * sin_yaw_half
    y = cos_roll_half * sin_pitch_half * cos_yaw_half + sin_roll_half * cos_pitch_half * sin_yaw_half
    z = cos_roll_half * cos_pitch_half * sin_yaw_half - sin_roll_half * sin_pitch_half * cos_yaw_half
    w = cos_roll_half * cos_pitch_half * cos_yaw_half + sin_roll_half * sin_pitch_half * sin_yaw_half
    
    return w
# print(euler_to_quaternion(0,0,0))

def init_pose(init):
    x = init[0]
    y= init[1]
    yaw = init[2]
    posible_yaw = {'+x':0,"+y":90,"-x":180,"-y":270}
    w = posible_yaw[yaw]
    w = euler_to_quaternion(0,0,w)
    xx = ((x-1)*2/6) + 1.62
    yy = ((y-1)*2/6) + 3.395
    return xx,yy,float(w)
import math

# def euler_from_quaternion(x, y, z, w):
#         """
#         Convert a quaternion into euler angles (roll, pitch, yaw)
#         roll is rotation around x in radians (counterclockwise)
#         pitch is rotation around y in radians (counterclockwise)
#         yaw is rotation around z in radians (counterclockwise)
#         """
#         t0 = +2.0 * (w * x + y * z)
#         t1 = +1.0 - 2.0 * (x * x + y * y)
#         roll_x = math.atan2(t0, t1)
     
#         t2 = +2.0 * (w * y - z * x)
#         t2 = +1.0 if t2 > +1.0 else t2
#         t2 = -1.0 if t2 < -1.0 else t2
#         pitch_y = math.asin(t2)
     
#         t3 = +2.0 * (w * z + x * y)
#         t4 = +1.0 - 2.0 * (y * y + z * z)
#         yaw_z = math.atan2(t3, t4)
     
        
#         return roll_x, pitch_y, yaw_z # in radians
# import numpy as np
def rot2eul(R):
    sy = np.sqrt(R[0, 0]**2 + R[1, 0]**2)
    singular = sy < 1e-6
    # beta = -np.arcsin(R[2,0])
    # alpha = np.arctan2(R[2,1]/np.cos(beta),R[2,2]/np.cos(beta))
    # gamma = np.arctan2(R[1,0]/np.cos(beta),R[0,0]/np.cos(beta))
    x = np.arctan2(R[2, 1], R[2, 2])
    y = np.arctan2(-R[2, 0], sy)
    z = np.arctan2(R[1, 0], R[0, 0])
    return [z,y,x]

 
# def quaternion_rotation_matrix(Q):
#     """
#     Covert a quaternion into a full three-dimensional rotation matrix.
 
#     Input
#     :param Q: A 4 element array representing the quaternion (q0,q1,q2,q3) 
 
#     Output
#     :return: A 3x3 element matrix representing the full 3D rotation matrix. 
#              This rotation matrix converts a point in the local reference 
#              frame to a point in the global reference frame.
#     """
#     # Extract the values from Q
#     x = Q[0]
#     y = Q[1]
#     z= Q[2]
#     w= Q[3]
     
#     # # First row of the rotation matrix
#     # r00 = 2 * (q0 * q0 + q1 * q1) - 1
#     # r01 = 2 * (q1 * q2 - q0 * q3)
#     # r02 = 2 * (q1 * q3 + q0 * q2)
     
#     # # Second row of the rotation matrix
#     # r10 = 2 * (q1 * q2 + q0 * q3)
#     # r11 = 2 * (q0 * q0 + q2 * q2) - 1
#     # r12 = 2 * (q2 * q3 - q0 * q1)
     
#     # # Third row of the rotation matrix
#     # r20 = 2 * (q1 * q3 - q0 * q2)
#     # r21 = 2 * (q2 * q3 + q0 * q1)
#     # r22 = 2 * (q0 * q0 + q3 * q3) - 1
     
#     # # 3x3 rotation matrix
#     # rot_matrix = np.array([[r00, r01, r02],
#     #                        [r10, r11, r12],
#     #                        [r20, r21, r22]])
    
#     return np.array([[1 - 2*y**2 - 2*z**2, 2*x*y - 2*z*w, 2*x*z + 2*y*w],
#                      [2*x*y + 2*z*w, 1 - 2*x**2 - 2*z**2, 2*y*z - 2*x*w],
#                      [2*x*z - 2*y*w, 2*y*z + 2*x*w, 1 - 2*x**2 - 2*y**2]])
                            
#     # return rot_matrix

# # print(init_pose(2,2,'+x'))

# import math
# import numpy as np

# def quat2mat(quaternion):
#     q_a, q_b, q_c, q_w = quaternion

#     rotation_matrix = np.array([
#         [1 - 2*q_b*q_b - 2*q_c*q_c, 2*q_a*q_b - 2*q_c*q_w, 2*q_a*q_c + 2*q_b*q_w],
#         [2*q_a*q_b + 2*q_c*q_w, 1 - 2*q_a*q_a - 2*q_c*q_c, 2*q_b*q_c - 2*q_a*q_w],
#         [2*q_a*q_c - 2*q_b*q_w, 2*q_b*q_c + 2*q_a*q_w, 1 - 2*q_a*q_a - 2*q_b*q_b]
#     ])

#     return rotation_matrix

import numpy as np
from transforms3d.quaternions import quat2mat, qmult
from transforms3d.affines import compose, decompose

def calculate_pose(h1,h2):
    [x1, y1, z1, q1_a, q1_b, q1_c, q1_w] = h1
    [x2, y2, z2, q2_a, q2_b, q2_c, q2_w] = h2
    # Convert the quaternions to rotation matrices
    rotation_matrix1 = quat2mat([q1_w, q1_a, q1_b, q1_c])
    rotation_matrix2 = quat2mat([q2_w, q2_a, q2_b, q2_c])

    # Create the translation vectors
    translation1 = np.array([x1, y1, z1])
    translation2 = np.array([x2, y2, z2])

    # Compose the transformation matrices for frame 1 to frame 2 and frame 2 to frame 3
    transform1_to_2 = np.eye(4)
    transform1_to_2[:3, :3] = rotation_matrix2
    transform1_to_2[:3, 3] = translation2
    transform2_to_3 = np.eye(4)
    transform2_to_3[:3, :3] = rotation_matrix1
    transform2_to_3[:3, 3] = translation1

    # transform1_to_2 = compose(translation2, rotation_matrix2)
    # transform2_to_3 = compose(translation1, rotation_matrix1)

    # Calculate the transformation from frame 1 to frame 3
    transform1_to_3 = np.dot(transform2_to_3, transform1_to_2)

    # Extract the position and orientation from the transformation matrix
    position, orientation, _, _ = decompose(transform1_to_3)
    return position, orientation

# # Example values
# x1, y1, z1 = 1.0, 2.0, 3.0
# q1_a, q1_b, q1_c, q1_w = 0.1, 0.2, 0.3, 0.4
# x2, y2, z2 = 4.0, 5.0, 6.0
# q2_a, q2_b, q2_c, q2_w = 0.5, 0.6, 0.7, 0.8

# # Calculate the transformation from frame 1 to frame 3
# position, orientation = calculate_pose(x1, y1, z1, q1_a, q1_b, q1_c, q1_w, x2, y2, z2, q2_a, q2_b, q2_c, q2_w)

# # Print the resulting position and orientation
# print("Position:")
# print(position)

# print("Orientation:")
# print(orientation)
