#include "mirage_m400.h"
#include "esphome/core/log.h"
#include <sstream>
#include <iomanip>

namespace esphome {
namespace mirage_m400 {

static const char *const TAG = "mirage_m400";

void MirageM400Component::setup() {
  ESP_LOGI(TAG, "Setting up Mirage M-400 component");
}

void MirageM400Component::loop() {
  while (available()) {
    uint8_t byte = read();
    if (byte == '\r' || byte == '\n') {
      if (!current_response_.empty()) {
        last_response = current_response_;
        response_buffer_.push(current_response_);
        ESP_LOGD(TAG, "Response received: %s", current_response_.c_str());
        current_response_.clear();
      }
    } else {
      current_response_ += static_cast<char>(byte);
    }
  }
}

void MirageM400Component::send_command(const std::string &command) {
  write_str(command.c_str());
  write_byte('\r');
  delay(50);
  ESP_LOGD(TAG, "Command sent: %s", command.c_str());
}

void MirageM400Component::register_number(MirageM400Number *number_entity, uint8_t zone) {
  number_entity->set_zone(zone);
  numbers_.push_back(number_entity);
}

void MirageM400Number::control(float value) {
  std::ostringstream ss;
  ss << "04" << std::setfill('0') << std::setw(2) << std::hex << (int)zone_ 
     << std::setfill('0') << std::setw(2) << std::hex << (int)value;
  parent_->send_command(ss.str());
  publish_state(value);
}

void MirageM400Component::register_switch(MirageM400Switch *switch_entity) {
  switch_entity->set_parent(this);
  switches_.push_back(switch_entity);
}

}  // namespace mirage_m400
}  // namespace esphome
