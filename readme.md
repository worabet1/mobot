# Catch me if you can
This repository contains a ROS2 package for the multi-TurtleBot3 Play Tag game. In the Play Tag game, the TurtleBot3 acts as a "Police" robot that tries to catch other "Thief" robots by moving and navigating in the environment.

## Purposed application
- Thief must try to avoid from police for a period of time until the escape door is unlocked
- Thief must try to escape with escape door while running away from police
- Police must try to catch the thief before the thief escape
- Map will have dynamic door that control with game controller for thief to juke the police

## Member
1. Chayanut Rassameecharoenchai 62340500012
2. Nachata Vongweeratorn 62340500030
3. Patcharapol Saechan 62340500036
4. Worameth Witanakorn 62340500045

## Functional requirements
- The thief must be able to run away from the police.
- The police must be able to chase the thief.
- The game controller must be able to open-close the door.
- The thief must be able to run to the escape door.

```
cd ~/turtlebot3_ws/src
git clone https://github.com/aumchayanut/mobot.git
cd ~/turtlebot3_ws/
colcon build
source install/setup.bash
```
