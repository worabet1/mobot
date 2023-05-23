#!/usr/bin/env python3
import rclpy
from rclpy.action import ActionClient
from geometry_msgs.msg import PoseStamped
from nav2_msgs.action import NavigateToPose

def goal_pose_client():
    rclpy.init(args=None)
    node = rclpy.create_node('goal_pose_client')

    # Create an action client for the "navigate_to_pose" action
    client = ActionClient(node, NavigateToPose, 'navigate_to_pose')

    # Wait for the action server to start
    node.get_logger().info('Waiting for action server...')
    client.wait_for_server()
    node.get_logger().info('Action server found.')

    # Create a goal pose
    goal_pose = PoseStamped()
    goal_pose.header.frame_id = 'map'
    goal_pose.pose.position.x = 1.0
    goal_pose.pose.position.y = 2.0
    goal_pose.pose.orientation.w = 1.0

    # Create a NavigateToPose goal with the goal pose
    goal = NavigateToPose.Goal()
    goal.pose = goal_pose

    # Send the goal to the action server and specify the callback functions
    client.wait_for_server()
    future = client.send_goal_async(goal, feedback_callback=feedback_callback)
    rclpy.spin_until_future_complete(node, future)
    goal_handle = future.result()

    if not goal_handle.accepted:
        node.get_logger().info('Goal rejected by server')
        return

    # Wait for the goal to complete
    node.get_logger().info('Goal sent successfully')
    future = goal_handle.get_result_async()
    rclpy.spin_until_future_complete(node, future)
    result = future.result()

    if result and result.result:
        node.get_logger().info('Goal succeeded')
    else:
        node.get_logger().info('Goal failed')

    node.destroy_node()
    rclpy.shutdown()

def feedback_callback(feedback_msg):
    # This function is called whenever feedback is received from the action server
    print('Received feedback:', feedback_msg.feedback)

if __name__ == '__main__':
    goal_pose_client()





# import rclpy
# from rclpy.action import ActionClient
# from rclpy.node import Node

# from custom_nav.action import Sendgoalpose


# class FibonacciActionClient(Node):

#     def __init__(self):
#         super().__init__('fibonacci_action_client')
#         self._action_client = ActionClient(self, Sendgoalpose, 'fibonacci')

#     def send_goal(self, order):
#         goal_msg = Sendgoalpose.Goal()
#         goal_msg.order = order

#         self._action_client.wait_for_server()

#         self._send_goal_future = self._action_client.send_goal_async(goal_msg, feedback_callback=self.feedback_callback)

#         self._send_goal_future.add_done_callback(self.goal_response_callback)

#     def goal_response_callback(self, future):
#         goal_handle = future.result()
#         if not goal_handle.accepted:
#             self.get_logger().info('Goal rejected :(')
#             return

#         self.get_logger().info('Goal accepted :)')

#         self._get_result_future = goal_handle.get_result_async()
#         self._get_result_future.add_done_callback(self.get_result_callback)

#     def get_result_callback(self, future):
#         result = future.result().result
#         self.get_logger().info('Result: {0}'.format(result.sequence))
#         rclpy.shutdown()

#     def feedback_callback(self, feedback_msg):
#         feedback = feedback_msg.feedback
#         self.get_logger().info('Received feedback: {0}'.format(feedback.partial_sequence))


# def main(args=None):
#     rclpy.init(args=args)

#     action_client = FibonacciActionClient()

#     action_client.send_goal(10)

#     rclpy.spin(action_client)


# if __name__ == '__main__':
#     main()