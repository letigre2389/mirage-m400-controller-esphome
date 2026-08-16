#pragma once

#include "esphome/core/component.h"
#include "esphome/components/uart/uart.h"
#include "esphome/components/text_sensor/text_sensor.h"
#include "esphome/components/switch/switch.h"
#include "esphome/components/number/number.h"

namespace esphome {
namespace mirage_m400 {

class MirageM400Component : public Component, public uart::UARTDevice {
 public:
  void setup() override;
  void loop() override;
  void dump_config() override;
  
  void send_command(const char *command);
  
  void register_text_sensor(text_sensor::TextSensor *sensor);
  void register_switch(switch_::Switch *sw);
  void register_number(number::Number *num);

 protected:
  std::vector<text_sensor::TextSensor *> text_sensors_;
  std::vector<switch_::Switch *> switches_;
  std::vector<number::Number *> numbers_;
  
  void process_response_(const std::string &response);
};

class MirageM400TextSensor : public text_sensor::TextSensor {
 public:
  // Empty for now; can extend later
};

class MirageM400Switch : public switch_::Switch {
 public:
  void set_zone(uint8_t zone) { zone_ = zone; }
  void set_type(uint8_t type) { type_ = type; }  // 0 = power, 1 = mute
  
 protected:
  uint8_t zone_{1};
  uint8_t type_{0};
  
  void write_state(bool state) override;
};

class MirageM400Number : public number::Number {
 public:
  void set_zone(uint8_t zone) { zone_ = zone; }
  void set_range(float min_val, float max_val, float step) {
    this->min_value_ = min_val;
    this->max_value_ = max_val;
    this->step_ = step;
  }
  
 protected:
  uint8_t zone_{1};
  
  void control(float value) override;
};

}  // namespace mirage_m400
}  // namespace esphome
#pragma once

#include "esphome/core/component.h"
#include "esphome/components/uart/uart.h"
#include "esphome/components/switch/switch.h"
#include "esphome/components/text_sensor/text_sensor.h"
#include "esphome/components/number/number.h"

namespace esphome {
namespace mirage_m400 {

// Forward declarations
class MirageM400Number;
class MirageM400Switch;
class MirageM400TextSensor;

class MirageM400Component : public Component, public uart::UARTDevice {
 public:
  MirageM400Component() = default;
  
  void setup() override;
  void loop() override;
  void dump_config() override;
  
  float get_setup_priority() const override { return setup_priority::LATE; }
  
  void set_uart_parent(uart::UARTComponent *parent);
  void send_command(const char *command);
  
  void register_text_sensor(MirageM400TextSensor *sensor) {
    this->text_sensor_ = sensor;
  }
  
  void register_switch(MirageM400Switch *sw) {
    this->switches_.push_back(sw);
  }
  
  void register_number(MirageM400Number *num) {
    this->numbers_.push_back(num);
  }

 protected:
  MirageM400TextSensor *text_sensor_{nullptr};
  std::vector<MirageM400Switch *> switches_;
  std::vector<MirageM400Number *> numbers_;
};

class MirageM400Number : public number::Number, public Component {
 public:
  void set_parent(MirageM400Component *parent) { this->parent_ = parent; }
  void set_zone(uint8_t zone) { this->zone_ = zone; }
  
  void control(float value) override;
  void dump_config() override;

 protected:
  MirageM400Component *parent_{nullptr};
  uint8_t zone_{1};
};

class MirageM400Switch : public switch_::Switch, public Component {
 public:
  void set_parent(MirageM400Component *parent) { this->parent_ = parent; }
  void set_zone(uint8_t zone) { this->zone_ = zone; }
  void set_type(int type) { this->type_ = type; }
  
  void write_state(bool state) override;
  void dump_config() override;

 protected:
  MirageM400Component *parent_{nullptr};
  uint8_t zone_{1};
  int type_{0};  // 0 = power, 1 = mute
};

class MirageM400TextSensor : public text_sensor::TextSensor, public Component {
 public:
  void set_parent(MirageM400Component *parent) { this->parent_ = parent; }
  void dump_config() override;

 protected:
  MirageM400Component *parent_{nullptr};
};

}  // namespace mirage_m400
}  // namespace esphome
