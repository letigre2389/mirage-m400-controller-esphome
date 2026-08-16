#pragma once

#include "esphome/core/component.h"
#include "esphome/components/uart/uart.h"
#include "esphome/components/text_sensor/text_sensor.h"

namespace esphome {
namespace mirage_m400 {

class MirageM400Component : public Component, public uart::UARTDevice {
 public:
  void setup() override;
  void loop() override;
  void dump_config() override;
  
  void send_command(const char *command);
  
  void register_text_sensor(text_sensor::TextSensor *sensor);
  void register_switch(void *sw);
  void register_number(void *num);

 protected:
  std::vector<text_sensor::TextSensor *> text_sensors_;
  std::vector<void *> switches_;
  std::vector<void *> numbers_;
  
  void process_response_(const std::string &response);
};

class MirageM400TextSensor {
 public:
  uint8_t zone{1};
};

class MirageM400Switch {
 public:
  uint8_t zone{1};
  uint8_t type{0};  // 0 = power, 1 = mute
};

class MirageM400Number {
 public:
  uint8_t zone{1};
  float min_value{0};
  float max_value{100};
  float step{1};
};

}  // namespace mirage_m400
}  // namespace esphome
