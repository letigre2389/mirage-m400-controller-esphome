#pragma once

#include "esphome.h"
#include "esphome/core/component.h"
#include "esphome/components/uart/uart.h"
#include "esphome/components/text_sensor/text_sensor.h"
#include "esphome/components/switch/switch.h"
#include "esphome/components/number/number.h"

namespace esphome {
namespace mirage_m400 {

class MirageM400Component : public Component, public uart::UARTDevice {
 public:
  explicit MirageM400Component(uart::UARTComponent *parent) : UARTDevice(parent) {}

  void setup() override;
  void loop() override;
  void dump_config() override;
  void send_command(const std::string &command);
  void register_switch(switch_::Switch *sw);
  void register_text_sensor(text_sensor::TextSensor *sensor);
  void register_number(number::Number *num);

 protected:
  void process_response_(const std::string &response);
  text_sensor::TextSensor *text_sensor_{nullptr};
  std::vector<switch_::Switch *> switches_;
  std::vector<number::Number *> numbers_;
};

}  // namespace mirage_m400
}  // namespace esphome
