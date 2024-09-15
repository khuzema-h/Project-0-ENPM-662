import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time


class MyController(Node):
    def __init__(self):
        super().__init__("my_controller")

        # Initialize publishers and subscribers
        self.pub = self.create_publisher(Twist, "/cmd_vel", 10)

        # Publish control commands
        cmd_vel = Twist()
        cmd_vel.linear.x = 1.0
        cmd_vel.linear.y = 0.0
        cmd_vel.linear.z = 0.0
        cmd_vel.angular.x = 0.0
        cmd_vel.angular.y = 0.0
        cmd_vel.angular.z = 0.0

        # Ask for scenario
        print(
            "Scenario 1: The TurtleBot moves at a constant velocity to reach a specific coordinate along a straight line \n"
        )
        print(
            "Scenario 2: The TurtleBot accelerates until it reaches a certain speed (v). \n It then continues to move at this constant velocity (v) over a distance of ​.\n Finally, the TurtleBot decelerates with a negative acceleration (- a) \n until it comes to a complete stop.\n"
        )
        scenario = int(input("Choose Scenario 1 or 2: "))  # Convert input to integer

        if scenario == 1:
            # x = v*t, where x is the distance travelled, v is the velocity and t is the time of travel
            # v is fixed at constant velocity of 1 m/s
            # Distance travelled can be controlled by varying the time of travel
            # Hence Time can be calculated by x/v to move the robot to a desired distance

            distance_travel = float(
                input("Enter the distance you want the turtlebot to travel: ")
            )

            # Timer initialization
            travel_time = distance_travel / cmd_vel.linear.x
            start_time = time.time()
            end_time = start_time + travel_time

            while time.time() < end_time:
                self.get_logger().info("Moving forward")
                self.pub.publish(cmd_vel)

            cmd_vel.linear.x = 0.0
            self.get_logger().info("Stopping Robot")

            self.pub.publish(cmd_vel)
            self.get_logger().info("Distance travelled = " + str(distance_travel))

        elif scenario == 2:
            # Acceleration loop

            top_speed = float(
                input("Enter the top speed you want the robot to reach: ")
            )
            distance_travel = float(
                input(
                    "Enter the distance you want the turtlebot to travel once desired velocity has been reached: "
                )
            )
            while cmd_vel.linear.x < top_speed:
                cmd_vel.linear.x += 1.0

                self.pub.publish(cmd_vel)
                self.get_logger().info(f"Accelerating, Speed: {cmd_vel.linear.x}")
                time.sleep(1)

            self.get_logger().info("Coasting")

            travel_time = distance_travel / cmd_vel.linear.x

            time.sleep(travel_time)
            self.get_logger().info("Stopping")

            while cmd_vel.linear.x > 0.0:
                cmd_vel.linear.x -= 1.0
                self.pub.publish(cmd_vel)
                self.get_logger().info(f"Deccelerating, Speed: {cmd_vel.linear.x}")
                time.sleep(1)

            self.get_logger().info("Robot has stopped")


def main(args=None):
    rclpy.init(args=args)
    controller = MyController()
    rclpy.spin(controller)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
