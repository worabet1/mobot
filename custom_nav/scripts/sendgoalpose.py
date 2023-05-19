import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from custom_nav.action import Sendgoalpose
from geometry_msgs.msg import PoseStamped

class SendGoalPoseActionServer(Node):

    def __init__(self):
        super().__init__('send_goal_pose_action_server')
        self._action_server = ActionServer(
            self,SendgoalPose,'send_goal_pose',
            execute_callback=self.execute_callback,
            cancel_callback=self.cancel_callback
        )
        self.get_logger().info('Send Goal Pose Action Server has been started.')

    def execute_callback(self, goal_handle):
        self.get_logger().info('Received goal pose: %s' % goal_handle.request.goal_pose)

        # TODO: Implement the action behavior based on the goal pose

        # Send a success result to the action client
        goal_handle.succeed()

    def cancel_callback(self, goal_handle):
        self.get_logger().info('Goal pose action was canceled')
        goal_handle.canceled()

def main(args=None):
    rclpy.init(args=args)
    node = SendGoalPoseActionServer()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()