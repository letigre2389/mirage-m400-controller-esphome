#include "mirage_m400.h"
#include "esphome/core/log.h"

namespace esphome {
namespace mirage_m400 {

static const char *const TAG = "mirage_m400";

void MirageM400Component::setup() {
  ESP_LOGI(TAG, "Setting up Mirage M-400 component");
}

void MirageM400Component::loop() {
  if (!this->available()) {
    return;
  }

  std::string response;
  while (this->available()) {
    uint8_t byte = this->read();
    if (byte == '\r' || byte == '\n') {
      if (!response.empty() && text_sensor_) {
        text_sensor_->set_last_response(response);
      }
      response.clear();
    } else {
      response += static_cast<char>(byte);
    }
  }
}

void MirageM400Component::send_command(const std::string &command) {
  this->write_str(command);
  this->write_byte('\r');
  delay(50);
}

void MirageM400Component::register_number(MirageM400Number *number) {
  numbers_.push_back(number);
}

void MirageM400Component::register_switch(MirageM400Switch *switch_) {
  switches_.push_back(switch_);
}

void MirageM400Component::register_text_sensor(MirageM400TextSensor *text_sensor) {
  text_sensor_ = text_sensor;
}

void MirageM400Component::set_uart_parent(uart::UARTComponent *parent) {
  this->set_parent(parent);
}

void MirageM400Number::control(float value) {
  auto *parent = static_cast<MirageM400Component *>(this->get_component());
  if (parent) {
    std::string cmd = "0401";
    cmd += std::to_string(zone_);
    char hex_val[3];
    snprintf(hex_val, sizeof(hex_val), "%02X", static_cast<uint8_t>(value));
    cmd += hex_val;
    parent->send_command(cmd);
  }
}

void MirageM400Number::dump_config() {
  LOG_NUMBER("", "Mirage M-400 Volume", this);
}

void MirageM400Switch::write_state(bool state) {
  auto *parent = static_cast<MirageM400Component *>(this->get_component());
  if (parent) {
    std::string cmd;
    if (type_ == 0) {  // POWER
      cmd = "01";
      cmd += (state ? "01" : "00");
    } else if (type_ == 1) {  // MUTE
      cmd = "02";
      cmd += (state ? "01" : "00");
    }
    char zone_str[3];
    snprintf(zone_str, sizeof(zone_str), "%02d", zone_);
    cmd += zone_str;
    parent->send_command(cmd);
  }
}

void MirageM400Switch::dump_config() {
  LOG_SWITCH("", "Mirage M-400 Switch", this);
}

void MirageM400TextSensor::dump_config() {
  LOG_TEXT_SENSOR("", "Mirage M-400 Response", this);
}

}  // namespace mirage_m400
}  // namespace esphome
