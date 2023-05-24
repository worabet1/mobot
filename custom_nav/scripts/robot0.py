#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import tf2_ros
from tf2_msgs.msg import TFMessage
from geometry_msgs.msg import PoseStamped,Twist
from custom_nav.msg import RobotPose,Gamecontroller
from utils import calculate_pose , mapoffset ,rot2eul,choosePath,possible_path,wall,thiefpathtoescapepolice,degreetoface,thiefpathtoexit
import numpy as np
import math
class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('tf_cal')
        self.odomtobase = []
        self.maptoodom = []
        self.pointx = 0
        self.pointy = 0
        self.yaw = 0
        self.num =0
        self.path=[]
        self.gamestate = 0
        self.doorstate1 = 0
        self.doorstate2 = 0
        self.escapedoor = 0
        self.policeposex = 0
        self.policeposey = 0
        self.thiefposey = 0
        self.thiefposex = 0
        self.position = [0.0,0.0]
        self.finishall=0
        self.subscription = self.create_subscription(
            TFMessage,
            '/tf',
            self.subscription_callback,
            10
        )
        self.nuang = 0
        self.map = mapoffset(0,0)

        self.pub_goal_1 = self.create_publisher(PoseStamped, '/tb3_0/goal_pose', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.pub_robot_pose = self.create_publisher(RobotPose, '/tb3_0/robotpose', 10)
        self.pub_goal_timer = self.create_timer(1.0, self.pubgoalpose)

        self.subgc = self.create_subscription(
            Gamecontroller,
            '/gamecontroller',
            self.gamecontroller,
            10
        )

        self.goOut = self.create_publisher(Twist, '/tb3_0/cmd_vel', 10)
        self.goOut_timer = self.create_timer(1.0, self.goouttt)
        


    def goouttt(self):
        twist = Twist()
        escapedoorindex = [[0,0],[3,0],[5,3],[2,5]]
        indices = [i for i, x in enumerate(self.escapedoor) if x == 1]
        ed = []
        for i in indices:
            ed.append(escapedoorindex[i])
        try:
            if self.gamestate == 2 and [self.thiefposex,self.thiefposey] in ed:
                print("goout by cmd vel")
                twist.linear.x = 0.0
                goout = 0
                if [self.thiefposex,self.thiefposey] == [0,0]:
                    if self.yaw >=170 and self.yaw <=190:
                        goout = 1
                    else:
                        twist.angular.z = 0.5
                if [self.thiefposex,self.thiefposey] == [3,0]:
                    if self.yaw >=260 and self.yaw <=280:
                        goout = 1
                    else:
                        twist.angular.z = 0.5
                if [self.thiefposex,self.thiefposey] == [5,3]:
                    if self.yaw >350 or self.yaw <10:
                        goout = 1
                    else:
                        twist.angular.z = 0.5
                if [self.thiefposex,self.thiefposey] == [2,5]:
                    if self.yaw >=80 and self.yaw <=100:
                        goout = 1
                    else:
                        twist.angular.z = 0.5
                if goout == 1:
                    twist.linear.x = 0.1
                    twist.angular.z = 0.0
                self.goOut.publish(twist)
        except:
            print("something wrong")

    def gamecontroller(self, msg):
        self.gamestate = msg.gamestate
        self.doorstate1 = msg.doorstate1
        self.doorstate2 = msg.doorstate2
        self.escapedoor = (msg.escapedoor.data).tolist()
        self.policeposex = msg.policeposex
        self.policeposey = msg.policeposey
        self.thiefposex = msg.thiefposex
        self.thiefposey = msg.thiefposey
    def pubgoalpose(self):
        pose_msg = RobotPose()
        pose_msg.robotx = self.pointx
        pose_msg.roboty = self.pointy
        pose_msg.robotyaw = self.yaw
        pose_msg.posex = float(self.position[0])
        pose_msg.posey = float(self.position[1])
        self.pub_robot_pose.publish(pose_msg)
        # if(self.gamestate == 1):
        #     self.path=thiefpathtoescapepolice(self.policeposex,self.policeposey,self.thiefposex,self.thiefposey,
        #                                       wall(self.doorstate1,self.doorstate2),degreetoface(self.yaw))
        # if(self.gamestate == 2):
        #     self.path=thiefpathtoexit(self.policeposex,self.policeposey,self.thiefposex,self.thiefposey,
        #                               wall(self.doorstate1,self.doorstate2),degreetoface(self.yaw),self.escapedoor)
    def timer_callback(self):
        pose_msg = PoseStamped()
        pose_msg.header.stamp = self.get_clock().now().to_msg()
        pose_msg.header.frame_id = 'map'
        if(self.gamestate == 1):
            self.path=thiefpathtoescapepolice(self.policeposex,self.policeposey,self.thiefposex,self.thiefposey,
                                              wall(self.doorstate1,self.doorstate2),degreetoface(self.yaw))
        if(self.gamestate == 2):
            self.path=thiefpathtoexit(self.policeposex,self.policeposey,self.thiefposex,self.thiefposey,
                                      wall(self.doorstate1,self.doorstate2),degreetoface(self.yaw),self.escapedoor)
        # print('Current thief path = ',self.path)
        if(self.gamestate >= 1 and self.gamestate != 5):
            try:
                self.num = self.path.index([self.pointx,self.pointy])+1
                prerotation=[self.path[self.num][0]-self.path[self.num+1][0],self.path[self.num][1]-self.path[self.num+1][1]]
                if(prerotation==[-1,0]):
                    rotation=0
                elif(prerotation==[1,0]):
                    rotation=180
                elif(prerotation==[0,-1]):
                    rotation=90
                elif(prerotation==[0,1]):
                    rotation=270
                pose_msg.pose.orientation.z = math.sin(rotation*math.pi/180/2)
                pose_msg.pose.orientation.w = math.cos(rotation*math.pi/180/2)
                # if ([self.pointx,self.pointy]==self.path[self.num]):
                #     if self.num < len(self.path) - 1:
                #         self.nuang += 1
                #         if self.nuang >= 1:
                #             self.nuang = 0
                #             self.num+=1
                # pose_msg.pose.position.x = self.path[self.num+1][0]/3.0+(1.62)
                # pose_msg.pose.position.y = self.path[self.num+1][1]/3.0+ (3.395)
                pose_msg.pose.position.x = ((self.path[self.num][0]+self.path[self.num+1][0])/2)/3.0+(1.62)
                pose_msg.pose.position.y = ((self.path[self.num][1]+self.path[self.num+1][1])/2)/3.0+ (3.395)
            except:
                try:
                    self.num = self.path.index([self.pointx,self.pointy])+1
                    prerotation=[self.path[self.num-1][0]-self.path[self.num][0],self.path[self.num-1][1]-self.path[self.num][1]]
                    if(prerotation==[-1,0]):
                        rotation=0
                    elif(prerotation==[1,0]):
                        rotation=180
                    elif(prerotation==[0,-1]):
                        rotation=90
                    elif(prerotation==[0,1]):
                        rotation=270
                    pose_msg.pose.position.x = (self.path[self.num][0]/3)+(1.62)
                    pose_msg.pose.position.y = (self.path[self.num][1]/3)+ (3.395)
                    pose_msg.pose.orientation.z = math.sin(rotation*math.pi/180/2)
                    pose_msg.pose.orientation.w = math.cos(rotation*math.pi/180/2)
                except:
                    pass
            pose_msg.pose.position.z = 0.0
            pose_msg.pose.orientation.x = 0.0
            pose_msg.pose.orientation.y = 0.0
            escapedoorindex = [[0,0],[3,0],[5,3],[2,5]]
            indices = [i for i, x in enumerate(self.escapedoor) if x == 1]
            ed = []
            for i in indices:
                ed.append(escapedoorindex[i])
            if self.gamestate == 2 and [self.thiefposex,self.thiefposey] in ed:
                pose_msg.pose.position.x = self.position[0]
                pose_msg.pose.position.y = self.position[1]
                if not self.finishall:
                    print('pub last goal pose')
                    self.pub_goal_1.publish(pose_msg)
                self.finishall += 1
            else:
                print("Go to goal")
                self.pub_goal_1.publish(pose_msg)
            print('Calculate current Pose robot 0')
            print('Current thief path = ',self.path)
            print('Going to ',pose_msg.pose.position.x,' ',pose_msg.pose.position.y)

    def subscription_callback(self, msg):
        for transform in msg.transforms:
            if transform.child_frame_id == 'tb3_0/base_footprint' and transform.header.frame_id == 'tb3_0/odom':
                self.odomtobase = [transform.transform.translation.x,
                             transform.transform.translation.y,
                             transform.transform.translation.z,
                             transform.transform.rotation.x,
                             transform.transform.rotation.y,
                             transform.transform.rotation.z,
                             transform.transform.rotation.w]
            if transform.child_frame_id == 'tb3_0/odom' and transform.header.frame_id == 'map':
                self.maptoodom = [transform.transform.translation.x,
                             transform.transform.translation.y,
                             transform.transform.translation.z,
                             transform.transform.rotation.x,
                             transform.transform.rotation.y,
                             transform.transform.rotation.z,
                             transform.transform.rotation.w]
        if ((self.odomtobase) and (self.maptoodom)):
            position, orientation = calculate_pose(self.maptoodom,self.odomtobase)
            rotation = rot2eul(orientation)
            self.pointx = int((position[0] - 1.62 + 2/12) / (1/3))
            self.pointy = int((position[1] - 3.395+ 2/12) / (1/3))
            self.yaw = int((int(((rotation[0] *180/math.pi) +360)*10) % 3600)/10.0)
            self.position = position
        else:
            pass
        

def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = MinimalSubscriber()
    rclpy.spin(minimal_subscriber)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
    print('end main')
