#!/usr/bin/env python3
import time
import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from custom_nav.action import Sendgoalpose


class FibonacciActionServer(Node):

    def __init__(self):
        super().__init__('fibonacci_action_server')
        self._action_server = ActionServer(
            self,
            Sendgoalpose,
            'fibonacci',
            self.execute_callback)

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')

        feedback_msg = Sendgoalpose.Feedback()
        feedback_msg.partial_sequence = [0, 1]

        for i in range(1, goal_handle.request.order):
            feedback_msg.partial_sequence.append(
                feedback_msg.partial_sequence[i] + feedback_msg.partial_sequence[i-1])
            self.get_logger().info('Feedback: {0}'.format(feedback_msg.partial_sequence))
            goal_handle.publish_feedback(feedback_msg)
            time.sleep(1)

        goal_handle.succeed()

        result = Sendgoalpose.Result()
        result.sequence = feedback_msg.partial_sequence
        return result


def main(args=None):
    rclpy.init(args=args)

    fibonacci_action_server = FibonacciActionServer()

    rclpy.spin(fibonacci_action_server)


if __name__ == '__main__':
    main()


# import rclpy
# from rclpy.action import ActionServer
# from rclpy.node import Node
# from custom_nav.action import Sendgoalpose
# from geometry_msgs.msg import PoseStamped

# class SendGoalPoseActionServer(Node):

#     def __init__(self):
#         super().__init__('send_goal_pose_action_server')
#         self._action_server = ActionServer(
#             self,SendgoalPose,'send_goal_pose',
#             execute_callback=self.execute_callback,
#             cancel_callback=self.cancel_callback
#         )
#         self.get_logger().info('Send Goal Pose Action Server has been started.')

#     def execute_callback(self, goal_handle):
#         self.get_logger().info('Received goal pose: %s' % goal_handle.request.goal_pose)

#         # TODO: Implement the action behavior based on the goal pose

#         # Send a success result to the action client
#         goal_handle.succeed()

#     def cancel_callback(self, goal_handle):
#         self.get_logger().info('Goal pose action was canceled')
#         goal_handle.canceled()

# def main(args=None):
#     rclpy.init(args=args)
#     node = SendGoalPoseActionServer()
#     rclpy.spin(node)
#     rclpy.shutdown()

# if __name__ == '__main__':
#     main()