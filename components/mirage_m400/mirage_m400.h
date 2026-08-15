#pragma once

#include "esphome/core/component.h"
#include "esphome/components/uart/uart.h"
#include "esphome/components/number/number.h"
#include "esphome/components/switch/switch.h"
#include "esphome/components/text_sensor/text_sensor.h"

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
  float get_setup_priority() const override { return setup_priority::HARDWARE; }

  void send_command(const std::string &command);
  void register_number(MirageM400Number *number);
  void register_switch(MirageM400Switch *switch_);
  void register_text_sensor(MirageM400TextSensor *text_sensor);
  void set_uart_parent(uart::UARTComponent *parent);

 private:
  std::vector<MirageM400Number *> numbers_;
  std::vector<MirageM400Switch *> switches_;
  MirageM400TextSensor *text_sensor_{nullptr};
};

class MirageM400Number : public number::Number, public Component {
 public:
  void set_zone(uint8_t zone) { zone_ = zone; }
  void control(float value) override;

 protected:
  void dump_config() override;

 private:
  uint8_t zone_{0};
};

class MirageM400Switch : public switch_::Switch, public Component {
 public:
  void set_zone(uint8_t zone) { zone_ = zone; }
  void set_type(uint8_t type) { type_ = type; }  // 0 = POWER, 1 = MUTE
  void write_state(bool state) override;

 protected:
  void dump_config() override;

 private:
  uint8_t zone_{0};
  uint8_t type_{0};
};

class MirageM400TextSensor : public text_sensor::TextSensor, public Component {
 public:
  void set_last_response(const std::string &response) {
    publish_state(response);
  }

 protected:
  void dump_config() override;
};

}  // namespace mirage_m400
}  // namespace esphome
#pragma once

#include "esphome/core/component.h"
#include "esphome/components/uart/uart.h"
#include "esphome/components/number/number.h"
#include <string>
#include <queue>

namespace esphome {
namespace mirage_m400 {

// Forward declaration
class MirageM400Number;

class MirageM400Component : public Component, public uart::UARTDevice {
 public:
  MirageM400Component() = default;

  void setup() override;
  void loop() override;
  void send_command(const std::string &command);
  void register_number(MirageM400Number *number_entity, uint8_t zone);
  std::string last_response;

 private:
  std::queue<std::string> response_buffer_;
  std::string current_response_;
  std::vector<MirageM400Number *> numbers_;
};

// Full definition after MirageM400Component
class MirageM400Number : public number::Number, public Component {
 public:
  void set_parent(MirageM400Component *parent) { parent_ = parent; }
  void set_zone(uint8_t zone) { zone_ = zone; }

 protected:
  void control(float value) override;
  MirageM400Component *parent_;
  uint8_t zone_;
};

}  // namespace mirage_m400
}  // namespace esphome
