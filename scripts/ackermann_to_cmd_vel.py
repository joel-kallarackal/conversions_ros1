#!/usr/bin/python3

import rospy
from geometry_msgs.msg import Twist
import numpy as np
from ackermann_msgs.msg import AckermannDrive

class Transformer():
    def __init__(self, wheelbase = 10):
        rospy.init_node('transformer_node', anonymous=True)
    
        # Subscribers
        rospy.Subscriber("/carla/ego_vehicle/ackermann_cmd", AckermannDrive, self.ackermann_to_twist)
        
        # Publishers
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        
        self.wheelbase = wheelbase
        
        print("Ackermann to Twist Transformer Started...")
            
    def ackermann_to_twist(self, data: AckermannDrive):
        '''
            Converts Ackermann steering commands to Twist 
        '''
        cmd_vel = Twist()
        cmd_vel.linear.x = data.speed
        cmd_vel.angular.z = (np.tan(data.steering_angle) * data.speed)/self.wheelbase
        
        self.cmd_vel_pub.publish(cmd_vel)    
    
def main():
    transformer = Transformer()
    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
