#!/usr/bin/env python3
from rclpy.clock import Clock

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseWithCovarianceStamped
from utils import  mapoffset,init_pose
init0 = [1,4,'+y']
init1 = [4,4,'-x']
class Initial(Node):
    def __init__(self):
        super().__init__('game_controller_initial')
        self.publisher_0 = self.create_publisher(
            PoseWithCovarianceStamped,
            '/tb3_0/initialpose',
            10  # QoS profile depth
        )
        self.publisher_1 = self.create_publisher(
            PoseWithCovarianceStamped,
            '/tb3_1/initialpose',
            10  # QoS profile depth
        )
        self.publish_initial_pose_0()
        self.publish_initial_pose_1()

    def publish_initial_pose_0(self):
        time_stamp = Clock().now()
        initial_pose = PoseWithCovarianceStamped()
        # Set the initial pose values
        x,y,a,b,c,d = init_pose(init0)
        initial_pose.header.stamp = time_stamp.to_msg()
        initial_pose.header.frame_id = "map"
        initial_pose.pose.pose.position.x = x
        initial_pose.pose.pose.position.y = y
        initial_pose.pose.pose.position.z = 0.0
        initial_pose.pose.pose.orientation.x = a
        initial_pose.pose.pose.orientation.y = b
        initial_pose.pose.pose.orientation.z = c
        initial_pose.pose.pose.orientation.w = d
        self.publisher_0.publish(initial_pose)
    def publish_initial_pose_1(self):
        time_stamp = Clock().now()
        initial_pose = PoseWithCovarianceStamped()
        x,y,a,b,c,d = init_pose(init1)
        initial_pose.header.stamp = time_stamp.to_msg()
        initial_pose.header.frame_id = "map"
        initial_pose.pose.pose.position.x = x
        initial_pose.pose.pose.position.y = y
        initial_pose.pose.pose.position.z = 0.0
        initial_pose.pose.pose.orientation.x = a
        initial_pose.pose.pose.orientation.y = b
        initial_pose.pose.pose.orientation.z = c
        initial_pose.pose.pose.orientation.w = d
        self.publisher_1.publish(initial_pose)
def main(args=None):
    rclpy.init(args=args)
    initial = Initial()
    rclpy.spin_once(initial)
    initial.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()