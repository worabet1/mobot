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

# wall(0,0,0) (1,0,0)  (0,1,0) (1,1,0) (0,0,1) (1,0,1)
def wall(d1,d2,d3):
    grid_paths = {
        (0, 0): {
            (1, 0): 1,(0, 1): 1
        },
        (0, 1): {
            (0, 0): 1,(1, 1): 0,(0, 2): 1
        },
        (0, 2): {
            (0, 1): 1,(1, 2): 1 ,(0, 3): 1
        },
        (0, 3): {
            (0, 2): 1,(1, 3): 1 ,(0, 4): 1
        },
        (0, 4): {
            (0, 3): 1,(1, 4): 1 ,(0, 5): 1
        },
        (0, 5): {
            (0, 4): 1,(1, 5): 1
        },
        (1, 0): {
            (0, 0): 1,(1, 1): 1,(2, 0): 0
        },
        (1, 1): {
            (1, 0): 1,(1, 2): 0,(0, 1): 0,(2, 1): 1
        },
        (1, 2): {
            (1, 1): 0,(1, 3): 0,(0, 2): 1,(2, 2): 1
        },
        (1, 3): {
            (1, 2): 0,(1, 4): 1,(0, 3): 1,(2, 3): d2
        },
        (1, 4): {
            (1, 3): 1,(1, 5): 0,(0, 4): 1,(2, 4): 0
        },
        (1, 5): {
            (1, 4): 0,(0, 5): 1,(2, 5): 1
        },
        (2, 0): {
            (2, 1): 1,(1, 0): 0,(3, 0): 1
        },
        (2, 1): {
            (2, 0): 1,(2, 2): 1,(1, 1): 1,(3, 1): 0
        },
        (2, 2): {
            (2, 1): 1,(2, 3): 1,(1, 2): 1,(3, 2): 0
        },
        (2, 3): {
            (2, 2): 1,(2, 4): d3,(1, 3): d2,(3, 3): 1
        },
        (2, 4): {
            (2, 3): d3,(2, 5): 1,(1, 4): 0,(3, 4): 1
        },
        (2, 5): {
            (2, 4): 1,(1, 5): 1,(3, 5): 1
        },
        (3, 0): {
            (3, 1): 1,(2, 0): 1,(4, 0): 1
        },
        (3, 1): {
            (3, 0): 1,(3, 2): 1,(2, 1): 0,(4, 1): 1
        },
        (3, 2): {
            (3, 1): 1,(3, 3): 1,(2, 2): 0,(4, 2): 1
        },
        (3, 3): {
            (3, 2): 1,(3, 4): 0,(2, 3): 1,(4, 3): 0
        },
        (3, 4): {
            (3, 3): 0,(3, 5): 1,(2, 4): 1,(4, 4): 0
        },
        (3, 5): {
            (3, 4): 1,(2, 5): 1,(4, 5): 1
        },
        (4, 0): {
            (4, 1): 0,(3, 0): 1,(5, 0): 1
        },
        (4, 1): {
            (4, 0): 0,(4, 2): 1,(3, 1): 1,(5, 1): 0
        },
        (4, 2): {
            (4, 1): 1,(4, 3): d1,(3, 2): 1,(5, 2): 0
        },
        (4, 3): {
            (4, 2): d1,(4, 4): 1,(3, 3): 0,(5, 3): 1
        },
        (4, 4): {
            (4, 3): 1,(4, 5): 0,(3, 4): 0,(5, 4): 1
        },
        (4, 5): {
            (4, 4): 0,(3, 5): 1,(5, 5): 1
        },
        (5, 0): {
            (4, 0): 1,(5, 1): 1
        },
        (5, 1): {
            (5, 0): 1,(4, 1): 0,(5, 2): 1
        },
        (5, 2): {
            (5, 1): 1,(4, 2): 0 ,(5, 3): 1
        },
        (5, 3): {
            (5, 2): 1,(4, 3): 1 ,(5, 4): 0
        },
        (5, 4): {
            (5, 3): 0,(4, 4): 1 ,(5, 5): 1
        },
        (5, 5): {
            (5, 4): 1,(4, 5): 1
        }
    }
    return grid_paths

def possible_path(start,end,wall):
    allpath = []
    unfinishpath = [[[start[0],start[1]]]]
    z = 1
    leastpathn = 100000
    while 1:
        for path in unfinishpath:
            if len(path)> leastpathn:
                unfinishpath.remove(path)
            else:
                pathend = path[len(path)-1] #[0,0]
                if pathend != end:
                    availablepath = []
                    if pathend[0]>=1:
                        availablepath.append([pathend[0]-1,pathend[1]])
                    if pathend[0] <=4:
                        availablepath.append([pathend[0]+1,pathend[1]])
                    if pathend[1]>=1:
                        availablepath.append([pathend[0],pathend[1]-1])
                    if pathend[1] <=4:
                        availablepath.append([pathend[0],pathend[1]+1])
                    check = 0
                    check2 = len(availablepath)
                    for i in availablepath:
                        if (i not in path) and wall[(pathend[0],pathend[1])][(i[0],i[1])]:
                            temp = path.copy()
                            temp.append(i)
                            unfinishpath.append(temp)
                            if path in unfinishpath:
                                check = 1
                        else:
                            check2 -= 1
                    if(check2 == 0):
                        unfinishpath.remove(path)
                    if check:
                        unfinishpath.remove(path)
                else:
                    leastpathn = len(path)
                    allpath.append(path)
                    unfinishpath.remove(path)       

        if len(unfinishpath) == 0:
            break
    return allpath
# print(possible_path([0,0],[5,5],wall(1,1,1)))

def choosePath(possiblePath,yaw):
    rank=[]
    for item in possiblePath:
        leaw = 0
        flag = 0
        if(yaw=="+x"):
            y=[-1 ,0]
        elif(yaw=="-x"):
            y=[1 ,0]
        elif(yaw=="+y"):
            y=[0 ,-1]
        elif(yaw=="-y"):
            y=[0 ,1]    
        for i in range(len(item)-1):
            xb = item[i][0]
            yb = item[i][1]
            xa = item[i+1][0]
            ya = item[i+1][1]
            x=[xb-xa ,yb-ya ]
            if x != y:
                if flag == 0:
                    leaw +=1000
                leaw +=1
            flag = 1
            y = x
        rank.append(leaw)
    finalPath = possiblePath[rank.index(min(rank))]
    return finalPath
# print(choosePath(possible_path([0,0],[5,5],wall(1,1,1)),'+x'))

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
