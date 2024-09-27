import rclpy
from rclpy.node import Node

from std_msgs.msg import Int32MultiArray

class Merger(Node):
	def __init__(self):
		super().__init__('merger')
		self.subscription1 = self.create_subscription(Int32MultiArray, '/input/array1', self.listener1_callback, 10)
		self.subscription2 = self.create_subscription(Int32MultiArray, '/input/array2', self.listener2_callback, 10)
		self.publisher_ = self.create_publisher(Int32MultiArray, '/output/array', 10)
		
		self.array1 = None
		self.array2 = None

	def listener1_callback(self, msg):
		self.array1 = msg.data
		self.process_arrays()

	def listener2_callback(self, msg):
		self.array2 = msg.data
		self.process_arrays()

	def process_arrays(self):
		if self.array1 is None or self.array2 is None:
			return
		
		msg = Int32MultiArray()
		msg.data = list(sorted(self.array1 + self.array2))
		
		self.publisher_.publish(msg)
		self.get_logger().info('Published message: %s' % msg.data)

def main(args=None):
	rclpy.init(args=args)
	
	merger = Merger()
	
	rclpy.spin(merger)
	
	merger.destroy_node()
	rclpy.shutdown()

if __name__ == '__main__':
	main()
