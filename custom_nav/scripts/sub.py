#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            Int32,
            '/my_topic',
            self.subscription_callback,
            10
        )

    def subscription_callback(self, msg):
        self.get_logger().info('Received: %d' % msg.data)

def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = MinimalSubscriber()
    rclpy.spin(minimal_subscriber)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
