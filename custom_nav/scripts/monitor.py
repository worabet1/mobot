#!/usr/bin/env python3
import sys
from custom_nav.srv import Monitorstart ,Monitorcontinuous
import rclpy
from rclpy.node import Node
import time
from custom_nav.msg import Gamecontroller
class MinimalClientAsync(Node):

    def __init__(self):
        super().__init__('gameControllerMonitor')
        self.cli = self.create_client(Monitorcontinuous, 'Monitorstart_service')
        self.subscription = self.create_subscription(
            Gamecontroller,
            '/gamecontroller',
            self.subscription_callback,
            10
        )
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = Monitorcontinuous.Request()
        self.old = 0
    def subscription_callback(self,msg):
        if msg.gamestate >= 1:
            print("*"*20)
            if msg.gamestate == 5:
                print("Robot has been gone already")
            if msg.gamestate == 4:
                print("Game Finished Police win")
            if msg.gamestate == 3:
                print("Game Finished Thief win")
            if msg.gamestate == 1:
                print("Game running")
            if msg.gamestate == 2:
                self.escapedoor = (msg.escapedoor.data).tolist()
                dooropen = []
                for i in range(len(self.escapedoor)):
                    if self.escapedoor[i]:
                        dooropen.append(i)
                print("Game running: Escape door open at door" + str(dooropen))
            if msg.gamestate != 3 and msg.gamestate != 4:
                print("Time remaining: " ,int(msg.timeremaining/60)," min ",msg.timeremaining%60," sec")
                if msg.doorstate1 == 0:
                    door1 = "open"
                else:
                    door1 = 'close'
                print("Door1: "+door1)
                if msg.doorstate2 == 0:
                    door2 = "open"
                elif msg.doorstate2 == 1:
                    door2 = 'close1'
                else:
                    door2 = 'close2'
                print("Door2: "+door2)
                print('Thief pose: X : ' + str(msg.thiefposex) + ' || Y : ' + str(msg.thiefposey))
                print('Police pose: X : ' + str(msg.policeposex) + ' || Y : ' + str(msg.policeposey))
        else :
            print("Ready to Start")

    def send_request(self, door1state, door2state):
        print("init ingame door to all open")
        self.req.door1state = door1state
        self.req.door2state = door2state
        self.future = self.cli.call_async(self.req)
        if self.future.done():
            response = self.future.result()
            print(response.door1respond, response.door2respond)
def main(args=None):
    rclpy.init(args=args)

    minimal_client = MinimalClientAsync()
    minimal_client.send_request(0,0)
    while rclpy.ok():
        rclpy.spin(minimal_client)
        print('ok')
        if minimal_client.future.done():
            try:
                response = minimal_client.future.result()
            except Exception as e:
                minimal_client.get_logger().info(
                    'Service call failed %r' % (e,))
            else:
                minimal_client.get_logger().info(
                    ' %d , %d |||||| %d , %d' %
                    (minimal_client.req.door1state, minimal_client.req.door2state, response.door1respond, response.door2respond))
            print("service finished")
    minimal_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()