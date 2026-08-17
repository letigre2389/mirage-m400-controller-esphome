#pragma once

#include "esphome.h"
#include "components/text_sensor.h"
#include "components/switch.h"
#include "components/number.h"

namespace esphome {
namespace mirage_m400 {

class MirageM400Number : public number::Number {
 public:
  void control(float value);
  void dump_config() override;
};

class MirageM400Switch : public switch::Switch {
 public:
  void write_state(bool state);
  void dump_config() override;
};

class MirageM400TextSensor : public text_sensor::TextSensor {
 public:
  void dump_config() override;
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
  void set_uart_parent(uart::UARTComponent *parent);

 protected:
  void process_response_(const std::string &response);

  // This must match the variable name used in the .cpp file loop()
  MirageM400TextSensor *text_sensor_{nullptr};
  std::vector<MirageM400Switch *> switches_;
  std::vector<MirageM400Number *> numbers_;
};

}  // namespace mirage_m400
}  // namespace esphome
