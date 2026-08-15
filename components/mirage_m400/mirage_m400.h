#pragma once

#include "esphome/core/component.h"
#include "esphome/components/uart/uart.h"
#include "esphome/components/switch/switch.h"
#include "esphome/components/number/number.h"
#include "esphome/components/text_sensor/text_sensor.h"

namespace esphome {
namespace mirage_m400 {

// Forward declarations
class MirageM400Switch;
class MirageM400Number;
class MirageM400TextSensor;

class MirageM400Component : public Component, public uart::UARTDevice {
 public:
  MirageM400Component() = default;
  ~MirageM400Component() = default;
  
  void set_uart_parent(uart::UARTComponent *parent) {
    this->set_parent(parent);
  }
  
  void setup() override;
  void loop() override;
  void send_command(const std::string &command);
  void register_switch(MirageM400Switch *sw);
  void register_number(MirageM400Number *num);
  void register_text_sensor(MirageM400TextSensor *ts);

 private:
  std::vector<MirageM400Switch *> switches_;
  std::vector<MirageM400Number *> numbers_;
  MirageM400TextSensor *text_sensor_{nullptr};
};

class MirageM400Switch : public switch_::Switch, public Component {
 public:
  void set_type(int type) { type_ = type; }
  void set_zone(uint8_t zone) { zone_ = zone; }
  void set_parent(MirageM400Component *parent) { parent_ = parent; }
  void write_state(bool state) override;

 private:
  int type_{0};
  uint8_t zone_{1};
  MirageM400Component *parent_{nullptr};
};

class MirageM400Number : public number::Number, public Component {
 public:
  void set_zone(uint8_t zone) { zone_ = zone; }
  void set_parent(MirageM400Component *parent) { parent_ = parent; }
  void control(float value) override;

 private:
  uint8_t zone_{1};
  MirageM400Component *parent_{nullptr};
};

class MirageM400TextSensor : public text_sensor::TextSensor, public Component {
 public:
  void set_parent(MirageM400Component *parent) { parent_ = parent; }

 private:
  MirageM400Component *parent_{nullptr};
};

}  // namespace mirage_m400
}  // namespace esphome
