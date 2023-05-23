#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import tf2_ros
from tf2_msgs.msg import TFMessage
from geometry_msgs.msg import PoseStamped
from utils import calculate_pose , mapoffset ,rot2eul,choosePath,possible_path,wall
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
        self.subscription = self.create_subscription(
            TFMessage,
            '/tf',
            self.subscription_callback,
            10
        )
        self.map = mapoffset(0,0)
        

        # super().__init__('pub_goal_tb3_1')
        self.pub_goal_1 = self.create_publisher(PoseStamped, '/tb3_1/goal_pose', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        if(len(self.path)==0):
            self.path=choosePath(possible_path([0,0],[3,4],wall(1,1,1)),'+x')
        prerotation=[self.path[self.num][0]-self.path[self.num+1][0],self.path[self.num][1]-self.path[self.num+1][1]]
        if(prerotation==[-1,0]):
            rotation=0
        elif(prerotation==[1,0]):
            rotation=180
        elif(prerotation==[0,-1]):
            rotation=90
        elif(prerotation==[0,1]):
            rotation=270
        pose_msg = PoseStamped()
        pose_msg.header.stamp = self.get_clock().now().to_msg()
        pose_msg.header.frame_id = 'map'
        pose_msg.pose.position.x = ((self.path[self.num][0]+self.path[self.num+1][0])/2+0.5)*1/3+(1.62-2/12)
        pose_msg.pose.position.y = ((self.path[self.num][1]+self.path[self.num+1][1])/2+0.5)*1/3+ (3.395 - (2/12))
        pose_msg.pose.position.z = 0.0
        pose_msg.pose.orientation.x = 0.0
        pose_msg.pose.orientation.y = 0.0
        pose_msg.pose.orientation.z = math.sin(rotation*math.pi/180/2)
        pose_msg.pose.orientation.w = math.cos(rotation*math.pi/180/2)
        if ([self.pointx,self.pointy]==self.path[self.num]):
            if self.num < len(self.path) - 2:
                self.num+=1
        self.pub_goal_1.publish(pose_msg)
        # self.get_logger().info('Published pose')
        # print(self.num)
        print('*******CurrentPose*******')
        print(self.pointx,self.pointy,self.yaw)


    def subscription_callback(self, msg):
        for transform in msg.transforms:
            if transform.child_frame_id == 'tb3_1/base_footprint' and transform.header.frame_id == 'tb3_1/odom':
                self.odomtobase = [transform.transform.translation.x,
                             transform.transform.translation.y,
                             transform.transform.translation.z,
                             transform.transform.rotation.x,
                             transform.transform.rotation.y,
                             transform.transform.rotation.z,
                             transform.transform.rotation.w]
            if transform.child_frame_id == 'tb3_1/odom' and transform.header.frame_id == 'map':
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
            self.pointx = int(math.floor((position[0] - 1.62+(2/12)) / (1/3)))
            self.pointy = int(math.floor((position[1] - 3.395 + (2/12)) / (1/3)))
            self.yaw = (int(((rotation[0] *180/math.pi) +360)*10) % 3600)/10.0
        else:
            print('else')
            pass
        # print('sub tf *******************')
        

def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = MinimalSubscriber()
    rclpy.spin(minimal_subscriber)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
    print('end main')
