#pragma once

#include "esphome.h"
#include "../text_sensor/text_sensor.h"
#include "../switch/switch.h"
#include "../number/number.h"
#include "../uart/uart.h"

namespace esphome {
namespace mirage_m400 {

class MirageM400Component;

class MirageM400Number : public number::Number {
 public:
  void set_parent(MirageM400Component *parent) { this->parent_ = parent; }
  void control(float value);
  void dump_config() override { ESP_LOGD("custom", "Mirage M400 Number"); }
 protected:
  MirageM400Component *parent_{nullptr};
  int zone_{0};
};

// To solve the 'switch' keyword issue, we inherit from the base switch class
// explicitly using the namespace.
class MirageM400Switch : public esphome::components::switch::Switch {
 public:
  void set_parent(MirageM400Component *parent) { this->parent_ = parent; }
  void write_state(bool state) override;
  void dump_config() override { ESP_LOGD("custom", "Mirage M400 Switch"); }
 protected:
  MirageM400Component *parent_{nullptr};
  int zone_{0};
  int type_{0};
};

class MirageM400TextSensor : public text_sensor::TextSensor {
 public:
  void set_parent(MirageM400Component *parent) { this->parent_ = parent; }
  void set_last_response(const std::string &response);
  void dump_config() override { ESP_LOGD("custom", "Mirage M400 Text Sensor"); }
 protected:
  MirageM400Component *parent_{nullptr};
};

class MirageM400Component : public Component, public uart::UARTDevice {
 public:
  void setup() override;
  void loop() override;
  void dump_config() override;

  void send_command(const std::string &command);
  void register_switch(MirageM400Switch *sw);
  void register_text_sensor(MirageM400TextSensor *sensor);
  void register_number(MirageM400Number *num);

 protected:
  void process_response_(const std::string &response);

  MirageM400TextSensor *text_sensor_{nullptr};
  std::vector<MirageM400Switch *> switches_;
  std::vector<MirageM400Number *> numbers_;
};

}  // namespace mirage_m400
}  // namespace esphome
