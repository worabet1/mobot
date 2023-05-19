#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import tf2_ros
from tf2_msgs.msg import TFMessage
from utils import euler_from_quaternion
from utils import quaternion_rotation_matrix , rot2eul , mapoffset
import numpy as np
import math
class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('tf_cal')
        self.odomtobase = []
        self.maptoodom = []
        self.subscription = self.create_subscription(
            TFMessage,
            '/tf',
            self.subscription_callback,
            10
        )
        self.map = mapoffset(0,0)

    def subscription_callback(self, msg):
        # print(msg.transforms)
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
        # print(self.odomtobase)
        # print(self.maptoodom)
        if ((self.odomtobase) and (self.maptoodom)):
            elmto=quaternion_rotation_matrix([self.maptoodom[3],self.maptoodom[4],self.maptoodom[5],self.maptoodom[6]])
            elotb=quaternion_rotation_matrix([self.odomtobase[3],self.odomtobase[4],self.odomtobase[5],self.odomtobase[6]])
            rotate=np.dot(elmto,elotb)
            t1=np.dot(rotate,np.matrix([[self.odomtobase[0]],[self.odomtobase[1]],[self.odomtobase[2]]]))
            translation=[t1[0,0]+self.maptoodom[0],t1[1,0]+self.maptoodom[1],t1[2,0]+self.maptoodom[2]]
            rotation1=rot2eul(elmto)
            rotation2=rot2eul(elotb)
            rotation=rot2eul(rotate)
            # print(translation)
            # print(rotation)
            pointx = int(round((translation[0] - 1.62) / 0.333))
            pointy = int(round((translation[1] - 3.395) / 0.333))
            yaw = (int(((rotation[0] *180/math.pi) +360)*10) % 3600)/10.0
            print(rotation1,rotation2)
            print('////////')
            print(rotation1[0]+rotation2[0])
            print(rotation[0])
            print('////////')
            print([pointx,pointy,yaw])
            print('*'*10)
        else:
            pass
        


        self.get_logger().info('_________________________________________-')

        # if msg.child_frame_id == 'base_footprint' and msg.header.frame_id == 'map':
            # try:
            #     transform = self.tf_buffer.transform(msg.header.frame_id, msg.child_frame_id, msg.header.stamp)
            #     self.publisher.publish(transform)
            #     self.get_logger().info('Published base_footprint to map transform')
            # except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
            #     self.get_logger().error(str(e))

def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = MinimalSubscriber()
    rclpy.spin(minimal_subscriber)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

