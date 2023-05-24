#!/usr/bin/env python3

from custom_nav.srv import Monitorstart ,Monitorcontinuous
from custom_nav.msg import Gamecontroller,RobotPose
import time
import rclpy
from rclpy.node import Node
from random import sample, randint
class GameController(Node):
    def __init__(self):
        super().__init__('GameControllerNode')
        self.d1 = 0
        self.d2 = 0
        self.gamestate = 0
        self.gametime = 0
        self.starttime = 0
        self.robot0pose = [0,0,0]
        self.robot1pose = [0,0,0]
        self.robot0grid = [0,0]
        self.robot1grid = [0,0]
        self.srv = self.create_service(Monitorcontinuous, 'Monitorstart_service', self.monitor)
        self.publisher_ = self.create_publisher(Gamecontroller, '/gamecontroller', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.escapedoor = [0,0,0,0]
        self.opendoor = 2 #CHANGE
        self.check = 0
        self.subrobot0pose = self.create_subscription(
            RobotPose,
            '/tb3_0/robotpose',
            self.subrobotpose0,
            10
        )
        self.subrobot1pose = self.create_subscription(
            RobotPose,
            '/tb3_1/robotpose',
            self.subrobotpose1,
            10
        )
    def subrobotpose0(self, msg):
        # self.get_logger().info('Received: %d' % msg.data)
        self.robot0pose[0]=msg.posex
        self.robot0pose[1]=msg.posey
        self.robot0grid[0]=msg.robotx
        self.robot0grid[1]=msg.roboty
        self.robot0pose[2]=msg.robotyaw

    def subrobotpose1(self, msg):
        # self.get_logger().info('Received: %d' % msg.data)
        self.robot1pose[0]=msg.posex
        self.robot1pose[1]=msg.posey
        self.robot1grid[0]=msg.robotx
        self.robot1grid[1]=msg.roboty
        self.robot1pose[2]=msg.robotyaw

    def timer_callback(self):
        msg = Gamecontroller()
        msg.doorstate1 = self.d1
        msg.doorstate2 = self.d2
        msg.timeremaining = self.gametime - (int(time.time()) - self.starttime)
        msg.thiefposex = self.robot0grid[0]
        msg.thiefposey = self.robot0grid[1]
        msg.policeposex = self.robot1grid[0]
        msg.policeposey = self.robot1grid[1]
        if abs(self.robot0pose[0] - self.robot1pose[0]) < 0.15 and (self.robot0pose[1] - self.robot1pose[1]) < 0.15:
            if self.gamestate == 1 or self.gamestate == 2:
                if self.gametime > 0:
                    self.gamestate = 4
        if msg.timeremaining <= 0 and self.gamestate != 0:
            self.gamestate = 4
        if self.robot0pose[0] < 1.62-1/6 or self.robot0pose[1] > 5.395-1/6 or self.robot0pose[0] > 3.62-1/6 or self.robot0pose[1] < 3.395-1/6 :
            log_message = 'Float values: ' + str(self.robot0pose[0]) + ', ' + str(self.robot0pose[1])
            self.get_logger().info(log_message)
            if self.gamestate == 2:
                self.gamestate = 3
        if self.robot0grid[0] < -50 or self.robot0grid[1] > 50 or self.robot0grid[0] > 50 or self.robot0grid[1] < -50 or self.robot0grid[0] < -50 or self.robot0grid[1] > 50 or self.robot0grid[0] > 50 or self.robot0grid[1] < -50:
            self.gamestate = 5
        if msg.timeremaining <= 60 and self.gamestate != 0:
            if not self.check:
                door = []
                for i in range(self.opendoor):
                    while True:
                        rand = randint(0,3)
                        if rand not in door:
                            door.append(rand)
                            break
                for item in door:    
                    self.escapedoor[item] = 1
                self.gamestate = 2
                self.check = 1
        msg.gamestate = self.gamestate
        msg.escapedoor.data = [int(self.escapedoor[j]) for j in range(len(self.escapedoor))]
        self.publisher_.publish(msg)

    def monitor(self, request, response):
        if request.door1state == 0:
            self.d1 = 0
        if request.door1state == 1:
            self.d1 = 1
        if request.door2state == 0:
            self.d2 = 0
        if request.door2state == 1:
            self.d2 = 1
        if request.door2state == 2:
            self.d2 = 2
        self.gamestate = request.gamestate
        if self.gametime != request.gametime:
            self.check = 0
            self.starttime = int(time.time())
            self.escapedoor = [0,0,0,0]
            self.gamestate = 1
        if request.gametime != 0:
            self.gametime = request.gametime
        return response

def main(args=None):
    rclpy.init(args=args)

    minimal_service = GameController()

    rclpy.spin(minimal_service)

    rclpy.shutdown()

if __name__ == '__main__':
    main()