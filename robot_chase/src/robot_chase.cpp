#include <cmath>
#include <memory>

#include "geometry_msgs/msg/twist.hpp"
#include "rclcpp/rclcpp.hpp"
#include "tf2_ros/buffer.h"
#include "tf2_ros/transform_listener.h"

using namespace std::chrono_literals;

class RobotChase : public rclcpp::Node {
public:
  RobotChase() : Node("robot_chase") {
    RCLCPP_INFO(this->get_logger(), "🤖 Robot Chase node started");

    tf_buffer_ = std::make_shared<tf2_ros::Buffer>(this->get_clock());
    tf_listener_ = std::make_shared<tf2_ros::TransformListener>(*tf_buffer_);

    cmd_pub_ =
        this->create_publisher<geometry_msgs::msg::Twist>("/rick/cmd_vel", 10);

    timer_ = this->create_wall_timer(100ms,
                                     std::bind(&RobotChase::controlLoop, this));
  }

private:
  void controlLoop() {
    try {
      // ✅ COMMON FRAME = world
      auto rick_tf = tf_buffer_->lookupTransform("world", "rick/base_link",
                                                 tf2::TimePointZero);

      auto morty_tf = tf_buffer_->lookupTransform("world", "morty/base_link",
                                                  tf2::TimePointZero);

      double dx =
          morty_tf.transform.translation.x - rick_tf.transform.translation.x;
      double dy =
          morty_tf.transform.translation.y - rick_tf.transform.translation.y;

      double distance = std::sqrt(dx * dx + dy * dy);

      geometry_msgs::msg::Twist cmd;

      if (distance > 0.3) {
        cmd.linear.x = 0.6;
        cmd.angular.z = 2.0 * std::atan2(dy, dx);
      } else {
        cmd.linear.x = 0.0;
        cmd.angular.z = 0.0;
      }

      cmd_pub_->publish(cmd);

      RCLCPP_INFO_THROTTLE(this->get_logger(), *this->get_clock(), 2000,
                           "Distance to Morty: %.2f", distance);
    } catch (const tf2::TransformException &ex) {
      RCLCPP_WARN_THROTTLE(this->get_logger(), *this->get_clock(), 2000,
                           "TF not ready: %s", ex.what());
    }
  }

  rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr cmd_pub_;
  rclcpp::TimerBase::SharedPtr timer_;
  std::shared_ptr<tf2_ros::Buffer> tf_buffer_;
  std::shared_ptr<tf2_ros::TransformListener> tf_listener_;
};

int main(int argc, char **argv) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<RobotChase>());
  rclcpp::shutdown();
  return 0;
}
