#include "mirage_m400.h"
#include "esphome/core/log.h"

namespace esphome {
namespace mirage_m400 {

static const char *TAG = "mirage_m400";

void MirageM400Component::setup() {
  ESP_LOGD(TAG, "Mirage M400 component setup");
}

void MirageM400Component::loop() {
  while (this->available()) {
    std::string response;
    while (this->available()) {
      uint8_t c = this->read();
      if (c == '\n' || c == '\r') {
        break;
      }
      response += (char)c;
    }
    if (!response.empty()) {
      this->process_response_(response);
    }
  }
}

void MirageM400Component::dump_config() {
  ESP_LOGCONFIG(TAG, "Mirage M400 Component:");
}

void MirageM400Component::send_command(const std::string &command) {
  this->write_str(command.c_str());
  this->write_byte('\r');  // Carriage return, not newline
}

void MirageM400Component::register_switch(switch_::Switch *sw) {
  this->switches_.push_back(sw);
}

void MirageM400Component::register_number(number::Number *num) {
  this->numbers_.push_back(num);
}

void MirageM400Component::register_text_sensor(text_sensor::TextSensor *sensor) {
  this->text_sensor_ = sensor;
}

void MirageM400Component::process_response_(const std::string &response) {
  if (this->text_sensor_) {
    this->text_sensor_->publish_state(response);
  }
  ESP_LOGD(TAG, "Response: %s", response.c_str());
}

}  // namespace mirage_m400
}  // namespace esphome
