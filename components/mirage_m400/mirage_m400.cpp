#include "mirage_m400.h"

namespace esphome {
namespace mirage_m400 {

void MirageM400Component::setup() {
  ESP_LOGD("custom", "Mirage M400 setup");
}

void MirageM400Component::loop() {
  while (this->available()) {
    std::string response;
    while (this->available()) {
      char c = this->read();
      if (c == '\n' || c == '\r') break;
      response += c;
    }
    if (!response.empty()) {
      this->process_response_(response);
    }
  }
}

void MirageM400Component::process_response_(const std::string &response) {
  if (this->text_sensor_) {
    this->text_sensor_->set_last_response(response);
  }
}

void MirageM400Component::send_command(const std::string &command) {
  this->write_str(command.c_str());
  this->write_byte('\n');
}

void MirageM400Component::register_switch(MirageM400Switch *sw) {
  this->switches_.push_back(sw);
  sw->set_parent(this);
}

void MirageM400Component::register_number(MirageM400Number *num) {
  this->numbers_.push_back(num);
  num->set_parent(this);
}

void MirageM400Component::register_text_sensor(MirageM400TextSensor *sensor) {
  this->text_sensor_ = sensor;
  sensor->set_parent(this);
}

void MirageM400Component::dump_config() {
  ESP_LOGD("custom", "Mirage M400 Component");
}

void MirageM400Number::control(float value) {
  if (!this->parent_) return;
  std::string cmd = "VOL " + std::to_string(this->zone_) + " " + std::to_string((int)value);
  this->parent_->send_command(cmd);
}

void MirageM400Switch::write_state(bool state) {
  if (!this->parent_) return;
  std::string cmd = (this->type_ == 0) ? "POWER " : "MUTE ";
  cmd += std::to_string(this->zone_) + (state ? " ON" : " OFF");
  this->parent_->send_command(cmd);
}

void MirageM400TextSensor::set_last_response(const std::string &response) {
  this->publish_state(response);
}

}  // namespace mirage_m400
}  // namespace esphome