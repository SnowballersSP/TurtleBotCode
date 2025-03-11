import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math
import time
from tf_transformations import euler_from_quaternion
from std_srvs.srv import Empty

class RoomScanner(Node):
    def __init__(self):
        super().__init__('room_scanner')

        # Publisher for robot movement
        self.vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        # Subscriber for odometry (position tracking)
        self.odom_sub = self.create_subscription(Odometry, '/odom', self.odom_callback, 10)

        # Client to save the map
        self.save_map_client = self.create_client(Empty, '/map_saver/save_map')

        # Initialize position tracking
        self.current_x = 0.0
        self.current_y = 0.0
        self.current_yaw = 0.0

        # Small delay for ROS setup
        time.sleep(2)

        self.get_logger().info("Starting Room Scanning and Mapping...")

        # Start mapping
        self.scan_room()

    def odom_callback(self, msg):
        """ Callback function to update robot's position using odometry """
        self.current_x = msg.pose.pose.position.x
        self.current_y = msg.pose.pose.position.y

        # Extract yaw from quaternion
        orientation_q = msg.pose.pose.orientation
        _, _, self.current_yaw = euler_from_quaternion([
            orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w
        ])

    def move_forward(self, distance, speed=0.2):
        """ Moves the robot forward a specific distance """
        twist = Twist()
        twist.linear.x = speed

        start_x, start_y = self.current_x, self.current_y
        while math.sqrt((self.current_x - start_x) ** 2 + (self.current_y - start_y) ** 2) < distance:
            self.vel_pub.publish(twist)
            time.sleep(0.1)

        # Stop the robot
        twist.linear.x = 0.0
        self.vel_pub.publish(twist)

    def rotate(self, angle, speed=0.5):
        """ Rotates the robot by a specific angle (in degrees) """
        twist = Twist()
        twist.angular.z = speed if angle > 0 else -speed

        start_yaw = self.current_yaw
        target_yaw = start_yaw + math.radians(angle)

        while abs(self.current_yaw - target_yaw) > 0.05:
            self.vel_pub.publish(twist)
            time.sleep(0.1)

        # Stop the robot
        twist.angular.z = 0.0
        self.vel_pub.publish(twist)

    def scan_room(self):
        """ Moves the robot in a square/spiral pattern to scan the room """
        for i in range(4):
            self.move_forward(1.0)  # Move 1 meter
            self.rotate(90)         # Rotate 90 degrees

        self.get_logger().info("Finished scanning. Saving map...")

        # Call the map save service
        if self.save_map_client.wait_for_service(timeout_sec=5.0):
            req = Empty.Request()
            self.save_map_client.call_async(req)
            self.get_logger().info("Map saved successfully!")
        else:
            self.get_logger().error("Failed to call map save service!")

def main(args=None):
    rclpy.init(args=args)
    node = RoomScanner()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()